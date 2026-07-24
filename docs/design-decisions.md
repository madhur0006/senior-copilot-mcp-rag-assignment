# Design Decisions

Record important choices here as implementation proceeds.

## Current decisions

1. **Follow ABB recommended repository layout** from `Submission_and_Evaluation_Guidelines.md`.
2. **Keep both Markdown and PDF corpora** so RAG can demonstrate PDF text extraction while Markdown stays easy to edit.
3. **Use the supplied Alarm API simulator** when it runs; assignment allows an equivalent source system if needed.
4. **Apple Silicon compatibility:** run simulator with `--platform linux/amd64` and Rosetta when required.
5. **Do not commit** the large `*.tar` simulator image or secrets (see `.gitignore`).

## Open decisions (later steps)

- Frontend framework (React vs Streamlit/Gradio)
- Vector store choice
- LLM provider for grounded answer generation
- MCP transport (stdio vs SSE/HTTP) for local Compose setup
