import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv('backend/.env')
api_key = os.getenv('GEMINI_API_KEY')
print(f"Testing key: {api_key[:8]}...")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

try:
    response = model.generate_content("What is the best way to recover from a pest attack in rice fields?")
    print("SUCCESS: Connection to Gemini established!")
    print("Response snippet:", response.text[:100], "...")
except Exception as e:
    print(f"FAILURE: Gemini API error - {e}")
    import traceback
    traceback.print_exc()
