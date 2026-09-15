import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_llm():
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing from environment variables.")
    
    # CHANGE THIS from "gemini-3.6-flash" to "gemini-1.5-flash"
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.2, 
        max_output_tokens=4096,
        api_key=GOOGLE_API_KEY
    )