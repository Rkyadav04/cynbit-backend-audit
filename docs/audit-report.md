# Cynbit Backend Technical Audit

**Assessment:** Backend Developer Intern  
**Review date:** 22 October 2026  
**Scope:** Publicly observable website behaviour and a locally implemented reference API  
**Status:** Initial audit — live backend findings require evidence verification

## 1. Executive Summary

This assessment reviews publicly observable aspects of Cynbit's website and proposes backend engineering improvements for inquiry and product-demo workflows.

The review focuses on server-side input validation, API response contracts, request throttling, data minimization, error handling, and testability. A local Django REST Framework implementation demonstrates how these controls can be implemented and verified independently.

The local implementation currently has two endpoints:

- `POST /api/v1/inquiries/`
- `POST /api/v1/demo-requests/`

Ten automated tests pass across the two endpoints. These tests validate the local reference implementation; they do not establish the behaviour or security posture of Cynbit's production backend.

## 2. Scope and Methodology

### In scope

- Publicly accessible website pages and forms.
- Normal browser interactions and observable HTTP requests.
- Public response headers, status codes, payload structures, and request timings where captured.
- Local implementation of validation, response serialization, throttling configuration, and automated tests.

### Out of scope

- Unauthorized access or account manipulation.
- Hidden endpoint enumeration, destructive tests, load testing, or exploitation.
- Access to private databases, production logs, or internal source code.
- Claims about production vulnerabilities without supporting evidence.

### Evidence classification

- **Verified observation:** Directly observed and recorded.
- **Potential risk:** A credible risk that requires additional evidence.
- **Not assessed:** The available public access did not establish the behaviour.

## 3. Public Application Surface

The official website presents an inquiry workflow at:

https://www.cynbit.in/contact

The careers website lists technical internship roles, including Backend Developer Intern:

https://cynbitwebsite.vercel.app/careers

These pages provide useful starting points for examining form workflows and data handling. Their public availability does not establish which backend services, databases, or API gateways process submissions.

## 4. Findings and Investigation Plan

### F-01: Server-side form validation

**Category:** Data validation  
**Status:** Verify live behaviour  
**Potential impact:** Invalid or oversized input could increase downstream processing errors or create inconsistent records if server-side controls are insufficient.

**Investigation:** Observe normal form submissions and document validation messages and HTTP responses. Do not infer backend validation from frontend messages alone.

**Recommendation:** Use explicit serializer validation, required-field constraints, length limits, and consistent field-level errors.

**Local verification:** Automated tests cover invalid email, blank required fields, and successful submissions.

### F-02: Public endpoint abuse controls

**Category:** Security and availability  
**Status:** Proposed control; production configuration not verified  
**Potential impact:** Automated submissions could consume application resources or create unwanted records.

**Recommendation:** Apply endpoint-specific rate limits, request-size limits, monitoring, and additional bot protection where justified.

**Local implementation:** Scoped throttling is configured for inquiry and demo-request endpoints. The configured rate is illustrative and requires production tuning. Application-level throttling is not a complete denial-of-service defence.

### F-03: API response data minimization

**Category:** Privacy and API design  
**Status:** Local implementation verified; production behaviour not verified  
**Potential impact:** Returning unnecessary fields can disclose internal or personal information.

**Recommendation:** Use explicit serializer field allowlists and avoid returning internal notes, secrets, administrative fields, or unrelated records.

**Local verification:** Automated tests assert the exact set of response fields.

### F-04: Error handling and API consistency

**Category:** Reliability  
**Status:** Partially verified locally  
**Potential impact:** Inconsistent status codes or unstructured errors can complicate client integration and incident diagnosis.

**Recommendation:** Use predictable success and validation responses, avoid stack traces in client-facing errors, and log unexpected failures with correlation IDs while redacting personal information.

**Next verification:** Add tests for malformed JSON, oversized payloads, server-side failures, and throttled responses.

### F-05: Personal-data handling

**Category:** Privacy and data governance  
**Status:** Further verification required  
**Potential impact:** Excessive collection, unnecessary retention, or inappropriate logging can expose personal information.

**Recommendation:** Minimize collected fields, define retention periods, restrict access to submitted records, and redact personal information from logs.

**Next verification:** Review the published privacy notice and record the actual data flow and any publicly identifiable third-party processing services.

## 5. Reference Architecture

```text
Public web form
      |
      v
HTTP request
      |
      v
API endpoint
      |
      v
Scoped throttling
      |
      v
Serializer validation
      |
      v
Database model
      |
      v
Explicit response serializer
      |
      v
HTTP response
```

The diagram represents the proposed local implementation, not a confirmed diagram of Cynbit's production architecture.

## 6. Local Implementation and Testing

**Technology:** Python, Django, Django REST Framework, SQLite development database.

**Endpoints:**

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/inquiries/` | Validate and create an inquiry |
| POST | `/api/v1/demo-requests/` | Validate and create a product-demo request |

**Test status:** 10 automated tests passed on 22 October 2026.

The tests cover successful creation, email validation, required fields, accepted product values, and response-field allowlists.

These results apply only to the local implementation. Production integration, deployment configuration, concurrency behaviour, and external email delivery are outside the current implementation scope.

## 7. Prioritized Remediation Roadmap

**Immediate**
1. Verify server-side validation on the actual public submission workflows.
2. Ensure responses do not expose unnecessary data.
3. Confirm consistent HTTP status codes and error handling.
4. Review public response headers and HTTPS behaviour.

**Short term**
1. Configure and monitor appropriate rate limits.
2. Add structured logging with sensitive-field redaction.
3. Add tests for throttling, malformed requests, and oversized inputs.
4. Review access controls for any administrative data retrieval.

**Longer term**
1. Introduce asynchronous notification delivery if required.
2. Add monitoring and alerting for failed submissions.
3. Establish data-retention and deletion policies.
4. Evaluate caching and database indexing using measured traffic and query behaviour.

## 8. Limitations

This is a scope-limited assessment based on public information and a locally implemented reference API. No access to Cynbit's private source code, production database, or internal observability systems was available.

Only findings supported by recorded evidence should be classified as verified issues. Recommendations are proposed engineering improvements and should not be interpreted as proof that the production system has the corresponding weaknesses.

## 9. References

- Cynbit official website: https://www.cynbit.in/
- Contact page: https://www.cynbit.in/contact
- Careers page: https://cynbitwebsite.vercel.app/careers
- Django REST Framework testing: https://www.django-rest-framework.org/api-guide/testing/
- Django REST Framework throttling: https://www.django-rest-framework.org/api-guide/throttling/
- OWASP API Security: https://owasp.org/www-project-api-security/

