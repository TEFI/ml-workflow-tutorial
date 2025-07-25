FROM python:3.11-slim

WORKDIR /app

# Install git for MLflow source tracking
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY train.py .
COPY training.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "train.py"]
