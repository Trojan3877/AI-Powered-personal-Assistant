"""
main.py — Core Assistant Logic
------------------------------
Handles:
- User input parsing
- Context memory
- OpenAI API calls (LLM)
- Command delegation to modules (scheduler, Q&A, etc.)
"""

import openai
import os
from modules.scheduler import handle_schedule
from modules.qa import answer_query

# Load API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simulated memory for context
context_memory = []

def process_user_input(user_input):
    """
    Routes user input to the appropriate module
    based on keywords or falls back to OpenAI chat model
    """
    context_memory.append(user_input)
    if "schedule" in user_input:
        return handle_schedule(user_input)
    elif "question" in user_input:
        return answer_query(user_input)
    else:
        return query_openai(user_input)

def query_openai(prompt):
    """
    Sends the prompt to OpenAI's API and returns the response
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        response = process_user_input(user_input)
        print("Assistant:", response)
