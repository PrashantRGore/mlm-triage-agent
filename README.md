# Agentic AI for Regulatory Medical Literature Monitoring (MLM)

An Agentic Retrieval-Augmented Generation (RAG) pipeline designed to automate the initial triage phase of Medical Literature Monitoring (MLM) in Pharmacovigilance. 

Built with **LangChain**, **ChromaDB**, and **Ollama**, this system operates entirely locally to ensure strict data privacy and regulatory compliance.

## The Business Problem: The Triage Bottleneck
In pharmacovigilance, regulatory agencies (EMA, FDA) mandate the continuous monitoring of medical literature for potential Adverse Drug Reactions (ADRs). Currently, domain experts manually read thousands of biomedical abstracts monthly, the vast majority of which do not contain valid Individual Case Safety Reports (ICSRs). This manual screening is a massive operational bottleneck.

## The Solution: Agentic RAG Architecture
This pipeline uses semantic search to find relevant literature and an Agentic LLM to extract the four mandatory criteria of a valid ICSR: 
1. Identifiable Patient 
2. Suspect Drug 
3. Adverse Event 
4. Identifiable Reporter

## Installation & Setup
1. `ollama pull mxbai-embed-large`
2. `ollama pull llama3.2`
3. `pip install -r requirements.txt`
4. `python mlm_agent_core.py`\n