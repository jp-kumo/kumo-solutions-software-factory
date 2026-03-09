# Portfolio One-Pager — Production RAG Support Assistant (Regulated Domain)

## Employer Problem
Organizations in regulated or high-risk workflows (healthcare, finance, compliance-heavy support) need AI assistants, but cannot tolerate fabricated answers, missing citations, or insecure retrieval behavior.

## Solution Built
Designed and implemented a production-oriented Retrieval-Augmented Generation (RAG) assistant with:
- source-grounded responses
- retrieval quality evaluation harness
- hallucination and confidence guardrails
- prompt-injection defense checks
- observability for answer quality, latency, and token cost

## Architecture (High Level)
- **Ingestion layer:** document normalization, chunking, metadata enrichment
- **Retrieval layer:** vector search + optional reranking
- **Generation layer:** constrained prompting + citation enforcement
- **Safety layer:** input/output policy checks + injection pattern detection
- **Evaluation layer:** offline golden-set evals + online quality telemetry
- **Ops layer:** CI/CD + infra as code + monitoring

## Tech Stack
- Python, FastAPI
- Vector store (FAISS/pgvector-compatible design)
- LLM API integration
- AWS deployment pattern (container/serverless options)
- Terraform for reproducible infrastructure
- GitHub Actions (or equivalent) for CI

## Measurable Impact (Portfolio Targets)
- Retrieval hit rate on golden queries: **>= 85%**
- Citation coverage for factual answers: **>= 95%**
- Hallucination incident rate: **decreasing trend week-over-week**
- P95 response latency: **tracked and optimized**
- Cost per 100 responses: **tracked with budget guardrails**

## What This Proves to Hiring Managers
- Can build beyond demos into reliable AI systems.
- Understands quality, safety, and governance requirements.
- Can operationalize ML/AI workflows with measurable service metrics.

## Resume Bullet Drafts
- Built a production-focused RAG assistant with citation enforcement, guardrails, and evaluation harness, improving answer reliability in a regulated-domain use case.
- Implemented retrieval/response observability (quality, latency, cost), enabling data-driven iteration and risk-controlled deployment.
- Added prompt-injection and policy checks plus infra-as-code deployment patterns to support secure, repeatable AI delivery.

## STAR Interview Story (Short)
- **S:** Team needed AI support capability but lacked trust due to hallucination risk.
- **T:** Deliver a reliable assistant with auditable quality and safety controls.
- **A:** Implemented RAG pipeline with eval harness, citation policy, and monitoring dashboards; added injection-defense checks and CI quality gates.
- **R:** Produced a measurable reliability baseline and trendable quality metrics, turning a risky prototype into a production-ready pattern.

## Next Iteration
- Add active-learning loop from user feedback.
- Add domain-specific compliance policy packs.
- Expand eval set with adversarial and long-tail scenarios.
