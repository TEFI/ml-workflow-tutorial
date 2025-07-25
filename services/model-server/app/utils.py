import mlflow
import pandas as pd
from config import MLFLOW_URI, MODEL_URI

def download_model_from_gcs():
    """
    Download a serialized model file from Google Cloud Storage and load it with mlflow.
    
    Returns:
        model: The deserialized machine learning model.
    """
    # Set remote tracking server
    mlflow.set_tracking_uri(MLFLOW_URI)

    # Load model from registry in Production stage
    model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)

    return model


def predict_with_model(model, data):
    """
    Run prediction using a trained model on a single input data point.

    Args:
        model: Trained MLflow PyFunc model.
        data (dict): Input features as a dictionary.

    Returns:
        list: Prediction result.
    """
    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary.")

    # Convert input to DataFrame and one-hot encode
    df = pd.get_dummies(pd.DataFrame([data]))

    # Align columns with training schema
    input_schema = model.metadata.get_input_schema()

    for col_spec in input_schema.inputs:
        name = col_spec.name
        dtype = col_spec.type.name
        if name not in df.columns:
            if dtype == "double":
                df[name] = 0.0
            elif dtype == "long":
                df[name] = 0
            elif dtype == "boolean":
                df[name] = False

    prediction = model.predict(df)
    return prediction.tolist()
