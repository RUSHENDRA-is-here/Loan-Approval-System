from .base_agent import BaseAgent
from typing import Dict, Any
from src.constants import DTI_RATIO_EXCELLENT, DTI_RATIO_GOOD, DTI_RATIO_FAIR


class FinancialRiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="FinancialRiskAgent",
            role="Assess financial risk through DTI, credit score, and debt analysis",
            description="Calculates risk metrics, identifies anomalies, and applies financial business rules",
        )

    def define_tools(self):
        return [
            {
                "name": "calculate_dti",
                "description": "Calculate Debt-to-Income ratio",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "monthly_income": {"type": "number"},
                        "monthly_obligations": {"type": "number"},
                    },
                    "required": ["monthly_income", "monthly_obligations"],
                },
            },
            {
                "name": "assess_credit_risk",
                "description": "Assess risk based on credit score",
                "input_schema": {
                    "type": "object",
                    "properties": {"credit_score": {"type": "integer"}},
                    "required": ["credit_score"],
                },
            },
            {
                "name": "detect_anomalies",
                "description": "Detect financial anomalies",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "loan_amount": {"type": "number"},
                        "annual_income": {"type": "number"},
                    },
                    "required": ["loan_amount", "annual_income"],
                },
            },
        ]

    def analyze(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial risk."""
        income = application_data.get("income", 0)
        liabilities = application_data.get("existing_liabilities", 0)
        loan_amount = application_data.get("loan_amount", 0)
        credit_score = application_data.get("credit_score", 0)
        tenure_months = application_data.get("tenure_months", 60)

        # Calculate monthly figures
        monthly_income = income / 12
        monthly_liabilities = liabilities / 12
        monthly_payment = loan_amount / tenure_months

        message = f"""Assess financial risk for loan application:

Annual Income: ${income:,.2f}
Monthly Income: ${monthly_income:,.2f}
Existing Liabilities: ${liabilities:,.2f}
Monthly Liabilities: ${monthly_liabilities:,.2f}
Loan Amount Requested: ${loan_amount:,.2f}
Monthly Loan Payment: ${monthly_payment:,.2f}
Credit Score: {credit_score}
Loan Tenure: {tenure_months} months

Calculate and analyze:
1. Debt-to-Income ratio (current and with new loan)
2. Credit score risk assessment
3. Loan amount vs income ratio
4. Anomaly detection
5. Overall financial risk level

Return as JSON with: analysis, findings, risk_level, confidence, reasoning
DTI thresholds: Excellent <{DTI_RATIO_EXCELLENT}%, Good <{DTI_RATIO_GOOD}%, Fair <{DTI_RATIO_FAIR}%
"""

        return self.execute(message, context=application_data)
