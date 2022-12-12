from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.predictor_api import predictor_api_router
from src.api.infection_api import infection_api_router
from src.api.model_manager_api import model_api_router
from src.models.database import init_database

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predictor_api_router)
app.include_router(infection_api_router)
app.include_router(model_api_router)

@app.on_event("startup")
async def init_config():
    init_database()

@app.get("/")
async def root():
    return {"message": "Hello World"}
