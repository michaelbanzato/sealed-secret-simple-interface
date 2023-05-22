### Sealed Secrets Simple Interface

This is a simple app using python, javascript and html/css to generate Sealed Secret YAML files.

##### Run locally:
- Add your cert.pem in cert/cert.pem #current is a empty file
- `python -m venv venv && source venv/bin/activate`
- `pip install -r requirements.txt`
- `python app.py`
- Access http://localhost:8080


##### Run on Kubernetes:
- Build the Dockerfile
- Create a deployment with generated image
- Mount your secret cert.pem into /app/cert/cert.pem