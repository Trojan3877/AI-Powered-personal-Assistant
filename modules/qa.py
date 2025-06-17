"""
qa.py — Question Answering Module
---------------------------------
Uses Snowflake for semantic answers if enabled,
otherwise delegates to OpenAI for general queries.
"""

import openai
import os

USE_SNOWFLAKE = os.getenv("USE_SNOWFLAKE", "false").lower() == "true"

def answer_query(query):
    """
    Routes the query to Snowflake Q&A logic or OpenAI fallback.
    """
    if USE_SNOWFLAKE:
        return query_snowflake(query)
    else:
        return query_openai(query)

def query_snowflake(query):
    """
    Placeholder function for Snowflake query handling.
    In production, this would query a semantic index or vector DB.
    """
    return f"🔍 [Snowflake]: Answer to '{query}' would be retrieved from a knowledge base."

def query_openai(prompt):
    """
    Uses OpenAI LLM as a fallback when Snowflake is disabled.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']
