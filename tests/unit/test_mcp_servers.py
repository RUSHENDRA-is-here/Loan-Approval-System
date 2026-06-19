"""
Unit tests for MCP servers
"""

import pytest
from src.mcp_servers import (
    applicant_db_server,
    risk_rules_server,
    decision_synthesis_server,
    notification_server,
)


class TestApplicantDBServer:
    """Test ApplicantDB MCP server"""

    def test_credit_history_retrieval(self):
        """Test retrieving credit history"""
        result = applicant_db_server.get_credit_history("APP001")

        assert result["status"] == "success"
        assert "data" in result
        assert result["data"]["credit_score"] == 750

    def test_employment_verification(self):
        """Test employment verification"""
        result = applicant_db_server.verify_employment("employed", 5.5)

        assert result["status"] == "success"
        assert result["data"]["stability_score"] > 0
        assert result["data"]["verification"] == "Verified"

    def test_applicant_data_validation_complete(self):
        """Test validation of complete applicant data"""
        app_data = {
            "applicant_id": "APP001",
            "age": 35,
            "income": 80000,
            "employment_type": "employed",
            "credit_score": 750,
            "loan_amount": 250000,
            "tenure_months": 60,
        }

        result = applicant_db_server.validate_applicant_data(app_data)

        assert result["status"] == "success"
        assert result["data"]["is_complete"] is True
        assert result["data"]["completeness_percentage"] == 100


class TestRiskRulesServer:
    """Test RiskRulesDB MCP server"""

    def test_dti_calculation_low(self):
        """Test DTI calculation for low DTI"""
        result = risk_rules_server.calculate_dti_ratio(5000, 1000)

        assert result["status"] == "success"
        assert result["data"]["dti_ratio"] == 20.0
        assert result["data"]["risk_level"] == "LOW"

    def test_dti_calculation_high(self):
        """Test DTI calculation for high DTI"""
        result = risk_rules_server.calculate_dti_ratio(2000, 1500)

        assert result["status"] == "success"
        assert result["data"]["dti_ratio"] == 75.0
        assert result["data"]["risk_level"] == "HIGH"

    def test_credit_risk_excellent(self):
        """Test credit risk for excellent score"""
        result = risk_rules_server.assess_credit_risk(800)

        assert result["status"] == "success"
        assert result["data"]["risk_level"] == "LOW"
        assert result["data"]["score_category"] == "Excellent"

    def test_credit_risk_poor(self):
        """Test credit risk for poor score"""
        result = risk_rules_server.assess_credit_risk(580)

        assert result["status"] == "success"
        assert result["data"]["risk_level"] == "CRITICAL"
        assert result["data"]["score_category"] == "Very Poor"

    def test_anomaly_detection_high_loan(self):
        """Test anomaly detection for high loan amount"""
        result = risk_rules_server.detect_anomalies(750000, 30000)

        assert result["status"] == "success"
        assert result["data"]["anomalies_detected"] is True
        assert len(result["data"]["anomaly_list"]) > 0

    def test_business_rules_violation(self):
        """Test business rules checking"""
        app_data = {
            "age": 18,  # Below 21 threshold
            "credit_score": 580,
            "income": 30000,
            "loan_amount": 200000,
        }

        result = risk_rules_server.apply_business_rules(app_data)

        assert result["status"] == "success"
        assert result["data"]["rules_passed"] is False
        assert len(result["data"]["violations"]) > 0


class TestDecisionSynthesisServer:
    """Test DecisionSynthesis MCP server"""

    def test_factor_synthesis_approved(self):
        """Test factor synthesis for approval"""
        result = decision_synthesis_server.synthesize_factors(
            profile_risk="LOW",
            financial_risk="LOW",
            credit_score=750,
            dti_ratio=20,
            factors=["Good credit", "Low DTI"],
        )

        assert result["status"] == "success"
        assert result["data"]["recommendation"] == "APPROVED"
        assert result["data"]["confidence"] > 0.7

    def test_factor_synthesis_rejected(self):
        """Test factor synthesis for rejection"""
        result = decision_synthesis_server.synthesize_factors(
            profile_risk="HIGH",
            financial_risk="CRITICAL",
            credit_score=550,
            dti_ratio=80,
            factors=["Poor credit", "High DTI"],
        )

        assert result["status"] == "success"
        assert result["data"]["recommendation"] == "REJECTED"

    def test_explanation_generation(self):
        """Test explanation generation"""
        result = decision_synthesis_server.generate_explanation(
            decision="APPROVED",
            factors=["Good credit", "Stable income"],
            risk_score=25,
            confidence=0.85,
        )

        assert result["status"] == "success"
        assert "approved" in result["data"]["explanation"].lower()
        assert len(result["data"]["detailed_factors"]) > 0

    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        result = decision_synthesis_server.calculate_confidence_score(
            profile_strength=0.8, financial_strength=0.85, anomaly_count=0
        )

        assert result["status"] == "success"
        assert 0 <= result["data"]["final_confidence"] <= 1


class TestNotificationServer:
    """Test NotificationSystem MCP server"""

    def test_audit_entry_creation(self):
        """Test creating audit entry"""
        result = notification_server.create_audit_entry(
            "APP001", "APPROVED", "Strong financials"
        )

        assert result["status"] == "success"
        assert "entry_id" in result["data"]
        assert result["data"]["applicant_id"] == "APP001"

    def test_notification_generation_approved(self):
        """Test notification generation for approval"""
        result = notification_server.generate_notification(
            "APP001", "APPROVED", "Good credit"
        )

        assert result["status"] == "success"
        assert "APPROVED" in result["data"]["notification"]

    def test_notification_generation_rejected(self):
        """Test notification generation for rejection"""
        result = notification_server.generate_notification(
            "APP002", "REJECTED", "Low credit score"
        )

        assert result["status"] == "success"
        assert "REJECTED" in result["data"]["notification"]

    def test_decision_logging(self):
        """Test logging decision"""
        result = notification_server.log_decision(
            "APP001", "CASE-001", "APPROVED", 25, 0.85
        )

        assert result["status"] == "success"
        assert result["data"]["log_status"] == "Decision logged successfully"

    def test_case_file_creation(self):
        """Test creating case file"""
        app_data = {
            "income": 80000,
            "loan_amount": 250000,
            "credit_score": 750,
        }
        analysis_data = {"risk_score": 25, "confidence": 0.85}

        result = notification_server.create_case_file(
            "APP001", "APPROVED", app_data, analysis_data
        )

        assert result["status"] == "success"
        assert "case_id" in result["data"]
        assert result["data"]["decision"] == "APPROVED"
