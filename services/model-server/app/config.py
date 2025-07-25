import os

MLFLOW_URI = os.getenv("MLFLOW_URI", "http://35.225.64.219:5000")
MODEL_URI = os.getenv("MODEL_URI", "models:/RandomForestModelv1@production")