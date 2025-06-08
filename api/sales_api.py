from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from utils.data_queries import (
    get_daily_sales,
    get_monthly_sales,
    get_weekly_sales,
    get_kpi_metrics,
    get_promotion_impact,
    get_product_category_sales,
    get_store_performance
)

app = FastAPI(
    title="Sales Ninja API",
    description="API for sales analytics and promotional impact analysis",
    version="1.0.0"
)

# Response Models
class SalesMetrics(BaseModel):
    total_net_sales: float
    total_volume: int
    transaction_count: int
    promotional_sales: float
    promotional_volume: int

class PromotionImpact(BaseModel):
    has_promotion: bool
    total_sales: float
    avg_sale_value: float
    total_volume: int
    avg_volume: float
    transaction_count: int

class ProductCategorySales(BaseModel):
    category_name: str
    total_sales: float
    total_volume: int
    transaction_count: int
    promotional_sales: float

class StorePerformance(BaseModel):
    store_name: str
    store_type: str
    region_country: str
    total_sales: float
    total_volume: int
    transaction_count: int

# API Routes
@app.get("/sales/daily/", response_model=List[SalesMetrics])
async def daily_sales(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get daily sales metrics between specified dates.
    """
    try:
        df = get_daily_sales(start_date, end_date)
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sales/monthly/", response_model=List[SalesMetrics])
async def monthly_sales(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get monthly aggregated sales metrics.
    """
    try:
        df = get_monthly_sales(start_date, end_date)
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sales/weekly/", response_model=List[SalesMetrics])
async def weekly_sales(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get weekly aggregated sales metrics.
    """
    try:
        df = get_weekly_sales(start_date, end_date)
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sales/kpi/", response_model=SalesMetrics)
async def kpi_metrics(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get overall KPI metrics for the specified date range.
    """
    try:
        df = get_kpi_metrics(start_date, end_date)
        return df.iloc[0].to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sales/promotion-impact/", response_model=List[PromotionImpact])
async def promotion_impact(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get promotional vs non-promotional sales comparison.
    """
    try:
        df = get_promotion_impact(start_date, end_date)
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sales/product-categories/", response_model=List[ProductCategorySales])
async def product_category_sales(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get sales metrics by product category.
    """
    try:
        df = get_product_category_sales(start_date, end_date)
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sales/store-performance/", response_model=List[StorePerformance])
async def store_performance(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get sales performance metrics by store.
    """
    try:
        df = get_store_performance(start_date, end_date)
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()} 