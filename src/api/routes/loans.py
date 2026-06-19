"""
Loan submission and status endpoints
"""

from fastapi import APIRouter, HTTPException
from src.models import LoanApplication, ApplicationStatus
from src.orchestration import LoanOrchestrator
from src.utils import get_logger
from typing import Dict, Any

router = APIRouter()
logger = get_logger("routes.loans")

# In-memory storage for demo (use database in production)
applications_store: Dict[str, Dict[str, Any]] = {}
orchestrator = LoanOrchestrator()


@router.post("/loans/submit")
async def submit_loan_application(application: LoanApplication):
    """Submit a new loan application for processing"""
    logger.info(f"Received application from {application.applicant_id}")

    try:
        # Process application through orchestrator
        decision_response = orchestrator.process_application(application)

        # Store in memory
        applications_store[application.applicant_id] = {
            "application": application.model_dump(),
            "decision": decision_response.model_dump(),
            "status": ApplicationStatus.COMPLETED,
        }

        logger.info(
            f"Application {application.applicant_id} processed: {decision_response.classification}"
        )

        return {
            "status": "success",
            "application_id": application.applicant_id,
            "decision": decision_response.classification,
            "case_id": decision_response.case_id,
            "confidence": decision_response.confidence,
            "message": f"Application processed. Decision: {decision_response.classification}",
        }

    except Exception as e:
        logger.error(f"Error processing application: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/loans/{application_id}")
async def get_application_status(application_id: str):
    """Get status of a loan application"""
    if application_id not in applications_store:
        raise HTTPException(status_code=404, detail="Application not found")

    app_data = applications_store[application_id]

    return {
        "application_id": application_id,
        "status": app_data["status"],
        "decision": app_data["decision"]["classification"],
        "case_id": app_data["decision"].get("case_id"),
        "confidence": app_data["decision"]["confidence"],
    }


@router.get("/loans")
async def list_applications():
    """List all applications (limited to last 10)"""
    applications = list(applications_store.items())[-10:]

    return {
        "total": len(applications_store),
        "applications": [
            {
                "application_id": app_id,
                "decision": app_data["decision"]["classification"],
                "status": app_data["status"],
            }
            for app_id, app_data in applications
        ],
    }
