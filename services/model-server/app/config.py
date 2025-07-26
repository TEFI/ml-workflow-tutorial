import os

MLFLOW_URI = os.getenv("MLFLOW_URI", "http://34.63.176.60:5000")
MODEL_URI = os.getenv("MODEL_URI", "models:/RandomForestModelv1@production")