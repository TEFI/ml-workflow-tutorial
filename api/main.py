import os
from fastapi import FastAPI
from google.cloud import storage
import joblib
import pandas as pd

app = FastAPI()

# Leer variables de entorno
BUCKET_NAME = os.getenv('BUCKET_NAME')
BLOB_NAME = os.getenv('BLOB_NAME')


def download_model_from_gcs(bucket_name, blob_name, destination_file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {blob_name} from bucket {bucket_name} to {destination_file_name}.")

download_model_from_gcs(BUCKET_NAME, BLOB_NAME, MODEL_LOCAL_PATH)

# Cargar modelo usando joblib
model = joblib.load(MODEL_LOCAL_PATH)

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return {"prediction": int(prediction[0])}
