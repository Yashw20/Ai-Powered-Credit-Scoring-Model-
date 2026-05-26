from fastapi import FastAPI

from schemas import LoanRequest

from predictor import predict_credit


app = FastAPI()


@app.get("/")

def home():

    return {

        "message":
        "AI Credit Scoring API Running"
    }


@app.post("/predict")

def predict(data: LoanRequest):

    result = predict_credit(
        data
    )

    return result