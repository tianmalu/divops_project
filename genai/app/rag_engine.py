from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import json
import random
from google import genai
from google.genai import types



load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def check_environment_variables():
    if not API_KEY :
        raise RuntimeError("Missing GEMINI_API_KEY in environment")

def call_gemini_api(prompt: str) -> str:
    """
    Call the Gemini API with the provided prompt and return the response.
    """
    check_environment_variables()
    # Load the configuration from the JSON file
    with open(os.path.join(os.path.dirname(__file__), "gemini_config.json"), "r", encoding="utf-8") as f:
        cfg = json.load(f)

    gen_cfg = types.GenerationConfig(**cfg["generation_config"])
    safe_cfg = [types.SafetySetting(**s) for s in cfg["safety_settings"]]

    gen_cfg = types.GenerateContentConfig(
        **cfg["generation_config"],
        safety_settings=safe_cfg,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )

    client = genai.Client(api_key = API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-04-17",
        contents=prompt,
        config=gen_cfg
    )
    # print("Response:", response.text)
    return response.text

def generate_tarot_response(question: str) -> str:
    template = open("app/tarot_prompt_template.txt", "r").read()
    prompt = PromptTemplate.from_template(template)
    return "The cards foresee a twist of fate in your journey..."  

def generate_tarot_response_test(question: str) -> str:
    sample_responses = [
        "The stars favor your path.",
        "A new journey begins at dawn.",
        "The river of fate flows with you.",
        "Fortune smiles upon your quest.",
    ]
    return random.choice(sample_responses)

def call_rag_with_spread(question: str, spread_size: int = 3) -> str:
    return "The cards foresee a twist of fate in your journey..."  

def store_feedback(user_id: str, question: str, feedback: str) -> None:
    # Placeholder for storing feedback
    pass



if __name__ == "__main__":
    result = call_gemini_api("Tell me a mystical tarot narrative for The Fool.")