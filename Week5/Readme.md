Week 5: Planning the cost of an AI feature

This week I made a calculator that estimates the cost of an AI feature before building it, and checks if it stays within the limits. A feature that works for 10 users can get expensive or blocked when 10,000 users use it.

What I learned:
- Cost is the tokens per day multiplied by the price per million tokens, then multiplied by 30 for the month
- RPM is requests per minute and TPM is tokens per minute, which are the provider's limits
- A safety margin (I used 20 percent) covers extra usage at peak time

How I did it:
All the numbers are in my .env file. budget.py reads them, calculates the cost and peak load, checks RPM, TPM and the budgets, and prints PASS or REVIEW for each. test_budget.py has 4 tests.

Commands:
- pip install -r requirements.txt
- python budget.py
- python -m unittest
