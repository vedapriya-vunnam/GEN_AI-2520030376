Week 6: Golden question set and baseline evaluation

This week I tested a local model (llama3.2 on Ollama) using a golden set, which is a fixed list of questions with known answers. Running the same questions every time lets us compare the model later when something changes. This first run is our baseline, saved as release v0.1.

What I learned:
- A golden set has 30 questions on tokens, tokenization, cost, text generation and positional encoding, each with an expected answer and keywords
- A baseline is the first score we record, so later versions can be compared with it
- The score is the matched keywords divided by the total keywords, multiplied by 100. A score of 60 or more is PASS, otherwise REVIEW
- Temperature 0 makes the model give the same answer each time, so the test is fair
- Keyword scoring is simple, but a correct answer in different words can still score low

How I did it:
main.py reads golden_set.json, sends each question to Ollama, scores the answer by checking which keywords appear in it, and saves everything to baseline_results.csv. At the end it prints a summary.

Result:
- 30 questions: 11 passed, 19 for review, 0 errors
- Average keyword coverage: 51.11 percent

Commands:
- pip install -r requirements.txt
- ollama pull llama3.2
- python main.py
