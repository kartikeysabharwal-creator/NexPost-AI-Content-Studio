from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# High-speed models actively supported by Groq Cloud
DEFAULT_MODEL = "openai/gpt-oss-120b"
AVAILABLE_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "allam-2-7b"
]

def get_llm(model_name=None, temperature=0.7):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is missing. Please set it in .env file or input via sidebar.")
    
    selected_model = model_name or os.getenv("GROQ_MODEL", DEFAULT_MODEL)
    return ChatGroq(
        groq_api_key=api_key,
        model_name=selected_model,
        temperature=temperature
    )

llm = get_llm()

if __name__ == "__main__":
    response = llm.invoke("Introduce yourself in one sentence.")
    print("Response:", response.content)
