from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import LoanRequest
from app.predictor import predict_credit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Credit Scoring API Running"
    }


@app.post("/predict")
def predict(data: LoanRequest):
    result = predict_credit(data)
    return result