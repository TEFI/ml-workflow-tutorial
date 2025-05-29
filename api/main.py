from fastapi import FastAPI
import pickle
import pandas as pd

app = FastAPI()
model = pickle.load(open('models/best_model.pkl', 'rb'))

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return {"prediction": int(prediction[0])}