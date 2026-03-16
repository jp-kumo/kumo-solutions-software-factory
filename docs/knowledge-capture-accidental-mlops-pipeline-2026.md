# Knowledge Capture: The "Accidental" MLOps Pipeline (2026)

## Source
- "How I Accidentally Built an MLOps Pipeline That Actually Works (And Uses Gen AI)"
- Author: Divy Yadav
- User-provided content (captured Mar 16, 2026)

---

## Why this matters for Jacques
This batch is a goldmine for **Portfolio Project #2 (Secure Health RAG)** and **Kumo Solutions** because it provides a "no-Kubernetes" AWS architecture for production AI. It demonstrates how to turn technical debt ("hero culture") into an automated system that provides direct business value to non-technical stakeholders (CFOs).

### Key Alignment Points:
1. **The "Translator" Pattern:** Using LLMs (Bedrock/Claude) to translate complex technical metrics into 30-second executive summaries. This is a high-value signal for Jacques’s "Boutique AI Consultancy" (Kumo).
2. **Event-Driven AI:** Using EventBridge and Step Functions to orchestrate workflows while the operator "sleeps." This fits Jacques's preference for nightly autonomous work.
3. **Low-Cost Production:** Proves that a production-grade MLOps system can run for ~$120/mo using serverless components.

---

## Core Synthesis & Architecture

### 1. The "ML Autopilot" Stack (No Kubernetes)
- **SageMaker Pipelines:** Visual backbone for data processing, training, and deployment.
- **AWS Lambda:** The "Glue" for triggering pipelines, checking S3 for new data, and sending notifications.
- **AWS Step Functions:** Orchestrates the flow ("Run pipeline → Check results → Update dashboard").
- **CloudWatch:** Early warning system for data drift and accuracy decay.
- **AWS Bedrock (Claude):** The "Translator" converting RMSE/p-values into business English.

### 2. The Logic Flow
- **Trigger:** EventBridge (Friday at 11 PM).
- **Validation:** Lambda checks for new S3 data.
- **Processing:** SageMaker handles cleaning, training (XGBoost), and evaluation.
- **Gate:** Deploy *only* if the new model improves performance by a defined threshold (e.g., 1%).
- **Reporting:** Bedrock generates a summary; Lambda pushes to Slack and QuickSight.

---

## Strategic Implementation for Jacques

### Portfolio Enhancement: "The Executive AI Summarizer"
**Context:** Recruiters and CFOs don't care about RMSE; they care about *accuracy gain* and *reliability*.
- **Action:** Integrate a **Bedrock Summary Node** into Project #1 (Mission Control) or Project #2 (Secure Health). After a task completes, generate a "Plain English Audit" for the dashboard.
- **Signal:** Shows you bridge the gap between "ML results" and "Business Impact."

### Kumo Solution: "The 4-Cent Executive Briefing"
**Offer:** Implement an automated summary layer for existing client AI pipelines. 
- **ROI:** Replaces 45-minute meetings with 15-second Slack updates. 
- **Cost:** ~$0.04/run.

---

## Suggested KB Tags
- mlops-serverless
- aws-sagemaker-pipelines
- aws-step-functions
- aws-bedrock-translator
- executive-reporting
- business-impact-ai
- automation-roi
- kumo
- portfolio-hiring
