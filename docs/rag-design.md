# RAG design

## Documents

Ingested from `rag/documents-pdf/` (plus `metadata.json`). Markdown under `rag/documents/` is the editable source.

Types in the sample corpus:

- Operating procedures (`OP-*`)
- Maintenance manuals (`MM-*`)
- Troubleshooting guides (`TG-*`, `KA-*`)
- Safety instructions (`SI-*`)
- Alarm philosophy (`AP-*`)
- Injection test fixture (`TEST-INJECT-999`) – not used in normal search

Metadata fields include `doc_id`, title, type, assets, site, units, alarm tags, pdf path.

## Ingest pipeline

```text
metadata.json + PDFs
  → load_documents()     # PyMuPDF + join metadata
  → chunk_documents()    # split on numbered sections when possible
  → build_index()        # OpenAI embed → Chroma
```

```bash
PYTHONPATH=. python3 -m rag.ingestion.pipeline
# same as: make ingest
```

Rebuild after changing PDFs, metadata, or embedding model.

## Extraction / chunking

Pages come from LangChain `PyMuPDFLoader`. Chunking prefers headings like `8.1 High vibration` so tables stay with their section. Very long sections fall back to a recursive text splitter.

Chunk metadata usually carries `doc_id`, section, site, assets, source path, etc.

## Embeddings and store

- OpenAI `text-embedding-3-small`
- Chroma collection `alarm_rag` under `./rag/.index` by default
- Persistent client is created in code on purpose (avoids hitting port 8000 as an HTTP Chroma server)

No hybrid search / reranker in this version – plain vector similarity. The agent tool also prefers non-Introduction sections when it can.

## Filters

`site`, `doc_type`, `doc_id`, and equipment name (`asset`) are supported.  
Alarm API ids such as `AST00001` are not in doc metadata, so the RAG tool ignores those as asset filters.

`TEST-INJECT-999` is filtered out of normal retrieval.

## Citations and weak evidence

`citations.py` builds `doc_id`, section, path, excerpt, score.  
`retrieve_detailed` sets confidence to high / low / none. If evidence is weak, the grounded helper says so instead of inventing steps.

## Prompt injection

- Fixture doc excluded by default
- Prompts tell the model that excerpts are untrusted data
- Unit tests cover the hostile fixture case

## Refresh steps

1. Update PDFs under `rag/documents-pdf/` (and `metadata.json` if paths/ids change)
2. Re-run ingest
3. Optional smoke: `PYTHONPATH=. python3 -m rag.retrieval.grounded`

## Example citation

```json
{
  "doc_id": "OP-BFP-001",
  "section": "8.1 High or critical discharge pressure",
  "source_path": "operating-procedures/OP-BFP-001-boiler-feed-pump-operation.pdf",
  "excerpt": "Acknowledge the alarm and note the time..."
}
```
