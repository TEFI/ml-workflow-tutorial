from google.cloud import storage
import uuid

def upload_file_to_gcs(upload_file, bucket_name: str, folder: str = "datasets") -> str:
    """Uploads a FastAPI UploadFile to GCS and returns the GCS path."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    filename = f"{folder}/{uuid.uuid4().hex}_{upload_file.filename}"
    blob = bucket.blob(filename)
    blob.upload_from_file(upload_file.file, content_type=upload_file.content_type)

    return f"gs://{bucket_name}/{filename}"
