from fastapi import FastAPI
from src.api.predictor_api import predictor_api_router

app = FastAPI()

app.include_router(predictor_api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
