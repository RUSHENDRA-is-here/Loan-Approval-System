import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
endpoint = os.getenv("ANTHROPIC_API_ENDPOINT")

client = Anthropic(api_key=api_key, base_url=endpoint)
MODEL = "claude-sonnet-4-6"

print(f"Loan Approval System initialized")
print(f"API Endpoint: {endpoint}")
print(f"Model: {MODEL}")
print(f"API Key configured: {'Yes' if api_key else 'No'}")

def get_loan_decision(application_data: str) -> str:
    """Get loan approval decision from Claude Sonnet."""
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Analyze this loan application and provide a decision:\n\n{application_data}"
            }
        ]
    )
    return message.content[0].text

if __name__ == "__main__":
    print("\nSystem ready for loan applications.")
