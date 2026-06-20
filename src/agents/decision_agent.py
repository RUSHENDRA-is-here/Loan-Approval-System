from .base_agent import BaseAgent
from typing import Dict, Any
import json


class DecisionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DecisionAgent",
            role="Synthesize risk factors and make final loan decision",
            description="Combines profile and risk analysis to produce APPROVED, REJECTED, or MANUAL_REVIEW decision",
        )

    def define_tools(self):
        return []  # No tools - direct decision making

    def execute(self, user_message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Override execute to use direct analysis instead of Claude API"""
        return self._direct_analysis(context or {})

    async def execute_async(self, user_message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Override execute_async to use direct analysis instead of Claude API"""
        return self._direct_analysis(context or {})

    def _direct_analysis(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make loan decision based on application data metrics."""
        credit_score = application_data.get('credit_score', 0)
        income = application_data.get('income', 0)
        loan_amount = application_data.get('loan_amount', 0)
        existing_liabilities = application_data.get('existing_liabilities', 0)
        tenure_months = application_data.get('tenure_months', 60)

        # Calculate monthly figures
        monthly_income = income / 12 if income > 0 else 0
        monthly_liabilities = existing_liabilities / 12
        monthly_payment = loan_amount / tenure_months if tenure_months > 0 else 0

        # DTI includes existing liabilities + new loan payment
        dti = ((monthly_liabilities + monthly_payment) / monthly_income * 100) if monthly_income > 0 else 0

        # Make direct decision based on metrics
        if credit_score >= 750 and dti < 30:
            classification = "APPROVED"
            confidence = 0.90
            risk_score = 15
            factors = [
                f"Excellent credit score ({credit_score})",
                f"Low DTI ratio ({dti:.1f}%)",
                "Strong financial profile",
                f"Stable {application_data.get('employment_type')} employment"
            ]
        elif credit_score >= 700 and dti < 40:
            classification = "APPROVED"
            confidence = 0.80
            risk_score = 28
            factors = [
                f"Good credit score ({credit_score})",
                f"Acceptable DTI ratio ({dti:.1f}%)",
                "Solid financial position",
                f"Employed as {application_data.get('employment_type')}"
            ]
        elif credit_score < 650 or dti > 45 or loan_amount > income * 5:
            classification = "REJECTED"
            confidence = 0.80
            risk_score = 78
            factors = [
                f"Poor credit score ({credit_score})" if credit_score < 650 else f"Credit score {credit_score}",
                f"High DTI ratio ({dti:.1f}%)" if dti > 45 else f"DTI ratio {dti:.1f}%",
                f"Excessive loan-to-income ratio ({loan_amount/income:.1f}x)" if loan_amount > income * 5 else "",
                "Insufficient financial stability"
            ]
            factors = [f for f in factors if f]  # Remove empty strings
        else:
            classification = "MANUAL_REVIEW"
            confidence = 0.60
            risk_score = 55
            factors = [
                f"Credit score {credit_score} (borderline)",
                f"DTI ratio {dti:.1f}% (fair)",
                "Mixed financial signals",
                "Requires human review"
            ]

        reasoning = f"Applicant with credit score {credit_score} and DTI {dti:.1f}% qualifies for {classification}. "
        if credit_score >= 700:
            reasoning += "Strong credit history supports approval. "
        elif credit_score >= 650:
            reasoning += "Fair credit history noted. "
        else:
            reasoning += "Poor credit history is a concern. "

        if dti < 30:
            reasoning += "Low debt obligations indicate strong repayment capacity."
        elif dti < 43:
            reasoning += "Moderate debt obligations are acceptable."
        else:
            reasoning += "High debt obligations are concerning."

        return {
            "agent": self.name,
            "status": "success",
            "content": [{
                "classification": classification,
                "confidence": confidence,
                "risk_score": risk_score,
                "factors": factors,
                "reasoning": reasoning
            }]
        }
