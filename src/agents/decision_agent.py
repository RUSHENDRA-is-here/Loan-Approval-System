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
        message = f"""Make a final loan decision based on the following analyses:

APPLICATION DATA:
- Applicant ID: {application_data.get('applicant_id')}
- Credit Score: {application_data.get('credit_score')}
- Loan Amount: ${application_data.get('loan_amount'):,.2f}
- Income: ${application_data.get('income'):,.2f}

PROFILE ANALYSIS:
{str(profile_analysis)}

FINANCIAL RISK ANALYSIS:
{str(risk_analysis)}

Based on these analyses, provide:
1. Decision: APPROVED, REJECTED, or MANUAL_REVIEW
2. Confidence score (0-1)
3. Risk score (0-100)
4. Key decision factors
5. Clear reasoning

Decision criteria:
- APPROVED: Low risk, confidence > 0.7, favorable profile and financials
- REJECTED: High risk, critical issues, confidence > 0.7 for rejection
- MANUAL_REVIEW: Borderline cases, insufficient clarity, confidence between 0.4-0.7

Return as JSON with: analysis, classification, confidence, risk_score, factors, reasoning
"""

        context = {**application_data, "profile_analysis": profile_analysis, "risk_analysis": risk_analysis}

        return self.execute(message, context=context)
