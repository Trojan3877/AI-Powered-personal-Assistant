# tests/test_qa.py
import pytest
from modules import qa

def test_answer_query_with_known_input(monkeypatch):
    # Mock Snowflake or OpenAI response
    monkeypatch.setattr(qa, "snowflake_query", lambda x: "Mocked Snowflake response")
    monkeypatch.setattr(qa, "fallback_openai_query", lambda x: "Mocked OpenAI response")

    result = qa.answer_query("What is the revenue?")
    assert "Mocked" in result

def test_answer_query_with_empty_input(monkeypatch):
    monkeypatch.setattr(qa, "fallback_openai_query", lambda x: "Please ask something.")

    result = qa.answer_query("")
    assert "Please ask" in result
