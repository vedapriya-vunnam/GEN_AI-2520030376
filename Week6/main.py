
import json
import csv
import requests
from datetime import datetime

# STEP 1: CONFIGURATION

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"
INPUT_FILE = "golden_set.json"
OUTPUT_FILE = "baseline_results.csv"

# STEP 2: LOAD GOLDEN QUESTION SET

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    golden_questions = json.load(file)

print("\n======================================")
print("GOLDEN QUESTION SET")
print("======================================")

print("Total Questions:", len(golden_questions))
print("Model:", MODEL_NAME)

# STEP 3: FUNCTION TO GET LLM ANSWER

def get_llm_answer(question):

    payload = {
        "model": MODEL_NAME,
        "prompt": question,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result.get("response", "").strip()

# STEP 4: KEYWORD-BASED SCORING

def calculate_score(answer, expected_keywords):

    answer = answer.lower()

    matched_keywords = []
    missing_keywords = []

    for keyword in expected_keywords:

        if keyword.lower() in answer:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    total_keywords = len(expected_keywords)

    if total_keywords == 0:
        score = 0
    else:
        score = (
            len(matched_keywords) / total_keywords
        ) * 100

    return (
        round(score, 2),
        matched_keywords,
        missing_keywords
    )

# STEP 5: RUN BASELINE EVALUATION

results = []

total_score = 0
successful_questions = 0

print("\n======================================")
print("BASELINE RUN STARTED")
print("======================================")

for index, item in enumerate(golden_questions, start=1):

    question_id = item["id"]
    question = item["question"]
    expected_answer = item["expected_answer"]
    keywords = item["keywords"]
    source = item["source"]

    print("\n--------------------------------------")
    print(f"Question {index}: {question_id}")
    print("Question:", question)

    try:

        # Get model response
        answer = get_llm_answer(question)

        # Calculate keyword score
        score, matched, missing = calculate_score(
            answer,
            keywords
        )

        status = "PASS" if score >= 60 else "REVIEW"

        total_score += score
        successful_questions += 1

        print("\nLLM Answer:")
        print(answer)

        print("\nExpected Answer:")
        print(expected_answer)

        print("\nMatched Keywords:", matched)
        print("Missing Keywords:", missing)

        print("Score:", score, "%")
        print("Status:", status)

        results.append({
            "Question_ID": question_id,
            "Question": question,
            "Expected_Answer": expected_answer,
            "LLM_Answer": answer,
            "Matched_Keywords": ", ".join(matched),
            "Missing_Keywords": ", ".join(missing),
            "Score": score,
            "Status": status,
            "Source": source,
            "Model": MODEL_NAME,
            "Release": "v0.1"
        })

    except Exception as error:

        print("Error:", error)

        results.append({
            "Question_ID": question_id,
            "Question": question,
            "Expected_Answer": expected_answer,
            "LLM_Answer": "",
            "Matched_Keywords": "",
            "Missing_Keywords": ", ".join(keywords),
            "Score": 0,
            "Status": "ERROR",
            "Source": source,
            "Model": MODEL_NAME,
            "Release": "v0.1"
        })

# STEP 6: SAVE RESULTS TO CSV

fieldnames = [
    "Question_ID",
    "Question",
    "Expected_Answer",
    "LLM_Answer",
    "Matched_Keywords",
    "Missing_Keywords",
    "Score",
    "Status",
    "Source",
    "Model",
    "Release"
]

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(results)

# STEP 7: BASELINE SUMMARY

if successful_questions > 0:
    average_score = total_score / successful_questions
else:
    average_score = 0

passed = sum(
    1 for result in results
    if result["Status"] == "PASS"
)

review = sum(
    1 for result in results
    if result["Status"] == "REVIEW"
)

errors = sum(
    1 for result in results
    if result["Status"] == "ERROR"
)

print("\n======================================")
print("BASELINE EVALUATION SUMMARY")
print("======================================")

print("Release Version: v0.1")
print("Model:", MODEL_NAME)
print("Total Questions:", len(golden_questions))
print("Successful Responses:", successful_questions)
print("Passed Questions:", passed)
print("Questions for Review:", review)
print("Failed Requests:", errors)

print(
    "Average Keyword Coverage:",
    round(average_score, 2), "%"
)

print("Evaluation Date:", datetime.now())

# STEP 8: COMPLETION

print("\nResults saved to:", OUTPUT_FILE)

print("\nBASELINE RUN COMPLETED!")
print("Release v0.1 created successfully.")
