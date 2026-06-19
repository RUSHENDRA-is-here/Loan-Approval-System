import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
endpoint = os.getenv("ANTHROPIC_API_ENDPOINT")

print(f"Loan Approval System initialized")
print(f"API Endpoint: {endpoint}")
print(f"API Key configured: {'Yes' if api_key else 'No'}")
