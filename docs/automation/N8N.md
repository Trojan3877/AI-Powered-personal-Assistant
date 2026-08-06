# n8n automation

## Scope and repository audit

This repository is a Python personal-assistant prototype with existing GitHub Actions for CI, security analysis, releases, deterministic benchmarks, README-metrics previews, data validation, and a scheduled supervisor smoke run. The n8n definitions in `n8n/` deliberately automate GitHub collaboration only; they do not execute the assistant, call OpenAI, access Snowflake, or change repository files.

The definitions are **inactive on import**. They are portable workflow JSON, not a deployment. No n8n host URL, webhook URL, token, or OAuth secret is committed.

## Prerequisites

Use a self-hosted n8n instance and bind one organization-wide GitHub OAuth credential in the n8n credential store to every GitHub Trigger or HTTP Request node. Never place that credential in these JSON files.

Set these environment variables in the n8n deployment:

| Variable | Required | Purpose |
| --- | --- | --- |
| `N8N_BASE_URL` | Yes | Base URL for the self-hosted n8n instance; no URL is hard-coded here. |
| `GITHUB_OWNER` | Yes | GitHub owner; set to `CoreyLeath-code`. |
| `GITHUB_TOKEN` | Optional | Fallback only for HTTP Request nodes when OAuth cannot be used; keep it in the environment/credential store, never in workflow JSON. |

The GitHub OAuth credential needs permission to read repository metadata, read/write issue labels, and write pull-request comments for this repository.

## Workflows

### Label bootstrap

- **Definition:** `n8n/label-bootstrap.json`
- **Trigger:** Manual execution.
- **Actions:** Reads the repository labels, computes only missing labels, and creates the documented label set. Existing labels are never updated, so their colors remain untouched.
- **Manual execution:** Import the JSON, bind the GitHub credential, confirm `GITHUB_OWNER`, then activate only for the manual run.
- **Failure recovery:** Re-run after correcting credential permissions. The workflow is idempotent because it posts only labels absent from the preceding GET response.

### Issue triage

- **Definition:** `n8n/issue-triage.json`
- **Trigger:** GitHub `issues` event, limited to newly opened issues.
- **Actions:** Ignores pull requests, assigns `needs-triage`, and adds one conservative topical label and one priority label only when a title/body keyword matches.
- **Manual execution:** Import, bind the GitHub credential, set repository owner/repository values from the environment, review the keyword rules, then activate.
- **Failure recovery:** Disable the workflow if it mislabels an issue; remove labels manually and adjust the explicit rule set before re-enabling. Ambiguous issues keep only `needs-triage`.

### Pull-request assistant

- **Definition:** `n8n/pull-request-assistant.json`
- **Trigger:** GitHub `pull_request` events for opened, reopened, or synchronized pull requests.
- **Actions:** Fetches changed files and posts a contextual checklist that identifies affected top-level areas and whether an issue reference appears in the PR body.
- **Manual execution:** Import, bind the GitHub credential, review the comment wording, then activate.
- **Failure recovery:** Disable the workflow to stop comments. Existing comments are informational and must be edited or removed manually if policy changes.

## Deliberately skipped automation

| Candidate | Reason it is not installed |
| --- | --- |
| Assistant execution | `.github/workflows/assistant-orchestrator.yml` already owns a scheduled smoke run and commits only its defined log; a second orchestrator risks duplicate execution and log writes. |
| Benchmark and metric publishing | Existing benchmark and metric-preview workflows establish the repository’s review path. This PR does not create unreviewed metric updates. |
| Security monitoring | Existing security, SAST, dependency-review, and CodeQL workflows already provide security execution; no alert-routing policy or destination is committed for n8n to use. |
| Release automation | `.github/workflows/release.yml` already creates releases from version tags. |
| README/documentation reminders | The repository has no agreed definition of a significant change; automatic issue creation would create noise. |
| Portfolio dashboard, project sync, community/review reminders | No canonical portfolio repository, GitHub Project, ownership policy, or reminder cadence is present in the repository. |

## Validation

The definitions are checked as JSON before opening the pull request. n8n runtime validation is intentionally deferred: this workspace has no configured `N8N_BASE_URL` or n8n credential, and the workflows must remain inactive until an administrator imports and configures them.
