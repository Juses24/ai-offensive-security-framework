---
schema_version: "1.0"

id: "hackerone-nextcloud-001"
title: "Nextcloud Out-of-Office API BOLA"

source:
  platform: "hackerone"
  author: null
  url: "https://hackerone.com/reports/3382343"
  report_id: "3382343"
  published_at: null

target:
  name: "Nextcloud"
  application_type: "Collaboration platform"
  technology_stack: []
  affected_versions:
    - "32.0.0.13"
  affected_endpoints:
    - method: "GET"
      path: "/ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}"
    - method: "GET"
      path: "/ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}/now"

classification:
  category: "api_security"
  vulnerability:
    - "BOLA"
    - "IDOR"
  owasp:
    - "API1:2023"
  cwe:
    - "CWE-639"
    - "CWE-862"
    - "CWE-863"
  cve: []

severity:
  value: "medium"
  cvss: null
  source: "author_reported"

verification:
  status: "author_reported"
  independently_reproduced: false

confidence: "medium"

intelligence:
  attack_surface:
    - "REST API"
    - "User-specific resources"
  techniques:
    - "Object identifier manipulation"
    - "Cross-user authorization testing"
  detection_patterns:
    - "User-controlled identifiers in API paths"
    - "Missing object ownership validation"
    - "Cross-user access to private resources"
    - "Authorization inconsistencies across endpoints"
  related_vulnerabilities:
    - "Sensitive Information Disclosure"
  potential_chains:
    - "BOLA + Business Logic Abuse"
    - "BOLA + Social Engineering"

tags:
  - "bola"
  - "idor"
  - "api-security"
  - "nextcloud"
  - "hackerone"

related_skills:
  - "API Security"
  - "Authentication"
  - "Authorization"

research:
  status: "analyzed"
  created_at: "2026-11-11"
  updated_at: "2026-11-11"
---

# Executive Summary

The report describes a BOLA vulnerability in the Nextcloud
Out-of-Office API.

An authenticated user can reportedly retrieve another
user's out-of-office information by manipulating the
userId path parameter.

The affected functionality exposes personal absence
information without validating object ownership.

# Target Context

- Application: Nextcloud.
- Application type: Collaboration platform.
- Affected version: 32.0.0.13 (author-reported).
- Authentication required: Yes.
- Attack surface: Out-of-Office REST API.
- Scope: Two controlled accounts in the reported test environment.

# Affected Endpoints

**Endpoint 1**

```http
GET /ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}
```

**Endpoint 2**

```http
GET /ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}/now
```

Both endpoints reportedly expose user-specific absence information.

# Vulnerability Details

- Vulnerability: Broken Object Level Authorization (BOLA).
- Related classification: IDOR.
- Root cause: Missing object ownership validation.
- Affected component: Out-of-Office API controller.
- Preconditions: Authenticated user and a target user identifier.
- Security boundary violated: Cross-user resource authorization.

According to the report, the GET methods retrieve information
using the userId supplied in the request without verifying
whether the authenticated user is authorized to access it.

The report identifies `NoAdminRequired` route attributes.
These attributes permit access without administrator privileges;
their presence alone does not establish the vulnerability.

# Discovery Methodology

According to the report:

1. Deploy a Nextcloud test instance.
2. Create two controlled user accounts.
3. Configure out-of-office information for one account.
4. Authenticate as the second account.
5. Request the first account's resource.
6. Compare the HTTP response with the expected authorization behavior.
7. Repeat the analysis against the real-time status endpoint.

# Technical Evidence

The report describes the following behavior:

- Bob authenticates using his own account.
- The request references Alice through the userId path parameter.
- The server reportedly returns HTTP 200 OK.
- The response contains Alice's absence information.

Expected behavior:

```http
HTTP/1.1 403 Forbidden
```

Reported behavior:

```http
HTTP/1.1 200 OK
```

The evidence is author-reported and has not been independently reproduced by AI-OSF.

Sensitive example credentials, personal data and tokens have
intentionally been excluded from this knowledge entry.

# Exploitation Analysis

- Exploitation condition: Authenticated access to the affected API.
- Technique: Manipulation of a user-controlled object identifier.
- Reproducibility: Described by the original report.
- Limitation: No independent reproduction performed by AI-OSF.

The report also describes enumeration of user identifiers.
The associated script and its complete evidence were not supplied.

# Impact Analysis

**Confidentiality:** Potential unauthorized disclosure of personal absence information.

**Integrity:** No modification demonstrated through the reported GET vulnerability.

**Availability:** No availability impact demonstrated.

Potential consequences include:

- Disclosure of employee absence schedules.
- Exposure of personal messages and replacement contacts.
- Social engineering opportunities.
- Organizational intelligence gathering.

# Vulnerability Chaining

Potential relationships to investigate:

- BOLA + Sensitive Information Disclosure.
- BOLA + Business Logic Abuse.
- BOLA + Social Engineering.

These are hypotheses, not independently confirmed vulnerability chains.

# Lessons Learned

- Authentication does not imply authorization.
- User-controlled identifiers require server-side ownership checks.
- Related API endpoints should enforce consistent authorization.
- Test cross-user access using separate controlled accounts.

# Detection Patterns

- User-controlled identifiers in API paths.
- Endpoints returning user-specific resources.
- Missing ownership validation.
- Authenticated requests accessing another user's objects.
- Similar functionality exposed through multiple endpoints.

# Remediation

- Enforce server-side object-level authorization.
- Retrieve the authenticated user identity from the session.
- Verify ownership before returning absence information.
- Apply consistent authorization checks to both GET endpoints.
- Add regression tests for cross-user access.
- Return HTTP 403 when access is unauthorized.

# References

- Original report: https://hackerone.com/reports/3382343
- OWASP API Security Top 10 — API1:2023.
- CWE-639.
- CWE-862.
- CWE-863.

# Research Notes

This entry is based on the report content supplied to AI-OSF.

The affected version, severity and technical behavior are author-reported.

The CWE mappings are proposed classifications and require validation.

Claims involving mass enumeration, regulatory consequences and
real-world attack scenarios require separate validation.
