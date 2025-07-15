import os

PROJECT_ID = os.getenv("PROJECT_ID", "your-project-id")
BUCKET_NAME = os.getenv("BUCKET_NAME", "your-bucket-name")
TRAINING_IMAGE = os.getenv("TRAINING_IMAGE", "training-image:latest")
REGION = os.getenv("REGION", "us-central1")
PARENT = f"projects/{PROJECT_ID}/locations/{REGION}"
