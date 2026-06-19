"""
Test fixtures for loan applications
"""

from src.models import LoanApplication, EmploymentType


# Test Scenario 1: Strong applicant - should be APPROVED
APPROVED_APPLICANT = LoanApplication(
    applicant_id="APP_APPROVED_001",
    age=35,
    income=80000,
    employment_type=EmploymentType.EMPLOYED,
    credit_score=750,
    loan_amount=250000,
    tenure_months=60,
    existing_liabilities=30000,
    location="New York",
    employment_years=5.5,
)

# Test Scenario 2: Marginal applicant - should be MANUAL_REVIEW
MANUAL_REVIEW_APPLICANT = LoanApplication(
    applicant_id="APP_REVIEW_001",
    age=28,
    income=45000,
    employment_type=EmploymentType.SELF_EMPLOYED,
    credit_score=680,
    loan_amount=200000,
    tenure_months=84,
    existing_liabilities=60000,
    location="Los Angeles",
    employment_years=2.0,
)

# Test Scenario 3: Poor applicant - should be REJECTED
REJECTED_APPLICANT = LoanApplication(
    applicant_id="APP_REJECTED_001",
    age=24,
    income=28000,
    employment_type=EmploymentType.SELF_EMPLOYED,
    credit_score=580,
    loan_amount=500000,
    tenure_months=120,
    existing_liabilities=80000,
    location="Chicago",
    employment_years=0.5,
)

# Test Scenario 4: High income, excellent credit
EXCELLENT_APPLICANT = LoanApplication(
    applicant_id="APP_EXCELLENT_001",
    age=45,
    income=150000,
    employment_type=EmploymentType.EMPLOYED,
    credit_score=800,
    loan_amount=300000,
    tenure_months=60,
    existing_liabilities=20000,
    location="San Francisco",
    employment_years=10.0,
)

# Test Scenario 5: Low income, bad credit
POOR_APPLICANT = LoanApplication(
    applicant_id="APP_POOR_001",
    age=22,
    income=20000,
    employment_type=EmploymentType.UNEMPLOYED,
    credit_score=550,
    loan_amount=100000,
    tenure_months=120,
    existing_liabilities=45000,
    location="Detroit",
    employment_years=0.0,
)

# Test Scenario 6: Anomaly - high loan to income
ANOMALY_HIGH_LOAN = LoanApplication(
    applicant_id="APP_ANOMALY_001",
    age=30,
    income=30000,
    employment_type=EmploymentType.EMPLOYED,
    credit_score=700,
    loan_amount=750000,  # 25x income - anomaly
    tenure_months=180,
    existing_liabilities=50000,
    location="Miami",
    employment_years=3.0,
)

# Test Scenario 7: Young applicant, good financials
YOUNG_APPLICANT = LoanApplication(
    applicant_id="APP_YOUNG_001",
    age=21,
    income=55000,
    employment_type=EmploymentType.EMPLOYED,
    credit_score=720,
    loan_amount=180000,
    tenure_months=60,
    existing_liabilities=15000,
    location="Boston",
    employment_years=1.5,
)

# Test Scenario 8: Senior applicant, stable income
SENIOR_APPLICANT = LoanApplication(
    applicant_id="APP_SENIOR_001",
    age=68,
    income=120000,
    employment_type=EmploymentType.RETIRED,
    credit_score=780,
    loan_amount=200000,
    tenure_months=120,  # Longer tenure due to age
    existing_liabilities=10000,
    location="Miami",
    employment_years=0.0,  # Retired
)

# Test Scenario 9: High DTI ratio
HIGH_DTI_APPLICANT = LoanApplication(
    applicant_id="APP_DTI_HIGH_001",
    age=40,
    income=60000,
    employment_type=EmploymentType.EMPLOYED,
    credit_score=700,
    loan_amount=300000,
    tenure_months=180,
    existing_liabilities=120000,  # Very high liabilities
    location="Austin",
    employment_years=8.0,
)

# Test Scenario 10: Perfect profile
PERFECT_APPLICANT = LoanApplication(
    applicant_id="APP_PERFECT_001",
    age=40,
    income=200000,
    employment_type=EmploymentType.EMPLOYED,
    credit_score=820,
    loan_amount=300000,
    tenure_months=60,
    existing_liabilities=50000,
    location="Seattle",
    employment_years=12.0,
)


# Test scenarios collection
TEST_SCENARIOS = {
    "approved": APPROVED_APPLICANT,
    "manual_review": MANUAL_REVIEW_APPLICANT,
    "rejected": REJECTED_APPLICANT,
    "excellent": EXCELLENT_APPLICANT,
    "poor": POOR_APPLICANT,
    "anomaly": ANOMALY_HIGH_LOAN,
    "young": YOUNG_APPLICANT,
    "senior": SENIOR_APPLICANT,
    "high_dti": HIGH_DTI_APPLICANT,
    "perfect": PERFECT_APPLICANT,
}
