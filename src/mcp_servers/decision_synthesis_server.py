"""
MCP Server: DecisionSynthesis
Provides tools for synthesizing decisions and explanations
"""

from typing import Dict, Any, List
from src.constants import DecisionRule


class DecisionSynthesisServer:
    def __init__(self):
        self.name = "DecisionSynthesis"

    def synthesize_factors(
        self,
        profile_risk: str,
        financial_risk: str,
        credit_score: int,
        dti_ratio: float,
        factors: List[str],
    ) -> Dict[str, Any]:
        """Synthesize all factors into decision recommendations"""
        risk_weights = {
            "LOW": 0.2,
            "MEDIUM": 0.5,
            "HIGH": 0.8,
            "CRITICAL": 1.0,
        }

        profile_score = risk_weights.get(profile_risk, 0.5)
        financial_score = risk_weights.get(financial_risk, 0.5)

        # Weighted average with financial risk getting more weight
        overall_risk = profile_score * 0.3 + financial_score * 0.7

        # Additional scoring for DTI and credit score
        if dti_ratio > 43:
            overall_risk += 0.15
        if credit_score < 650:
            overall_risk += 0.15

        overall_risk = min(1.0, overall_risk)
        risk_score = int(overall_risk * 100)

        # Determine recommendation
        if overall_risk < 0.3:
            recommendation = "APPROVED"
            confidence = 0.9
        elif overall_risk < 0.5:
            recommendation = "APPROVED"
            confidence = 0.75
        elif overall_risk < 0.7:
            recommendation = "MANUAL_REVIEW"
            confidence = 0.6
        else:
            recommendation = "REJECTED"
            confidence = 0.8

        return {
            "status": "success",
            "data": {
                "overall_risk": round(overall_risk, 2),
                "risk_score": risk_score,
                "recommendation": recommendation,
                "confidence": confidence,
                "contributing_factors": factors,
                "factor_count": len(factors),
            },
        }

    def generate_explanation(
        self,
        decision: str,
        factors: List[str],
        risk_score: int,
        confidence: float,
    ) -> Dict[str, Any]:
        """Generate detailed explanation for decision"""
        explanations = {
            "APPROVED": f"Application approved with confidence {confidence:.0%}. Applicant meets approval criteria with acceptable risk profile (score: {risk_score}/100).",
            "REJECTED": f"Application rejected with confidence {confidence:.0%}. Significant risk factors identified (score: {risk_score}/100).",
            "MANUAL_REVIEW": f"Application requires manual review. Borderline case with confidence {confidence:.0%} (score: {risk_score}/100). Review recommended.",
        }

        base_explanation = explanations.get(
            decision, "Decision pending further review."
        )

        if factors:
            factors_text = "Key factors: " + ", ".join(factors)
        else:
            factors_text = "No specific risk factors identified."

        return {
            "status": "success",
            "data": {
                "decision": decision,
                "explanation": base_explanation,
                "detailed_factors": factors_text,
                "risk_factors": [f for f in factors if "risk" in f.lower()],
                "positive_factors": [
                    f for f in factors if "good" in f.lower() or "strong" in f.lower()
                ],
            },
        }

    def calculate_confidence_score(
        self, profile_strength: float, financial_strength: float, anomaly_count: int
    ) -> Dict[str, Any]:
        """Calculate confidence score for decision"""
        base_confidence = (profile_strength + financial_strength) / 2

        # Reduce confidence based on anomalies
        anomaly_penalty = anomaly_count * 0.05
        adjusted_confidence = max(0.0, min(1.0, base_confidence - anomaly_penalty))

        return {
            "status": "success",
            "data": {
                "base_confidence": round(base_confidence, 2),
                "anomaly_penalty": round(anomaly_penalty, 2),
                "final_confidence": round(adjusted_confidence, 2),
                "confidence_level": self._categorize_confidence(adjusted_confidence),
            },
        }

    def _categorize_confidence(self, confidence: float) -> str:
        """Categorize confidence level"""
        if confidence >= 0.85:
            return "Very High"
        elif confidence >= 0.70:
            return "High"
        elif confidence >= 0.50:
            return "Moderate"
        else:
            return "Low"


# Singleton instance
decision_synthesis_server = DecisionSynthesisServer()
