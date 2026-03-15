# Knowledge Capture: 10 Essential AI Engineering Papers (Synthesis)

## Source
- "10 Papers Every Future AI Engineer Must Read"
- Author: Slayman
- User-provided transcript (captured Mar 15, 2026)

---

## Why this matters for Jacques
This batch provides the **theoretical lineage** and **first-principles logic** behind modern AI systems. It is the "interview gold" for high-level engineering roles where explainability and architectural trade-offs are prioritized over just making things work.

### Core Signal for Portfolio/Interviews:
1. **Transformer Heritage:** Understanding *Self-Attention* (2017) explains why current models scale so well and where they struggle with context length.
2. **In-Context Learning vs. Fine-Tuning:** The *Few-Shot Learners* (2020) vs. *LoRA* (2021) debate allows Jacques to explain *when* to use prompt engineering vs. *when* a lightweight rank adapter is needed.
3. **RAG Maturity:** Knowing the original *RAG* (2020) paper helps justify why Jacques uses iterative retrieval and source grounding instead of relying on model memory.
4. **Agent Anatomy:** The *Brain/Perception/Action* survey framework is exactly what Jacques is implementing in the Project #1 "Reliability Control Plane."

---

## Strategic Technical Breakdown

| Concept | Paper/Breakthrough | Key Takeaway for Jacques |
| :--- | :--- | :--- |
| **Architecture** | Attention is All You Need (2017) | Transformers replaced RNNs; enabled parallel training and long-range dependencies. |
| **Prompting** | GPT-3 / Few-Shot Learners (2020) | Scale + Prompting = In-context learning. Demonstrates that models can "learn" from examples in the prompt. |
| **Alignment** | InstructGPT (2022) | RLHF (Reinforcement Learning from Human Feedback) makes models helpful/safe. Direct precursor to DPO. |
| **Fine-Tuning** | LoRA (2021) | Parameter-efficient tuning. Jacques can mention this for specialized domain tasks (Legal/Medical). |
| **Retrieval** | RAG (2020) | Combines retrieval (DBs) with generation. Solves "frozen knowledge" and reduces hallucination. |
| **Agents** | Rise of LLM Agents Survey (2023) | Defines Agent = Brain (LLM) + Perception (Tools/Memory) + Action (APIs). |
| **Efficiency** | Mixture of Experts (MoE) | Mixture of Experts routers run only relevant "expert" sub-networks. Basis for GPT-4/5 style efficiency. |
| **Compression** | DistilBERT / Quantization | Knowledge distillation (teacher/student) and int8 quantization (LLM.int8). Essential for edge/local AI. |
| **Integration** | Model Context Protocol (MCP) | Anthropic's 2024 standard for connecting tools/data. Jacques already uses this in OpenClaw. |

---

## Strategic Insight: The "AI Infrastructure" Pitch
- **Insight:** The video concludes with the shift from "pure theory" to "production infrastructure" (Scaling laws, infra, system design).
- **Jacques's Alignment:** Jacques's current path (Cloud + AI Engineering) is the practical application of these papers. He isn't just reading research; he's building the **Infrastructure (AWS/Terraform)** and **Observability (Telemetry)** that makes these theoretical papers useful to a business.

---

## Refined Interview Signal
*"I understand the lineage from original Transformer self-attention to modern MoE architectures. In my projects, I apply the RAG pattern for grounded knowledge and the modular Agent framework (Brain/Perception/Action) to ensure that agentic workflows remain traceable and governed by business policy."*

---

## Suggested KB Tags
- ai-research-lineage
- transformers
- lora-fine-tuning
- rag-architecture
- agent-frameworks
- mixture-of-experts
- mcp-standard
- hiring-signal
- interview-prep
- kumo
