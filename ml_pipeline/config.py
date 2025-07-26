import os

EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME", "random-forest-classifier")
MLFLOW_URI = os.getenv("MLFLOW_URI", "http://146.148.62.66:5000")
