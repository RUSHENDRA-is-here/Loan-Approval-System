"""
LangChain-based orchestrator for multi-agent loan approval workflow
"""

import json
import asyncio
from typing import Dict, Any, Optional
from src.agents import (
    ApplicantProfileAgent,
    FinancialRiskAgent,
    DecisionAgent,
    ComplianceAgent,
)
from src.models import LoanApplication, DecisionResponse, DecisionClassification
from src.mcp_servers import (
    applicant_db_server,
    risk_rules_server,
    decision_synthesis_server,
    notification_server,
)
from src.utils import get_logger


class LoanOrchestrator:
    def __init__(self):
        self.logger = get_logger("orchestrator")
        self.profile_agent = ApplicantProfileAgent()
        self.risk_agent = FinancialRiskAgent()
        self.decision_agent = DecisionAgent()
        self.compliance_agent = ComplianceAgent()

    async def process_application_async(
        self, application: LoanApplication
    ) -> DecisionResponse:
        """Process loan application asynchronously through all agents"""
        self.logger.info(f"Starting orchestration for {application.applicant_id}")

        try:
            # Step 1: Validate application data
            self.logger.info("Step 1: Validating application data")
            validation_result = applicant_db_server.validate_applicant_data(
                application.to_dict()
            )
            if not validation_result["data"]["is_complete"]:
                raise ValueError(
                    f"Incomplete application: {validation_result['data']['missing_fields']}"
                )

            app_dict = application.to_dict()

            # Step 2: Parallel execution of Profile and Risk agents
            self.logger.info("Step 2: Running Profile and Risk agents in parallel")
            profile_task = asyncio.create_task(
                self.profile_agent.execute_async(
                    f"Analyze profile for {application.applicant_id}", app_dict
                )
            )
            risk_task = asyncio.create_task(
                self.risk_agent.execute_async(
                    f"Analyze financial risk for {application.applicant_id}", app_dict
                )
            )

            profile_result = await profile_task
            risk_result = await risk_task

            self.logger.info(
                f"Profile agent status: {profile_result['status']}, Risk agent status: {risk_result['status']}"
            )

            # Extract and parse results
            profile_analysis = self._extract_analysis(profile_result)
            risk_analysis = self._extract_analysis(risk_result)

            # Step 3: Apply MCP server rules
            self.logger.info("Step 3: Applying MCP business rules")
            rules_result = risk_rules_server.apply_business_rules(app_dict)
            if not rules_result["data"]["rules_passed"]:
                self.logger.warning(f"Business rule violations: {rules_result['data']['violations']}")

            # Step 4: Decision synthesis
            self.logger.info("Step 4: Making decision")
            decision_result = await self.decision_agent.execute_async(
                f"Decide on loan for {application.applicant_id}",
                {**app_dict, "profile": profile_analysis, "risk": risk_analysis},
            )

            decision_analysis = self._extract_analysis(decision_result)

            # Extract decision classification
            classification = self._extract_classification(decision_analysis)
            confidence = decision_analysis.get("confidence", 0.5)
            risk_score = decision_analysis.get("risk_score", 50)
            factors = decision_analysis.get("factors", [])
            reasoning = decision_analysis.get("reasoning", "Decision made based on analysis")

            # Step 5: Compliance and audit
            self.logger.info("Step 5: Logging and compliance")
            compliance_result = await self.compliance_agent.execute_async(
                f"Process compliance for {application.applicant_id}",
                {**app_dict, "decision": classification},
            )

            compliance_analysis = self._extract_analysis(compliance_result)
            case_id = compliance_analysis.get("case_id", "CASE-UNKNOWN")

            # Step 6: Create audit entry
            notification_server.create_audit_entry(
                application.applicant_id,
                str(classification),
                reasoning,
            )

            self.logger.info(f"Orchestration completed for {application.applicant_id}: {classification}")

            # Build response
            response = DecisionResponse(
                application_id=application.applicant_id,
                classification=classification,
                confidence=confidence,
                risk_score=int(risk_score),
                factors=factors,
                reasoning=reasoning,
                profile_analysis=profile_analysis,
                risk_analysis=risk_analysis,
                compliance_notes=compliance_analysis.get("summary", ""),
                case_id=case_id,
            )

            return response

        except Exception as e:
            self.logger.error(f"Orchestration failed: {str(e)}")
            raise

    def process_application(self, application: LoanApplication) -> DecisionResponse:
        """Process loan application (synchronous wrapper)"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.process_application_async(application))

    def _extract_analysis(self, agent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract analysis from agent result"""
        if agent_result.get("status") == "error":
            return {
                "error": agent_result.get("error"),
                "analysis": "Agent execution failed",
                "confidence": 0.0,
                "risk_score": 50,
                "factors": [],
                "reasoning": "Agent execution failed",
            }

        # Try to extract JSON from content
        for content in agent_result.get("content", []):
            if isinstance(content, dict):
                # Already parsed JSON
                if "analysis" in content or "classification" in content:
                    return content
            elif isinstance(content, str):
                # Try to parse string as JSON
                try:
                    parsed = json.loads(content)
                    if isinstance(parsed, dict):
                        return parsed
                except json.JSONDecodeError:
                    continue

        # If no JSON found, try to parse raw text
        raw_text = ""
        for content in agent_result.get("content", []):
            if isinstance(content, dict) and "text" in content:
                raw_text = content["text"]
            elif isinstance(content, str):
                raw_text = content

        # Try to extract JSON from raw text
        if raw_text:
            try:
                # Look for JSON in the text
                start_idx = raw_text.find("{")
                end_idx = raw_text.rfind("}") + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = raw_text[start_idx:end_idx]
                    parsed = json.loads(json_str)
                    if isinstance(parsed, dict):
                        return parsed
            except (json.JSONDecodeError, ValueError):
                pass

        return {
            "analysis": "No structured analysis returned",
            "raw_content": agent_result.get("content", []),
            "confidence": 0.5,
            "risk_score": 50,
            "factors": [],
            "reasoning": "Unable to parse structured response",
        }

    def _extract_classification(self, analysis: Dict[str, Any]) -> DecisionClassification:
        """Extract decision classification from analysis"""
        classification_str = analysis.get("classification", "").upper()

        if "APPROV" in classification_str:
            return DecisionClassification.APPROVED
        elif "REJECT" in classification_str:
            return DecisionClassification.REJECTED
        elif "REVIEW" in classification_str or "MANUAL" in classification_str:
            return DecisionClassification.MANUAL_REVIEW
        else:
            # Default based on risk score
            risk_score = analysis.get("risk_score", 50)
            if risk_score < 40:
                return DecisionClassification.APPROVED
            elif risk_score > 70:
                return DecisionClassification.REJECTED
            else:
                return DecisionClassification.MANUAL_REVIEW
