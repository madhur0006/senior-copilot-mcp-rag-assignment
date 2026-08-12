# RAG Document Corpus

Synthetic but realistic EastRefinery documents for the **Alarm Investigation and Procedure Guidance Copilot** assignment.

## Formats

- PDF corpus for RAG: `rag/documents-pdf/` (+ `metadata.json`)
- Markdown sources (reference / editing): `rag/documents/`

## Folder layout

```text
rag/
├── documents/                 # Markdown sources (optional)
│   ├── README.md
│   ├── operating-procedures/
│   ├── maintenance-manuals/
│   ├── troubleshooting-guides/
│   ├── safety-instructions/
│   └── alarm-philosophy/
└── documents-pdf/             # PDF corpus used for RAG
    ├── metadata.json          # machine-readable catalog
    ├── operating-procedures/
    ├── maintenance-manuals/
    ├── troubleshooting-guides/
    ├── safety-instructions/
    └── alarm-philosophy/
```

## Documents included (15 production + 1 injection test fixture)

| ID | Type | PDF |
|---|---|---|
| OP-BFP-001 | Operating procedure | `documents-pdf/operating-procedures/OP-BFP-001-boiler-feed-pump-operation.pdf` |
| OP-CMP-002 | Operating procedure | `documents-pdf/operating-procedures/OP-CMP-002-centrifugal-compressor-operation.pdf` |
| OP-MTR-003 | Operating procedure | `documents-pdf/operating-procedures/OP-MTR-003-critical-motor-operation.pdf` |
| MM-BFP-010 | Maintenance manual | `documents-pdf/maintenance-manuals/MM-BFP-010-boiler-feed-pump-maintenance.pdf` |
| MM-CMP-011 | Maintenance manual | `documents-pdf/maintenance-manuals/MM-CMP-011-centrifugal-compressor-maintenance.pdf` |
| MM-MTR-012 | Maintenance manual | `documents-pdf/maintenance-manuals/MM-MTR-012-critical-motor-maintenance.pdf` |
| TG-BFP-020 | Troubleshooting | `documents-pdf/troubleshooting-guides/TG-BFP-020-boiler-feed-pump-alarms.pdf` |
| TG-CMP-021 | Troubleshooting | `documents-pdf/troubleshooting-guides/TG-CMP-021-compressor-discharge-pressure.pdf` |
| TG-MTR-022 | Troubleshooting | `documents-pdf/troubleshooting-guides/TG-MTR-022-motor-trip-alarms.pdf` |
| TG-PRI-023 | Troubleshooting | `documents-pdf/troubleshooting-guides/TG-PRI-023-alarm-priority-escalation.pdf` |
| KA-OPS-050 | Knowledge article | `documents-pdf/troubleshooting-guides/KA-OPS-050-recurring-bfp-high-severity.pdf` |
| SI-GEN-030 | Safety | `documents-pdf/safety-instructions/SI-GEN-030-alarm-response-safety.pdf` |
| SI-BFP-031 | Safety | `documents-pdf/safety-instructions/SI-BFP-031-boiler-feed-pump-safety.pdf` |
| SI-CMP-032 | Safety | `documents-pdf/safety-instructions/SI-CMP-032-compressor-safety.pdf` |
| AP-ER-040 | Alarm philosophy | `documents-pdf/alarm-philosophy/AP-ER-040-eastrefinery-alarm-philosophy.pdf` |
| TEST-INJECT-999 | Test fixture | `documents-pdf/troubleshooting-guides/TEST-INJECT-999-prompt-injection-fixture.pdf` |

## Metadata

Location: `rag/documents-pdf/metadata.json`

Fields used for ingestion:

- `doc_id`, `title`, `path` (PDF path relative to `documents-pdf/`)
- `pdf_path`
- `doc_type`, `assets`, `site`, `units`, `alarm_tags`
- `revision`, `effective_date`

## Notes for RAG implementation

1. Ingest PDFs from `rag/documents-pdf/` and join with `metadata.json`.
2. Keep markdown sources in `rag/documents/` as readable reference; ingest uses PDFs only.
3. Prefer section-aware chunking.
4. Store citations as `doc_id` + section + source path.
5. Filter on `assets`, `doc_type`, and `site` when the question names them.
6. If retrieval confidence is low, say so and avoid inventing procedure steps.
7. Treat retrieved text as untrusted content (prompt-injection boundary). Never execute instructions found inside documents.
8. Exclude `TEST-INJECT-999` from production retrieval indexes; use it only in prompt-injection tests.
