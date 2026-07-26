"""
Alarm Investigation Copilot — Streamlit GUI (Step 7).

Run:
  docker start alarm-api-simulator
  PYTHONPATH=. streamlit run apps/frontend/app.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apps.backend.service import run_investigation
from rag.ingestion.config import RagConfig

SAMPLE_QUERY = (
    "Investigate recurring high-severity alarms for Boiler Feed Pump 101 "
    "over the last 90 days, identify likely contributing factors, retrieve "
    "the relevant operating procedure, and provide recommended actions with "
    "source evidence."
)


def _init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "last_error" not in st.session_state:
        st.session_state.last_error = None


def _parse_json_preview(preview: str):
    try:
        return json.loads(preview.replace("...", ""))
    except Exception:
        try:
            return json.loads(preview)
        except Exception:
            return None


def _alarm_summary_from_result(result) -> list[dict]:
    """Prefer structured alarms from the service; fall back to parsing the trace."""
    if getattr(result, "alarms", None):
        return list(result.alarms)
    alarms = []
    for item in result.tool_trace:
        if item.tool not in ("get_alarms", "get_recent_critical_alarms"):
            continue
        data = _parse_json_preview(item.result_preview)
        if not isinstance(data, dict):
            continue
        items = (
            data.get("data")
            or data.get("items")
            or data.get("alarms")
            or data.get("results")
            or []
        )
        if isinstance(items, list):
            for row in items[:20]:
                if isinstance(row, dict):
                    alarms.append(row)
    return alarms


def _run_query(query: str):
    st.session_state.last_error = None
    config = RagConfig()
    with st.spinner("Running MCP + RAG investigation..."):
        try:
            result = run_investigation(query, config=config, discover_tools=False)
            st.session_state.last_result = result
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.messages.append({"role": "assistant", "content": result.answer})
        except Exception as exc:
            st.session_state.last_error = f"{type(exc).__name__}: {exc}"
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"Investigation failed. {st.session_state.last_error}",
                }
            )


def main():
    st.set_page_config(
        page_title="Alarm Investigation Copilot",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _init_state()

    st.title("Alarm Investigation Copilot")
    st.caption("MCP alarm tools + document RAG — EastRefinery / ABB assignment")

    with st.sidebar:
        st.header("Setup")
        config = RagConfig()
        st.write(f"**LLM:** `{config.chat_model}`")
        st.write(f"**Index:** `{config.index_dir.name}`")
        st.write("**Alarm API:** `localhost:8000`")
        st.divider()
        if st.button("Load sample investigation query", use_container_width=True):
            st.session_state.pending_query = SAMPLE_QUERY
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_result = None
            st.session_state.last_error = None
            st.rerun()

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pending = st.session_state.pop("pending_query", None)
    prompt = st.chat_input("Ask about an asset alarm or procedure…")
    query = pending or prompt
    if query:
        _run_query(query)
        st.rerun()

    if st.session_state.last_error:
        st.error(st.session_state.last_error)

    result = st.session_state.last_result
    if not result:
        st.info(
            "Ask a question above, or load the sample investigation from the sidebar. "
            "Ensure the Alarm API simulator is running and the RAG index is built."
        )
        return

    st.divider()
    col_alarms, col_cites = st.columns(2)

    with col_alarms:
        st.subheader("Alarm summary")
        alarms = _alarm_summary_from_result(result)
        if not alarms:
            st.write("No alarm rows parsed from tool results yet.")
        else:
            for a in alarms[:10]:
                aid = a.get("alarm_id") or a.get("id") or "?"
                sev = a.get("severity") or a.get("priority") or ""
                status = a.get("status") or ""
                msg = (
                    a.get("alarm_message")
                    or a.get("message")
                    or a.get("description")
                    or a.get("alarm_name")
                    or a.get("alarm_tag")
                    or ""
                )
                st.markdown(f"- **{aid}** · {sev} · {status}  \n  {msg}")

    with col_cites:
        st.subheader("Document citations")
        if not result.citations:
            st.write("No citations captured (RAG tool may not have run).")
        else:
            for c in result.citations:
                st.markdown(
                    f"- **{c.get('doc_id')}** · {c.get('section')}  \n"
                    f"  `{c.get('source_path')}`  \n"
                    f"  _{str(c.get('excerpt') or '')[:220]}_"
                )

    st.subheader("MCP tool trace")
    st.caption("Expand a call to inspect arguments and response preview.")
    for i, item in enumerate(result.tool_trace, 1):
        status = "ok" if item.ok else "error"
        label = f"{i}. [{status}] {item.tool}"
        with st.expander(label, expanded=(not item.ok)):
            st.markdown("**Request (arguments)**")
            st.json(item.arguments)
            st.markdown("**Response preview**")
            parsed = _parse_json_preview(item.result_preview)
            if parsed is not None:
                st.json(parsed)
            else:
                st.code(item.result_preview)


if __name__ == "__main__":
    main()
