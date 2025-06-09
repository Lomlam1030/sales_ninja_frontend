from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from typing import List, Optional
from services.data_service import (
    get_daily_sales,
    get_daily_predictions,
    get_sales_by_region,
    get_kpi_metrics,
    get_actuals_vs_predictions
)

app = FastAPI(
    title="Sales Ninja API",
    description="Backend API for Sales Analytics Dashboard",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Sales Ninja API"}

@app.get("/api/daily-sales")
async def daily_sales_endpoint(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get daily sales data between start_date and end_date"""
    try:
        # Convert string dates to date objects
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
        
        return await get_daily_sales(start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/predictions")
async def predictions_endpoint(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get sales predictions between start_date and end_date"""
    try:
        # Convert string dates to date objects
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
        
        return await get_daily_predictions(start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regions")
async def regions_endpoint(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get sales data aggregated by region"""
    try:
        # Convert string dates to date objects
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
        
        return await get_sales_by_region(start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/kpi-metrics")
async def kpi_metrics_endpoint(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get overall KPI metrics"""
    try:
        # Convert string dates to date objects
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
        
        return await get_kpi_metrics(start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/actuals-vs-predictions")
async def actuals_vs_predictions_endpoint(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get comparison of actual sales vs predictions"""
    try:
        # Convert string dates to date objects
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
        
        return await get_actuals_vs_predictions(start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 