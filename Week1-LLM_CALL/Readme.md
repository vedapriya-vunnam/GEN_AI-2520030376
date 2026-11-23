# Week 1: My first LLM call

This week I called an AI model (Gemini) from Python for the first time. I asked it "What is Artificial Intelligence?" and printed the answer in the terminal.

## What I learned
- What an API key is, and why I keep it in a .env file instead of in the code
- How to load the key using python-dotenv
- How to create a Gemini client and send it a prompt

## How I did it
In main.py I load the key from .env, make the client, send the question, and print what comes back.

## Commands
- pip install -r requirements.txt
- python main.py
