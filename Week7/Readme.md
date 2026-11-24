Week 7: Next-token prediction

This week I looked at how a language model decides the next word. I used a small pretrained model called distilgpt2. I type a sentence, and the program shows the 10 most likely next tokens with their probabilities and draws a bar graph of them. This is the basic idea behind all text generation.

What I learned:
- Next-token prediction means the model looks at the text so far and guesses which token comes next
- Logits are the raw scores the model gives to every token in its vocabulary
- Softmax turns those logits into probabilities that add up to 1
- Top-k means picking only the k tokens with the highest probabilities, and I used k = 10
- The model does not know one correct answer. It gives a probability to many possible tokens

How I did it:
next_token.py loads distilgpt2 using the transformers library and takes my sentence as input. It converts the sentence into tokens, runs the model and takes the logits of the last position. Then it applies softmax, picks the top 10 tokens using torch.topk, prints them with their probability and logit, and shows a bar graph using matplotlib.

Commands:
- pip install -r requirements_1.txt
- python next_token.py

The first run needs internet to download the model.
