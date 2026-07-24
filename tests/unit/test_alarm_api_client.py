from __future__ import annotations

import httpx
import pytest
import respx

from connectors.alarm_api import (
    AlarmApiAuthError,
    AlarmApiClient,
    AlarmApiConfig,
    AlarmApiNotFoundError,
    AlarmApiTimeoutError,
    AlarmApiValidationError,
)


@pytest.fixture
def config() -> AlarmApiConfig:
    return AlarmApiConfig(
        ALARM_API_BASE_URL="http://alarm.test",
        ALARM_API_TOKEN="secret-token-should-not-appear-in-logs",
        REQUEST_TIMEOUT_SECONDS=2,
        RETRY_COUNT=2,
        ALARM_API_CLIENT_ID="unit-test-client",
        ALARM_API_METADATA_TAG="unit",
    )


@respx.mock
def test_health_does_not_require_auth(config: AlarmApiConfig) -> None:
    route = respx.get("http://alarm.test/health").mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )
    with AlarmApiClient(config) as client:
        assert client.health()["status"] == "ok"
    assert route.called
    assert "Authorization" not in route.calls.last.request.headers


@respx.mock
def test_search_assets_sends_bearer_and_trace_headers(config: AlarmApiConfig) -> None:
    respx.get("http://alarm.test/assets/search").mock(
        return_value=httpx.Response(
            200,
            json={
                "results": [{"asset_id": "AST00001", "asset_name": "Boiler Feed Pump 101"}],
                "total_results": 1,
            },
        )
    )
    with AlarmApiClient(config) as client:
        data = client.search_assets("Boiler Feed Pump 101", trace_id="trace-abc")
    assert data["results"][0]["asset_id"] == "AST00001"
    req = respx.calls.last.request
    assert req.headers["Authorization"] == "Bearer secret-token-should-not-appear-in-logs"
    assert req.headers["trace_id"] == "trace-abc"
    assert req.headers["trace-id"] == "trace-abc"
    assert req.headers["x-client-id"] == "unit-test-client"


@respx.mock
def test_get_alarms_passes_pagination_and_filters(config: AlarmApiConfig) -> None:
    respx.get("http://alarm.test/alarms").mock(
        return_value=httpx.Response(200, json={"data": [], "page": 1})
    )
    with AlarmApiClient(config) as client:
        client.get_alarms(
            asset_id="AST00001",
            severity=["high", "critical"],
            page=2,
            page_size=10,
            sort_order="desc",
        )
    params = respx.calls.last.request.url.params
    assert params["asset_id"] == "AST00001"
    assert params["page"] == "2"
    assert params["page_size"] == "10"
    # httpx encodes multi values; accept either repeated or comma depending on version
    assert "high" in str(respx.calls.last.request.url)


@respx.mock
def test_auth_error_mapping(config: AlarmApiConfig) -> None:
    respx.get("http://alarm.test/alarms").mock(
        return_value=httpx.Response(401, json={"detail": "Unauthorized"})
    )
    with AlarmApiClient(config) as client:
        with pytest.raises(AlarmApiAuthError) as exc:
            client.get_alarms()
    assert exc.value.status_code == 401


@respx.mock
def test_not_found_mapping(config: AlarmApiConfig) -> None:
    respx.get("http://alarm.test/alarms/ALM-MISSING").mock(
        return_value=httpx.Response(404, json={"detail": "not found"})
    )
    with AlarmApiClient(config) as client:
        with pytest.raises(AlarmApiNotFoundError):
            client.get_alarm("ALM-MISSING")


@respx.mock
def test_validation_error_mapping(config: AlarmApiConfig) -> None:
    respx.post("http://alarm.test/alarms/priority-score").mock(
        return_value=httpx.Response(422, json={"detail": [{"msg": "field required"}]})
    )
    with AlarmApiClient(config) as client:
        with pytest.raises(AlarmApiValidationError):
            client.get_priority_score("ALM1")


@respx.mock
def test_retries_on_503_then_succeeds(config: AlarmApiConfig, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(AlarmApiClient, "_sleep_backoff", staticmethod(lambda attempt: None))
    route = respx.get("http://alarm.test/health").mock(
        side_effect=[
            httpx.Response(503, json={"detail": "busy"}),
            httpx.Response(503, json={"detail": "busy"}),
            httpx.Response(200, json={"status": "ok"}),
        ]
    )
    with AlarmApiClient(config) as client:
        assert client.health()["status"] == "ok"
    assert route.call_count == 3


@respx.mock
def test_timeout_maps_to_alarm_api_timeout(
    config: AlarmApiConfig, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(AlarmApiClient, "_sleep_backoff", staticmethod(lambda attempt: None))
    respx.get("http://alarm.test/health").mock(side_effect=httpx.ReadTimeout("slow"))
    with AlarmApiClient(config) as client:
        with pytest.raises(AlarmApiTimeoutError) as exc:
            client.health()
    assert exc.value.retry_count == config.retry_count


@respx.mock
def test_operator_recommendations_post_body(config: AlarmApiConfig) -> None:
    respx.post("http://alarm.test/recommendations/operator-actions").mock(
        return_value=httpx.Response(200, json={"recommendations": []})
    )
    with AlarmApiClient(config) as client:
        client.get_operator_recommendations("ALM123", trace_id="t-1")
    body = respx.calls.last.request.read()
    assert b"ALM123" in body
    assert respx.calls.last.request.headers["trace-id"] == "t-1"


def test_error_to_dict_redacts_token_fields() -> None:
    from connectors.alarm_api.errors import AlarmApiError

    err = AlarmApiError(
        "boom",
        status_code=500,
        details={"authorization": "Bearer abc", "token": "xyz", "ok": 1},
    )
    # details are stored as provided; client redacts before attach.
    # Ensure helper used by client works:
    from connectors.alarm_api.client import _safe_details

    safe = _safe_details(err.details)
    assert safe["authorization"] == "***REDACTED***"
    assert safe["token"] == "***REDACTED***"
    assert safe["ok"] == 1
