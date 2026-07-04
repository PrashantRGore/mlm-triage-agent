import os
import logging
import datetime
import pandas as pd
from typing import List, Dict, Any
from pydantic import BaseModel, Field

# LangChain Imports
from langchain_community.document_loaders.pubmed import PubMedLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("MLM_Triage_Agent")

class TriageDecision(BaseModel):
    patient_details: str = Field(description="Extract age, sex, or state 'Not specified'")
    suspect_drug: str = Field(description="Extract the drug name")
    adverse_event: str = Field(description="Extract the adverse event")
    is_valid_icsr: bool = Field(description="True ONLY if patient, drug, and event are all explicitly mentioned as a case study")
    rationale: str = Field(description="One short sentence explaining why")

class MLMTriageAgent:
    def __init__(self, db_path: str = "./chroma_mlm_db", model_name: str = "llama3.2"):
        self.db_path = db_path
        self.model_name = model_name
        
        logger.info("Initializing Local Embeddings and LLM...")
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        self.llm = ChatOllama(model=self.model_name, temperature=0.1)
        self.structured_llm = self.llm.with_structured_output(TriageDecision)
        
        self.vector_store = Chroma(
            persist_directory=self.db_path,
            embedding_function=self.embeddings,
            collection_name="mlm_abstracts"
        )
        
    def fetch_literature(self, query: str, max_docs: int = 50) -> List[Document]:
        logger.info(f"Fetching up to {max_docs} abstracts for query: '{query}'")
        try:
            loader = PubMedLoader(query=query, load_max_docs=max_docs)
            docs = loader.load()
            logger.info(f"Successfully retrieved {len(docs)} abstracts.")
            return docs
        except Exception as e:
            logger.error(f"Failed to fetch literature from PubMed API: {str(e)}")
            return []

    def ingest_to_vector_store(self, docs: List[Document]) -> None:
        if not docs:
            logger.warning("No documents to ingest. Skipping vector storage.")
            return
        logger.info("Vectorizing abstracts and storing in ChromaDB...")
        self.vector_store.add_documents(documents=docs)
        logger.info("Ingestion complete.")

    def run_triage_decision(self, abstract_text: str) -> Dict[str, Any]:
        template = """
        You are a highly experienced pharmacovigilance literature reviewer.
        Review the following medical abstract and extract the required clinical entities 
        to determine if it represents a valid Individual Case Safety Report (ICSR).
        
        Abstract: {abstract}
        """
        prompt = ChatPromptTemplate.from_template(template)
        triage_chain = prompt | self.structured_llm
        
        try:
            result: TriageDecision = triage_chain.invoke({"abstract": abstract_text})
            return result.dict()
        except Exception as e:
            logger.error(f"LLM parsing failed for abstract: {str(e)}")
            return {
                "patient_details": "Error", "suspect_drug": "Error",
                "adverse_event": "Error", "is_valid_icsr": False,
                "rationale": f"System parsing error: {str(e)}"
            }

    def process_triage_batch(self, vector_query: str, k: int = 5) -> pd.DataFrame:
        logger.info(f"Executing semantic search for: '{vector_query}' (k={k})")
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
        retrieved_docs = retriever.invoke(vector_query)
        
        audit_log = []
        for idx, doc in enumerate(retrieved_docs, start=1):
            logger.info(f"Processing abstract {idx}/{len(retrieved_docs)}...")
            triage_dict = self.run_triage_decision(abstract_text=doc.page_content)
            log_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "pubmed_id": doc.metadata.get("uid", "Unknown"),
                "title": doc.metadata.get("Title", "Unknown Title"),
                **triage_dict
            }
            audit_log.append(log_entry)
            
        return pd.DataFrame(audit_log)

if __name__ == "__main__":
    mlm_agent = MLMTriageAgent()
    literature_query = "pembrolizumab AND hepatotoxicity"
    new_abstracts = mlm_agent.fetch_literature(query=literature_query, max_docs=20)
    mlm_agent.ingest_to_vector_store(new_abstracts)
    
    clinical_target = "case report of severe hepatic injury"
    audit_df = mlm_agent.process_triage_batch(vector_query=clinical_target, k=5)
    
    output_filename = "mlm_triage_audit_log.csv"
    audit_df.to_csv(output_filename, index=False)
    logger.info(f"Triage complete. Regulatory audit log saved to {output_filename}")\n