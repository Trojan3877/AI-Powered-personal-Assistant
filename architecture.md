# AI-Powered Personal Assistant Architecture

This document separates the executable interactive runtime from the separate supervisor demonstration so the repository does not imply integrations that are not wired into the main application.

## Interactive runtime

```mermaid
flowchart LR
    U[User] --> CLI[main.py]
    CLI --> R[assistant.main.process_user_input]
    R --> C[(deque maxlen=100)]
    R -->|schedule intent| S[modules.scheduler.handle_schedule]
    R -->|Q&A intent| Q[modules.qa.answer_query]
    R -->|fallback| O1[assistant.main.query_openai]
    Q -->|USE_SNOWFLAKE=true| P[Snowflake placeholder]
    Q -->|default| O2[modules.qa.query_openai]
    S --> OUT[CLI response]
    P --> OUT
    O1 --> OUT
    O2 --> OUT
```

### Runtime boundaries

- `main.py` is the interactive CLI entry point.
- `assistant/main.py` owns the keyword router and bounded prompt deque.
- `modules/scheduler.py` returns simulated scheduling confirmations; it has no durable task/calendar side effect.
- `modules/qa.py` optionally calls OpenAI. Its Snowflake branch is a placeholder.
- External provider calls are optional and are not exercised by default tests/benchmarks.

## Separate supervisor demonstration

```mermaid
flowchart LR
    P[Prompt] --> SUP[AssistantSupervisor]
    SUP -->|portfolio/profile| MEM[Memory_Agent stub]
    SUP -->|search/latest| WEB[Web_Search_Agent stub]
    SUP -->|other| ACT[System_Action_Agent stub]
    MEM --> LOG[DailyLog.md]
    WEB --> LOG
    ACT --> LOG
```

The worker methods currently return fixed demonstration strings. They do not perform live vector retrieval, web search, or system actions. `AssistantSupervisor` is not called by the interactive CLI router.

## Trust boundaries

```mermaid
flowchart TD
    LOCAL[Local deterministic runtime] --> CONFIG{External provider enabled?}
    CONFIG -->|no| SAFE[Local safe/configuration response]
    CONFIG -->|yes| PROVIDER[External LLM provider]
    PROVIDER --> LOCAL

    LOCAL --> LOGGING[Local process/file logging]
    LOGGING --> POLICY[Future redaction + retention policy]

    CAL[Future calendar/tool adapter] --> AUTH[Future authenticated tool boundary]
```

Before handling sensitive personal data or executing consequential tools, add explicit authentication, authorization, idempotency, redaction, retention, timeout/cancellation, error normalization, and audit controls.
