import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import mlflow

# Load data
data = pd.read_csv('titanic_train.csv')

# Drop target column
X = data.drop(['Survived'], axis=1)
y = data['Survived']

# Remove columns with names, tickets, cabins (if they exist)
columns_to_drop = ['Name', 'Ticket', 'Cabin']
for col in columns_to_drop:
    if col in X.columns:
        X = X.drop(col, axis=1)

# Convert categorical variables to numeric
X = pd.get_dummies(X)

# Simple split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

mlflow.start_run()
# Train model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

score = clf.score(X_test, y_test)
mlflow.log_metric("accuracy", score)

# Save model
joblib.dump(clf, 'random_forest_model.joblib')

mlflow.sklearn.log_model(clf, "model")
mlflow.end_run()
