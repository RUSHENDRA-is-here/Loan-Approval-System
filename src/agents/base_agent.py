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
        self.model = settings.claude_model or "global.anthropic.claude-opus-4-5-20251101-v1:0"
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

CRITICAL INSTRUCTIONS:
1. Analyze the provided information carefully
2. Apply business logic and rules
3. Return ONLY valid JSON with no markdown or extra text
4. Provide specific, clear reasoning
5. Return numbers for numeric fields (not strings)
6. Return arrays for list fields
7. Use this exact JSON format:

{{
    "analysis": "Your detailed analysis",
    "findings": {{"key": "value"}},
    "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "confidence": 0.75,
    "reasoning": "Clear explanation of findings"
}}

REMEMBER: Output ONLY JSON, no markdown code blocks, no extra text."""

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

            # Log raw response for debugging
            self.logger.info(f"Response content blocks: {len(response.content)}")
            for i, block in enumerate(response.content):
                self.logger.info(f"Block {i}: type={getattr(block, 'type', 'unknown')}")
                if hasattr(block, "type"):
                    if block.type == "text":
                        text_content = block.text
                        self.logger.info(f"Text content: {text_content[:200]}")
                        try:
                            data = json.loads(text_content)
                            result["content"].append(data)
                        except json.JSONDecodeError:
                            result["content"].append({"text": text_content})
                    elif block.type == "tool_use":
                        self.logger.info(f"Tool use: {block.name}")
                        result["content"].append(
                            {"tool_use": block.name, "input": block.input}
                        )

            self.logger.info(f"Final result content: {result['content']}")
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
