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
        current_dti = (monthly_liabilities / monthly_income * 100) if monthly_income > 0 else 0
        new_dti = ((monthly_liabilities + monthly_payment) / monthly_income * 100) if monthly_income > 0 else 0
        loan_to_income = loan_amount / income if income > 0 else 0

        message = f"""You are a financial risk analyst. Assess financial risk. Return ONLY JSON.

FINANCIAL DATA:
- Annual Income: ${income:,.2f}
- Monthly Income: ${monthly_income:,.2f}
- Existing Monthly Liabilities: ${monthly_liabilities:,.2f}
- Current DTI: {current_dti:.1f}%
- Loan Amount: ${loan_amount:,.2f}
- New Monthly Payment: ${monthly_payment:,.2f}
- New DTI (with loan): {new_dti:.1f}%
- Credit Score: {credit_score}
- Loan-to-Income Ratio: {loan_to_income:.2f}x

RISK THRESHOLDS:
- DTI < 20%: Excellent
- DTI 20-30%: Good
- DTI 30-43%: Fair/Acceptable
- DTI > 43%: Poor
- Credit 750+: Excellent
- Credit 700-749: Good
- Credit 650-699: Fair
- Credit < 650: Poor
- Loan/Income > 5x: Anomaly

Return this exact JSON (ONLY JSON, no markdown):
{{
  "analysis": "Summary of financial risk assessment",
  "findings": {{
    "current_dti": {current_dti:.1f},
    "new_dti": {new_dti:.1f},
    "credit_category": "excellent|good|fair|poor",
    "loan_to_income": {loan_to_income:.2f},
    "anomalies": ["list", "of", "anomalies"]
  }},
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "confidence": 0.85,
  "reasoning": "Explain DTI impact, credit score assessment, loan amount appropriateness"
}}"""

        return self.execute(message, context=application_data)
