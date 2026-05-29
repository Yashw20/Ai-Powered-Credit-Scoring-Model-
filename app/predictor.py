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

# Load FULL pipeline directly
model = joblib.load(model_path)

print("Model loaded successfully")


def predict_credit(data):

    input_dict = {

        "loan_amnt": data.loan_amnt,
        "int_rate": data.int_rate,
        "annual_inc": data.annual_inc,
        "dti": data.dti,
        "total_acc": data.total_acc,
        "mort_acc": data.mort_acc,
        "pub_rec_bankruptcies": data.pub_rec_bankruptcies

    }

    # Convert to dataframe
    input_df = pd.DataFrame([input_dict])

    print("\nInput Data:")
    print(input_df)

    # Pipeline handles preprocessing automatically
    probability = model.predict_proba(input_df)[0][1]

    credit_score = int(
        300 + ((1 - probability) * 550)
    )

    # Risk category
    if credit_score >= 750:
        risk = "Low"

    elif credit_score >= 650:
        risk = "Medium"

    else:
        risk = "High"

    return {

        "default_probability": round(
            float(probability), 3
        ),

        "credit_score": credit_score,

        "risk": risk
    }