FROM python:3.9-slim

WORKDIR /app

COPY train.py .
COPY training.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "train.py"]
