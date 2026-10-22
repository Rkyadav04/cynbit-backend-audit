# Cynbit Backend Technical Audit Report

**Assessment:** Backend Developer Intern  
**Review date:** 22 October 2026  
**Scope:** Publicly accessible Cynbit pages and a separate local reference API  
**Assessment status:** Public-surface review; production API behaviour remains unverified unless a finding is supported by a recorded browser observation.

## 1. Executive summary

Cynbit's public website exposes several workflows relevant to backend engineering: general contact/inquiry, product-demo requests, and careers/application information. The product page publicly describes Cynbit Studio, TenantEase, and Revio, and includes a demo-request workflow. The contact page includes information for contacting the company. The careers page describes an engineering culture emphasizing documentation, peer reviews, and iterative sprints.

These public pages suggest useful audit questions around input validation, privacy, request handling, response contracts, and abuse prevention. They do **not** prove that the production backend has a vulnerability or even establish which API, database, or service handles each form.

A local Django REST Framework reference implementation demonstrates two proposed endpoints:
- `POST /api/v1/inquiries/`
- `POST /api/v1/demo-requests/`

The developer reported 10 local automated tests passing. These tests validate the reference implementation only; they are not evidence of the production site's security.

## 2. Scope and methodology

### In scope
- Publicly accessible pages and visible form fields.
- Normal browser use and low-volume observation of requests that occur naturally during page interaction.
- Public response headers and request/response details if captured through browser DevTools.
- Local reference implementation and its automated tests.

### Out of scope
- Unauthorized access, account manipulation, or attempts to access another person's data.
- Aggressive endpoint enumeration, fuzzing against production, load testing, exploitation, or disruption.
- Access to private source code, databases, production logs, or internal infrastructure.

### Evidence rules
- **Observed:** Directly visible in a cited public page or recorded in a dated browser observation.
- **Hypothesis / potential risk:** A plausible concern that has not been confirmed in the target system.
- **Not assessed:** Cannot be established from the available public surface or current evidence.
- Never label a weakness as “confirmed” without reproducible evidence.

## 3. Public application surface

### 3.1 Contact page
URL: https://www.cynbit.in/contact

The publicly indexed page includes contact information and a “Common Inquiries” section describing how prospective customers can start a project and ask about custom AI automation. The live page should be inspected in a browser to verify the exact form fields and the current submission flow before describing those details as observed.

### 3.2 Product suite and demo workflow
URL: https://www.cynbit.in/products

The page describes three products:
- **Cynbit Studio:** learning, coding missions, AI feedback, and career preparation.
- **TenantEase:** property and tenant management, rent/payment tracking, and tenant profiles.
- **Revio:** review management, sentiment analysis, and role-based access concepts.

The page includes a “Schedule a Demo” workflow with product selection and fields including full name, work email, company name, and a message. This is a public-page observation; the backend endpoint, storage, validation, and notification path are not established by the page alone.

### 3.3 Careers page
URL: https://www.cynbit.in/careers

The publicly indexed careers page describes a documentation-led culture, asynchronous communication, collaborative reviews, and iterative sprints. The page is useful context for presenting the report with a clear methodology, evidence trail, and prioritized remediation plan. Do not infer a private hiring rubric from marketing content.

## 4. Findings and investigation register

### F-01 — Server-side validation of public submissions
**Category:** Input validation  
**Status:** Not verified on production; local control demonstrated  
**Severity:** Undetermined until evidence and impact are established

**Why investigate:** Public forms commonly accept user-controlled values. Client-side validation can improve usability but cannot replace server-side validation.

**Evidence currently available:** Public contact/product pages show user-facing workflows. No captured production request/response pair in this evidence pack establishes how server-side validation behaves.

**Potential impact if absent:** Invalid or oversized data could be persisted or passed to downstream services, creating inconsistent records or processing errors.

**Recommendation:** Enforce required fields, type and length constraints, email syntax validation, allowed product values, normalization where appropriate, and consistent field-level `400 Bad Request` responses. Set a request-body size limit at the application or edge layer.

**Verification plan:** In the browser, submit only ordinary test values through the intended form. Record the request method, destination, content type, status, and response. Do not send repeated, oversized, or deliberately malicious requests to production. If the form prevents submission client-side, state that backend validation remains unverified.

**Local implementation:** DRF serializers validate the inquiry and demo-request payloads. The local test suite checks invalid email and required fields.

### F-02 — Data minimization and response-field control
**Category:** Privacy / API design  
**Status:** Local control demonstrated; production response not verified  
**Severity:** Undetermined

**Why investigate:** Inquiry, demo, and candidate workflows can handle personal information. API responses should return only fields needed by the client.

**Evidence currently available:** Public product/contact/careers pages establish that user-facing business workflows exist; they do not establish the shape of stored records or response payloads.

**Potential impact if absent:** Unnecessary personal or internal fields in responses or logs can increase exposure if those responses/logs are later accessed by an unauthorized party.

**Recommendation:** Use explicit response serializers/allowlists, avoid returning internal notes or administrative fields, redact personal information from logs, and define retention and deletion rules.

**Verification plan:** Capture the response to a normal submission if the browser exposes it. Review only fields actually returned. Do not infer database columns from form fields.

**Local implementation:** Automated tests assert exact response keys for the reference endpoints.

### F-03 — Public form abuse and resource consumption
**Category:** Availability / abuse prevention  
**Status:** Production controls not verified; local scoped throttling configured  
**Severity:** Undetermined

**Why investigate:** Public submission flows can attract automated or duplicate submissions.

**Evidence currently available:** Public inquiry/demo workflows exist. There is no evidence in this pack that production rate limiting is absent or incorrectly configured.

**Potential impact if controls are insufficient:** Spam records, notification abuse, and increased processing cost.

**Recommendation:** Use appropriately tuned edge/WAF limits, application-level throttling, request-size limits, bot detection where justified, monitoring, and a reviewable process for false positives. Apply idempotency where duplicate business actions would be harmful.

**Verification plan:** Review publicly returned headers and normal form behaviour only. Do not attempt to trigger production throttling by repeated submissions. Ask the system owner for configuration evidence if deeper confirmation is required.

**Local implementation:** The reference API uses DRF `ScopedRateThrottle`. DRF documents that built-in throttling is intended for basic usage policies and is not a complete security or denial-of-service defence.

### F-04 — Error handling and observability
**Category:** Reliability / information disclosure  
**Status:** Production error behaviour not verified  
**Severity:** Undetermined

**Why investigate:** API clients need predictable status codes and actionable validation errors, while internal exceptions must not leak stack traces or secrets.

**Evidence currently available:** No production error response or malformed-request response has been recorded in this evidence pack.

**Recommendation:** Return stable error schemas; use `400` for validation errors, `415` for unsupported media types where applicable, and `429` for throttling. Do not expose stack traces to clients. Use structured server-side logs with request/correlation IDs and redaction of personal data.

**Verification plan:** Record errors naturally encountered during normal use. Do not deliberately provoke server exceptions on production.

**Local implementation:** The local tests validate field-level `400` responses. Additional tests for malformed JSON, throttling, and unexpected failures are recommended.

### F-05 — Authentication and authorization boundaries
**Category:** Access control  
**Status:** Not assessed from the available public workflow  
**Severity:** Not assigned

**Why investigate:** Public form creation may intentionally be anonymous, while access to submitted records, admin functions, or tenant/business data should be restricted.

**Evidence currently available:** Public marketing content describes product concepts, including role-based access for Revio and tenant profiles for TenantEase. These descriptions do not prove how authorization is implemented.

**Recommendation:** Keep public create endpoints separate from administrative list/detail endpoints. Require authentication and explicit authorization for private records. For multi-tenant applications, scope every data query to the user's authorized organization and test cross-tenant denial.

**Verification plan:** Do not probe private records or attempt cross-account access. Request authorized test credentials and written scope if authenticated access-control testing is expected.

### F-06 — Performance and caching
**Category:** Performance  
**Status:** Not measured  
**Severity:** Not assigned

**Why investigate:** Public pages can be reviewed for transfer size, cache headers, duplicate requests, and obvious request waterfalls, but a single browser visit is not a load test.

**Evidence currently available:** No timestamped request waterfall, response-size measurements, or repeatable performance baseline is included here.

**Recommendation:** Measure representative page-load requests, set appropriate caching for static assets, avoid caching personalized responses publicly, and optimize database queries only after code/query evidence exists. Add pagination for any future list endpoints.

**Verification plan:** Capture a single normal page load using DevTools with cache state recorded. Avoid claiming performance problems without measurements.

## 5. Local reference implementation

The local Django REST Framework project demonstrates two POST endpoints and explicit validation.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v1/inquiries/` | POST | Create an inquiry |
| `/api/v1/demo-requests/` | POST | Create a product-demo request |

### Local test status
The developer reported the following output on 22 October 2026:
- Django system check: no issues.
- Automated tests: 10 passed.
- Test database created and destroyed successfully.

This is a reported local test result. Re-run `python manage.py check` and `python manage.py test inquiries demo_requests` immediately before final submission.

## 6. Proposed architecture

```text
Public browser form
       |
       v
HTTPS / edge controls
       |
       v
Request size and rate controls
       |
       v
Django URL routing
       |
       v
Scoped throttle
       |
       v
Serializer validation
       |
       v
Database transaction / persistence
       |
       +------> Optional async notification task
       |
       v
Explicit response serializer
       |
       v
HTTP response
```

This is a proposed reference architecture, not a representation of Cynbit's internal deployment. If notification delivery is required, use an asynchronous worker and retry strategy, and ensure retries do not create duplicate business records.

## 7. Prioritized remediation roadmap

### P0 — Before release / immediate validation
1. Verify the live contact and demo submission request/response flow using normal interactions.
2. Record exact evidence: URL, date/time, method, status, content type, and redacted payload/response.
3. Confirm that production conclusions are not inferred from local code.
4. Check public responses for accidental stack traces or sensitive values only when naturally observable.

### P1 — Core API hardening
1. Enforce server-side field and payload-size validation.
2. Use explicit response serializers.
3. Apply endpoint-specific rate limits and edge controls.
4. Keep public submission endpoints separate from private data retrieval.
5. Add structured, redacted logging and useful error responses.

### P2 — Reliability and data governance
1. Define data-retention and deletion periods.
2. Add idempotency for workflows where duplicates cause business impact.
3. Add safe asynchronous notification delivery if needed.
4. Add tests for malformed requests, throttling, and unexpected failures.
5. Monitor error rates, submission volume, latency, and delivery failures.

### P3 — Measured performance improvement
1. Establish a repeatable baseline.
2. Inspect caching and static asset delivery.
3. Profile database queries with representative workloads.
4. Add pagination and indexes only where justified by actual query patterns.
5. Load-test only a locally controlled or explicitly authorized environment.

## 8. Limitations

This report is a scope-limited public-surface review. The current evidence does not prove a production vulnerability, identify Cynbit's actual API implementation, or confirm its database, authentication, caching, rate-limiting, or logging configuration. The local reference API is separate from Cynbit's systems.

The final submitted version should append real, timestamped browser observations and screenshots where collected. If an item was not checked, leave it as “not verified” rather than fabricating evidence.

## 9. References

1. Cynbit official website: https://www.cynbit.in/
2. Cynbit contact page: https://www.cynbit.in/contact
3. Cynbit product suite: https://www.cynbit.in/products
4. Cynbit careers: https://www.cynbit.in/careers
5. Django REST Framework throttling: https://www.django-rest-framework.org/api-guide/throttling/
6. Django REST Framework testing: https://www.django-rest-framework.org/api-guide/testing/
7. Django REST Framework exceptions: https://www.django-rest-framework.org/api-guide/exceptions/
8. OWASP API Security Top 10 (2023): https://api-security.owasp.org/editions/2023/en/0x11-t10/
