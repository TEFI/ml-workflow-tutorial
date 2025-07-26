import os

MLFLOW_URI = os.getenv("MLFLOW_URI", "http://146.148.62.66:5000")
MODEL_URI = os.getenv("MODEL_URI", "models:/RandomForestModelv1@production")