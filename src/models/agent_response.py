from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from enum import Enum


class DecisionClassification(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class AgentResponse(BaseModel):
    agent_name: str = Field(..., description="Name of the agent")
    status: str = Field(..., description="Status of agent execution")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Agent output data")
    error: Optional[str] = Field(default=None, description="Error message if any")
    timestamp: Optional[str] = Field(default=None, description="Execution timestamp")


class DecisionResponse(BaseModel):
    application_id: str
    classification: DecisionClassification = Field(..., description="Loan approval decision")
    confidence: float = Field(ge=0, le=1, description="Confidence score (0-1)")
    risk_score: float = Field(ge=0, le=100, description="Overall risk score (0-100)")
    factors: List[str] = Field(default=[], description="Key factors in decision")
    reasoning: str = Field(..., description="Explanation of decision")
    profile_analysis: Optional[Dict[str, Any]] = Field(default=None)
    risk_analysis: Optional[Dict[str, Any]] = Field(default=None)
    compliance_notes: Optional[str] = Field(default=None)
    case_id: Optional[str] = Field(default=None, description="Case ID for audit trail")

    class Config:
        json_schema_extra = {
            "example": {
                "application_id": "APP123",
                "classification": "APPROVED",
                "confidence": 0.85,
                "risk_score": 25,
                "factors": ["Good credit score", "Low DTI ratio", "Stable employment"],
                "reasoning": "Applicant meets all approval criteria with strong financial profile",
                "case_id": "CASE-2024-001",
            }
        }
