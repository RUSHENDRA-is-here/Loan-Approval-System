from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from typing import Any, Dict, List, Optional
from src.utils import get_logger
from src.config import settings
import json


class BaseAgent:
    def __init__(self, name: str, role: str, description: str = ""):
        self.name = name
        self.role = role
        self.description = description
        self.client = settings.get_anthropic_client()
        self.model = settings.claude_model
        self.max_tokens = settings.max_tokens
        self.logger = get_logger(f"agent.{name.lower()}")

    def define_tools(self) -> List[Dict[str, Any]]:
        """Define agent-specific tools. Override in subclass."""
        return []

    def _build_system_prompt(self) -> str:
        """Build system prompt for the agent."""
        return f"""You are {self.name}, a specialized loan approval agent.

Role: {self.role}

Description: {self.description}

You are part of a multi-agent system analyzing loan applications. Your job is to:
1. Analyze the provided information carefully
2. Apply business logic and rules
3. Return structured, JSON-formatted responses
4. Provide clear reasoning for your analysis

Always return your response as valid JSON with the following structure:
{{
    "analysis": "Your detailed analysis",
    "findings": {{"key": "value", ...}},
    "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "confidence": 0.0-1.0,
    "reasoning": "Clear explanation of findings"
}}
"""

    async def execute_async(
        self, user_message: str, context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Execute agent asynchronously."""
        tools = self.define_tools()
        messages = [{"role": "user", "content": user_message}]

        try:
            self.logger.info(f"Executing agent with message length: {len(user_message)}")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                tools=tools if tools else None,
                messages=messages,
                system=self._build_system_prompt(),
            )

            self.logger.info(f"Agent execution completed. Stop reason: {response.stop_reason}")

            # Parse response content
            result = {
                "agent": self.name,
                "status": "success",
                "stop_reason": response.stop_reason,
                "content": [],
            }

            for block in response.content:
                if hasattr(block, "type"):
                    if block.type == "text":
                        try:
                            data = json.loads(block.text)
                            result["content"].append(data)
                        except json.JSONDecodeError:
                            result["content"].append({"text": block.text})
                    elif block.type == "tool_use":
                        result["content"].append(
                            {"tool_use": block.name, "input": block.input}
                        )

            return result

        except Exception as e:
            self.logger.error(f"Agent execution failed: {str(e)}")
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e),
                "content": [],
            }

    def execute(self, user_message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute agent synchronously (wrapper around async)."""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.execute_async(user_message, context))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, role={self.role})"
