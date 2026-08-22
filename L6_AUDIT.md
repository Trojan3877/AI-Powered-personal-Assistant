# AI-Powered Personal Assistant — L6 Engineering Audit

Audit date: 2026-08-22

Scope: runtime architecture, routing semantics, external-service boundaries, tests/CI, benchmark evidence, container/release automation, documentation accuracy, privacy/security boundaries, and production-readiness claims.

## Executive assessment

The repository is a credible portfolio-scale assistant prototype with a deliberately small deterministic core, optional provider access, bounded in-process prompt retention, multi-version CI, separate security/quality workflows, machine-readable benchmarks, Docker packaging, and semantic-tag release automation.

The strongest engineering property is that routine tests and benchmarks do not require a live model download or external API. That keeps verification reproducible and avoids coupling baseline correctness to network availability.

The main weakness is architectural overstatement risk: several names imply capabilities that are not live integrations. The Snowflake path is a placeholder, the supervisor memory/search/system workers return deterministic strings, and the scheduler does not persist or execute real calendar actions. The README must therefore distinguish executable behavior from demonstrations.

## Findings by priority

### P1 — External LLM call has no explicit resilience contract

**Observed:** `assistant/main.py` and `modules/qa.py` construct an OpenAI client and call chat completions when `OPENAI_API_KEY` is present.

**Gap:** the code does not define explicit request timeout, cancellation, retry/backoff, circuit-breaking, rate-limit handling, provider-error translation, response schema validation, or cost/token budgets.

**Risk:** a provider outage, slow response, quota event, or malformed response can become unbounded or inconsistent application behavior.

**Recommendation:** centralize the provider adapter; set bounded timeouts; define which failures are retryable; cap retries; add cancellation; normalize provider exceptions into stable application errors; record token/cost metadata; and add deterministic failure-injection tests.

### P1 — Tool naming exceeds current integration reality

**Observed:** `agents/supervisor.py` contains memory, web-search, and system-action workers, but those methods return fixed demonstration strings. `modules/qa.py` contains a Snowflake branch that returns a placeholder string.

**Risk:** a reader can reasonably infer live retrieval, web search, system automation, or Snowflake-backed RAG when those capabilities are not implemented.

**Recommendation:** keep the stubs clearly labeled in code and docs, or replace them with adapter interfaces plus contract tests before making integration claims. Separate mock/stub benchmark numbers from real-provider measurements.

### P1 — Scheduling is simulated, not durable

**Observed:** `modules/scheduler.py` derives a next-day timestamp and returns a confirmation string.

**Gap:** there is no durable task object, timezone-aware persistence, idempotency key, external calendar write, cancellation/update semantics, or execution worker.

**Risk:** the assistant can tell a user something is “scheduled” without any persistent effect.

**Recommendation:** return a structured proposed action, require explicit execution through a calendar/task adapter, store provider IDs, support update/cancel, and test duplicate/retry behavior.

### P1 — Semantic quality is not evaluated

**Observed:** existing benchmarks measure local routing latency and supervisor stub paths.

**Gap:** no versioned evaluation fixture measures intent accuracy, ambiguous prompts, tool-selection correctness, hallucination-sensitive questions, refusal behavior, prompt injection, or provider failure handling.

**Recommendation:** add a deterministic evaluation set with expected route/tool/safety outcomes, report accuracy and class-wise confusion, and keep semantic evaluation separate from latency microbenchmarks.

### P1 — Privacy and retention controls are incomplete

**Observed:** the main router retains up to 100 raw prompts in process memory. The supervisor can append prompt excerpts to `DailyLog.md`.

**Gap:** there is no explicit data-classification policy, redaction layer, user-configurable retention, encryption boundary, deletion workflow, audit policy, or sensitive-field handling.

**Risk:** personal-assistant prompts can contain high-sensitivity content that should not be copied into logs or retained by default.

**Recommendation:** classify prompt/tool data, redact sensitive fields before logging, prefer metadata-only telemetry, define retention/deletion behavior, and test that secrets/tokens/PII-like patterns are not emitted into logs.

### P2 — Core router uses substring keyword matching

**Observed:** scheduling and Q&A routes match keywords anywhere in the lowercased prompt.

**Risk:** substring collisions and ambiguous multi-intent requests can route incorrectly, with no confidence or conflict policy.

**Recommendation:** add explicit token/intent fixtures, precedence documentation, ambiguous-intent handling, and a structured router result. If ML/LLM routing is later introduced, retain the deterministic router as a baseline.

### P2 — Supervisor is not integrated with the interactive runtime

**Observed:** `main.py` delegates to `assistant.main.process_user_input`; that function routes only to scheduler, Q&A, or OpenAI fallback. `AssistantSupervisor` is a separate demonstration path.

**Risk:** architecture diagrams can accidentally imply an agent hierarchy that is not present in the actual CLI execution path.

**Recommendation:** preserve two diagrams: the real interactive runtime and the separate supervisor experiment. Integrate only when there is a clear orchestration contract and tests.

### P2 — Benchmark provenance is incomplete

**Observed:** `benchmark-results.json` records generation time, harness path, iteration count, and latency statistics.

**Gap:** the committed artifact does not record commit SHA, Python version, OS/runner class, CPU model, warm-up policy, or process/container configuration.

**Risk:** readers may compare results across materially different environments as if they were equivalent.

**Recommendation:** emit runtime/platform/commit metadata from the harness and treat cross-host comparisons as descriptive unless the environment is controlled.

### P2 — Benchmark scope is micro-level only

**Observed:** benchmarked paths are deterministic local functions and supervisor stub workers.

**Gap:** no HTTP/service-level workload, concurrent clients, provider calls, throughput, saturation, memory, or cost measurements are included.

**Recommendation:** add separate experiments for local component latency, provider-backed end-to-end latency, concurrency, failure injection, and resource/cost behavior. Do not derive throughput from reciprocal micro-latency.

### P2 — Observability is mostly file/workflow based

**Observed:** there are workflow summaries, benchmark JSON, sample logs, and a daily Markdown ledger.

**Gap:** no structured runtime metrics/traces, correlation IDs, tool timing, error taxonomy, or redaction-aware telemetry contract is demonstrated in the core runtime.

**Recommendation:** add structured logging and metrics around route choice, tool/provider duration, normalized errors, and token/cost data while excluding raw sensitive prompt content by default.

### P2 — Release provenance can go further

**Observed after this release-prep branch:** semantic tags publish a GitHub Release, source archive, SHA-256 checksum, and GHCR image.

**Gap:** the release does not yet attach an SBOM, image digest manifest, provenance attestation, or signature.

**Recommendation:** add CycloneDX/SPDX SBOM attachment, GitHub artifact attestations or equivalent provenance, image digest recording, and optional signing before presenting the artifacts as supply-chain hardened.

## What already meets a strong senior-engineering bar

- Core CI runs across Python 3.10, 3.11, and 3.12.
- Lint/compile validation is separate from tests, improving signal isolation.
- Secret and dependency auditing are distinct from ordinary correctness CI.
- The default runtime can be validated without live external services.
- Prompt retention is bounded to a fixed-size deque.
- Benchmarks are emitted as machine-readable JSON.
- The Dockerfile packages only the default core path rather than pulling optional heavyweight ML/dashboard dependencies.
- Release automation is tag-driven and now publishes both source evidence and a container package.

## Recommended implementation sequence

1. Central provider adapter with timeout/cancellation/retry/error contract.
2. Structured scheduling proposal + durable/idempotent calendar adapter.
3. Replace or formalize Snowflake/search/memory/action stubs behind tested interfaces.
4. Add versioned routing/tool-selection/adversarial evaluation fixtures.
5. Add privacy-aware structured telemetry and redaction tests.
6. Add benchmark provenance metadata and end-to-end provider/concurrency experiments.
7. Add SBOM, image-digest manifest, and release provenance attestations.

## Release gate for v1.0.0 portfolio baseline

A portfolio v1.0.0 is reasonable if it is described as a documented assistant-systems prototype rather than an autonomous production agent. Before tagging, require green tests, code-quality, benchmark, security, and CodeQL checks for the release commit and ensure the README continues to label simulated/stub integrations accurately.
