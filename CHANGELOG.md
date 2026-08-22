# Changelog

All notable changes to AI-Powered Personal Assistant are documented here.

This project uses Semantic Versioning with release tags in the form `vMAJOR.MINOR.PATCH`.

## [Unreleased]

No unreleased changes are currently documented.

## [1.0.0] - 2026-08-22

### Added

- L6 engineering audit with prioritized production-hardening findings.
- README architecture and system-design Mermaid flowcharts aligned to the actual runtime.
- Clean-checkout Quickstart and reproducibility contract.
- Research-style benchmark table sourced only from committed machine-readable evidence.
- Explicit Q&A explaining simulated scheduling, provider-backed behavior, and stub integrations.
- Release badge and documented semantic-tag release contract.
- Source archive and SHA-256 checksum publication on version tags.
- GHCR container image publication on version tags.

### Documentation corrections

- Clarified that the interactive runtime routes only to scheduling, Q&A, or optional OpenAI fallback.
- Clarified that `AssistantSupervisor` is a separate demonstration path rather than part of the CLI routing flow.
- Clarified that supervisor memory/search/system workers are deterministic stubs.
- Clarified that the Snowflake path is a placeholder rather than a live Snowflake integration.
- Clarified that scheduling returns simulated confirmations and does not create persistent calendar events.
- Restricted benchmark claims to local component microbenchmarks and avoided inferring throughput or semantic quality.

### Known limitations

- External provider calls do not yet have a complete timeout/retry/circuit-breaker/error-normalization contract.
- Scheduling is not durable or connected to a real calendar provider.
- Semantic routing/tool-selection quality is not yet evaluated with a versioned fixture set.
- Privacy-aware redaction, retention policy, and structured runtime observability remain follow-up work.
- Release artifacts do not yet include SBOM attachment, signing, or provenance attestations.
