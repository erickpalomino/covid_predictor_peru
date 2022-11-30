from fastapi import APIRouter, Body
from src.predictor.predictor_middleware import load_model,get_prediction
import datetime

predictor_api_router=APIRouter(prefix="/predictor")

@predictor_api_router.get('/predict')
async def predictor_predict():
    prediction=get_prediction()
    return ({
        "date": (datetime.datetime.now()+datetime.timedelta(1)).strftime("%Y-%m-%d"),
        "prediction":int(prediction)
    })
