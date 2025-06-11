import requests
from typing import Dict, Any, Optional
from datetime import datetime, date

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to the API endpoint."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method, url, **kwargs)
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
        return self._make_request("GET", "api/daily-sales", params=params)

    def get_predictions(self, start_date: str, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get sales predictions."""
        params = {"start_date": start_date}
        if end_date:
            params["end_date"] = end_date
        return self._make_request("GET", "api/predictions", params=params)

    def get_regions(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get regional sales data."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._make_request("GET", "api/regions", params=params)

    def get_kpi_metrics(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get KPI metrics."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._make_request("GET", "api/kpi-metrics", params=params)

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics."""
        return self._make_request("GET", "api/dashboard/stats")

    def get_sales_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get sales data for a specific date range."""
        params = {"start_date": start_date, "end_date": end_date}
        return self._make_request("GET", "api/sales", params=params)

    def get_inventory_status(self) -> Dict[str, Any]:
        """Get current inventory status."""
        return self._make_request("GET", "api/inventory/status")

    def get_top_products(self, limit: int = 10) -> Dict[str, Any]:
        """Get top selling products."""
        params = {"limit": limit}
        return self._make_request("GET", "api/products/top", params=params) 