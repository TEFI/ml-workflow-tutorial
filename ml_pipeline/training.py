import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import mlflow
from google.cloud import storage


def train_model(args):
    # Set remote MLflow tracking URI (Kubernetes service)
    mlflow.set_tracking_uri("http://34.45.69.115:5000")
    mlflow.start_run()

    # Load CSV (from GCS or local path)
    if args.gcs_path.startswith("gs://"):
        import gcsfs
        fs = gcsfs.GCSFileSystem()
        with fs.open(args.gcs_path) as f:
            data = pd.read_csv(f)
    else:
        data = pd.read_csv(args.gcs_path)

    # Preprocessing
    X = data.drop(columns=["Survived"])
    y = data["Survived"]
    for col in ["Name", "Ticket", "Cabin"]:
        if col in X.columns:
            X = X.drop(columns=[col])
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model
    clf = RandomForestClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        min_samples_split=args.min_samples_split,
        min_samples_leaf=args.min_samples_leaf
    )
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)

    # Log parameters and metrics to MLflow
    mlflow.log_param("n_estimators", args.n_estimators)
    mlflow.log_param("max_depth", args.max_depth)
    mlflow.log_param("min_samples_split", args.min_samples_split)
    mlflow.log_param("min_samples_leaf", args.min_samples_leaf)
    mlflow.log_param("dataset_path", args.gcs_path)
    mlflow.log_metric("accuracy", accuracy)

    # Save model locally
    local_model_path = "random_forest_model.joblib"
    joblib.dump(clf, local_model_path)
    mlflow.sklearn.log_model(clf, "model")

    # Upload model to GCS
    model_filename = os.path.basename(args.gcs_path).replace(".csv", "_model.joblib")
    destination_path = f"models/{model_filename}"
    upload_to_gcs(local_model_path, f"gs://ml-artifacts-tutorial/{destination_path}")

    mlflow.end_run()


def upload_to_gcs(local_file: str, gcs_uri: str):
    if not gcs_uri.startswith("gs://"):
        raise ValueError("Destination GCS path must start with 'gs://'")

    # Parse bucket name and blob path
    bucket_name, blob_path = gcs_uri.replace("gs://", "").split("/", 1)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.upload_from_filename(local_file)
