# Arkansas AI Governance Checklist (2026)

**Purpose:** Practical compliance checklist for Kumo/Taste & Power AI-assisted content and automation workflows in Arkansas.

**Important:** This is an operational checklist, not legal advice. Final legal review should be done by Arkansas counsel before public launch.

---

## 1) Core operating principles (always-on)

- [ ] **Truthful representation:** Never imply a synthetic person is a real human if that could mislead users.
- [ ] **Clear disclosure:** Add clear, plain-language AI-use disclosures in content, landing pages, and offers where relevant.
- [ ] **No deceptive claims:** Avoid “undetectable,” “human-written guaranteed,” or unverifiable performance claims.
- [ ] **Data minimization:** Collect only what is needed for delivery.
- [ ] **Least privilege:** Restrict access to credentials, models, and stores.
- [ ] **Audit trail:** Keep durable records of major content/automation decisions and changes.

---

## 2) Arkansas-focused legal/control checks

## 2.1 Consumer protection / deceptive practices
- [ ] Review all marketing copy for misleading AI claims.
- [ ] Ensure testimonials/reviews are authentic and properly disclosed.
- [ ] Ensure paid/affiliate relationships are clearly disclosed.

## 2.2 Publicity rights (voice/likeness)
- [ ] Do not use a real person’s voice/likeness (or close replication) without explicit permission.
- [ ] Keep proof of consent/license for any likeness/voice assets.
- [ ] Add takedown process for rights complaints.

## 2.3 Data/privacy controls
- [ ] Publish clear privacy notice (what data, why, retention, sharing, contact).
- [ ] Obtain consent where required before collecting sensitive data.
- [ ] Support user requests to access/delete exported data where applicable.
- [ ] Keep retention windows defined and enforced.

## 2.4 High-risk AI governance (if applicable)
- [ ] Document intended use, risks, and mitigation controls.
- [ ] Perform impact assessment for systems affecting significant outcomes.
- [ ] Provide explanation/appeal paths where automated decisions are used.

---

## 3) Federal/Platform baseline checks (must align)

- [ ] FTC truth-in-advertising alignment for AI claims.
- [ ] FTC endorsement disclosure alignment (material connections clearly disclosed).
- [ ] Platform policy alignment for TikTok/YouTube on synthetic or manipulated media.
- [ ] Keep a moderation-response SOP for policy flags and takedowns.

---

## 4) Content publishing controls (Taste & Power + synthetic media)

- [ ] Add channel-level disclosure statement for AI-assisted production where needed.
- [ ] Keep metadata log per episode: script source, generation tools, edit pass owner, publish timestamp.
- [ ] Verify no prohibited impersonation/deceptive identity elements.
- [ ] Validate that sponsored/affiliate content is disclosed in description and on-page CTA.

---

## 5) Product/service controls (Kumo offers)

- [ ] Include compliance clause in proposal/SOW (no deceptive output, consent-required assets).
- [ ] Include client responsibility clause (rights to input data/assets).
- [ ] Include data handling clause (retention, deletion, access restrictions).
- [ ] Include incident response clause (notification process + rollback/takedown path).

---

## 6) Technical safeguards checklist

- [ ] Secrets in manager/vault, not in code or plaintext docs.
- [ ] Structured logging with token/PII redaction.
- [ ] Access controls by role; admin actions audited.
- [ ] Source and model version tracking for generated outputs.
- [ ] Backup + restore + deletion verification workflow.

---

## 7) Recordkeeping pack (for defensibility)

Maintain these artifacts in `docs/` and `memory/`:
- [ ] Model/tool inventory by workflow
- [ ] Disclosure templates used
- [ ] Consent/license evidence for likeness/voice/content
- [ ] Policy review snapshots (platform + legal)
- [ ] Incident/takedown log
- [ ] Monthly governance review notes

---

## 8) Governance cadence

- **Weekly:** Policy/claim review of new content and offer pages
- **Monthly:** Privacy/retention and access review
- **Quarterly:** Full legal/compliance review with counsel

---

## 9) “Stop” triggers (do not publish/deploy)

Stop and escalate if any of the following is true:
- [ ] synthetic media could be reasonably mistaken for a real person without disclosure
- [ ] consent/license proof is missing for voice/likeness use
- [ ] key claims are unsubstantiated or potentially deceptive
- [ ] data handling for sensitive user data is unclear
- [ ] platform policy conflict unresolved

---

## 10) Immediate next actions (this week)

1. Add disclosure blocks to Taste & Power and Kumo pages/scripts.
2. Add SOW compliance clause to all pilot templates.
3. Create a `docs/governance/` folder with evidence templates.
4. Schedule monthly governance review reminder.

---

## Suggested source validation list (for legal review)

Before external launch, verify latest text/effective dates with:
- Arkansas Attorney General website and press releases
- Arkansas legislative tracker / enrolled acts
- FTC AI and endorsements guidance pages
- Platform policy pages (TikTok, YouTube)

