"""
MCP Server: NotificationSystem
Provides tools for logging, notifications, and audit trails
"""

from typing import Dict, Any
import uuid
from datetime import datetime


class NotificationServer:
    def __init__(self):
        self.name = "NotificationSystem"
        # In-memory audit log (in production, use database)
        self.audit_log = []

    def create_audit_entry(
        self, applicant_id: str, decision: str, reasoning: str
    ) -> Dict[str, Any]:
        """Create audit trail entry"""
        entry_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        audit_entry = {
            "entry_id": entry_id,
            "applicant_id": applicant_id,
            "decision": decision,
            "reasoning": reasoning,
            "timestamp": timestamp,
            "status": "logged",
        }

        self.audit_log.append(audit_entry)

        return {
            "status": "success",
            "data": {
                "entry_id": entry_id,
                "applicant_id": applicant_id,
                "timestamp": timestamp,
                "message": f"Audit entry created for {applicant_id}",
            },
        }

    def generate_notification(
        self, applicant_id: str, decision: str, reason: str
    ) -> Dict[str, Any]:
        """Generate notification message"""
        notifications = {
            "APPROVED": f"Dear Applicant, your loan application (ID: {applicant_id}) has been APPROVED. Our team will contact you shortly with next steps.",
            "REJECTED": f"Dear Applicant, your loan application (ID: {applicant_id}) has been REJECTED. Reason: {reason}. You can reapply after 90 days.",
            "MANUAL_REVIEW": f"Dear Applicant, your loan application (ID: {applicant_id}) requires manual review. We will contact you within 3 business days.",
        }

        notification_text = notifications.get(
            decision, f"Application status update for {applicant_id}: {decision}"
        )

        return {
            "status": "success",
            "data": {
                "applicant_id": applicant_id,
                "decision": decision,
                "notification": notification_text,
                "notification_type": "email",
                "scheduled": True,
            },
        }

    def log_decision(
        self,
        applicant_id: str,
        case_id: str,
        decision: str,
        risk_score: int,
        confidence: float,
    ) -> Dict[str, Any]:
        """Log decision with metadata"""
        timestamp = datetime.utcnow().isoformat()

        log_entry = {
            "case_id": case_id,
            "applicant_id": applicant_id,
            "decision": decision,
            "risk_score": risk_score,
            "confidence": confidence,
            "timestamp": timestamp,
            "status": "logged",
        }

        self.audit_log.append(log_entry)

        return {
            "status": "success",
            "data": {
                "case_id": case_id,
                "log_status": "Decision logged successfully",
                "timestamp": timestamp,
                "log_id": str(len(self.audit_log)),
            },
        }

    def create_case_file(
        self,
        applicant_id: str,
        decision: str,
        application_data: Dict[str, Any],
        analysis_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create complete case file"""
        case_id = f"CASE-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

        case_file = {
            "case_id": case_id,
            "applicant_id": applicant_id,
            "decision": decision,
            "created_at": datetime.utcnow().isoformat(),
            "application_summary": {
                "income": application_data.get("income"),
                "loan_amount": application_data.get("loan_amount"),
                "credit_score": application_data.get("credit_score"),
            },
            "analysis_summary": analysis_data,
            "status": "active",
        }

        self.audit_log.append(case_file)

        return {
            "status": "success",
            "data": {
                "case_id": case_id,
                "applicant_id": applicant_id,
                "decision": decision,
                "case_status": "Active",
                "created_at": case_file["created_at"],
            },
        }

    def get_audit_history(self, applicant_id: str) -> Dict[str, Any]:
        """Retrieve audit history for applicant"""
        history = [
            entry
            for entry in self.audit_log
            if entry.get("applicant_id") == applicant_id
        ]

        return {
            "status": "success",
            "data": {
                "applicant_id": applicant_id,
                "entry_count": len(history),
                "entries": history[-10:],  # Last 10 entries
            },
        }


# Singleton instance
notification_server = NotificationServer()
