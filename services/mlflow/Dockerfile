# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Install system dependencies needed for psycopg2 and GCS support
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install MLflow, PostgreSQL connector, and Google Cloud Storage support
RUN pip install --no-cache-dir mlflow psycopg2-binary google-cloud-storage

# Copy the current directory contents into the container (optional if configs/scripts needed)
COPY . .

# Expose MLflow's default port
EXPOSE 5000

# Start the MLflow tracking server with PostgreSQL and GCS
CMD ["mlflow", "server", \
     "--backend-store-uri=postgresql://mlflow_user:mlflow123@35.234.123.45:5432/mlflow_db", \
     "--default-artifact-root=gs://ml-artifacts-tutorial", \
     "--host=0.0.0.0"]
