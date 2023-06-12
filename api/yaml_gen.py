import subprocess


def generate_yml(namespace=None, secret_name=None, variables=None, values=None):
    namespace = namespace
    secret_name = secret_name
    variables = variables
    values = values

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
    return sealedsecret
