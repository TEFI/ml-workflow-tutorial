import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import mlflow

parser = argparse.ArgumentParser()
parser.add_argument("--n_estimators", type=int, default=100)
parser.add_argument("--max_depth", type=int, default=None)
parser.add_argument("--min_samples_split", type=int, default=2)
parser.add_argument("--min_samples_leaf", type=int, default=1)
parser.add_argument("--gcs_path", type=str, required=True)  # gs://bucket/path/to/file.csv
args = parser.parse_args()

# Download from GCS (use gcsfs if gs://, or assume local otherwise)
if args.gcs_path.startswith("gs://"):
    import gcsfs
    fs = gcsfs.GCSFileSystem()
    with fs.open(args.gcs_path) as f:
        data = pd.read_csv(f)
else:
    data = pd.read_csv(args.gcs_path)

# Preprocess
X = data.drop(['Survived'], axis=1)
y = data['Survived']
for col in ['Name', 'Ticket', 'Cabin']:
    if col in X.columns:
        X = X.drop(col, axis=1)
X = pd.get_dummies(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Track with MLflow
mlflow.start_run()
clf = RandomForestClassifier(
    n_estimators=args.n_estimators,
    max_depth=args.max_depth,
    min_samples_split=args.min_samples_split,
    min_samples_leaf=args.min_samples_leaf
)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

mlflow.log_param("n_estimators", args.n_estimators)
mlflow.log_param("max_depth", args.max_depth)
mlflow.log_param("min_samples_split", args.min_samples_split)
mlflow.log_param("min_samples_leaf", args.min_samples_leaf)
mlflow.log_param("dataset_path", args.gcs_path)
mlflow.log_metric("accuracy", accuracy)

joblib.dump(clf, 'random_forest_model.joblib')
mlflow.sklearn.log_model(clf, "model")
mlflow.end_run()
