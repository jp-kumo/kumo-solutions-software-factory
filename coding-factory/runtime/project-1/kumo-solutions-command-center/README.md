# Kumo Solutions Command Center (Project 1)
*Autonomous Agent Reliability & Portfolio Management Infrastructure*

## Overview
This is the central execution environment for Jacques Payne's professional portfolio projects and Kumo Solutions' delivery operations. It serves two purposes:
1. **Showcase:** Concrete proof of agent reliability engineering (Project 1 in portfolio).
2. **Operations:** Managing the lifecycle of multiple portfolio projects and Kumo client delivery.

## Core Features
- **Reliability Control Plane:** Orchestrated with LangGraph to wrap agent tasks in validation and cost-routing logic.
- **Observability Hub:** Tracing and evaluation dashboards for all "Kumo-built" agent systems.
- **Project Registry:** Unified DB for tracking status, evidence artifacts, and hiring signal metrics across the portfolio.

## Architecture
- **Backend:** Python (FastAPI + Pydantic)
- **Orchestration:** LangGraph (Stateful, multi-agent flows)
- **Database:** PostgreSQL (Portfolio data & Agent state)
- **Telemetry:** Langfuse / OpenTelemetry
- **Frontend:** Appsmith (Executive Dashboard)

## Repository Structure
- `/backend`: Core API and agent control plane logic.
- `/db`: Schema migrations and SQL queries.
- `/docs`: Architecture, runbooks, and portfolio positioning.
- `/scripts`: Deployment, backup, and evaluation automation.
