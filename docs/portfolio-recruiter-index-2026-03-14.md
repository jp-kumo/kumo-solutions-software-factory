# Jacques Payne — Cloud & AI Engineering Portfolio
*Hiring-ready projects demonstrating production-grade reliability, governance, and operational excellence.*

---

## 1. Agent Reliability Control Plane (MACP)
**Problem:** AI agents are prone to failure, cost spikes, and hallucinations when running long-horizon, multi-step tasks.
**Solution:** A custom control plane built with **LangGraph** that wraps agent workflows in production-grade guardrails including model routing by task complexity, Pydantic validation gates, and confidence-based human-in-the-loop (HITL) escalation.
**Signal:** Proves the ability to move beyond "demos" to stable, auditable AI systems.
**Stack:** Python, LangGraph, FastAPI, Pydantic, Langfuse (Observability), Postgres.

## 2. Regulated Document Intelligence Pipeline
**Problem:** Document extraction in high-trust industries (e.g., Legal, Healthcare) fails due to poor OCR quality and lack of citation lineage.
**Solution:** A governed extraction engine that benchmarks multiple parsers (e.g., **Docling**, LlamaIndex), assigns uncertainty scores to outputs, and enforces mandatory citation grounding for every generated fact.
**Signal:** Demonstrates precision and risk-management discipline essential for regulated enterprise environments.
**Stack:** Python, IBM Docling, ADK, SQLite, Pydantic (Schema enforcement).

## 3. OpenClaw Runtime Governance & FinOps
**Problem:** Autonomous AI usage often leads to runaway API costs and rate-limit interruptions.
**Solution:** Implementation of a global governance policy that offloads low-value "heartbeat" checks to local models (**Ollama/Llama 3.2**), leverages prompt caching (reducing costs by up to 90%), and implements context pruning to maintain high performance under budget constraints.
**Signal:** Highlights competence in AI infrastructure and cost-effective operations (FinOps).
**Stack:** OpenClaw, Ollama, Bash/Python (Audit scripts), Linux/Docker.

## 4. Multi-Stream Business Automation Engine
**Problem:** SME founders are bottlenecks for repetitive operational tasks (lead gen, follow-up, billing).
**Solution:** A suite of linked **n8n** workflows that autonomously identifies leads, executes personalized follow-up cadences, and handles Stripe invoicing, escalating only high-value exceptions to the owner.
**Signal:** Shows a "Builder-Operator" mindset—converting technical automation into direct business ROI.
**Stack:** n8n, CRM APIs, OpenAI/Claude APIs, Stripe, Slack.

---
**Contact:** Jacques Payne | [jacquespayne.9914@gmail.com](mailto:jacquespayne.9914@gmail.com) | Little Rock, AR
