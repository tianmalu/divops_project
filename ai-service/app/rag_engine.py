from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import random

load_dotenv()

def generate_tarot_response(question: str) -> str:
    template = open("app/tarot_prompt_template.txt", "r").read()
    prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")

    #return llm.predict(prompt.format(question=question))
    return "The cards foresee a twist of fate in your journey..."  # fake output for testing

def generate_tarot_response_test(question: str) -> str:
    sample_responses = [
        "The stars favor your path.",
        "A new journey begins at dawn.",
        "The river of fate flows with you.",
        "Fortune smiles upon your quest.",
    ]
    return random.choice(sample_responses)