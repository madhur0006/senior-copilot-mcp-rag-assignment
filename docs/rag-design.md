# RAG Design — LangChain + OpenAI + Chroma (Steps 5h–5n)

## Stack (locked)

| Piece | Choice |
|-------|--------|
| Load PDF | LangChain `PyMuPDFLoader` |
| Metadata | `rag/documents-pdf/metadata.json` joined onto each Document |
| Chunk | Section-aware (keeps tables); LangChain splitter only if huge |
| Embeddings | LangChain `OpenAIEmbeddings` (`text-embedding-3-small`) |
| Vector store | LangChain `Chroma` at `./rag/.index` |
| Chat (RAG-only) | LangChain `ChatOpenAI` (`gpt-4o-mini`) |
| Agent | LangGraph in `apps.backend` (Step 6) |

### Env

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o-mini
DOCUMENT_PDF_PATH=./rag/documents-pdf
METADATA_PATH=./rag/documents-pdf/metadata.json
VECTOR_STORE_URL=./rag/.index
```

## Pipeline

```
metadata.json + PDFs
    → load_documents()
    → chunk_documents()
    → build_index()
    → retrieve_detailed()
    → generate_grounded_answer()
```

## Commands

```bash
PYTHONPATH=. python3 -m rag.ingestion.pipeline
PYTHONPATH=. python3 -m rag.retrieval.grounded
PYTHONPATH=. python -m pytest tests/unit/test_rag_*.py -q
```

> Rebuild the index after changing embedding model/provider.
