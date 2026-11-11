
# Nextcloud Out-of-Office API — BOLA

## 1. Metadata

- Platform: HackerOne
- Target: Nextcloud
- Category: API Security
- Vulnerability: Broken Object Level Authorization (BOLA)
- Related vulnerability: IDOR
- OWASP: API1:2023
- CWE: CWE-639 (proposed mapping)
- Affected version: 32.0.0.13 (author-reported)
- Severity: Medium (as reported)
- Verification: Author-reported, not independently verified
- Research status: Analyzed

## 2. Executive Summary

The report describes a BOLA vulnerability in the Nextcloud
Out-of-Office API.

An authenticated user can reportedly retrieve another
user's out-of-office information by manipulating the
userId path parameter.

The affected functionality exposes personal absence
information without validating object ownership.

## 3. Affected Endpoints

GET /ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}

GET /ocs/v2.php/apps/dav/api/v1/outOfOffice/{userId}/now

## 4. Root Cause

According to the report, the controller retrieves absence
information using the userId supplied in the request.

The GET methods reportedly do not verify whether the
authenticated user owns the requested resource.

The report identifies the following implementation details:

- NoAdminRequired route attributes.
- Missing object ownership validation.
- Direct use of the userId path parameter.
- Absence service access without the required ownership check.

## 5. Authentication and Authorization Context

The reported test environment contains two controlled accounts:

- Bob: authenticated requesting user.
- Alice: owner of the absence information.

Bob uses his own authentication token while requesting
Alice's resource.

The expected authorization behavior is to deny access
to another user's private absence information.

## 6. Discovery Methodology

According to the report:

1. Deploy a Nextcloud test instance.
2. Create two controlled user accounts.
3. Configure out-of-office information for one account.
4. Authenticate as the second account.
5. Request the first account's resource.
6. Compare the HTTP response with the expected authorization behavior.
7. Repeat the analysis against the real-time status endpoint.

## 7. Evidence

The report describes the following behavior:

- Authenticated request using Bob's identity.
- Path parameter referencing Alice.
- HTTP 200 response.
- Response containing Alice's absence information.

Expected behavior:
HTTP 403 Forbidden.

Reported behavior:
HTTP 200 OK.

Sensitive example credentials, personal data and tokens
have intentionally been excluded from this knowledge entry.

## 8. Exposed Information

The report identifies these potentially exposed fields:

- Absence start date.
- Absence end date.
- Absence status.
- Personal absence message.
- Replacement user identifier.
- Replacement user display name.
- Current absence status.

## 9. Impact Analysis

Primary impact: Confidentiality.

Potential consequences:

- Unauthorized disclosure of personal information.
- Exposure of employee absence schedules.
- Disclosure of travel or contact information.
- Social engineering opportunities.
- Organizational intelligence gathering.

Integrity:
No modification demonstrated through the reported GET vulnerability.

Availability:
No availability impact demonstrated.

## 10. Vulnerability Classification

Primary classification:
OWASP API1:2023 — Broken Object Level Authorization.

Proposed CWE mapping:
- CWE-639: Authorization Bypass Through User-Controlled Key.
- CWE-862: Missing Authorization.
- CWE-863: Incorrect Authorization.

The CWE mappings are proposed classifications and should
be validated against the final implementation details.

## 11. Vulnerability Chaining Opportunities

Potential relationships to investigate:

- BOLA + Sensitive Information Disclosure.
- BOLA + Business Logic Abuse.
- BOLA + Social Engineering.

These are potential scenarios, not independently
confirmed vulnerability chains.

## 12. Remediation

- Enforce server-side object-level authorization.
- Retrieve the authenticated user identity from the session.
- Verify ownership before returning absence information.
- Apply consistent authorization checks to both GET endpoints.
- Add regression tests for cross-user access.
- Return HTTP 403 when access is unauthorized.

## 13. AI-OSF Intelligence

### Detection Patterns

- User-controlled identifiers in API paths.
- Endpoints returning user-specific resources.
- Missing ownership validation.
- Authenticated requests accessing another user's objects.
- Similar functionality exposed through multiple endpoints.

### Related Skills

- API Security.
- Authentication.
- Authorization.
- BOLA / IDOR.

### Reusability

High.

### Confidence

Medium as a research reference.
Not independently reproduced by AI-OSF.

## 14. References

- HackerOne report: Nextcloud Out-of-Office API BOLA.
- OWASP API Security Top 10 — API1:2023.
- CWE-639.
- CWE-862.
- CWE-863.

## 15. Research Notes

This entry is based on the supplied report content.

The reported vulnerability and technical evidence have
not yet been independently reproduced.

Claims involving mass enumeration, regulatory consequences
and real-world attack scenarios require separate validation.
