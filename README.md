# Cynbit Backend Technical Audit

**Backend Developer Intern Assessment | October 2026**

An evidence-driven review of publicly observable website workflows, accompanied by a local Django REST Framework reference implementation demonstrating backend validation, API response contracts, request throttling, and automated testing.

> **Scope note:** This repository is an independent assessment project. The API implementation is a local reference design, not Cynbit's production backend. Recommendations and potential risks are distinguished from issues verified through direct observation.

## Table of Contents

- [Overview](#overview)
- [Objectives](#objectives)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Example Requests](#example-requests)
- [Testing](#testing)
- [Security Considerations](#security-considerations)
- [Audit Report and Evidence](#audit-report-and-evidence)
- [Limitations](#limitations)
- [References](#references)

## Overview

The project explores how backend engineers can improve the reliability, security, and maintainability of public inquiry and product-demo workflows.

The reference implementation provides two REST API endpoints using Django REST Framework. It demonstrates server-side input validation, controlled response fields, database persistence, scoped request throttling, and automated tests.

The accompanying technical audit documents the public application surface, investigation methodology, potential risks, evidence requirements, and recommended improvements.

## Objectives

- Examine publicly observable website and form behaviour.
- Identify backend engineering risks and improvement opportunities.
- Demonstrate explicit API contracts and server-side validation.
- Apply basic request-throttling controls.
- Verify expected behaviour with automated tests.
- Document findings and remediation priorities clearly.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Application framework and ORM |
| Django REST Framework | REST API endpoints, serializers, and testing |
| SQLite | Local development database |
| Git and GitHub | Version control and submission |

## Architecture

The local reference API follows this request flow:

```text
HTTP Client
    |
    v
Django URL Routing
    |
    v
API View
    |
    v
Scoped Request Throttling
    |
    v
Serializer Validation
    |
    v
Django ORM / Database
    |
    v
Serialized HTTP Response
```

This diagram represents the local implementation only. Cynbit's internal production architecture has not been established by this project.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/inquiries/` | Create an inquiry |
| POST | `/api/v1/demo-requests/` | Create a product-demo request |

### Inquiry API

Accepts:

- `name`: required, maximum 100 characters
- `email`: required, valid email address, maximum 254 characters
- `company`: optional, maximum 150 characters
- `industry`: optional, maximum 100 characters
- `message`: required, maximum 3,000 characters

### Product-Demo API

Accepts:

- `name`: required, maximum 100 characters
- `work_email`: required, valid email address, maximum 254 characters
- `company`: required, maximum 150 characters
- `product`: one of the configured product choices
- `message`: optional, maximum 2,000 characters

### Response Behaviour

| Status | Meaning |
|---|---|
| `201 Created` | Request accepted and record created |
| `400 Bad Request` | Invalid input or failed serializer validation |
| `429 Too Many Requests` | Request throttled when the configured limit is exceeded |

Unexpected infrastructure failures may produce other status codes. Production error handling should avoid exposing stack traces or sensitive internal details.

## Getting Started

### Prerequisites

- Python 3.10 or later, compatible with the installed dependencies
- pip
- Git (optional, for cloning the repository)

### 1. Clone the repository

Replace `YOUR_USERNAME` with the repository owner's GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/cynbit-backend-audit.git
cd cynbit-backend-audit
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked by the PowerShell execution policy, use an appropriate policy for your environment or activate the environment using another supported shell.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Apply database migrations

```powershell
python manage.py migrate
```

### 5. Run Django checks and automated tests

```powershell
python manage.py check
python manage.py test inquiries demo_requests
```

### 6. Start the development server

```powershell
python manage.py runserver
```

Open the following URLs in your browser:

- Inquiry API: http://127.0.0.1:8000/api/v1/inquiries/
- Product-demo API: http://127.0.0.1:8000/api/v1/demo-requests/

The Django REST Framework browsable API is available for interactive local testing.

## Example Requests

### Create an inquiry

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/inquiries/" -H "Content-Type: application/json" -d '{"name":"Test User","email":"test@example.com","company":"Example Ltd","industry":"Technology","message":"Testing the inquiry API"}'
```

### Create a product-demo request

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/demo-requests/" -H "Content-Type: application/json" -d '{"name":"Test User","work_email":"test@example.com","company":"Example Ltd","product":"cynbit_studio","message":"Requesting a product demo"}'
```

Use synthetic data only. Each successful request creates a record in the local development database.

## Testing

The local implementation currently has **10 automated tests passing**.

The tests cover:

- Successful inquiry creation
- Invalid email rejection
- Blank required-field rejection
- Successful product-demo request creation
- Invalid product rejection
- Blank company rejection
- Explicit response-field allowlists

Run the test suite using:

```powershell
python manage.py test inquiries demo_requests
```

The test results demonstrate the behaviour of this local implementation. They do not validate Cynbit's production systems.

## Security Considerations

The reference implementation demonstrates several basic backend controls:

- Server-side serializer validation
- Explicit field allowlists for API responses
- Maximum field lengths
- Scoped request throttling
- Automated tests for invalid inputs
- Avoidance of unnecessary personal information in model string representations

### Further production improvements

The following areas require additional design, testing, or deployment work:

1. Configure production-grade rate limiting and abuse detection.
2. Add request-size limits and monitoring.
3. Introduce structured logging with personal-data redaction.
4. Define data-retention and deletion policies.
5. Protect administrative data access with authentication and authorization.
6. Add tests for malformed JSON, throttling, database failures, and concurrent requests.
7. Use a production database and deployment-specific configuration.
8. Add notification delivery and idempotency if required by the actual workflow.

These recommendations should not be interpreted as proof that the corresponding weaknesses exist in Cynbit's production environment.

## Audit Report and Evidence

The detailed audit report is maintained separately to keep this README concise.

- **Technical audit:** [`docs/audit-report.md`](docs/audit-report.md)
- **Evidence log:** [`evidence/evidence-log.md`](evidence/evidence-log.md)
- **Remediation roadmap:** [`docs/remediation-roadmap.md`](docs/remediation-roadmap.md)

These links should point to files included in the repository. If any of the files have not yet been created, add them before submission or remove the corresponding links until they exist.

The audit distinguishes direct observations, potential risks, and areas that could not be verified through public access.

## Limitations

- This is a local reference implementation, not an integration with Cynbit's production backend.
- Production source code, database configuration, internal logs, and private infrastructure were not available for inspection.
- The local application uses Django's development configuration and SQLite unless otherwise configured.
- The implementation does not include production email delivery, CAPTCHA, a complete administrative workflow, or a deployment-ready abuse-prevention system.
- Live-site conclusions must be supported by recorded evidence rather than assumptions.

## References

- [Cynbit Official Website](https://www.cynbit.in/)
- [Cynbit Contact Page](https://www.cynbit.in/contact)
- [Cynbit Careers Page](https://cynbitwebsite.vercel.app/careers)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Django REST Framework Throttling](https://www.django-rest-framework.org/api-guide/throttling/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

---

**Assessment deliverable:** Backend Technical Audit and Local Reference API  
**Last verified locally:** 22 October 2026  
**Test status:** 10 tests passed
