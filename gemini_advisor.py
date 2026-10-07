import os
from dotenv import load_dotenv
from google import genai


def get_ai_explanation(crop_name, farm_size, soil_type):
    load_dotenv()

    if not os.getenv("GEMINI_API_KEY"):
        return "API key not found. Add GEMINI_API_KEY to your private .env file."

    try:
        client = genai.Client()
        prompt = (
            f"Give a short, simple explanation of best practices for growing "
            f"{crop_name} on a {farm_size}-hectare farm with {soil_type} soil."
        )
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt,
        )
        return response.output_text
    except Exception as error:
        return f"AI explanation unavailable: {type(error).__name__}: {error}"


if __name__ == "__main__":
    print(get_ai_explanation("Maize", 5, "Loamy"))