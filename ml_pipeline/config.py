import os

EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME", "random-forest-classifier")
MLFLOW_URI = os.getenv("MLFLOW_URI", "http://34.29.28.17:5000")
