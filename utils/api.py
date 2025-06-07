import requests
from typing import Dict, Any, Optional

class APIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to the API endpoint."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics."""
        return self._make_request("GET", "/api/dashboard/stats")

    def get_sales_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get sales data for a specific date range."""
        params = {"start_date": start_date, "end_date": end_date}
        return self._make_request("GET", "/api/sales", params=params)

    def get_inventory_status(self) -> Dict[str, Any]:
        """Get current inventory status."""
        return self._make_request("GET", "/api/inventory/status")

    def get_top_products(self, limit: int = 10) -> Dict[str, Any]:
        """Get top selling products."""
        params = {"limit": limit}
        return self._make_request("GET", "/api/products/top", params=params) 