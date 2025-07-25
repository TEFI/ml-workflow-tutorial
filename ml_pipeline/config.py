import os

EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME", "random-forest-classifier")
MLFLOW_URI = os.getenv("MLFLOW_URI", "http://35.225.64.219:5000")
