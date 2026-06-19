"""
Decision detail and history endpoints
"""

from fastapi import APIRouter, HTTPException
from src.mcp_servers import notification_server
from src.utils import get_logger
from typing import Dict, Any

router = APIRouter()
logger = get_logger("routes.decisions")

# Reference to applications store (imported in main.py context)
applications_store = {}


@router.get("/decisions/{case_id}")
async def get_decision_details(case_id: str):
    """Get detailed decision information"""
    logger.info(f"Retrieving decision for case {case_id}")

    # In production, lookup from database
    for app_id, app_data in applications_store.items():
        if app_data["decision"].get("case_id") == case_id:
            decision = app_data["decision"]
            return {
                "case_id": case_id,
                "application_id": app_id,
                "classification": decision["classification"],
                "confidence": decision["confidence"],
                "risk_score": decision["risk_score"],
                "factors": decision["factors"],
                "reasoning": decision["reasoning"],
                "profile_analysis": decision.get("profile_analysis"),
                "risk_analysis": decision.get("risk_analysis"),
            }

    raise HTTPException(status_code=404, detail="Decision not found")


@router.get("/decisions/{application_id}/history")
async def get_decision_history(application_id: str):
    """Get decision history for applicant"""
    logger.info(f"Retrieving history for {application_id}")

    # Get from notification server audit log
    history = notification_server.get_audit_history(application_id)

    return {
        "application_id": application_id,
        "entries": history["data"]["entries"],
        "total_entries": history["data"]["entry_count"],
    }


@router.post("/decisions/{case_id}/manual-review")
async def escalate_to_manual_review(case_id: str):
    """Escalate a decision to manual review"""
    logger.info(f"Escalating case {case_id} to manual review")

    # In production, update database
    return {
        "case_id": case_id,
        "status": "escalated",
        "message": "Case escalated to manual review team",
        "review_queue_position": 1,
    }
