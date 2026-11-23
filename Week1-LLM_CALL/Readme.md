## Week 1 – First LLM Call

**What I did:** Made our very first call to an AI model (Gemini) from Python and printed its answer.

**Topics covered**
- What an API key is and why it goes in `.env`
- Loading secrets with `python-dotenv`
- Creating a Gemini client and sending a prompt

**How we implemented it (`main.py`)**
1. Load the API key from `.env`
2. Create the Gemini client
3. Ask: "What is Artificial Intelligence?"
4. Print the reply

**Commands used**
```bash
pip install -r requirements.txt
python main.py
```
