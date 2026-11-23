Week 3: Tracking tokens, cost and speed

This week I added tracking to every AI call, so I can see the tokens used, the time taken and the rough cost. Everything is saved in MongoDB. This matters because AI calls cost money and we need to know where it goes.

What I learned:
- Tokens are small pieces of text. Cost depends on input tokens (my question) and output tokens (the answer)
- Latency is the time one call takes
- How to retry when there is a temporary error, waiting 1 second and then 2 seconds, up to 3 attempts
- How to save records in a MongoDB database

How I did it:
llm_client.py times each call, counts tokens, works out the cost and retries on errors. usage_logger.py saves each call to MongoDB. I added MONGODB_URI to my .env file for the connection.

Commands:
- pip install -r requirements.txt
- python main.py
- python -m unittest
