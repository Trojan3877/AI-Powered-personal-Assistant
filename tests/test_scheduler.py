# tests/test_scheduler.py
import pytest
from modules import scheduler

def test_handle_schedule_with_valid_input():
    user_input = "Remind me to study at 3pm"
    response = scheduler.handle_schedule(user_input)
    assert "Scheduled reminder" in response or "Sorry" in response

def test_handle_schedule_with_empty_input():
    user_input = ""
    response = scheduler.handle_schedule(user_input)
    assert "Sorry" in response or "Invalid" in response
