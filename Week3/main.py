import os
from dotenv import load_dotenv
 
from llm_client import GeminiProvider, OllamaProvider, LLMClient
from usage_logger import UsageLogger
 
 
load_dotenv(override=True)
 
usage_logger = UsageLogger()
 
try:
    provider_name = input(
        "Choose provider (gemini/ollama): "
    ).strip().lower()
 
    if provider_name == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key not found in .env")
        provider = GeminiProvider(api_key)
 
    elif provider_name == "ollama":
        provider = OllamaProvider("llama3.2")
 
    else:
        raise ValueError("Invalid provider selected")
 
    client = LLMClient(provider, usage_logger)
 
    prompt = input("Enter your question: ")
    answer = client.generate(prompt)
 
    print("\\nLLM Response:")
    print(answer)
 
finally:
    usage_logger.close()
