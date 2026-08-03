from assistant import main


def test_fallback_does_not_call_openai_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = main.process_user_input("Summarize my backlog")

    assert "OPENAI_API_KEY" in result


def test_context_memory_records_non_empty_inputs(monkeypatch):
    monkeypatch.setattr(main, "answer_query", lambda _: "answer")
    main.context_memory.clear()

    main.process_user_input("What should I do next?")

    assert list(main.context_memory) == ["What should I do next?"]
