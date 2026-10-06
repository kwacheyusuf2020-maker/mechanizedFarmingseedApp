import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

def get_ai_explanation(crop_name, farm_size, soil_type):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "API Key missing from .env file."

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            f"Give a short, simple explanation of best practices for growing "
            f"{crop_name} on a {farm_size} hectare farm with {soil_type} soil."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI explanation unavailable right now: {e}"

# Quick test
if __name__ == "__main__":
    result = get_ai_explanation("Maize", 5, "Loamy")
    print(result)