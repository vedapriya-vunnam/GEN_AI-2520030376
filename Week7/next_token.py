
import torch
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM

# Step 1: Load a small pretrained language model
model_name = "distilgpt2"

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

model.eval()

# Step 2: Enter input sentence
text = input("\nEnter a sentence: ")

# Step 3: Convert text into tokens
inputs = tokenizer(text, return_tensors="pt")

print("\nInput Tokens:")
print(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]))

# Step 4: Get model logits
with torch.no_grad():
    outputs = model(**inputs)

logits = outputs.logits[0, -1, :]

# Step 5: Convert logits into probabilities
probabilities = torch.softmax(logits, dim=-1)

# Step 6: Find top-k candidates
k = 10
top_probs, top_ids = torch.topk(probabilities, k)

print("\nTop 10 Next-Token Predictions:")
print("--------------------------------")

tokens = []
probs = []

for i in range(k):
    token_id = top_ids[i].item()
    token = tokenizer.decode([token_id])
    probability = top_probs[i].item()

    tokens.append(repr(token))
    probs.append(probability * 100)

    print(
        f"{i+1}. Token: {repr(token):15} "
        f"Probability: {probability * 100:.4f}% "
        f"Logit: {logits[token_id].item():.4f}"
    )

# Step 7: Display probability graph
plt.figure(figsize=(10, 5))
plt.bar(tokens, probs)

plt.xlabel("Next Token Candidates")
plt.ylabel("Probability (%)")
plt.title("Top 10 Next-Token Probabilities")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
