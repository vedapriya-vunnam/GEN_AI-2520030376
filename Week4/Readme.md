Week 4: Tokenizers

This week I checked how AI models split text into tokens. A model only understands numbers, so a tokenizer cuts the text into pieces and gives each piece a number. I tried 3 tokenizers on the same sentence in English, Telugu and Hindi.

What I learned:
- BPE (GPT-2) joins the most common pairs of characters
- WordPiece (BERT) splits a word into smaller known parts
- SentencePiece (XLM-R) works on raw text, so it suits many languages
- Telugu and Hindi give more tokens than English for the same meaning, so they cost more

How I did it:
tokenizer.py loads the 3 tokenizers from Hugging Face, runs them on each sentence and prints the tokens, token IDs and token count.

Commands:
- pip install -r requirements.txt
- python tokenizer.py

The first run needs internet to download the tokenizers.
