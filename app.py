from flask import Flask, render_template, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-yaml', methods=['POST'])
def generate_yaml():
    namespace = request.form.get('namespace').strip().replace(' ', '-')
    secret_name = request.form.get('secret-name').strip().replace(' ', '-')
    variables = [var.strip().replace(' ', '-') for var in request.form.getlist('variable[]')]
    values = request.form.getlist('value[]')

    # Check if namespace and at least one variable-value pair are provided
    if not namespace or not secret_name or not any(variables) or not any(values):
        return "Namespace, secret name and at least one variable-value pair are required."
    # Check cert.pem
    check_cert_cmd = f'openssl x509 -in cert/cert.pem -noout'
    if subprocess.call(check_cert_cmd, shell=True) != 0:
        return "Invalid certificate. Check /app/cert/cert.pem"

    # Command to generate the YAML file
    cmd = ['kubectl', 'create', 'secret', 'generic', secret_name, '-n', namespace, '--dry-run=client']
    for variable, value in zip(variables, values):
        if variable and value:
            cmd.extend(['--from-literal', f'{variable}={value}'])
    cmd.extend(['-o', 'yaml'])

    # Execute the command and capture the output
    output = subprocess.check_output(cmd)

    # Write the output to a temporary file
    temp_file = 'static/generated-file.yaml'
    with open(temp_file, 'wb') as f:
        f.write(output)

    # Use kubeseal to generate the sealed secret
    sealedsecret = f'static/{namespace}-{secret_name}-sealed-secret.yaml'
    seal_cmd = f'kubeseal --cert cert/cert.pem --format=yaml < {temp_file} > {sealedsecret}'
    subprocess.run(seal_cmd, shell=True)

    # Return the renamed file for download
    return send_file(sealedsecret, as_attachment=True)

# Remove yaml files after each request
@app.teardown_request
def remove_temp_files(exception=None):
    os.system('sleep 5 && rm -f static/*.yaml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
