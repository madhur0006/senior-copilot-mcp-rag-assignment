# RAG Design

## Source document types

Corpus under `rag/documents-pdf/` (ingested) with editable Markdown mirrors in `rag/documents/`:

- Operating procedures (`OP-*`)
- Maintenance manuals (`MM-*`)
- Troubleshooting guides (`TG-*`, `KA-*`)
- Safety instructions (`SI-*`)
- Alarm philosophy (`AP-*`)
- Prompt-injection fixture (`TEST-INJECT-999`, excluded from normal retrieval)

Metadata: `rag/documents-pdf/metadata.json` (`doc_id`, `title`, `doc_type`, `assets`, `site`, `units`, `alarm_tags`, `pdf_path`, …).

## Ingestion flow

```text
metadata.json + PDFs
  → load_documents()          # PyMuPDFLoader + metadata join
  → chunk_documents()         # section-aware chunking
  → build_index()             # OpenAI embeddings → Chroma
```

Command:

```bash
PYTHONPATH=. python3 -m rag.ingestion.pipeline
# or: make ingest
```

Rebuild the index after changing embedding model/provider or corpus files.

## Text extraction

LangChain `PyMuPDFLoader` loads each PDF page; parent metadata from `metadata.json` is attached to every page/chunk.

## Chunking strategy

Section-aware split on numbered headings (e.g. `8.1 High vibration`) so procedure tables stay intact. Only sections longer than a hard max are further split with `RecursiveCharacterTextSplitter`.

## Chunk metadata

Typical fields on each chunk: `doc_id`, `title`, `section`, `doc_type`, `site`, `assets`, `units`, `pdf_path` / source path, revision where present.

## Embedding model

- Provider: OpenAI
- Model: `text-embedding-3-small` (`OPENAI_EMBEDDING_MODEL`)

## Vector database / index

- LangChain Chroma collection `alarm_rag`
- Path: `VECTOR_STORE_URL` (default `./rag/.index`)
- Explicit `chromadb.PersistentClient` (avoids HttpClient on `:8000`)

## Hybrid search / reranking

Not used. Dense similarity search only. Optional preference for non-Introduction sections when ranking tool excerpts for the agent.

## Retrieval filters

Supported filters include `site`, `doc_type`, `doc_id`, and equipment `asset` name (substring). Alarm API ids like `AST00001` are not document metadata and are skipped by the copilot RAG tool.

`TEST-INJECT-999` is excluded from normal search.

## Citation construction

`rag/retrieval/citations.py` builds citations with `doc_id`, `section`, `source_path`, excerpt, and distance score. GUI and agent surfaces show these fields.

## Low-confidence handling

`retrieve_detailed` labels confidence `high` / `low` / `none` using distance thresholds and empty-hit handling. Grounded helper returns an insufficient-evidence message instead of inventing steps.

## Prompt-injection protections

- Hostile fixture excluded from default retrieval
- Grounded / agent prompts treat retrieved text as untrusted data
- Unit tests assert hostile instructions are not obeyed

## Index refresh process

1. Update Markdown (optional) and regenerate PDFs if needed (`rag/scripts/md_to_pdf.py`)
2. Update `metadata.json` if paths/ids change
3. Run `PYTHONPATH=. python3 -m rag.ingestion.pipeline` (`reset=True` rebuilds collection)
4. Smoke with `PYTHONPATH=. python3 -m rag.retrieval.grounded`

## Example retrieval

```bash
PYTHONPATH=. python3 -m rag.retrieval.grounded
PYTHONPATH=. python3 -m pytest tests/unit/test_rag_*.py tests/integration/test_rag_retrieve_live.py -q
```

Example citation shape:

```json
{
  "doc_id": "OP-BFP-001",
  "section": "8.1 High or critical discharge pressure",
  "source_path": "operating-procedures/OP-BFP-001-boiler-feed-pump-operation.pdf",
  "excerpt": "Acknowledge the alarm and note the time..."
}
```
