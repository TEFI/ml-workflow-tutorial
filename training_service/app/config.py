import os

PROJECT_ID = os.getenv("PROJECT_ID", "sodium-pager-461309-p3")
BUCKET_NAME = os.getenv("BUCKET_NAME", "ml-artifacts-tutorial")
TRAINING_IMAGE = os.getenv("TRAINING_IMAGE", "training-image:latest")
REGION = os.getenv("REGION", "us-central1")
PARENT = f"projects/{PROJECT_ID}/locations/{REGION}"
