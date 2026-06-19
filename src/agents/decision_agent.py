from .base_agent import BaseAgent
from typing import Dict, Any


class DecisionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DecisionAgent",
            role="Synthesize risk factors and make final loan decision",
            description="Combines profile and risk analysis to produce APPROVED, REJECTED, or MANUAL_REVIEW decision",
        )

    def define_tools(self):
        return [
            {
                "name": "synthesize_decision",
                "description": "Synthesize all factors into a decision",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "profile_risk": {"type": "string"},
                        "financial_risk": {"type": "string"},
                        "overall_factors": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["profile_risk", "financial_risk"],
                },
            }
        ]

    def analyze(
        self,
        application_data: Dict[str, Any],
        profile_analysis: Dict[str, Any],
        risk_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Make loan decision based on all analyses."""
        credit_score = application_data.get('credit_score', 0)
        income = application_data.get('income', 0)
        loan_amount = application_data.get('loan_amount', 0)
        dti = (application_data.get('existing_liabilities', 0) / (income / 12)) * 100 if income > 0 else 0

        message = f"""You are a loan decision expert. Make a final loan decision based on this data:

APPLICATION DATA:
- Applicant ID: {application_data.get('applicant_id')}
- Age: {application_data.get('age')}
- Credit Score: {credit_score}
- Annual Income: ${income:,.2f}
- Loan Amount: ${loan_amount:,.2f}
- Monthly DTI: {dti:.1f}%
- Employment: {application_data.get('employment_type')}

DECISION RULES:
- Credit Score >= 750: Excellent (LOW risk)
- Credit Score 700-749: Good (LOW risk)
- Credit Score 650-699: Fair (MEDIUM risk)
- Credit Score < 650: Poor (HIGH risk)
- DTI < 30%: Good
- DTI 30-43%: Fair
- DTI > 43%: Poor

Make your decision using this exact JSON format (no markdown, just raw JSON):
{{
  "analysis": "Brief analysis of the application",
  "classification": "APPROVED or REJECTED or MANUAL_REVIEW",
  "confidence": 0.85,
  "risk_score": 25,
  "factors": [
    "Factor 1 explaining decision",
    "Factor 2 explaining decision",
    "Factor 3 explaining decision"
  ],
  "reasoning": "Detailed reasoning for this specific decision. Explain credit score impact, DTI impact, and overall financial health."
}}

CRITICAL: Return ONLY the JSON object, no other text."""

        context = {**application_data, "profile_analysis": profile_analysis, "risk_analysis": risk_analysis}

        return self.execute(message, context=context)
