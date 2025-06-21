from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils import download_model_from_gcs, predict_with_model

router = APIRouter()

# Load the model at startup
try:
    model = download_model_from_gcs()
except Exception as e:
    model = None
    print(f"Model loading failed: {e}")

# Define expected input schema strictly
class PredictionInput(BaseModel):
    Pclass: int
    Sex: str
    Age: int
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str

@router.post("/predict")
def predict(input_data: PredictionInput):
    """
    Predict endpoint that receives structured features with strict types.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")

    try:
        features = input_data.model_dump()
        prediction = predict_with_model(model, features)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")
