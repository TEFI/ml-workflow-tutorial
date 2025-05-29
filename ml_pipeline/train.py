import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import mlflow

data = pd.read_csv('titanic.csv')
X = data.drop(['Survived'], axis=1)
y = data['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

mlflow.start_run()
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
score = clf.score(X_test, y_test)
mlflow.log_metric("accuracy", score)

joblib.dump(clf, '../models/best_model.pkl')
mlflow.sklearn.log_model(clf, "model")
mlflow.end_run()