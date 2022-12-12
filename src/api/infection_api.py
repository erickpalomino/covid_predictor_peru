from fastapi import APIRouter, Body
from src.infection.infection_middleware import *
from src.models.data_manager import init_database

infection_api_router=APIRouter(prefix="/infection")

@infection_api_router.get('/7days')
async def get_7_days_infection():
    return (get_infection_7_days(datetime.datetime.now()))

@infection_api_router.get('/get/day')
async def get_infection_day(date):
    return (getInfectionDay(date))

@infection_api_router.get('/update')
async def predictor_update():
    return (init_database())

@infection_api_router.get('/7days/predict')
async def get_7_days_predict():
    return (get_infection_with_prediction())

