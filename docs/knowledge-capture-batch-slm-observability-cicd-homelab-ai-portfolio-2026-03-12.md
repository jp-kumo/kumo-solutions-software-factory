# Knowledge Capture Batch: SLM Build, Observability Stack, Kubernetes CI/CD, Homelab Strategy, and AI Portfolio Projects

## Sources
1. Build a Small Language Model (SLM) from scratch
   - https://youtu.be/JuXlq-WNRBY?si=PWYwpHPuPYvy_Mqp
2. Loki + Prometheus + Grafana + Docker monitoring/logging
   - https://youtu.be/IdWD-lHTurY?si=tV5EJ_zsJ7W22BJi
3. 5 AI Engineer Projects to build in 2026
   - https://youtu.be/9WIsvEswZTk?si=RHgs9CAGhJSTL0Pi
4. 5 AI Projects that give unfair advantage
   - https://youtu.be/p54vr-NyxDc?si=i2yNhYk9Qh1x31uh
5. Kubernetes CI/CD with Jenkins + GitOps + ArgoCD
   - https://youtu.be/o4QG_kqYvHk?si=gWw9ggjrle7tvZ9A
6. Secure AWS EKS CI/CD with ArgoCD + GitHub Actions (OIDC/Pod Identity)
   - https://youtu.be/KOE_6QYQqA4?si=iIsengI9hKtGL73g
7. Kubernetes CI/CD pipeline (ArgoCD + GitHub Actions)
   - https://youtu.be/GlhK7mz5IJo?si=GWzmFcRDuZesolm9
8. Google Cloud Live multimodal agents workshop (duplicate source in prior batch)
   - https://www.youtube.com/live/wiZkPAReXmI?si=zIgbmGV7FNfNTlMP
9. Kubernetes homelab strategy for career leverage
   - https://youtu.be/S7sJA51CxIo?si=lid5gw0DAVt2ICpp
10. OnSpace full-stack app tutorial (duplicate source in prior batch)
   - https://youtu.be/AqUpzZRZAyA?si=upud5CRnCE6JzUdG

---

## Distilled insights

### A) SLM-from-scratch is a strong “systems understanding” signal
- End-to-end SLM pipeline skills:
  - dataset choice and tokenization,
  - efficient storage/memory mapping,
  - batching and training loops,
  - transformer internals (attention/FFN/residuals),
  - inference and sampling controls.
- Portfolio value is highest when paired with:
  - benchmark comparisons,
  - explicit trade-offs (size/speed/quality),
  - reproducible training/eval scripts.

### B) Observability stack should combine metrics + logs for root-cause speed
- Core pattern:
  - metrics (Prometheus) detect anomalies,
  - logs (Loki) explain causality,
  - Grafana unifies both views.
- Practical production lesson:
  - low-cardinality labels and efficient indexing strategy matter,
  - dashboard filters/variables accelerate triage,
  - this is a high-value differentiator versus “model-only demos.”

### C) Kubernetes CI/CD maturity is now about secure GitOps, not just deployment
- Strong convergent pattern across multiple sources:
  - CI builds + tags immutable images,
  - image pushed to registry (ECR/GHCR/Docker Hub),
  - GitOps repo updated automatically,
  - ArgoCD detects drift and rolls out safely.
- Security upgrades that matter:
  - OIDC federation (no long-lived cloud credentials in CI),
  - IAM trust narrowing by repo/org scope,
  - pod identity for runtime-to-cloud auth.

### D) Homelab can be a legitimate career accelerant when treated as production
- Key signal is not “running Kubernetes” but operating it with discipline:
  - GitOps pipelines,
  - stateful workloads + backup strategy,
  - monitoring/alerting and incident response basics,
  - repeatable infra-as-code.
- Hiring relevance increases when projects show reliability and operational depth.

### E) Portfolio strategy that wins in 2026 is “production realism + evaluation”
- Repeated recommendation set from portfolio-focused sources:
  - production RAG with eval and CI gating,
  - local model benchmarking and trade-off reporting,
  - monitoring/observability for AI systems,
  - finetuning with measured deltas,
  - realtime multimodal systems with latency budgets.
- Critical pattern: move beyond tutorial parity and add measurable quality/cost/latency controls.

---

## Project idea leverage for Kumo Solutions and Coding Factory

### 1) Project #1 Mission Control upgrades (immediate)
- Add an **AI Observability module**:
  - prompt/tool trace logs,
  - quality drift dashboards,
  - incident timeline views (metrics + logs).
- Add **GitOps security checklist gates**:
  - OIDC auth required for CI,
  - no static cloud secrets in repos,
  - image immutability and rollout policy checks.

### 2) New portfolio slices aligned to hiring + consulting demand
- **Slice A:** Production RAG with automated eval regression gate
- **Slice B:** Agent observability stack (Loki/Prometheus/Grafana + trace mapping)
- **Slice C:** Secure EKS GitOps pipeline with OIDC + ArgoCD image updater
- **Slice D:** Realtime multimodal mini-system (voice/video + tool invocation)
- **Slice E:** Local SLM benchmark report (quality-speed-cost comparison)

### 3) Kumo offer packaging opportunities
- **AI Reliability & Observability Accelerator**
- **Secure GitOps for AI Workloads (EKS/K8s)**
- **RAG Readiness with Evaluation Governance**
- **Platform Engineering for High-Trust AI Ops**

---

## Guardrails and implementation cautions
- Keep architecture complexity proportional to need (avoid over-agenting).
- Add strict rollout controls and rollback plans for CD pipelines.
- Protect noisy observability costs via label discipline and log retention policy.
- Enforce separation of concerns across CI credentials, runtime identities, and deployment rights.
- Treat generated code/app-builder output as starting point; enforce review, tests, and policy checks before production.

---

## Bottom line
This batch strongly supports a practical strategy:
- build fewer but deeper production-grade assets,
- instrument everything (quality, latency, cost, reliability),
- and position Kumo as the team that can ship AI systems safely and repeatedly in real operating environments.
