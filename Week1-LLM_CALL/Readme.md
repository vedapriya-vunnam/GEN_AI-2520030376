Week 1: My first LLM call

This week I called an AI model (Gemini) from Python for the first time. I asked it "What is Artificial Intelligence?" and printed the answer in the terminal.

What I learned:
- An LLM is an AI trained on a lot of text, and we use it over the internet through an API
- An API key is a secret password for my requests, so I keep it in a .env file and not in the code
- How to load the key using python-dotenv
- How to create a Gemini client and send it a prompt

How I did it:
In main.py I load the key from .env, create the Gemini client, send the question and print the answer.

Commands:
- pip install -r requirements.txt
- python main.py
