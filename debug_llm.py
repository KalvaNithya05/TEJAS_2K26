from services.llm_advisor import LLMAdvisor
import os
from dotenv import load_dotenv

# Force load .env
load_dotenv('backend/.env')

advisor = LLMAdvisor()
print(f"API Key loaded: {advisor.api_key[:10]}...{advisor.api_key[-5:] if advisor.api_key else 'None'}")

test_data = {
    "decision": "PLANT_CROP",
    "reason": "Good conditions",
    "eco_advisory": ["Use compost"],
    "schemes": []
}

print("Attempting to generate explanation...")
try:
    explanation = advisor.generate_explanation(test_data)
    print(f"Result: {explanation}")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
