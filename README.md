# 🤖 AI-Powered Medical Literature Monitoring (MLM) Triage Platform

> **Agentic Retrieval-Augmented Generation (RAG) for Pharmacovigilance Medical Literature Monitoring**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Agentic%20AI-1C3C3C?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-111827?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-ChromaDB-5B21B6?style=for-the-badge)

---

## Executive Summary

This project demonstrates how **Agentic AI**, **Retrieval-Augmented Generation (RAG)**, **semantic vector search**, and **locally hosted Large Language Models (LLMs)** can automate the initial triage stage of **Medical Literature Monitoring (MLM)** for Pharmacovigilance.

The solution retrieves biomedical literature from PubMed, stores it in a semantic vector database, retrieves relevant publications through similarity search, and uses a locally hosted LLM to produce structured pharmacovigilance decisions with an auditable output.

---

## Business Problem

Medical Literature Monitoring is a mandatory pharmacovigilance activity required by regulators such as the FDA and EMA. Safety teams manually review thousands of scientific publications to identify potential Individual Case Safety Reports (ICSRs).

Challenges include:

- High manual effort
- Low signal-to-noise ratio
- Repetitive literature screening
- Need for consistent regulatory decisions
- Auditability and traceability

---

## Solution Overview

The platform:

1. Retrieves literature from PubMed.
2. Generates vector embeddings.
3. Stores documents in ChromaDB.
4. Performs semantic similarity search.
5. Uses an AI Agent to assess literature.
6. Extracts structured safety entities.
7. Produces an auditable ICSR assessment.

---

# Solution Architecture

```mermaid
flowchart LR
User([Medical Reviewer])
Source["PubMed"]
subgraph Platform["AI-Powered Literature Triage Platform"]
Acquire["Literature Acquisition"]
Knowledge["Semantic Knowledge Management"]
Agent["AI Agent Orchestrator"]
Assessment["Clinical Safety Assessment"]
Decision["Regulatory Decision Engine"]
Governance["Audit & Traceability"]
end
Output["Structured ICSR Assessment"]
User-->Acquire-->Source-->Knowledge-->Agent-->Assessment-->Decision-->Governance-->Output
```

---

# AI Workflow

```mermaid
flowchart LR
Query-->Retrieve-->Embed-->Store["ChromaDB"]-->Search-->Reason["Llama 3.2"]-->Extract-->Decision-->Audit
```

---

# Technical Architecture

```mermaid
flowchart TB
User([User])-->Workflow
subgraph Workflow["AI Agent Orchestrator"]
Retrieve-->Embed
Search-->Prompt
Prompt-->LLM
LLM-->Parser
end
PubMed-->Embed
Embed-->VectorDB[(ChromaDB)]
Search-->VectorDB
Parser-->CSV[(Audit Log)]
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| AI Framework | LangChain |
| LLM | Llama 3.2 (Ollama) |
| Embeddings | mxbai-embed-large |
| Vector Database | ChromaDB |
| Literature Source | PubMed |
| Validation | Pydantic |

---

## Project Structure

```text
mlm-triage-agent/
├── mlm_agent_core.py
├── requirements.txt
├── chroma_mlm_db/
└── README.md
```

---

## Installation

```bash
git clone https://github.com/PrashantRGore/mlm-triage-agent.git
cd mlm-triage-agent

ollama pull mxbai-embed-large
ollama pull llama3.2

pip install -r requirements.txt

python mlm_agent_core.py
```

---

## Example Output

The generated audit log contains:

- PubMed ID
- Article Title
- Patient Details
- Suspect Drug
- Adverse Event
- Valid ICSR
- Clinical Rationale
- Timestamp

---

## Current Capabilities

- Agentic AI workflow
- Retrieval-Augmented Generation (RAG)
- Semantic retrieval
- Local LLM inference
- Structured outputs
- Regulatory audit logging
- Privacy-first architecture

---

## Future Roadmap

- Human-in-the-loop review
- Confidence scoring
- Multi-agent workflow
- PDF full-text ingestion
- Knowledge Graph integration
- Power BI dashboard

---

## Disclaimer

This repository is a portfolio and learning project demonstrating AI techniques for Medical Literature Monitoring. It is **not validated for production use** in regulated pharmacovigilance environments.

---

**Author:** Prashant Gore

*AI • Pharmacovigilance • Life Sciences Digital Transformation*
