import google.generativeai as genai

def get_ai_explanation(crop_name, farm_size, soil_type):
    try:
        genai.configure(api_key="YOUR_API_KEY_HERE")
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Give a short, simple explanation of best practices for growing "
            f"{crop_name} on a {farm_size} hectare farm with {soil_type} soil."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "AI explanation unavailable right now. Please try again later."


# Quick test
if __name__ == "__main__":
    result = get_ai_explanation("Maize", 5, "Loamy")
    print(result)