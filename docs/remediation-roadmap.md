# Remediation Roadmap

This roadmap is a proposed improvement plan based on public workflow discovery and a local reference implementation. It is not a statement that Cynbit has confirmed vulnerabilities.

## Priority definitions

- **P0 — Verify first:** establish evidence and correct any confirmed release-blocking issue.
- **P1 — Core controls:** foundational validation, response minimization, and abuse controls.
- **P2 — Reliability and governance:** logging, retention, idempotency, and operational monitoring.
- **P3 — Optimization:** measured performance and scaling work.

## Roadmap

| Priority | Work item | Rationale | Acceptance criteria |
|---|---|---|---|
| P0 | Observe normal contact/demo request flow | Avoid basing findings on assumptions. | Evidence log records timestamp, page, method, destination, status, content type, and redacted response where available. |
| P0 | Separate verified issues from hypotheses | Keeps report credible and reproducible. | Each finding has status, evidence, impact, recommendation, and verification plan. |
| P1 | Server-side validation | Client validation can be bypassed; server must enforce contract. | Tests cover required fields, invalid email, unsupported product, and max lengths. |
| P1 | Explicit response allowlists | Avoid returning unnecessary/internal fields. | Tests assert exact public response keys. |
| P1 | Endpoint-specific throttling and edge controls | Reduce ordinary abuse and resource consumption. | Limits configured for each endpoint; monitor 429 behaviour in local/staging tests. |
| P1 | Request-body limits | Avoid oversized submissions consuming excess resources. | Edge/app body limit is documented and tested in a controlled environment. |
| P1 | Separate public write and private read APIs | Anonymous submitters should not gain access to submitted records. | No public list/detail endpoint; private retrieval requires authentication and authorization. |
| P2 | Structured, redacted logging | Support debugging without storing unnecessary PII. | Logs include request/correlation IDs and exclude message bodies, tokens, and unnecessary personal data. |
| P2 | Retention/deletion policy | Minimize the lifecycle of personal data. | Documented retention period, deletion workflow, and responsible owner. |
| P2 | Idempotency and duplicate handling | Avoid duplicate business effects on retries. | Defined duplicate policy; tests prove retry behaviour where applicable. |
| P2 | Asynchronous notifications if needed | Decouple slow email/notification providers from the request. | Retry/backoff, failure monitoring, and no duplicate business records. |
| P2 | Failure-path tests | Validate robustness beyond happy paths. | Tests cover malformed JSON, throttling, and controlled service/database failure handling. |
| P3 | Performance baseline | Optimize from measurement, not guesswork. | Reproducible page/API measurements and documented environment. |
| P3 | Query optimization | Indexing should match real query patterns. | Query plans or profiling justify each index; regression tests remain green. |
| P3 | Authorized load testing | Evaluate capacity safely. | Only performed against local/staging systems with explicit authorization and agreed limits. |

## Recommended implementation sequence

1. Complete public browser observations and evidence log.
2. Run local checks and all tests.
3. Confirm `.gitignore` excludes virtual environments, databases, `.env` files, and credentials.
4. Publish the report and roadmap.
5. Review each claim for evidence and qualify unverified items.
6. Submit the GitHub repository as the primary deliverable.
