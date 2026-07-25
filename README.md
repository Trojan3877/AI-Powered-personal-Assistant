# AI-Powered Personal Assistant

[![CI](https://github.com/CoreyLeath-code/AI-Powered-personal-Assistant/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/CoreyLeath-code/AI-Powered-personal-Assistant/actions/workflows/ci-cd.yml)
[![Code Quality](https://github.com/CoreyLeath-code/AI-Powered-personal-Assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/CoreyLeath-code/AI-Powered-personal-Assistant/actions/workflows/ci.yml)
[![Benchmarks](https://github.com/CoreyLeath-code/AI-Powered-personal-Assistant/actions/workflows/benchmarks.yml/badge.svg)](https://github.com/CoreyLeath-code/AI-Powered-personal-Assistant/actions/workflows/benchmarks.yml)
[![Security](https://github.com/CoreyLeath-code/AI-Powered-personal-Assistant/actions/workflows/security.yml/badge.svg)](https://github.com/CoreyLeath-code/AI-Powered-personal-Assistant/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An autonomous personal-assistant prototype built around deterministic intent routing,
scheduling utilities, optional OpenAI-backed question answering, and GitOps-friendly
execution logs. The project is intentionally lightweight in its core path so tests,
benchmarks, and container builds can run without model downloads or live API calls.

## Architecture

```text
User Prompt
   |
   v
Assistant Router
   |-- schedule/reminder intent --> Scheduler module
   |-- question/explanation intent -> QA module
   |-- portfolio/profile intent ---> Supervisor memory worker
   |-- latest/search intent -------> Supervisor search worker
   `-- fallback -------------------> Optional OpenAI client

Operational logs
   |
   v
DailyLog.md / logs/session_log.json / benchmark-results.json
```

## Research Metrics And Benchmarks

The table separates measured repository evidence from target service objectives.
Measured values come from the deterministic benchmark harness and sample log data in
this repository. Target values are engineering goals for a productionized assistant
service and should be revalidated against live infrastructure before use in an SLA.

### Recorded Benchmark Results

Latest local benchmark command:

```bash
python benchmarks/assistant_benchmarks.py --iterations 500 --output benchmark-results.json
```

| Benchmark | Metric | Recorded value | Evidence |
|---|---:|---:|---|
| Intent router, QA path | Mean latency | 0.001144 ms | `benchmark-results.json` |
| Intent router, schedule path | Mean latency | 0.003916 ms | `benchmark-results.json` |
| Intent router, fallback path | Mean latency | 0.000982 ms | `benchmark-results.json` |
| Supervisor memory route | Mean latency | 0.291320 ms | `benchmark-results.json` |
| Supervisor search route | Mean latency | 0.266136 ms | `benchmark-results.json` |
| Sample QA log | Mean recorded latency | 1.90 s | `logs/session_log.json` |
| Sample QA log | Correct sample responses | 3 / 3 | `logs/session_log.json` |

### Engineering Quality Metrics

| Dimension | Current repository status | Industry-readiness signal |
|---|---|---|
| Test execution | 22 deterministic tests with 96% local coverage | No live OpenAI/Snowflake calls in CI |
| Benchmark publishing | Dedicated JSON harness with `python -m json.tool` validation in Actions | Benchmark artifacts are machine-readable |
| Dependency strategy | Core, dev, dashboard, and ML dependencies split by use case | CI avoids heavyweight model downloads |
| Static checks | Ruff, pytest, coverage, compile validation, Bandit, and TruffleHog workflows | Failures are no longer masked by `|| echo` |
| Documentation quality | README metrics distinguish measured results from targets | Avoids overstating production readiness |
| Container path | Docker installs core runtime requirements only | Smaller, faster default image |

### Production Target Metrics

| Capability | Target | Rationale |
|---|---:|---|
| Router p95 latency | < 25 ms | Deterministic keyword routing should stay CPU-local |
| Scheduler p95 latency | < 50 ms | Calendar parsing can remain synchronous until external APIs are introduced |
| QA fallback availability | 99.9% | Requires provider timeout/retry/circuit-breaker controls |
| Benchmark JSON validity | 100% of runs | Required for reliable dashboard publishing |
| CI signal quality | 0 masked failures | Build status should represent real repository health |
| Secrets exposure tolerance | 0 verified findings | Required before production deployment |

## Quick Start

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Optional extras:

```bash
python -m pip install -r requirements-dashboard.txt  # Streamlit dashboard
python -m pip install -r requirements-ml.txt         # Local transformer engine
```

## Validation

```bash
ruff check .
pytest --cov=assistant --cov=modules --cov=agents --cov=scripts --cov-report=term-missing
python benchmarks/assistant_benchmarks.py --output benchmark-results.json
python -m json.tool benchmark-results.json
python -m compileall -q assistant modules agents scripts src
```

## Senior review follow-up: assistant behavior and reproducibility

This section closes the documentation items tracked in [issue #7](https://github.com/CoreyLeath-code/AI-Powered-personal-Assistant/issues/7). Recorded values are local deterministic-harness evidence; production availability, provider quality, privacy, and cost are not implied.

### Verification contract

From a clean checkout:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt -r requirements-dev.txt
pytest --cov=assistant --cov=modules --cov=agents --cov=scripts --cov-report=term-missing
ruff check .
python benchmarks/assistant_benchmarks.py --iterations 500 --output benchmark-results.json
python -m json.tool benchmark-results.json
python -m compileall -q assistant modules agents scripts src
```

The benchmark JSON and `logs/session_log.json` are the canonical evidence for latency and sample-response claims. The current README records 22 deterministic tests and 96% local coverage; these must be rechecked in the workflow run for the reviewed commit. Provider-backed evaluation, secret scanning, dependency scanning, and image-size measurements should be reported as CI artifacts, not represented by an unqualified “production” badge.

### Engineering decisions and failure modes

- **Deterministic routing first:** local intent routing keeps the common path fast and testable, while optional provider fallback improves breadth at the cost of network latency, quota, and failure handling.
- **Tool execution is a trust boundary:** calendar/search/memory adapters need schema validation, timeouts, idempotency, and redacted logs before they can handle user data.
- **Quality is more than route latency:** the next evaluation set should include ambiguous intents, prompt injection attempts, unavailable tools, provider timeouts, and hallucination-sensitive answers with expected-safe behavior.
- **Next production step:** publish a versioned evaluation fixture with pass/fail criteria for helpfulness, refusal behavior, tool correctness, p95 latency, and cost per request; keep the current microbenchmarks labeled as component measurements.


## Known Gaps

- The OpenAI and Snowflake integrations are adapter stubs, not production credential
  management or retry systems.
- `logs/session_log.json` is a small recorded sample, not a statistically significant
  evaluation dataset.
- The local transformer engine is optional and intentionally excluded from default CI
  because model downloads make routine validation slow and flaky.
