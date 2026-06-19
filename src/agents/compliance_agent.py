from .base_agent import BaseAgent
from typing import Dict, Any
import uuid
from datetime import datetime


class ComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ComplianceAgent",
            role="Log decisions, create audit trails, and send notifications",
            description="Ensures all decisions are properly documented for compliance and regulatory requirements",
        )

    def define_tools(self):
        return [
            {
                "name": "log_decision",
                "description": "Log decision to audit trail",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "decision": {"type": "string"},
                        "applicant_id": {"type": "string"},
                    },
                    "required": ["decision", "applicant_id"],
                },
            },
            {
                "name": "generate_notification",
                "description": "Generate notification message",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "decision": {"type": "string"},
                        "applicant_id": {"type": "string"},
                        "reasoning": {"type": "string"},
                    },
                    "required": ["decision", "applicant_id"],
                },
            },
        ]

    def process(
        self, application_data: Dict[str, Any], decision_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process compliance and audit requirements."""
        case_id = str(uuid.uuid4())[:12].upper()
        timestamp = datetime.utcnow().isoformat()

        message = f"""Process compliance and notification for loan decision:

CASE ID: {case_id}
TIMESTAMP: {timestamp}
APPLICANT ID: {application_data.get('applicant_id')}

DECISION:
{str(decision_data)}

Perform:
1. Create audit trail entry
2. Log decision with timestamp and case ID
3. Generate notification (approved/rejected/review)
4. Note any compliance considerations
5. Summary of actions taken

Return as JSON with: case_id, timestamp, action_taken, notification_sent, audit_entry, compliance_notes, summary
"""

        context = {**application_data, "decision_data": decision_data, "case_id": case_id}

        return self.execute(message, context=context)
