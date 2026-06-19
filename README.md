# Loan Approval System

A loan approval system built with Claude AI API integration.

## Setup Instructions

### Prerequisites
- Python 3.12+
- uv package manager

### Installation

1. Create virtual environment:
```bash
uv venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env` file with your API keys (already created)
- Make sure `.env` is in `.gitignore` to keep secrets safe

### Environment Variables
- `ANTHROPIC_API_KEY`: Your Claude API key
- `ANTHROPIC_API_ENDPOINT`: API endpoint URL

## Development

Run the application:
```bash
python main.py
```
