Week 2: Using Gemini and Ollama together

This week I made the code work with both Gemini and Ollama, and I choose one when I run the program. Gemini is a cloud model that runs on Google's servers. Ollama is a local model that runs on my own laptop, so it is free and works offline.

What I learned:
- The difference between a cloud model and a local model
- Abstraction: one common class (LLMProvider) that both models follow, so the main code does not care which model is used
- How to test my code with a fake provider, so the test does not need a real API

How I did it:
llm_client.py has GeminiProvider, OllamaProvider and LLMClient. main.py asks for the provider and the question, then prints the answer. test_client.py checks the client using a fake provider.

Commands:
- pip install -r requirements.txt
- ollama pull llama3.2
- python main.py
- python -m unittest
