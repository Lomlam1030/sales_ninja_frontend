import requests
from typing import Dict, Any, Optional
from datetime import datetime, date

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request to the API endpoint."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {str(e)}")
            return None

    def get_daily_sales(self, start_date: str, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get daily sales data."""
        params = {"start_date": start_date}
        if end_date:
            params["end_date"] = end_date
        return self._make_request("api/daily-sales", params)

    def get_predictions(self, start_date: str, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get sales predictions."""
        params = {"start_date": start_date}
        if end_date:
            params["end_date"] = end_date
        return self._make_request("api/predictions", params)

    def get_regions(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get regional sales data."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._make_request("api/regions", params)

    def get_kpi_metrics(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get KPI metrics."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._make_request("api/kpi-metrics", params) 