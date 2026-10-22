# Evidence Log — Cynbit Backend Audit

**Review date:** 22 October 2026  
**Purpose:** Separate publicly observed page content from live network observations and hypotheses.

> This file contains publicly accessible page-level observations from the cited pages. It does not claim that live API requests, response headers, status codes, server-side validation, or production security controls have been tested. Complete the browser-observation rows only after personally observing them in DevTools.

## Evidence register

| ID | Evidence type | Source | Observation | What it supports | What it does not prove |
|---|---|---|---|---|---|
| E-01 | Public page content | https://www.cynbit.in/contact | The page contains contact information and a “Common Inquiries” section about starting a project and custom AI automation. | Contact/inquiry is a relevant public workflow to investigate. | Does not prove a particular form endpoint, HTTP method, backend service, validation behaviour, or data storage. |
| E-02 | Public page content | https://www.cynbit.in/products | The page describes Cynbit Studio, TenantEase, and Revio and presents a “Schedule a Demo” workflow with product selection and fields including full name, work email, company name, and message. | Demo-request workflow is a relevant public workflow to investigate. | Does not prove how the form submits, whether it succeeds, the API payload, or production controls. |
| E-03 | Public page content | https://www.cynbit.in/careers | The page describes documentation-led culture, asynchronous communication, collaborative reviews, and iterative sprints. | Supports presenting findings in a clear, documented, prioritized format. | Does not prove an internal engineering process or assessment scoring rubric. |
| E-04 | Local test result reported by developer | Local Django project | Developer reported `python manage.py check` with no issues and 10 tests passing on 22 October 2026. | The local reference implementation's test suite was reported passing. | Does not test Cynbit's production system. Re-run before submission. |
| E-05 | To be collected by reviewer | Browser DevTools → Network, normal contact/demo interaction | Record date/time, page URL, request method, request destination, content type, status, timing, and redacted response. | Can establish the specific request/response behaviour actually observed. | A single observation does not establish the complete backend architecture or absence of vulnerabilities. |
| E-06 | To be collected by reviewer | Browser form validation | Record whether an ordinary missing required field is blocked client-side and what visible message appears. | Documents user-visible validation. | Client-side validation alone does not prove server-side validation. |
| E-07 | To be collected by reviewer | Browser DevTools → response headers | Record only headers actually returned by the observed response and identify the response URL/status. | Can support a narrow header/configuration observation. | One response does not prove headers are absent across all routes or deployment layers. |
| E-08 | To be collected by reviewer | Browser DevTools → Network waterfall | Record request timing, transferred bytes, cache status, and repeatability for one normal page load. | Establishes a limited baseline for that page load. | Does not establish load capacity or general performance under traffic. |

## Safe browser evidence collection

1. Open the public page in Chrome or Edge.
2. Open DevTools (`F12`) and select **Network**.
3. Enable **Preserve log** and reload the page.
4. Observe normal requests while browsing the page.
5. If submitting a form, use only synthetic data and a normal, intended interaction. Avoid repeated submissions.
6. Record the request URL, method, status, content type, and response structure if available.
7. Redact names, email addresses, phone numbers, tokens, cookies, and other personal or secret values from screenshots.
8. Do not enumerate hidden endpoints, attempt to access private records, send oversized/malicious payloads to production, or conduct load testing.

## Suggested screenshot names

- `E01-contact-page.png`
- `E02-product-demo-form.png`
- `E03-normal-request-redacted.png` — only if a request is actually observed
- `E04-validation-behaviour.png` — only if observed
- `E05-response-headers.png` — only if captured
- `E06-local-tests-passing.png`

Only include screenshots that you actually captured. Do not manufacture screenshots or request/response data.
