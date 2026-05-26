import joblib
import pandas as pd

model = joblib.load(
    "../models/credit_scoring_model.pkl"
)

def predict_credit(data):

    input_df = pd.DataFrame([{
        "loan_amnt": data.loan_amnt,
        "int_rate": data.int_rate,
        "annual_inc": data.annual_inc,
        "dti": data.dti,
        "total_acc": data.total_acc,
        "mort_acc": data.mort_acc,
        "pub_rec_bankruptcies": data.pub_rec_bankruptcies
    }])

    # Debug output
    print("\nInput columns sent:")
    print(input_df.columns.tolist())

    print("\nModel expects:")
    print(model.feature_names_in_)

    probability = model.predict_proba(
        input_df
    )[0][1]

    credit_score = int(
        300 + ((1 - probability) * 550)
    )

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
