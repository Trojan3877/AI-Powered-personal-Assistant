# tests/test_main.py
from assistant import main


def test_process_user_input_with_schedule(monkeypatch):
    monkeypatch.setattr(main, "handle_schedule", lambda x: "Scheduled reminder for 3pm")
    input_text = "remind me to study at 3pm"
    result = main.process_user_input(input_text)
    assert "Scheduled reminder" in result


def test_process_user_input_with_question(monkeypatch):
    monkeypatch.setattr(main, "answer_query", lambda x: "This is a mock answer.")
    input_text = "question about revenue forecast"
    result = main.process_user_input(input_text)
    assert "mock answer" in result


def test_process_user_input_with_empty():
    result = main.process_user_input("")
    assert result == "I'm sorry, I didn't understand that."



def test_prompt_history_is_bounded(monkeypatch):
    monkeypatch.setattr(main, "query_openai", lambda _: "fallback")

    main.context_memory.clear()
    try:
        for index in range(main.CONTEXT_MEMORY_LIMIT + 1):
            assert main.process_user_input(f"message {index}") == "fallback"

        assert len(main.context_memory) == main.CONTEXT_MEMORY_LIMIT
        assert main.context_memory[0] == "message 1"
        assert main.context_memory[-1] == f"message {main.CONTEXT_MEMORY_LIMIT}"
    finally:
        main.context_memory.clear()
