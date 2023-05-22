FROM python:3.8

# Install kubectl
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list && \
    apt-get update && \
    apt-get install -y kubectl

# Install kubeseal
RUN curl -L -o /usr/local/bin/kubeseal https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.16.0/kubeseal-linux-amd64 && \
    chmod +x /usr/local/bin/kubeseal

# Working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY static/ ./static/
COPY templates/ ./templates/
COPY cert/ ./cert/

# Expose port
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]
