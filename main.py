# tests/test_main.py
import pytest
from assistant import main

def test_process_user_input_with_schedule(monkeypatch):
    monkeypatch.setattr(main.scheduler, "handle_schedule", lambda x: "Scheduled reminder for 3pm")
    input_text = "Remind me to study at 3pm"
    result = main.process_user_input(input_text)
    assert "Scheduled reminder" in result

def test_process_user_input_with_question(monkeypatch):
    monkeypatch.setattr(main.qa, "answer_query", lambda x: "This is a mock answer.")
    input_text = "What is the revenue forecast?"
    result = main.process_user_input(input_text)
    assert "mock answer" in result

def test_process_user_input_with_empty(monkeypatch):
    result = main.process_user_input("")
    assert result == "I'm sorry, I didn't understand that."
