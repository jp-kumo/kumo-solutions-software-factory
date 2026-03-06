# Gate 04 — Security Intake Review

Project: Kumo Solutions Mission Control v1  
Date: 2026-03-03  
Reviewer Role: Security / Compliance Agent  
Decision Type: Security intake (pre-coding)

## 1) Scope and context

### In-scope v1 surfaces
- Internal Appsmith operational UI (owner/chief-of-staff usage)
- PostgreSQL data layer (system of record)
- Metabase read/reporting access
- Containerized single-host deployment (homelab/VPS class)
- Internal network exposure through optional reverse proxy

### Out-of-scope (v1)
- External/public customer access
- Mobile app clients
- Production SSO federation (future extension)
- Public API productization (internal API is future extension)

## 2) OWASP Top 10:2025 applicability review

Note: OWASP Web Top 10 canonical list version may lag calendar year naming; this intake uses current OWASP Top 10 categories as control families and maps applicability to Mission Control v1.

| OWASP Category | Applicability to v1 | Why it matters here | Initial intake status |
|---|---|---|---|
| Broken Access Control | High | Internal role boundaries (owner/chief-of-staff/agents), admin pages, record edits | **Open risk** |
| Cryptographic Failures | Medium | Secrets at rest/in transit, DB credentials, backup encryption | **Open risk** |
| Injection | High | SQL queries, Appsmith bindings, dashboard filters/parameters | **Open risk** |
| Insecure Design | High | Internal-first design can drift into internet exposure without controls | **Open risk** |
| Security Misconfiguration | High | Containers, reverse proxy, default creds, permissive network/db settings | **Open risk** |
| Vulnerable/Outdated Components | Medium | Appsmith/Metabase/Postgres container images and plugins | **Open risk** |
| Identification & Authentication Failures | Medium | Weak auth model if relying on defaults/shared accounts | **Open risk** |
| Software & Data Integrity Failures | Medium | Unpinned images, unsigned updates, backup/restore integrity | **Open risk** |
| Security Logging & Monitoring Failures | Medium | Need auditable status/decision changes per product requirements | **Open risk** |
| SSRF | Low-Medium | Possible via connectors/plugins or metadata fetch features | **Watchlist risk** |

## 3) ASVS mapping scope (web/backend)

ASVS target profile for v1: **ASVS Level 1 baseline**, with selected Level 2 controls for auth/session/data protection where practical.

### Web/UI scope (Appsmith-facing)
- V1 Architecture, design, and threat modeling (minimum lightweight threat model)
- V2 Authentication
- V3 Session management
- V4 Access control
- V5 Validation, sanitization, and encoding
- V7 Error handling and logging
- V8 Data protection
- V9 Communications
- V14 Configuration

### Backend/data scope (PostgreSQL + platform wiring)
- V5 Validation and parameterization at data query boundaries
- V6 Stored cryptography (secrets, key handling expectations)
- V8 Data protection (sensitive fields, backups, retention)
- V9 Transport layer security for all admin access
- V10 Malicious code/dependency risk hygiene for images/components
- V12 File/resource controls (if attachments added later)
- V13 API/web service controls (for future internal API)
- V14 Configuration and hardening (DB/network/container baselines)

### Explicit exclusions for this gate
- Payment/security controls irrelevant to this internal tool
- Advanced anti-automation controls (public bot threat not primary in v1)

## 4) OWASP API Top 10 applicability

Current v1 has **no formal external API product surface**, but API risks are still partially applicable because:
- Appsmith and Metabase rely on service interfaces and query endpoints
- Future internal API is planned extension

Applicability decision:
- **Apply API Top 10 as “preventive design checklist” now** (especially authorization, excessive data exposure, injection, and asset management)
- **Full API Top 10 gate required at first internal API implementation milestone**

Priority API risk themes to preempt now:
1. API1 Broken Object Level Authorization
2. API3 Broken Object Property Level Authorization / excessive data exposure
3. API8 Security Misconfiguration
4. API10 Unsafe consumption of upstream components/services

## 5) OWASP MASVS applicability decision

- Mobile client is **not in v1 scope**.
- MASVS applicability: **Not required for current release gate**.
- Trigger condition: If native/hybrid mobile client is introduced, open a MASVS L1 intake before mobile code reaches staging.

## 6) Security risk register (initial)

| Risk ID | Risk | Likelihood | Impact | Initial Rating | Required mitigation before GO | Owner |
|---|---|---:|---:|---|---|---|
| SEC-01 | Excessive or broken access control across internal roles | Medium | High | High | Define role matrix; enforce least privilege in Appsmith + DB grants; verify unauthorized edit/read tests | Main Orchestrator + Security |
| SEC-02 | SQL/data injection through dynamic bindings/queries | Medium | High | High | Parameterized queries only; disallow raw concatenation; input validation patterns; negative test cases | API/Data Agent + QA |
| SEC-03 | Security misconfiguration (default creds, open ports, weak network boundaries) | High | High | Critical | Harden container/network defaults; rotate all defaults; private network segmentation; TLS on admin ingress | Platform Agent |
| SEC-04 | Missing/weak authentication/session controls | Medium | High | High | Strong auth settings; no shared admin account for normal ops; session timeout policy; credential hygiene | Platform + Owner |
| SEC-05 | Insufficient logging/auditability of critical changes | Medium | Medium | Medium | Audit logs for project status/security/release decisions; immutable log retention window | Web + Data |
| SEC-06 | Vulnerable/outdated container components | Medium | Medium | Medium | Pin image versions; update cadence; vulnerability scan in release checklist | Platform |
| SEC-07 | Unencrypted or untested backups exposing operational data | Medium | Medium | Medium | Encrypt backups at rest; secure backup destination; quarterly restore test | Platform |
| SEC-08 | Overexposed Metabase/Appsmith endpoints to internet | Medium | High | High | Restrict ingress by IP/VPN/private network; disable unnecessary public sharing features | Platform |

## 7) Gate recommendation

### Default security gate posture
- **NO-GO / BLOCK** by default until high/critical intake risks have explicit mitigation evidence.

### Conditional release path
Gate can move to **GO (with conditions)** only when all are true:
1. Access control matrix documented and enforced in UI + DB permissions.
2. Query/input handling standard established (parameterization and tests).
3. Deployment hardening checklist completed (auth, secrets, network, TLS, defaults removed).
4. Audit logging for critical fields/actions implemented.
5. Backup encryption + restore test evidence recorded.

### Risk acceptance policy note
- Any **material residual risk** (High/Critical) requires **explicit owner-only written risk acceptance**.
- Without owner acceptance, security recommendation remains **BLOCK**.

## 8) Intake outcome summary (decision-ready)

### Current disposition
- Gate 04 status: **BLOCK** (security-by-design enforcement active)
- Reason: required mitigation evidence is not yet attached for all High/Critical risks
- Earliest security unblock path: complete the exit checklist below

### Exit checklist required for Gate 04 GO
1. **Access control matrix evidence attached**
   - UI role matrix and DB grants documented
   - Negative authorization tests captured
2. **Injection/data handling evidence attached**
   - Parameterized query standard documented
   - QA negative tests for injection vectors attached
3. **Deployment hardening evidence attached**
   - Default credentials rotated
   - Secrets handling verified
   - Network exposure restricted
   - TLS/reverse proxy controls documented
4. **Audit logging evidence attached**
   - Critical status/security/release changes are logged
   - Retention policy documented
5. **Backup security evidence attached**
   - Backup encryption confirmed
   - Restore test completed and recorded

### Decision rules
- If all checklist items are evidenced: **GO**
- If some items remain but risk is low/non-material: **CONDITIONAL GO** (with due dates/owners)
- If unresolved High/Critical risk remains: **NO-GO/BLOCK** unless owner explicitly accepts material residual risk in writing

### Owner decision note
Any material business/security risk acceptance is **owner-only** and must be explicit in writing.