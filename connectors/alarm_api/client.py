import time
import uuid
import httpx

from connectors.alarm_api.config import AlarmApiConfig
from connectors.alarm_api.errors import (
    AlarmApiAuthError,
    AlarmApiError,
    AlarmApiNotFoundError,
    AlarmApiTimeoutError,
    AlarmApiValidationError,
)


class AlarmApiClient:
    """HTTP client for the Alarm Management API."""

    def __init__(self, config=None):
        self.config = config or AlarmApiConfig()
        self.client = httpx.Client(
            base_url=self.config.normalized_base_url,
            timeout=self.config.timeout_seconds,
            headers={
                "Accept": "application/json",
                "User-Agent": "alarm-investigation-connector/0.1",
            },
        )

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def health(self):
        return self._request("GET", "/health", auth=False)

    def search_assets(self, query, site=None, unit=None, equipment_type=None, limit=25):
        params = {"query": query, "limit": limit}
        if site:
            params["site"] = site
        if unit:
            params["unit"] = unit
        if equipment_type:
            params["equipment_type"] = equipment_type
        return self._request("GET", "/assets/search", params=params)

    def get_asset_metadata(self, asset_id):
        return self._request("GET", f"/assets/{asset_id}/metadata")

    def get_alarms(self, asset_id=None, severity=None, status=None, 
                   start_time=None, end_time=None, page=1, page_size=50):
        params = {"page": page, "page_size": page_size}
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
        return self._request("GET", "/alarms", params=params)

    def get_alarm(self, alarm_id):
        return self._request("GET", f"/alarms/{alarm_id}")

    def get_alarm_summary(self, payload):
        return self._request("POST", "/alarms/summary", json=payload)

    def correlate_alarms(self, payload):
        return self._request("POST", "/alarms/correlation", json=payload)

    def get_priority_score(self, alarm_id, weights=None):
        body = {"alarm_id": alarm_id}
        if weights:
            body.update(weights)
        return self._request("POST", "/alarms/priority-score", json=body)

    def get_operator_recommendations(self, alarm_id):
        body = {
            "alarm_id": alarm_id,
            "include_related": True,
            "include_asset_context": True,
            "include_historical_pattern": True,
        }
        return self._request("POST", "/recommendations/operator-actions", json=body)

    def _request(self, method, path, params=None, json=None, auth=True):
        """Make HTTP request with retries."""
        trace_id = str(uuid.uuid4())
        headers = self._build_headers(trace_id, auth)
        
        max_attempts = self.config.retry_count + 1
        for attempt in range(max_attempts):
            try:
                response = self.client.request(
                    method, path, params=params, json=json, headers=headers
                )
                
                if response.status_code in [429, 502, 503, 504] and attempt < max_attempts - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                
                return self._handle_response(response)
                
            except httpx.TimeoutException:
                if attempt < max_attempts - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raise AlarmApiTimeoutError(f"Timeout: {method} {path}")
            
            except httpx.RequestError as e:
                if attempt < max_attempts - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raise AlarmApiError(f"Request failed: {str(e)}")
        
        raise AlarmApiError(f"Failed after {max_attempts} attempts")
    
    def _build_headers(self, trace_id, auth):
        headers = {
            "trace-id": trace_id,
            "x-client-id": self.config.client_id,
            "x-metadata-tag": self.config.metadata_tag,
        }
        if auth:
            headers["Authorization"] = f"Bearer {self.config.token}"
        return headers
    
    def _handle_response(self, response):
        status = response.status_code
        
        try:
            data = response.json() if response.content else {}
        except:
            data = {"text": response.text}
        
        if status in [401, 403]:
            raise AlarmApiAuthError("Authentication failed", status, data)
        if status == 404:
            raise AlarmApiNotFoundError("Resource not found", status, data)
        if status in [400, 422]:
            raise AlarmApiValidationError("Validation error", status, data)
        if status >= 400:
            raise AlarmApiError(f"HTTP {status}", status, data)
        
        return data
