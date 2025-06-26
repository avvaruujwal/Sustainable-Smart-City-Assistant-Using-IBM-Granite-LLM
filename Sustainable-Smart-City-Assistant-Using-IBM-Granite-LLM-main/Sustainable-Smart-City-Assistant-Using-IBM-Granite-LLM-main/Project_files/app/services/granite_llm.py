import random
import requests
import json
from app.config import settings

def get_watsonx_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": settings.WATSONX_API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    response = requests.post(url, headers=headers, data=data, timeout=15)
    response.raise_for_status()
    return response.json()["access_token"]

def ask_granite(prompt: str) -> str:
    """
    Sends a prompt to the IBM Watsonx Granite LLM (chat endpoint) and returns the generated response.
    """
    token = get_watsonx_token()
    url = f"{settings.WATSONX_URL}/ml/v1/text/chat"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": settings.WATSONX_MODEL_ID,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "project_id": settings.WATSONX_PROJECT_ID,
        "parameters": {"max_new_tokens": 1024}
    }
    params = {"version": "2023-05-29"}
    print("Payload being sent to Watsonx (chat endpoint):\n", json.dumps(payload, indent=2))
    try:
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=30)
        print("Watsonx response status:", response.status_code)
        if response.status_code != 200:
            print("Watsonx error response:", response.text)
        response.raise_for_status()
        result = response.json()
        print("[DEBUG] Full Watsonx response:", json.dumps(result, indent=2))
        # Extract the generated text from the chat response (new format)
        if (
            "choices" in result and result["choices"] and
            "message" in result["choices"][0] and
            "content" in result["choices"][0]["message"]
        ):
            return result["choices"][0]["message"]["content"]
        else:
            print("[ERROR] 'choices' or 'content' missing in Watsonx response.")
            return f"[ERROR] Unexpected Watsonx response: {json.dumps(result)}"
    except Exception as e:
        print(f"[EXCEPTION] Error contacting Watsonx: {e}")
        try:
            print("[EXCEPTION] Response text:", response.text)
        except Exception:
            pass
        return f"Error contacting Watsonx: {e}"

def ask_city_question(prompt: str) -> str:
    """
    Answers only sustainable city, smart city, and urban living related questions. Greets for greetings, politely declines unrelated prompts.
    """
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    prompt_lower = prompt.strip().lower()
    if any(greet in prompt_lower for greet in greetings) and len(prompt_lower.split()) <= 3:
        return random.choice([
            "Hello! How can I assist you with smart city or sustainability topics today?",
            "Hi there! Ask me anything about sustainable cities or urban living.",
            "Hey! Ready to help with your city or sustainability questions."
        ])
    # Check if the prompt is about city/sustainability topics
    city_keywords = [
        "city", "urban", "municipal", "governance", "transport", "infrastructure", "energy", "waste", "water", "air quality", "public transport", "policy", "sustainability", "eco", "green", "renewable", "smart city", "environment", "climate", "building", "planning", "development"
    ]
    if any(word in prompt_lower for word in city_keywords):
        system_prompt = (
            "You are a helpful AI assistant specialized in sustainable cities, smart city governance, urban planning, "
            "and eco-friendly living. Answer all questions with a focus on sustainability, city management, "
            "environmental impact, and smart urban solutions."
        )
        full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        return ask_granite(full_prompt)
    else:
        return "I'm here to help with questions about sustainable cities, smart city governance, and urban living. Please ask something related to these topics!"

def get_sustainability_tips(category: str) -> str:
    """
    Returns generic sustainability tips for any category.
    """
    prompt = f"Provide 3 practical sustainability tips for the category: {category}."
    return ask_granite(prompt)

def generate_summary(text: str) -> str:
    """
    Returns a generic summary of the provided text.
    """
    prompt = f"Summarize the following policy document in 3-4 sentences:\n\n{text}"
    return ask_granite(prompt)

def generate_eco_tip(topic: str) -> str:
    """
    Returns 1 or 2 concise, actionable eco-friendly tips for sustainable cities or city-related sustainability topics.
    """
    prompt = (
        f"You are an expert in sustainable cities and urban living. "
        f"Give me 1 or 2 concise, actionable tips for making a city more sustainable, specifically about: {topic}. "
        f"The tips should be practical and focused on city or community-level sustainability."
    )
    return ask_granite(prompt)

def generate_city_report(kpi_data: dict) -> str:
    """Generates a detailed, well-structured sustainability report based on city KPI data."""
    city = kpi_data.get('city_name', 'the city')
    year = kpi_data.get('year', 'the specified year')

    # Summarize KPI data if it's too long
    kpi_json = json.dumps(kpi_data, indent=2)
    if len(kpi_json) > 1000:
        kpi_json = '\n'.join([f"- {k}: {v}" for k, v in list(kpi_data.items())[:10]]) + '\n...'

    prompt = f"""
You are an expert sustainability analyst. Generate a comprehensive, professional Sustainability Report for {city} for the year {year}, using the following KPI data:
{kpi_json}

The report must be well-structured, readable, and organized into the following sections (use markdown headings):

1. Air Quality
2. Energy Usage
3. Water Usage
4. Waste Management
5. Public Transport
6. Environmental Protection
7. Summary or Insights

For each section:
- Present the relevant data clearly.
- Where possible, calculate and mention useful insights (e.g., percentages, comparisons, trends, impacts).
- Use bullet points or short paragraphs for clarity.
- For Air Quality, comment on whether AQI is good/poor and its implications.
- For Energy Usage, mention renewable energy share if possible.
- For Public Transport, discuss benefits or trends.
- For Environmental Protection, mention any notable efforts or gaps.

Finish with a Summary or Insights section that highlights key findings, areas of improvement, and actionable recommendations for the city.

Format the report with clear markdown headings and bullet points or paragraphs. Make it professional, concise, and easy to read.
If you cannot generate a report, explain why in a user-friendly way.
"""
    response = ask_granite(prompt)
    if not response or len(response.strip()) < 20 or "sorry" in response.lower() or "couldn't" in response.lower():
        return ("The AI was unable to generate a sustainability report for the provided data. "
                "Please check your KPI data for completeness and clarity, and try again. "
                "If the problem persists, contact support.")
    return response 