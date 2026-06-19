from .base_agent import BaseAgent
from typing import Dict, Any
import json


class ApplicantProfileAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ApplicantProfileAgent",
            role="Analyze applicant's profile, income stability, and employment history",
            description="Evaluates applicant demographics, employment type, income consistency, and credit history",
        )

    def define_tools(self):
        return [
            {
                "name": "fetch_credit_history",
                "description": "Fetch applicant's credit history from database",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "applicant_id": {"type": "string"},
                    },
                    "required": ["applicant_id"],
                },
            },
            {
                "name": "verify_employment",
                "description": "Verify employment details of applicant",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "employment_type": {"type": "string"},
                        "years_employed": {"type": "number"},
                    },
                    "required": ["employment_type"],
                },
            },
        ]

    def analyze(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze applicant profile."""
        age = application_data.get('age', 0)
        emp_years = application_data.get('employment_years', 0)

        message = f"""You are analyzing a loan applicant's profile. Return ONLY JSON.

APPLICANT DATA:
- Applicant ID: {application_data.get('applicant_id')}
- Age: {age}
- Annual Income: ${application_data.get('income'):,.2f}
- Employment Type: {application_data.get('employment_type')}
- Employment Years: {emp_years}
- Location: {application_data.get('location')}

PROFILE ASSESSMENT RULES:
- Age 18-30: Young, may have less history (MEDIUM risk)
- Age 30-65: Prime working years (LOW risk)
- Age 65+: Near/past retirement (MEDIUM risk)
- Employment < 1 year: Unstable (HIGH risk)
- Employment 1-5 years: Developing (MEDIUM risk)
- Employment 5+ years: Stable (LOW risk)

Return this exact JSON format (ONLY JSON, no markdown):
{{
  "analysis": "Summary of profile assessment",
  "findings": {{
    "income_stability": "stable|developing|unstable",
    "employment_risk": "LOW|MEDIUM|HIGH",
    "age_category": "young|prime|senior",
    "profile_score": 0.85
  }},
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "confidence": 0.80,
  "reasoning": "Explain age, employment, and income stability assessment"
}}"""

        return self.execute(message, context=application_data)
