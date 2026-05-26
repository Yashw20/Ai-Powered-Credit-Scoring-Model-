from pydantic import BaseModel


class LoanRequest(BaseModel):

    loan_amnt: float

    int_rate: float

    annual_inc: float

    dti: float

    total_acc: int

    mort_acc: int

    pub_rec_bankruptcies: float