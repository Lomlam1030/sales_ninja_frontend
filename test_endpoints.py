import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_daily_sales():
    """Test the daily sales endpoint"""
    start_date = "2007-01-01"
    end_date = "2007-01-31"
    
    response = requests.get(
        f"{BASE_URL}/api/daily-sales",
        params={"start_date": start_date, "end_date": end_date}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Daily Sales Endpoint:")
        print(f"Number of records: {len(data)}")
        if data:
            print("Sample record:", data[0])
    else:
        print("\n❌ Daily Sales Endpoint Error:", response.text)

def test_predictions():
    """Test the predictions endpoint"""
    start_date = "2007-01-01"
    end_date = "2007-01-31"
    
    response = requests.get(
        f"{BASE_URL}/api/predictions",
        params={"start_date": start_date, "end_date": end_date}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Predictions Endpoint:")
        print(f"Number of records: {len(data)}")
        if data:
            print("Sample record:", data[0])
    else:
        print("\n❌ Predictions Endpoint Error:", response.text)

def test_regions():
    """Test the regions endpoint"""
    start_date = "2007-01-01"
    end_date = "2007-01-31"
    
    response = requests.get(
        f"{BASE_URL}/api/regions",
        params={"start_date": start_date, "end_date": end_date}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Regions Endpoint:")
        print(f"Number of regions: {len(data)}")
        if data:
            print("Sample region:", data[0])
    else:
        print("\n❌ Regions Endpoint Error:", response.text)

def test_kpi_metrics():
    """Test the KPI metrics endpoint"""
    start_date = "2007-01-01"
    end_date = "2007-01-31"
    
    response = requests.get(
        f"{BASE_URL}/api/kpi-metrics",
        params={"start_date": start_date, "end_date": end_date}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ KPI Metrics Endpoint:")
        print("Metrics:", data)
    else:
        print("\n❌ KPI Metrics Endpoint Error:", response.text)

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_daily_sales()
    test_predictions()
    test_regions()
    test_kpi_metrics()
    print("\nDone testing!") 