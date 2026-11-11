
# BOLA - Broken Object Level Authorization

## Metadata

- Category: API Security
- OWASP: API1:2023
- CWE: CWE-639 (potential mapping)
- Severity: Context-dependent
- Status: Knowledge Base Entry
- Tags: BOLA, IDOR, API, Authorization, Access Control

## 1. Description

Broken Object Level Authorization occurs when an API
does not correctly verify whether the authenticated
user is authorized to access a requested object.

The vulnerability may allow users to access objects
belonging to other users or tenants.

## 2. Root Cause

Missing or insufficient authorization checks
at the object level.

## 3. Common Attack Surface

- GET /users/{id}
- GET /invoices/{id}
- GET /orders/{id}
- GET /documents/{id}
- PUT /profiles/{id}
- DELETE /resources/{id}

## 4. Discovery Methodology

1. Identify object identifiers.
2. Understand ownership relationships.
3. Identify two controlled test accounts.
4. Create test objects under each account.
5. Compare authorized and unauthorized access.
6. Test read and write operations where permitted.
7. Record HTTP evidence.
8. Evaluate the impact.

## 5. Evidence Requirements

- Account A and Account B ownership.
- Original request.
- Modified request.
- HTTP response.
- Proof that the object belongs to another account.
- Confirmation that access was unauthorized.

## 6. Important Distinctions

BOLA:
Authorization failure involving access to objects.

BFLA:
Authorization failure involving access to functions.

IDOR:
An insecure direct object reference is a common
implementation pattern associated with BOLA.

## 7. Potential Impact

- Unauthorized data disclosure.
- Unauthorized modification.
- Unauthorized deletion.
- Cross-tenant data exposure.
- Business impact depending on affected resources.

## 8. Remediation

- Enforce object-level authorization server-side.
- Validate ownership on every relevant operation.
- Apply tenant isolation.
- Avoid relying on unpredictable identifiers
  as an authorization mechanism.
- Add authorization regression tests.

## 9. Vulnerability Chaining

Potential combinations to investigate:

- BOLA + Sensitive Information Disclosure.
- BOLA + Mass Assignment.
- BOLA + Business Logic Abuse.
- BOLA + Broken Function Level Authorization.

Each combination requires independent validation.

## 10. References

- OWASP API Security Top 10 - API1:2023
- CWE-639
- CWE-862
- CWE-863

## 11. AI-OSF Classification

- Skill: API Security
- Related Skills: Authentication, Authorization
- Confidence: Educational reference
- Reusability: High
## Related Writeups

### Nextcloud Out-of-Office API — BOLA

- Platform: HackerOne
- Vulnerability: Broken Object Level Authorization
- OWASP: API1:2023
- CWE: CWE-639 (proposed)
- Verification: Author-reported, not independently verified

Detailed analysis:

[Nextcloud Out-of-Office API — BOLA](../../writeups/hackerone/nextcloud-out-of-office-bola.md)

### Reusable Security Patterns

- User-controlled object identifiers.
- Missing ownership validation.
- Cross-user access to private resources.
- Authorization inconsistencies across API endpoints.
