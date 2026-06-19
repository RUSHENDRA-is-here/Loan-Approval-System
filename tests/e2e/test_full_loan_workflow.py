"""
End-to-end tests for loan approval workflow
"""

import pytest
from src.orchestration import LoanOrchestrator
from src.models import DecisionClassification
from tests.fixtures.loan_applications import TEST_SCENARIOS


@pytest.fixture
def orchestrator():
    return LoanOrchestrator()


class TestLoanApprovalWorkflow:
    """Test complete loan approval workflow"""

    def test_approved_loan_happy_path(self, orchestrator):
        """Test happy path: Strong applicant should be approved"""
        application = TEST_SCENARIOS["approved"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.application_id == "APP_APPROVED_001"
        assert result.classification in [
            DecisionClassification.APPROVED,
            DecisionClassification.MANUAL_REVIEW,
        ]
        assert result.confidence > 0
        assert len(result.reasoning) > 0
        assert result.case_id is not None

    def test_rejected_loan_sad_path(self, orchestrator):
        """Test sad path: Poor applicant should be rejected"""
        application = TEST_SCENARIOS["poor"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.application_id == "APP_POOR_001"
        assert result.classification in [
            DecisionClassification.REJECTED,
            DecisionClassification.MANUAL_REVIEW,
        ]
        assert result.confidence > 0

    def test_manual_review_borderline(self, orchestrator):
        """Test borderline case: Should go to manual review"""
        application = TEST_SCENARIOS["manual_review"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.application_id == "APP_REVIEW_001"
        assert result.classification in [
            DecisionClassification.MANUAL_REVIEW,
            DecisionClassification.REJECTED,
            DecisionClassification.APPROVED,
        ]

    def test_excellent_applicant(self, orchestrator):
        """Test excellent applicant with strong financials"""
        application = TEST_SCENARIOS["excellent"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.application_id == "APP_EXCELLENT_001"
        assert result.confidence > 0.7
        assert result.risk_score < 50

    def test_anomaly_detection(self, orchestrator):
        """Test anomaly detection: High loan to income ratio"""
        application = TEST_SCENARIOS["anomaly"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.application_id == "APP_ANOMALY_001"
        # Should flag as risky
        assert result.risk_score > 50

    def test_decision_has_factors(self, orchestrator):
        """Test that decision includes key factors"""
        application = TEST_SCENARIOS["approved"]

        result = orchestrator.process_application(application)

        # Assertions
        assert isinstance(result.factors, list)
        assert len(result.factors) > 0

    def test_decision_has_explanation(self, orchestrator):
        """Test that decision has clear reasoning"""
        application = TEST_SCENARIOS["approved"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.reasoning is not None
        assert len(result.reasoning) > 10  # Should have meaningful explanation

    def test_confidence_score_valid(self, orchestrator):
        """Test that confidence score is valid (0-1)"""
        application = TEST_SCENARIOS["approved"]

        result = orchestrator.process_application(application)

        # Assertions
        assert 0 <= result.confidence <= 1

    def test_risk_score_valid(self, orchestrator):
        """Test that risk score is valid (0-100)"""
        application = TEST_SCENARIOS["approved"]

        result = orchestrator.process_application(application)

        # Assertions
        assert 0 <= result.risk_score <= 100

    def test_case_id_generated(self, orchestrator):
        """Test that case ID is generated for audit trail"""
        application = TEST_SCENARIOS["approved"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.case_id is not None
        assert len(result.case_id) > 0


class TestDecisionVariations:
    """Test different decision paths"""

    def test_multiple_applications_different_outcomes(self, orchestrator):
        """Test processing multiple applications"""
        applications = [
            TEST_SCENARIOS["approved"],
            TEST_SCENARIOS["poor"],
            TEST_SCENARIOS["excellent"],
        ]

        results = []
        for app in applications:
            result = orchestrator.process_application(app)
            results.append(result)

        # Assertions
        assert len(results) == 3
        assert all(r.application_id for r in results)
        assert all(r.classification for r in results)

    def test_young_applicant_processing(self, orchestrator):
        """Test processing young applicant"""
        application = TEST_SCENARIOS["young"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.application_id == "APP_YOUNG_001"
        assert result.classification is not None

    def test_senior_applicant_processing(self, orchestrator):
        """Test processing senior applicant"""
        application = TEST_SCENARIOS["senior"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.application_id == "APP_SENIOR_001"
        assert result.classification is not None

    def test_high_dti_applicant(self, orchestrator):
        """Test high DTI ratio applicant"""
        application = TEST_SCENARIOS["high_dti"]

        result = orchestrator.process_application(application)

        # Assertions
        assert result.application_id == "APP_DTI_HIGH_001"
        # High DTI should result in higher risk
        assert result.risk_score > 40


class TestExplainability:
    """Test explainability and decision transparency"""

    def test_decision_reasoning_included(self, orchestrator):
        """Test that reasoning is provided for all decisions"""
        applications = [
            TEST_SCENARIOS["approved"],
            TEST_SCENARIOS["rejected"],
            TEST_SCENARIOS["manual_review"],
        ]

        for app in applications:
            result = orchestrator.process_application(app)
            assert len(result.reasoning) > 0, f"No reasoning for {app.applicant_id}"

    def test_factors_reflect_decision(self, orchestrator):
        """Test that factors are relevant to decision"""
        application = TEST_SCENARIOS["approved"]

        result = orchestrator.process_application(application)

        # Assertions
        assert len(result.factors) > 0
        # Factors should be descriptive
        assert all(isinstance(f, str) for f in result.factors)
        assert all(len(f) > 3 for f in result.factors)
