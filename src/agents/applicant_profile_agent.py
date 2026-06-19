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
        message = f"""Analyze the following loan application profile:

Applicant ID: {application_data.get('applicant_id')}
Age: {application_data.get('age')}
Income: ${application_data.get('income'):,.2f}
Employment Type: {application_data.get('employment_type')}
Employment Years: {application_data.get('employment_years', 'Not specified')}
Location: {application_data.get('location')}

Provide analysis of:
1. Income stability indicators
2. Employment risk assessment
3. Applicant completeness
4. Credit history summary (if available)

Return as JSON with: analysis, findings, risk_level, confidence, reasoning
"""

        return self.execute(message, context=application_data)
