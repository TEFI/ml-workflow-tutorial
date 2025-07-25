from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import joblib
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.models.signature import infer_signature
from ml_pipeline.config import EXPERIMENT_NAME, MLFLOW_URI


def train_model(args):
    # Set remote MLflow tracking URI (Kubernetes service)
    mlflow.set_tracking_uri(MLFLOW_URI)
    run_name = f"rf_n{args.n_estimators}_d{args.max_depth}_{datetime.now().strftime('%H%M%S')}"

    mlflow.set_experiment(EXPERIMENT_NAME)
    with mlflow.start_run(run_name=run_name):

        # Load CSV (from GCS or local path)
        if args.gcs_path.startswith("gs://"):
            import gcsfs
            fs = gcsfs.GCSFileSystem()
            with fs.open(args.gcs_path) as f:
                data = pd.read_csv(f)
        else:
            data = pd.read_csv(args.gcs_path)

        # Enforce correct types
        data["Age"] = pd.to_numeric(data["Age"], errors="coerce")
        data["Age"] = data["Age"].fillna(0).round().astype("int64")
        data["Fare"] = data["Fare"].astype("float64")
        data["PassengerId"] = data["PassengerId"].astype("int64")
        data["Pclass"] = data["Pclass"].astype("int64")
        data["SibSp"] = data["SibSp"].astype("int64")
        data["Parch"] = data["Parch"].astype("int64")
        for col in ["Sex_female", "Sex_male", "Embarked_C", "Embarked_Q", "Embarked_S"]:
            if col in data.columns:
                data[col] = data[col].astype("bool")

        # Preprocessing
        y = data["Survived"]
        X = data.drop(columns=["Survived"])

        # Drop irrelevant
        for col in ["Name", "Ticket", "Cabin"]:
            if col in X.columns:
                X = X.drop(columns=[col])

        # One-hot encode
        X = pd.get_dummies(X)

        # Ensure full feature set
        expected_cols = [
            "PassengerId", "Pclass", "Age", "SibSp", "Parch", "Fare",
            "Sex_female", "Sex_male", "Embarked_C", "Embarked_Q", "Embarked_S"
        ]
        X = X.reindex(columns=expected_cols, fill_value=0)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=6)

        mlflow.log_param("random_state", 6)
        # Train model
        clf = RandomForestClassifier(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            min_samples_split=args.min_samples_split,
            min_samples_leaf=args.min_samples_leaf
        )

        # cross validation
        cv_scores = cross_val_score(clf, X_train, y_train, cv=5)
        mlflow.log_metric("cv_score_mean", cv_scores.mean())
        mlflow.log_metric("cv_score_std", cv_scores.std())

        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test)
        signature = infer_signature(X_test, y_test)
        # Log parameters and metrics to MLflow
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("max_depth", args.max_depth)
        mlflow.log_param("min_samples_split", args.min_samples_split)
        mlflow.log_param("min_samples_leaf", args.min_samples_leaf)      
        mlflow.log_metric("accuracy", accuracy)

        mlflow.sklearn.log_model(clf, "model", signature=signature)

        joblib.dump(clf, "random_forest_model.joblib")
        mlflow.log_artifact("random_forest_model.joblib")

        client = MlflowClient()
        experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
        runs = client.search_runs([experiment.experiment_id], order_by=["metrics.accuracy DESC"])

        best_accuracy = None
        if runs:
            best_accuracy = runs[0].data.metrics.get("accuracy")

        if best_accuracy is None or accuracy >= best_accuracy:
            print("📌 Registering new best model...")
            import time
            from mlflow.exceptions import MlflowException

            for _ in range(5):
                try:
                    result = mlflow.register_model(
                        model_uri=f"runs:/{mlflow.active_run().info.run_id}/model",
                        name="RandomForestModelv1"
                    )
                    break
                except MlflowException as e:
                    print("🕒 Waiting for artifact propagation...")
                    time.sleep(2)
            else:
                raise RuntimeError("❌ Failed to register model after multiple attempts.")


            client.set_registered_model_alias(
                name="RandomForestModelv1",
                alias="production",
                version=result.version
            )


        else:
            print("⚠️ Not the best model, skipping registration.")
