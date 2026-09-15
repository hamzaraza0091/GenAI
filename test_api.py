import os
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print(f"Testing API Key starting with: {api_key[:5]}...")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get("models", [])
    valid_models = [m['name'].replace('models/', '') for m in models if "generateContent" in m.get("supportedGenerationMethods", [])]
    
    print("\n✅ API KEY IS VALID! You have access to these exact model names:\n")
    for vm in valid_models:
        print(f" 👉 {vm}")
        
    if valid_models:
        test_model = valid_models[0] # Pick the first available model
        print(f"\n--- Testing LangChain with {test_model} ---")
        try:
            llm = ChatGoogleGenerativeAI(model=test_model, api_key=api_key)
            result = llm.invoke("Respond with exactly one word: SUCCESS")
            print(f"Bot replied: {result.content}")
        except Exception as e:
            print(f"LangChain Error: {e}")
else:
    print(f"\n❌ API KEY ERROR: {response.status_code}")
    print(response.text)