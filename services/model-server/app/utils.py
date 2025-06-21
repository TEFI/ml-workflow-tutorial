import os
import io
import joblib
import pandas as pd
from google.cloud import storage

# Load environment variables
BUCKET_NAME = os.getenv("BUCKET_NAME")
BLOB_NAME = os.getenv("BLOB_NAME")

def download_model_from_gcs():
    """
    Download a serialized model file from Google Cloud Storage and load it with joblib.
    
    Returns:
        model: The deserialized machine learning model.
    """
    if not BUCKET_NAME or not BLOB_NAME:
        raise ValueError("BUCKET_NAME and BLOB_NAME must be set in environment variables.")

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(BLOB_NAME)

    content = blob.download_as_bytes()
    model = joblib.load(io.BytesIO(content))

    print(f"Downloaded {BLOB_NAME} from bucket {BUCKET_NAME}.")
    return model


def predict_with_model(model, data):
    """
    Run prediction using a trained model on a single input data point.

    Args:
        model: Trained model that implements the .predict method and has 'feature_names_in_' attribute.
        data (dict): Input features as a dictionary.

    Returns:
        list: Prediction result as a list.
    """
    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary.")

    # Convert input data to a one-row DataFrame and align with training feature set
    df = pd.get_dummies(pd.DataFrame([data]))
    df = df.reindex(columns=model.feature_names_in_, fill_value=0)

    prediction = model.predict(df)
    return prediction.tolist()





