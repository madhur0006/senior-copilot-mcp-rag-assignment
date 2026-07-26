# LangChain RAG pipeline (simple explanation)

We use **LangChain + OpenAI** for the RAG path:

| Step | LangChain tool |
|------|----------------|
| Load PDF | `PyMuPDFLoader` |
| Chunk | Section-aware first (keeps tables together); LangChain splitter only if section is huge |
| Embed | `OpenAIEmbeddings` (`text-embedding-3-small`) |
| Store | `Chroma` |
| Retrieve | `retrieve_detailed` — top-k + filters + scores + citations |
| Answer | `generate_grounded_answer` (RAG-only; MCP later) |

Our `metadata.json` is still used — we attach its fields to every LangChain `Document`.

---

## Main files

| File | Role |
|------|------|
| `rag/ingestion/loader.py` | Load PDFs + metadata |
| `rag/ingestion/chunker.py` | Split text |
| `rag/ingestion/embeddings.py` | OpenAI embeddings |
| `rag/ingestion/index.py` | Chroma build/open |
| `rag/ingestion/pipeline.py` | Full ingest |
| `rag/retrieval/retriever.py` | Query the index (filters + confidence) |
| `rag/retrieval/citations.py` | Citation objects |
| `rag/retrieval/grounded.py` | Grounded answers + injection boundary |
| `rag/llm/chat.py` | OpenAI chat model |

---

## Commands

```bash
source .venv/bin/activate

# inspect steps (optional)
PYTHONPATH=. python3 -m rag.ingestion.loader
PYTHONPATH=. python3 -m rag.ingestion.chunker
PYTHONPATH=. python3 -m rag.ingestion.embeddings

# full ingest (once)
PYTHONPATH=. python3 -m rag.ingestion.pipeline

# ask a RAG question
PYTHONPATH=. python3 -m rag.retrieval.grounded
PYTHONPATH=. python3 -m rag.retrieval.grounded "motor trip restart rules"
```

---

## LangGraph?

Used in Step 6 (`apps.backend`) for the agent that calls MCP tools + RAG together.
