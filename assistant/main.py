"""Core assistant routing logic."""

import os
from collections import deque

from modules.qa import answer_query
from modules.scheduler import handle_schedule

CONTEXT_MEMORY_LIMIT = 100
# Retain a small recent window for local routing context without unbounded prompt storage.
context_memory: deque[str] = deque(maxlen=CONTEXT_MEMORY_LIMIT)

SCHEDULE_KEYWORDS = {"schedule", "remind", "meeting", "appointment", "calendar"}
QA_KEYWORDS = {"question", "what", "who", "when", "where", "why", "how", "explain"}


def process_user_input(user_input: str) -> str:
    """Route user input to the appropriate module based on keywords."""
    if not user_input or not user_input.strip():
        return "I'm sorry, I didn't understand that."

    context_memory.append(user_input)
    lower = user_input.lower()

    if any(keyword in lower for keyword in SCHEDULE_KEYWORDS):
        return handle_schedule(user_input)
    if any(keyword in lower for keyword in QA_KEYWORDS):
        return answer_query(user_input)

    return query_openai(user_input)


def query_openai(prompt: str) -> str:
    """Send the prompt to OpenAI when configured, otherwise return a safe fallback."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OpenAI API key is not configured. Please set OPENAI_API_KEY to enable live answers."

    from openai import OpenAI  # pragma: no cover

    client = OpenAI(api_key=api_key)  # pragma: no cover
    response = client.chat.completions.create(
        model=os.getenv("LANGUAGE_MODEL", "gpt-3.5-turbo"),
        messages=[{"role": "user", "content": prompt}],
    )  # pragma: no cover
    return response.choices[0].message.content  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    while True:
        prompt = input("You: ")
        response = process_user_input(prompt)
        print("Assistant:", response)
