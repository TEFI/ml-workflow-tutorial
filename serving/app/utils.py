import os
import io
import joblib
import pandas as pd
from google.cloud import storage

BUCKET_NAME = os.getenv('BUCKET_NAME')
BLOB_NAME = os.getenv('BLOB_NAME')

def download_model_from_gcs():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(BLOB_NAME)
    content = blob.download_as_bytes()
    model = joblib.load(io.BytesIO(content))
    print(f"Downloaded {BLOB_NAME} from bucket {BUCKET_NAME}.")
    return model
    

def predict_with_model(model, data):
    df = pd.get_dummies(pd.DataFrame([data])).reindex(columns=model.feature_names_in_, fill_value=0)
    prediction = model.predict(df)
    return prediction.tolist()





