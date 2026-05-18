---
doc_id: "5.33"
title: "security incident response"
section: "Procedures"
summary: "Respond to security incidents: assessment, containment, eradication, recovery, lessons learned."
status: "accepted"
updated: "2026-05-17"
---

# 5.33 — Security Incident Response

**Purpose:** Respond to security incidents with structured assessment, containment, and remediation.

**When to use:**
- Suspected data breach
- Unauthorized access detected
- Malware/intrusion suspected
- Vulnerability exploited
- Credential compromise

**Severity levels:**
- **Critical:** Active exploit, data exfiltration, system compromise
- **High:** Vulnerability exploited, limited scope
- **Medium:** Suspicious activity, unconfirmed breach
- **Low:** Policy violation, potential weakness

---

## Prerequisites

- [ ] Incident response team identified
- [ ] Communication channels ready
- [ ] Forensic tools available
- [ ] Escalation path defined

---

## Steps

### 1. Detect and assess

Identify:
- What happened
- When it started
- Scope (systems, data, users)
- Attack vector (if known)

Document in incident tracker:
```markdown
**Incident ID:** SEC-YYYY-MM-DD-###
**Detected:** {timestamp}
**Reporter:** {name}
**Initial scope:** {description}
**Severity:** {Critical/High/Medium/Low}
```

### 2. Contain

**Immediate (minutes):**
- Isolate affected systems
- Revoke compromised credentials
- Block malicious IPs
- Enable kill switches

**Short-term (hours):**
- Snapshot evidence
- Patch exploited vulnerability
- Rotate exposed secrets

### 3. Eradicate

Remove threat:
- Delete malicious code/files
- Close attack vectors
- Verify no persistence

### 4. Recover

Restore service:
- Validate systems clean
- Restore from clean backups (if needed)
- Monitor for re-infection

### 5. Communicate

**Internal:**
- Notify stakeholders
- Update status page
- Brief executives (if critical)

**External (if required):**
- Regulatory notifications
- Customer notifications
- Public disclosure (if needed)

### 6. Document

Create post-incident report:
```markdown
## Security Incident Report

**ID:** SEC-YYYY-###
**Timeline:** {start to resolution}
**Root cause:** {analysis}
**Impact:** {data/systems/users}
**Response:** {actions taken}
**Lessons:** {what to improve}
```

### 7. Lessons learned

Within 1 week:
- What worked
- What didn't
- Process improvements
- Technical fixes

Update:
- Security rules
- Monitoring/alerts
- Response procedures

---

## Validation

- [ ] Incident contained
- [ ] Threat eradicated
- [ ] Systems recovered
- [ ] Evidence preserved
- [ ] Communications sent
- [ ] Report completed
- [ ] Lessons incorporated

---

## Common Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Scope unclear | Limited logging | Assume worst, investigate |
| Can't contain | Missing isolation | Emergency network segment |
| Evidence lost | Delayed response | Document gaps, improve |

---

## See Also

- Security overview: `docs/security/README.md`
- Incident response plan: `docs/security/incident-response.md`
- Runbooks: `docs/runbooks/`
