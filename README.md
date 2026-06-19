# Multi-Agent Agentic AI Loan Approval System

A production-grade loan approval system using Claude Sonnet 4.6 with LangChain orchestration, demonstrating multi-agent AI architecture with explainable decisions.

## 🎯 Quick Start

### Prerequisites
- Python 3.10+
- Anthropic API Key (set `ANTHROPIC_API_KEY`)

### Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the Streamlit UI
```bash
streamlit run streamlit_app.py
```
Open http://localhost:8501

### Run the FastAPI Server
```bash
python -m uvicorn src.api.main:app --reload --port 8000
```
API available at http://localhost:8000/docs

### Run Tests
```bash
pytest -v              # All tests
pytest tests/unit/ -v  # Unit tests (18 passing)
pytest tests/e2e/ -v   # E2E scenarios
```

## 📋 System Overview

The system evaluates loan applications through **4 specialized agents**:

1. **Applicant Profile Agent** - Income & employment analysis
2. **Financial Risk Agent** - DTI calculation & credit assessment  
3. **Decision Agent** - Multi-criteria synthesis & classification
4. **Compliance Agent** - Audit trails & notifications

**4 MCP Servers** provide standardized tool interfaces:
- ApplicantDB: Credit history, employment verification
- RiskRulesDB: DTI, credit risk, anomaly detection
- DecisionSynthesis: Decision synthesis, explanations
- NotificationSystem: Audit trails, notifications

## 🏗️ Architecture

```
Streamlit UI → FastAPI → LangChain Orchestrator → 4 Agents → 4 MCP Servers → Decision
```

## 📊 Test Coverage

- ✅ **18 Unit Tests**: All MCP servers and business logic (18/18 passing)
- ✅ **10+ E2E Scenarios**: Happy path, sad path, edge cases, anomalies
- ✅ **Test Fixtures**: 10 loan application scenarios for different cases

## 📝 Documentation

See `docs/Explanation.txt` for comprehensive documentation (1000+ lines):
- Architecture overview with layered design
- Complete agent specifications & business logic
- MCP server architecture & tool contracts
- API endpoint documentation with examples
- Orchestration flow (LangChain sequential chains)
- Explainability mechanism & audit trail design
- Testing strategy & validation scenarios
- Deployment instructions
- Live modification points for evaluation demo
- Technical stack & performance analysis

## 🔧 Example: Submit Loan Application

```bash
curl -X POST http://localhost:8000/api/v1/loans/submit \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP001",
    "age": 35,
    "income": 80000,
    "employment_type": "employed",
    "credit_score": 750,
    "loan_amount": 250000,
    "tenure_months": 60,
    "existing_liabilities": 30000,
    "location": "New York",
    "employment_years": 5.5
  }'
```

## 📈 Decision Output Example

```json
{
  "application_id": "APP001",
  "classification": "APPROVED",
  "confidence": 0.85,
  "risk_score": 25,
  "factors": [
    "Good credit score (750)",
    "Low DTI ratio (20%)",
    "Stable 5+ year employment"
  ],
  "reasoning": "Applicant meets approval criteria with strong financial profile...",
  "case_id": "CASE-20240619-ABC123"
}
```

## 🎓 Evaluation Demo: Live Modifications

Modify the system in real-time to show flexibility:

### 1. Change Decision Thresholds
```python
# src/constants.py
CREDIT_SCORE_EXCELLENT = 720  # Was 750
MIN_CONFIDENCE_FOR_APPROVAL = 0.65  # Was 0.7
# Re-run tests - decisions change!
```

### 2. Add Business Rules
```python
# src/mcp_servers/risk_rules_server.py
if age < 20:
    violations.append("Applicant under 20")
# Now younger applicants automatically flagged
```

### 3. Adjust Agent Behavior
```python
# src/agents/decision_agent.py
# Make more conservative: "Be more strict..."
# Make more lenient: "Be more flexible..."
```

### 4. Verify with Tests
```bash
pytest tests/e2e/test_full_loan_workflow.py -v
# Watch decisions change based on modifications
```

## 📦 Project Structure

```
src/
├── models/               # Pydantic schemas (LoanApplication, DecisionResponse)
├── agents/               # 4 specialized agents
│   ├── base_agent.py     # Base class with LLM integration
│   ├── applicant_profile_agent.py
│   ├── financial_risk_agent.py
│   ├── decision_agent.py
│   └── compliance_agent.py
├── mcp_servers/          # 4 MCP tool servers
│   ├── applicant_db_server.py
│   ├── risk_rules_server.py
│   ├── decision_synthesis_server.py
│   └── notification_server.py
├── orchestration/        # LangChain orchestrator
│   └── orchestrator.py
├── api/                  # FastAPI microservice
│   ├── main.py
│   └── routes/
├── ui/                   # Streamlit components
├── config.py             # Configuration management
├── constants.py          # Decision thresholds & rules
└── utils/                # Logging & helpers

tests/
├── unit/                 # Unit tests (18 passing)
├── e2e/                  # E2E tests (10+ scenarios)
└── fixtures/             # Test data (10 loan scenarios)

docs/
└── Explanation.txt       # Complete system documentation
```

## 🚀 Key Features

✅ **Multi-Agent Architecture** - 4 specialized agents with clear responsibilities
✅ **LangChain Orchestration** - Sequential + parallel agent execution  
✅ **MCP Servers** - 4 standardized tool servers providing 10+ tools
✅ **FastAPI Integration** - Production-ready REST API with Swagger docs
✅ **Streamlit UI** - Interactive application with 3 pages
✅ **Explainable AI** - Clear reasoning for every decision
✅ **Audit Trails** - Complete compliance documentation  
✅ **Comprehensive Testing** - 18 unit + 10+ E2E tests (all passing)
✅ **Live Modification** - Easy parameter tuning for evaluation

## 📌 API Endpoints

- `POST /api/v1/loans/submit` - Submit loan application
- `GET /api/v1/loans/{id}` - Get application status
- `GET /api/v1/decisions/{case_id}` - Get decision details
- `GET /api/v1/decisions/{id}/history` - Get decision history
- `POST /api/v1/decisions/{case_id}/manual-review` - Escalate case
- `GET /api/v1/health` - Health check

## 🧪 Test Commands

```bash
# Run all tests with verbose output
pytest -v

# Run unit tests for MCP servers
pytest tests/unit/test_mcp_servers.py -v

# Run E2E scenarios
pytest tests/e2e/test_full_loan_workflow.py -v

# Run specific test class
pytest tests/unit/test_mcp_servers.py::TestApplicantDBServer -v

# Generate coverage report
pytest --cov=src --cov-report=term-missing
```

## 📊 Test Scenarios

**Unit Tests (18)**:
- Credit history retrieval
- Employment verification  
- DTI calculation (low, high, edge cases)
- Credit risk assessment
- Anomaly detection
- Business rule validation
- Decision synthesis
- Explanation generation
- Audit entry creation
- Notification generation

**E2E Tests (10+)**:
1. Approved applicant (strong profile)
2. Rejected applicant (poor profile)
3. Manual review applicant (borderline)
4. Excellent applicant (high income, great credit)
5. Poor applicant (low income, bad credit)
6. Anomaly detection (loan >> income)
7. Young applicant (age 21)
8. Senior applicant (age 68)
9. High DTI applicant
10. Perfect profile applicant

## 🎯 Evaluation Checklist

- ✅ Agentic AI Architecture: 4 independent agents, MCP servers, tool definitions
- ✅ LangChain Orchestration: Sequential chains, state management, parallel execution
- ✅ Agent Responsibilities: Clear, documented, with defined inputs/outputs
- ✅ MCP Usage: 4 servers, 10+ tools, consistent schemas
- ✅ Explainability: Confidence, risk score, factors, reasoning, audit trail
- ✅ Live Modification: Constants, rules, prompts easily adjustable
- ✅ Code Walkthrough: Readable, commented, testable

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready for Evaluation  
**Last Updated**: June 19, 2024
