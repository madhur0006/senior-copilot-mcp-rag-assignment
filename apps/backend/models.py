"""Investigation result models."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ToolTraceItem:
    tool: str
    arguments: dict = field(default_factory=dict)
    result_preview: str = ""
    ok: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class InvestigationResult:
    query: str
    answer: str
    tool_trace: list[ToolTraceItem] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)
    alarms: list[dict] = field(default_factory=list)
    mcp_tools_discovered: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "answer": self.answer,
            "tool_trace": [t.to_dict() for t in self.tool_trace],
            "citations": self.citations,
            "alarms": self.alarms,
            "mcp_tools_discovered": self.mcp_tools_discovered,
        }
