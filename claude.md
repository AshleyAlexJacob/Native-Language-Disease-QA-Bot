# Claude Development Best Practices (RAG Health QA System)

## Project Context

This project is a **Retrieval-Augmented Generation (RAG) based Native Language Health QA Bot** that leverages WHO (World Health Organization) healthcare documents to provide safe, accurate, and localized health advisory responses.

### Core Goals

* Provide **accurate, evidence-based health guidance**
* Ensure responses are **grounded strictly in WHO documents**
* Support **multilingual/native language interaction**
* Prevent hallucinations and unsafe medical advice
* Maintain **traceability via citations**

---

## 0. Plan, Then Execute Workflow

### Planning Phase

Before writing code:

1. Understand requirements and user query flow
2. Design RAG architecture
3. Define safety and compliance constraints
4. Identify dependencies and tools
5. Define APIs and schemas
6. Plan evaluation strategy

### Execution Phase

1. Build ingestion pipeline
2. Implement embeddings and vector DB
3. Build retrieval pipeline
4. Integrate LLM with grounded prompting
5. Add multilingual support
6. Implement safety guardrails
7. Write tests and validate system

---

## 1. RAG Architecture

### Flow

User Query → Language Detection → (Optional Translation) → Embedding → Vector Search → Context Assembly → LLM → Safety Filter → Response

---

## 2. Project Structure

```
project_root/
├── main.py
├── config/
│   └── rag.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── embeddings/
├── tests/
└── src/
    ├── ingestion/
    ├── retrievers/
    ├── embeddings/
    ├── vectorstores/
    ├── services/
    │   ├── rag_service.py
    │   └── health_service.py
    ├── routers/
    ├── schemas/
    ├── prompts/
    ├── core/
    ├── utils/
    └── llms.py
```

---

## 3. RAG-Specific Best Practices

### Chunking

* Use semantic chunking
* Maintain chunk size ~300–500 tokens
* Preserve medical context

### Embeddings

* Use high-quality embedding models
* Normalize embeddings

### Retrieval

* Use top-k retrieval (k=3–5)
* Consider reranking
* Avoid irrelevant context injection

### Prompting

* Enforce strict grounding
* Include citations
* Add medical disclaimers

---

## 4. Safety Guidelines (CRITICAL)

* No diagnosis or prescriptions
* No hallucinated facts
* Always cite WHO sources
* Include disclaimer: “Consult a healthcare professional”
* Detect emergency queries and respond safely

---

## 5. Multilingual Support

* Detect user language
* Translate queries if needed
* Generate response in native language

---

## 6. Testing Strategy

### Unit Tests

* Test ingestion
* Test chunking
* Test embeddings
* Test retrieval accuracy

### Integration Tests

* End-to-end query pipeline
* API response validation

---

## 7. Code Quality Standards

* Follow PEP8
* Use type hints
* Write docstrings
* Keep functions small and readable

---

## 8. Logging & Monitoring

* Log queries and retrieved chunks

---

## 9. Deployment

* Use Docker
* Enable health checks
* Secure environment variables

---

## 10. Summary

This system must prioritize:

1. Accuracy
2. Safety
3. Grounding
4. Multilingual accessibility

**Never compromise on medical safety and factual correctness.**
