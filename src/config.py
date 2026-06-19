from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False

    # Anthropic/Claude Settings
    anthropic_api_key: Optional[str] = None
    anthropic_api_endpoint: Optional[str] = None
    claude_model: str = "claude-sonnet-4-6"
    max_tokens: int = 2048

    # MCP Server Settings
    mcp_applicant_db_port: int = 8001
    mcp_risk_rules_port: int = 8002
    mcp_decision_synthesis_port: int = 8003
    mcp_notification_port: int = 8004

    # Orchestration Settings
    orchestration_timeout_seconds: int = 30
    enable_parallel_execution: bool = True

    # Streamlit Settings
    streamlit_page_title: str = "Loan Approval System"
    streamlit_page_layout: str = "wide"

    # Logging Settings
    log_level: str = "INFO"
    log_format: str = "json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def get_anthropic_client(self):
        from anthropic import Anthropic

        kwargs = {"api_key": self.anthropic_api_key}
        # Use default Anthropic API endpoint (don't override)
        # if self.anthropic_api_endpoint:
        #     kwargs["base_url"] = self.anthropic_api_endpoint

        return Anthropic(**kwargs)


# Singleton settings instance
settings = Settings()
