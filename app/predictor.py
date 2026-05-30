import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

model_path = os.path.join(
    BASE_DIR,
    "models",
    "credit_scoring_model.pkl"
)

artifacts = joblib.load(model_path)
model    = artifacts["model"]
imputer  = artifacts["imputer"]
scaler   = artifacts["scaler"]
features = artifacts["features"]

print("Model loaded successfully")
print("Features:", features)


def predict_credit(data):

    input_dict = {
        "loan_amnt":            float(data.loan_amnt),
        "int_rate":             float(data.int_rate),
        "annual_inc":           float(data.annual_inc),
        "dti":                  float(data.dti),
        "total_acc":            float(data.total_acc),
        "mort_acc":             float(data.mort_acc),
        "pub_rec_bankruptcies": float(data.pub_rec_bankruptcies),
        "loan_to_income":       float(data.loan_amnt) / (float(data.annual_inc) + 1),
        "debt_burden":          float(data.dti) * float(data.int_rate),
        "risk_index":           float(data.pub_rec_bankruptcies) * 10 + float(data.dti),
        "monthly_payment_ratio": float(data.loan_amnt) / (float(data.annual_inc) / 12 + 1)
    }

    input_df = pd.DataFrame([input_dict])[features]

    print("\nInput columns sent:")
    print(input_df.columns.tolist())

    X = scaler.transform(imputer.transform(input_df))

    probability = model.predict_proba(X)[0][1]

    credit_score = int(300 + ((1 - probability) * 550))

    if credit_score >= 750:
        risk = "Low"
    elif credit_score >= 650:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "default_probability": round(float(probability), 3),
        "credit_score": credit_score,
        "risk": risk
    }