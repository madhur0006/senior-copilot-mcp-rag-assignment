from __future__ import annotations

import logging
import time
import uuid
from typing import Any, Mapping

import httpx

from connectors.alarm_api.config import AlarmApiConfig
from connectors.alarm_api.errors import (
    AlarmApiAuthError,
    AlarmApiError,
    AlarmApiNotFoundError,
    AlarmApiTimeoutError,
    AlarmApiValidationError,
)

logger = logging.getLogger(__name__)

RETRYABLE_STATUS_CODES = {429, 502, 503, 504}


class AlarmApiClient:
    """HTTP client for the Alarm Management API simulator.

    Responsibilities:
    - Bearer auth
    - Trace / client metadata headers
    - Timeouts and retries
    - Safe logging (token never logged)
    - Typed convenience methods used later by the MCP server
    """

    def __init__(
        self,
        config: AlarmApiConfig | None = None,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.config = config or AlarmApiConfig()
        self._client = httpx.Client(
            base_url=self.config.normalized_base_url,
            timeout=httpx.Timeout(self.config.timeout_seconds),
            transport=transport,
            headers={
                "Accept": "application/json",
                "User-Agent": "alarm-investigation-connector/0.1",
            },
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> AlarmApiClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Public API methods used by the use case
    # ------------------------------------------------------------------

    def health(self) -> dict[str, Any]:
        return self.request("GET", "/health", auth=False)

    def search_assets(
        self,
        query: str,
        *,
        site: str | None = None,
        unit: str | None = None,
        equipment_type: str | None = None,
        limit: int = 25,
        trace_id: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"query": query, "limit": limit}
        if site:
            params["site"] = site
        if unit:
            params["unit"] = unit
        if equipment_type:
            params["equipment_type"] = equipment_type
        return self.request("GET", "/assets/search", params=params, trace_id=trace_id)

    def get_asset_metadata(self, asset_id: str, *, trace_id: str | None = None) -> dict[str, Any]:
        return self.request("GET", f"/assets/{asset_id}/metadata", trace_id=trace_id)

    def get_alarms(
        self,
        *,
        asset_id: str | None = None,
        severity: list[str] | None = None,
        status: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        page: int = 1,
        page_size: int = 50,
        sort_by: str = "start_time",
        sort_order: str = "desc",
        trace_id: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
        if asset_id:
            params["asset_id"] = asset_id
        if severity:
            params["severity"] = severity
        if status:
            params["status"] = status
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        return self.request("GET", "/alarms", params=params, trace_id=trace_id)

    def get_alarm(self, alarm_id: str, *, trace_id: str | None = None) -> dict[str, Any]:
        return self.request("GET", f"/alarms/{alarm_id}", trace_id=trace_id)

    def get_alarm_summary(
        self,
        payload: Mapping[str, Any],
        *,
        trace_id: str | None = None,
    ) -> dict[str, Any]:
        return self.request("POST", "/alarms/summary", json=payload, trace_id=trace_id)

    def correlate_alarms(
        self,
        payload: Mapping[str, Any],
        *,
        trace_id: str | None = None,
    ) -> dict[str, Any]:
        return self.request("POST", "/alarms/correlation", json=payload, trace_id=trace_id)

    def get_priority_score(
        self,
        alarm_id: str,
        *,
        weights: Mapping[str, float] | None = None,
        trace_id: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"alarm_id": alarm_id}
        if weights:
            body.update(weights)
        return self.request("POST", "/alarms/priority-score", json=body, trace_id=trace_id)

    def get_operator_recommendations(
        self,
        alarm_id: str,
        *,
        include_related: bool = True,
        include_asset_context: bool = True,
        include_historical_pattern: bool = True,
        trace_id: str | None = None,
    ) -> dict[str, Any]:
        body = {
            "alarm_id": alarm_id,
            "include_related": include_related,
            "include_asset_context": include_asset_context,
            "include_historical_pattern": include_historical_pattern,
        }
        return self.request(
            "POST",
            "/recommendations/operator-actions",
            json=body,
            trace_id=trace_id,
        )

    # ------------------------------------------------------------------
    # Core request helper
    # ------------------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
        trace_id: str | None = None,
        auth: bool = True,
        metadata_tag: str | None = None,
    ) -> dict[str, Any]:
        resolved_trace_id = trace_id or str(uuid.uuid4())
        headers = self._build_headers(
            auth=auth,
            trace_id=resolved_trace_id,
            metadata_tag=metadata_tag,
        )

        attempts = self.config.retry_count + 1
        last_error: Exception | None = None

        for attempt in range(1, attempts + 1):
            try:
                logger.info(
                    "alarm_api_request",
                    extra={
                        "method": method,
                        "path": path,
                        "trace_id": resolved_trace_id,
                        "attempt": attempt,
                        # Never include Authorization / token here.
                    },
                )
                response = self._client.request(
                    method,
                    path,
                    params=params,
                    json=json,
                    headers=headers,
                )
                if response.status_code in RETRYABLE_STATUS_CODES and attempt < attempts:
                    self._sleep_backoff(attempt)
                    continue
                return self._handle_response(
                    response,
                    trace_id=resolved_trace_id,
                    retry_count=attempt - 1,
                )
            except httpx.TimeoutException as exc:
                last_error = exc
                if attempt >= attempts:
                    raise AlarmApiTimeoutError(
                        f"Alarm API timed out calling {method} {path}",
                        trace_id=resolved_trace_id,
                        retry_count=attempt - 1,
                    ) from exc
                self._sleep_backoff(attempt)
            except httpx.TransportError as exc:
                last_error = exc
                if attempt >= attempts:
                    raise AlarmApiError(
                        f"Alarm API transport error calling {method} {path}: {exc}",
                        trace_id=resolved_trace_id,
                        retry_count=attempt - 1,
                    ) from exc
                self._sleep_backoff(attempt)

        raise AlarmApiError(
            f"Alarm API request failed after retries: {last_error}",
            trace_id=resolved_trace_id,
            retry_count=self.config.retry_count,
        )

    def _build_headers(
        self,
        *,
        auth: bool,
        trace_id: str,
        metadata_tag: str | None,
    ) -> dict[str, str]:
        headers = {
            # Simulator OpenAPI uses both spellings across endpoints.
            "trace_id": trace_id,
            "trace-id": trace_id,
            "x-client-id": self.config.client_id,
            "x-metadata-tag": metadata_tag or self.config.metadata_tag,
        }
        if auth:
            headers["Authorization"] = f"Bearer {self.config.token}"
        return headers

    def _handle_response(
        self,
        response: httpx.Response,
        *,
        trace_id: str,
        retry_count: int,
    ) -> dict[str, Any]:
        status = response.status_code
        try:
            payload: Any = response.json() if response.content else {}
        except ValueError:
            payload = {"raw": response.text}

        if status == 401 or status == 403:
            raise AlarmApiAuthError(
                "Alarm API authentication failed",
                status_code=status,
                trace_id=trace_id,
                retry_count=retry_count,
                details=_safe_details(payload),
            )
        if status == 404:
            raise AlarmApiNotFoundError(
                "Alarm API resource not found",
                status_code=status,
                trace_id=trace_id,
                retry_count=retry_count,
                details=_safe_details(payload),
            )
        if status == 422 or status == 400:
            raise AlarmApiValidationError(
                "Alarm API validation error",
                status_code=status,
                trace_id=trace_id,
                retry_count=retry_count,
                details=_safe_details(payload),
            )
        if status >= 400:
            raise AlarmApiError(
                f"Alarm API error HTTP {status}",
                status_code=status,
                trace_id=trace_id,
                retry_count=retry_count,
                details=_safe_details(payload),
            )

        if not isinstance(payload, dict):
            return {"data": payload}
        return payload

    @staticmethod
    def _sleep_backoff(attempt: int) -> None:
        # 0.2s, 0.4s, 0.8s... capped
        delay = min(0.2 * (2 ** (attempt - 1)), 2.0)
        time.sleep(delay)


def _safe_details(payload: Any) -> Any:
    """Return response details without accidental secret leakage."""
    if isinstance(payload, dict):
        redacted = dict(payload)
        for key in list(redacted):
            if "token" in key.lower() or "authorization" in key.lower():
                redacted[key] = "***REDACTED***"
        return redacted
    return payload
