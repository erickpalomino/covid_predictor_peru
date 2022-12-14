from fastapi import APIRouter, Body
from src.predictor.predictor_middleware import load_model,get_prediction
from src.models.data_manager import init_database
import datetime

predictor_api_router=APIRouter(prefix="/predictor")

@predictor_api_router.get('/predict')
async def predictor_predict():
    prediction=get_prediction()
    return ({
        "date": (datetime.datetime.now()).strftime("%Y-%m-%d"),
        "prediction":int(prediction)
    })





