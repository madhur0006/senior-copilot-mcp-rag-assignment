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
def config():
    return AlarmApiConfig(
        ALARM_API_BASE_URL="http://alarm.test",
        ALARM_API_TOKEN="test-token",
        REQUEST_TIMEOUT_SECONDS=2,
        RETRY_COUNT=2,
        ALARM_API_CLIENT_ID="unit-test",
        ALARM_API_METADATA_TAG="test",
    )


@respx.mock
def test_health_does_not_require_auth(config):
    route = respx.get("http://alarm.test/health").mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )
    with AlarmApiClient(config) as client:
        result = client.health()
        assert result["status"] == "ok"
    assert route.called
    assert "Authorization" not in route.calls.last.request.headers


@respx.mock
def test_search_assets_sends_auth_header(config):
    respx.get("http://alarm.test/assets/search").mock(
        return_value=httpx.Response(
            200,
            json={"results": [{"asset_id": "AST00001"}], "total_results": 1},
        )
    )
    with AlarmApiClient(config) as client:
        data = client.search_assets("BFP 101")
    
    assert data["results"][0]["asset_id"] == "AST00001"
    req = respx.calls.last.request
    assert req.headers["Authorization"] == "Bearer test-token"
    assert "trace-id" in req.headers
    assert req.headers["x-client-id"] == "unit-test"


@respx.mock
def test_get_alarms_with_filters(config):
    respx.get("http://alarm.test/alarms").mock(
        return_value=httpx.Response(200, json={"data": [], "page": 1})
    )
    with AlarmApiClient(config) as client:
        client.get_alarms(asset_id="AST00001", severity=["high"], page=2, page_size=10)
    
    params = respx.calls.last.request.url.params
    assert params["asset_id"] == "AST00001"
    assert params["page"] == "2"
    assert params["page_size"] == "10"


@respx.mock
def test_auth_error_raises_auth_error(config):
    respx.get("http://alarm.test/alarms").mock(
        return_value=httpx.Response(401, json={"error": "Unauthorized"})
    )
    with AlarmApiClient(config) as client:
        with pytest.raises(AlarmApiAuthError):
            client.get_alarms()


@respx.mock
def test_not_found_raises_not_found_error(config):
    respx.get("http://alarm.test/alarms/MISSING").mock(
        return_value=httpx.Response(404, json={"error": "not found"})
    )
    with AlarmApiClient(config) as client:
        with pytest.raises(AlarmApiNotFoundError):
            client.get_alarm("MISSING")


@respx.mock
def test_validation_error_raises_validation_error(config):
    respx.post("http://alarm.test/alarms/priority-score").mock(
        return_value=httpx.Response(422, json={"error": "invalid"})
    )
    with AlarmApiClient(config) as client:
        with pytest.raises(AlarmApiValidationError):
            client.get_priority_score("ALM1")


@respx.mock
def test_retries_on_server_error(config, monkeypatch):
    monkeypatch.setattr("time.sleep", lambda x: None)
    route = respx.get("http://alarm.test/health").mock(
        side_effect=[
            httpx.Response(503, json={"error": "busy"}),
            httpx.Response(503, json={"error": "busy"}),
            httpx.Response(200, json={"status": "ok"}),
        ]
    )
    with AlarmApiClient(config) as client:
        result = client.health()
        assert result["status"] == "ok"
    assert route.call_count == 3


@respx.mock
def test_timeout_raises_timeout_error(config, monkeypatch):
    monkeypatch.setattr("time.sleep", lambda x: None)
    respx.get("http://alarm.test/health").mock(side_effect=httpx.ReadTimeout("slow"))
    with AlarmApiClient(config) as client:
        with pytest.raises(AlarmApiTimeoutError):
            client.health()


@respx.mock
def test_operator_recommendations_sends_alarm_id(config):
    respx.post("http://alarm.test/recommendations/operator-actions").mock(
        return_value=httpx.Response(200, json={"recommendations": []})
    )
    with AlarmApiClient(config) as client:
        client.get_operator_recommendations("ALM123")
    body = respx.calls.last.request.read()
    assert b"ALM123" in body
