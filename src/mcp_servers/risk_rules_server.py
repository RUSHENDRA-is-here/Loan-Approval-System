"""
MCP Server: RiskRulesDB
Provides tools for risk assessment and business rule validation
"""

from typing import Dict, Any
from src.constants import (
    DTI_RATIO_EXCELLENT,
    DTI_RATIO_GOOD,
    DTI_RATIO_FAIR,
    CREDIT_SCORE_EXCELLENT,
    CREDIT_SCORE_GOOD,
    CREDIT_SCORE_FAIR,
    CREDIT_SCORE_POOR,
)


class RiskRulesServer:
    def __init__(self):
        self.name = "RiskRulesDB"

    def calculate_dti_ratio(
        self, monthly_income: float, monthly_obligations: float
    ) -> Dict[str, Any]:
        """Calculate Debt-to-Income ratio"""
        if monthly_income <= 0:
            return {
                "status": "error",
                "error": "Invalid monthly income",
                "dti_ratio": None,
            }

        dti_ratio = (monthly_obligations / monthly_income) * 100

        if dti_ratio < DTI_RATIO_EXCELLENT:
            risk_level = "LOW"
        elif dti_ratio < DTI_RATIO_GOOD:
            risk_level = "LOW"
        elif dti_ratio < DTI_RATIO_FAIR:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        return {
            "status": "success",
            "data": {
                "dti_ratio": round(dti_ratio, 2),
                "risk_level": risk_level,
                "reasoning": f"DTI of {dti_ratio:.2f}% indicates {risk_level} risk",
                "monthly_income": monthly_income,
                "monthly_obligations": monthly_obligations,
            },
        }

    def assess_credit_risk(self, credit_score: int) -> Dict[str, Any]:
        """Assess credit risk based on credit score"""
        if credit_score >= CREDIT_SCORE_EXCELLENT:
            risk_level = "LOW"
            recommendation = "Excellent credit profile"
        elif credit_score >= CREDIT_SCORE_GOOD:
            risk_level = "LOW"
            recommendation = "Good credit profile"
        elif credit_score >= CREDIT_SCORE_FAIR:
            risk_level = "MEDIUM"
            recommendation = "Fair credit profile - monitor"
        elif credit_score >= CREDIT_SCORE_POOR:
            risk_level = "HIGH"
            recommendation = "Poor credit profile - high caution"
        else:
            risk_level = "CRITICAL"
            recommendation = "Very poor credit - significant risk"

        return {
            "status": "success",
            "data": {
                "credit_score": credit_score,
                "risk_level": risk_level,
                "recommendation": recommendation,
                "score_category": self._categorize_credit_score(credit_score),
            },
        }

    def detect_anomalies(self, loan_amount: float, annual_income: float) -> Dict[str, Any]:
        """Detect financial anomalies"""
        anomalies = []
        flags = []

        loan_to_income_ratio = loan_amount / annual_income if annual_income > 0 else 0

        if loan_to_income_ratio > 5:
            anomalies.append("Loan amount exceeds 5x annual income")
            flags.append("HIGH_LOAN_RATIO")
        elif loan_to_income_ratio > 3:
            anomalies.append("Loan amount is 3-5x annual income")
            flags.append("ELEVATED_LOAN_RATIO")

        if annual_income < 25000:
            anomalies.append("Very low annual income")
            flags.append("LOW_INCOME")

        return {
            "status": "success",
            "data": {
                "loan_to_income_ratio": round(loan_to_income_ratio, 2),
                "anomalies_detected": len(anomalies) > 0,
                "anomaly_list": anomalies,
                "risk_flags": flags,
                "anomaly_count": len(anomalies),
            },
        }

    def apply_business_rules(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply standard business rules"""
        violations = []

        age = application_data.get("age", 0)
        if age < 21:
            violations.append("Applicant under 21 years old")
        elif age > 80:
            violations.append("Applicant over 80 years old")

        credit_score = application_data.get("credit_score", 0)
        if credit_score < 600:
            violations.append("Credit score below minimum threshold (600)")

        income = application_data.get("income", 0)
        loan_amount = application_data.get("loan_amount", 0)
        if loan_amount > income * 5:
            violations.append("Loan amount exceeds 5x annual income")

        return {
            "status": "success",
            "data": {
                "rules_passed": len(violations) == 0,
                "violations": violations,
                "violation_count": len(violations),
            },
        }

    def _categorize_credit_score(self, score: int) -> str:
        """Categorize credit score"""
        if score >= 750:
            return "Excellent"
        elif score >= 700:
            return "Good"
        elif score >= 650:
            return "Fair"
        elif score >= 600:
            return "Poor"
        else:
            return "Very Poor"


# Singleton instance
risk_rules_server = RiskRulesServer()
