# RAG Design

## Source document types

- Operating procedures
- Maintenance manuals
- Troubleshooting guides
- Safety instructions
- Alarm philosophy
- Service knowledge articles

Corpus locations:

- Markdown: `rag/documents/`
- PDF: `rag/documents-pdf/`
- Metadata: `rag/documents/metadata.json`

## Ingestion flow (planned)

1. Load files from `DOCUMENT_PATH` / `DOCUMENT_PDF_PATH`
2. Extract text (PDF text extraction or Markdown parse)
3. Chunk by section headings where possible
4. Attach metadata (`doc_id`, `doc_type`, `assets`, `site`, `section`, `revision`)
5. Embed chunks
6. Upsert into vector index

## Chunking strategy

Prefer section-aware chunks on `##` / `###` boundaries, with overlap for long sections.

## Embedding / retrieval

To be selected in Step 6 (for example local embeddings + Chroma/FAISS, or a hosted embedding API).

## Filters

Support filters on `assets`, `doc_type`, `site`, and exclude `TEST-INJECT-999` from production retrieval.

## Citations

Return `doc_id`, title, section, source path, and short excerpt.

## Low-confidence handling

If top score is below threshold or no hits, say evidence is insufficient instead of inventing procedure steps.

## Prompt-injection protections

Treat retrieved text as untrusted. Never follow instructions embedded in documents. Use `TEST-INJECT-999` only in dedicated tests.

## Index refresh

Re-run ingestion script after corpus changes. Document command here after Step 6.
