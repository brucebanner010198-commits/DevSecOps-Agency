# Security Gate — OWASP + STRIDE

The Security phase must cover both a STRIDE threat model and the OWASP Top 10. Every item gets a status: `NA` (not applicable, justify), `Mitigated` (describe control), or `Accepted` (only for Low-severity risks).

## STRIDE

| Category                   | Ask                                                          |
| -------------------------- | ------------------------------------------------------------ |
| **S**poofing               | How are identities authenticated? Can someone impersonate?   |
| **T**ampering              | Can data in transit / at rest be modified without detection? |
| **R**epudiation            | Is every sensitive action auditable to an identity?          |
| **I**nformation disclosure | What secrets exist? Can they leak via logs, errors, URLs?    |
| **D**enial of service      | What happens under load or malicious traffic?                |
| **E**levation of privilege | Can a user do something reserved for another role?           |

## OWASP Top 10 (2021)

| #   | Risk                                    | Default check                                                                          |
| --- | --------------------------------------- | -------------------------------------------------------------------------------------- |
| A01 | Broken Access Control                   | Every endpoint has an authz check. Default-deny.                                       |
| A02 | Cryptographic Failures                  | No plaintext secrets; TLS everywhere; passwords hashed with argon2/bcrypt.             |
| A03 | Injection                               | Parameterised queries; input validation; output encoding.                              |
| A04 | Insecure Design                         | Threat model exists; abuse cases considered; rate limits in place.                     |
| A05 | Security Misconfiguration               | Least-privilege defaults; no debug endpoints in prod; CSP/HSTS set.                    |
| A06 | Vulnerable / Outdated Components        | CI runs SCA (e.g., `npm audit`, `pip-audit`, Dependabot/Renovate configured).         |
| A07 | Identification & Authentication Failures| MFA option for privileged accounts; session expiry; bruteforce protection.             |
| A08 | Software & Data Integrity Failures      | CI signs artifacts; verify signatures on deploy; no unsafe deserialisation.            |
| A09 | Security Logging & Monitoring           | Auth events logged; alert on anomalies; logs shipped off-box.                          |
| A10 | Server-Side Request Forgery             | Allowlist outbound URLs; block link-local / metadata endpoints.                        |

## Severity scale

| Level     | Meaning                                                   | Action                          |
| --------- | --------------------------------------------------------- | ------------------------------- |
| Critical  | Exploitable remotely for full compromise of user data     | **Block pipeline until fixed**  |
| High      | Exploitable with significant impact, or scale multiplier  | Must mitigate before deploy     |
| Medium    | Exploitable under limited conditions                      | Mitigate or accept with ticket  |
| Low       | Theoretical or very low impact                            | Accept with note                |

## Threat-model template

```markdown
# Threat Model — <project>

## Scope
<assets, trust boundaries, data flows>

## STRIDE

| Category | Threat                       | Severity | Mitigation                         |
| -------- | ---------------------------- | -------- | ---------------------------------- |
| S        | Credential stuffing on login | High     | rate-limit + argon2 + MFA option   |
| T        | Tampering with invoice totals| Critical | HMAC signed payloads server-side   |
| ...      |                              |          |                                    |

## OWASP Top 10 coverage
<A01..A10 table with status + mitigation>

## Residual risks
<anything accepted, with rationale>
```
