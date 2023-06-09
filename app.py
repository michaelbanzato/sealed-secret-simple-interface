from flask import Flask, render_template, request, send_file
from api.yaml_gen import generate_yaml
from os import system

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

    sealedsecret = generate_yaml(namespace=namespace,
                                 secret_name=secret_name,
                                 variables=variables,
                                 values=values)

    # Return the renamed file for download
    return send_file(sealedsecret, as_attachment=True)

# Remove yaml files after each request
@app.teardown_request
def remove_temp_files(exception=None):
    system('sleep 5 && rm -f static/*.yaml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
