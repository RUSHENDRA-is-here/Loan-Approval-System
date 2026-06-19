from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class EmploymentType(str, Enum):
    EMPLOYED = "employed"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"
    RETIRED = "retired"


class ApplicationStatus(str, Enum):
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    MANUAL_REVIEW = "manual_review"
    COMPLETED = "completed"


class LoanApplication(BaseModel):
    applicant_id: str = Field(..., description="Unique identifier for the applicant")
    age: int = Field(gt=18, lt=100, description="Applicant age")
    income: float = Field(gt=0, description="Annual income in dollars")
    employment_type: EmploymentType = Field(..., description="Type of employment")
    credit_score: int = Field(ge=300, le=850, description="Credit score (300-850)")
    loan_amount: float = Field(gt=0, description="Requested loan amount in dollars")
    tenure_months: int = Field(gt=0, le=360, description="Loan tenure in months")
    existing_liabilities: float = Field(ge=0, description="Total existing liabilities in dollars")
    location: str = Field(..., description="Applicant location")
    employment_years: Optional[float] = Field(default=None, description="Years of employment")
    application_timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "applicant_id": "APP123",
                "age": 35,
                "income": 75000,
                "employment_type": "employed",
                "credit_score": 720,
                "loan_amount": 250000,
                "tenure_months": 60,
                "existing_liabilities": 50000,
                "location": "New York",
                "employment_years": 5.5,
            }
        }

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
