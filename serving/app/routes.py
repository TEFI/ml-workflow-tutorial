from fastapi import APIRouter
from app.utils import download_model_from_gcs, predict_with_model

router = APIRouter()
model = download_model_from_gcs()

@router.post("/predict")
def predict(data: dict):
    prediction = predict_with_model(model, data)
    return {"prediction": int(prediction[0])}
