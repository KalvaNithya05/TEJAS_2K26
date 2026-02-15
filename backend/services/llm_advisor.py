import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMAdvisor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            print("Warning: GEMINI_API_KEY not found. LLM features will be disabled.")
            self.model = None

    def generate_explanation(self, recovery_data):
        """
        Generates a human-readable explanation of the recovery plan using Google Gemini.
        """
        if not self.model:
            return "AI explanation unavailable (API Key missing)."

        prompt = f"""
        You are an expert agricultural advisor for Indian farmers. 
        Analyze the following recovery plan and provide a simple, encouraging explanation in English.
        
        Recovery Plan Data:
        - Decision: {recovery_data.get('decision')}
        - Reason: {recovery_data.get('reason')}
        - Eco Advice: {recovery_data.get('eco_advisory')}
        - Schemes: {recovery_data.get('schemes')}
        
        Structure your response:
        1. **Situation Analysis**: What happened and why.
        2. **Action Plan**: Clear steps on what to do next.
        3. **Eco-Friendly Tip**: Highlight one key eco-friendly practice.
        4. **Government Support**: Mention relevant schemes.
        
        Keep it under 200 words. Use simple language.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"LLM Error: {e}")
            print("Falling back to Mock Explanation due to API error.")
            return self._generate_mock_explanation(recovery_data)

    def _generate_mock_explanation(self, recovery_data):
        """
        Generates a static but realistic explanation when API is unavailable.
        """
        decision = recovery_data.get('decision', 'Review Required')
        eco_tip = recovery_data.get('eco_advisory', [{'solution': 'Use organic compost'}])[0]['solution']
        
        return f"""
        **Situation Analysis**: The system has detected conditions requiring attention based on your inputs. The decision is to {decision}.
        
        **Action Plan**: 
        1. Follow the recommended recovery steps immediately.
        2. Monitor soil moisture and nutrient levels daily.
        3. Consult with local agricultural extension officers if symptoms persist.
        
        **Eco-Friendly Tip**: {eco_tip}. This will help improve long-term soil health.
        
        **Government Support**: Check eligibility for the schemes listed below, such as PMFBY, which can provide financial safety nets.
        
        *(Note: This is a robust system-generated explanation because the AI service is currently unreachable)*
        """
