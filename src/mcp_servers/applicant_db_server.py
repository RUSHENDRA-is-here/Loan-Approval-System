"""
MCP Server: ApplicantDB
Provides tools for accessing applicant profile and credit information
"""

from typing import Dict, Any, Optional


class ApplicantDBServer:
    def __init__(self):
        self.name = "ApplicantDB"

    def get_credit_history(self, applicant_id: str) -> Dict[str, Any]:
        """Fetch credit history for applicant"""
        # Mock data - in production, this would query a database
        mock_histories = {
            "APP001": {
                "credit_score": 750,
                "years_of_credit": 10,
                "accounts_open": 5,
                "accounts_closed": 2,
                "late_payments": 0,
                "charge_offs": 0,
                "bankruptcies": 0,
                "inquiries_last_6m": 1,
                "summary": "Excellent credit history",
            },
            "APP002": {
                "credit_score": 680,
                "years_of_credit": 5,
                "accounts_open": 3,
                "accounts_closed": 1,
                "late_payments": 2,
                "charge_offs": 0,
                "bankruptcies": 0,
                "inquiries_last_6m": 3,
                "summary": "Fair credit history with recent inquiries",
            },
        }

        if applicant_id in mock_histories:
            return {"status": "success", "data": mock_histories[applicant_id]}
        return {
            "status": "success",
            "data": {
                "credit_score": 700,
                "years_of_credit": 8,
                "summary": "Standard credit profile",
            },
        }

    def verify_employment(
        self, employment_type: str, years_employed: Optional[float] = None
    ) -> Dict[str, Any]:
        """Verify employment details"""
        employment_scores = {
            "employed": 0.85,
            "self_employed": 0.70,
            "unemployed": 0.0,
            "retired": 0.80,
        }

        stability_score = employment_scores.get(employment_type, 0.5)

        if years_employed:
            if years_employed < 1:
                stability_score *= 0.7
            elif years_employed >= 5:
                stability_score *= 1.1

        return {
            "status": "success",
            "data": {
                "employment_type": employment_type,
                "years_employed": years_employed or 0,
                "stability_score": min(1.0, stability_score),
                "verification": "Verified",
            },
        }

    def validate_applicant_data(self, applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate applicant data completeness"""
        required_fields = [
            "applicant_id",
            "age",
            "income",
            "employment_type",
            "credit_score",
            "loan_amount",
            "tenure_months",
        ]

        missing_fields = [f for f in required_fields if f not in applicant_data]
        completeness = (len(required_fields) - len(missing_fields)) / len(required_fields)

        return {
            "status": "success",
            "data": {
                "is_complete": len(missing_fields) == 0,
                "completeness_percentage": completeness * 100,
                "missing_fields": missing_fields,
                "validation_status": "Valid" if len(missing_fields) == 0 else "Incomplete",
            },
        }


# Singleton instance
applicant_db_server = ApplicantDBServer()
