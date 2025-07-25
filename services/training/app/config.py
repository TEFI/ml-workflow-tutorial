import os

PROJECT_ID = os.getenv("PROJECT_ID", "sodium-pager-461309-p3")
REGION = os.getenv("REGION", "us-central1")
BUCKET_NAME = os.getenv("BUCKET_NAME", "ml-artifacts-tutorial")
PARENT = f"projects/{PROJECT_ID}/locations/{REGION}"
SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT", "terraform-deployer@{PROJECT_ID}.iam.gserviceaccount.com")
IMAGE_URI = os.getenv("IMAGE_URI", "us-central1-docker.pkg.dev/sodium-pager-461309-p3/trainer/training-api:latest")
