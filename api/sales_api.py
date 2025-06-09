from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from services.local_data import (
    get_daily_sales,
    get_daily_predictions,
    get_actuals_vs_predictions,
    get_prediction_accuracy_metrics,
    get_sales_by_region,
    get_region_time_series
)
from models.responses import (
    DailySalesResponse,
    TopProductsResponse,
    RegionalSalesResponse
)

app = FastAPI(
    title="Sales Ninja API",
    description="Backend API for Sales Analytics Dashboard",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response Models
class SalesMetrics(BaseModel):
    date: str
    total_sales: float
    total_records: int
    average_value: float

class KPIMetrics(BaseModel):
    total_sales: float
    total_volume: int
    total_orders: int
    average_order_value: float
    unique_customers: int
    promotional_sales: float
    promotional_volume: int
    promotional_orders: int

class PromotionImpact(BaseModel):
    has_promotion: bool
    total_sales: float
    avg_sale_value: float
    total_volume: int
    avg_volume: float
    total_orders: int

class ProductCategorySales(BaseModel):
    category_name: str
    total_sales: float
    total_volume: int
    total_orders: int
    promotional_sales: float

class StorePerformance(BaseModel):
    store_name: str
    store_type: str
    region_country: str
    total_sales: float
    total_volume: int
    total_orders: int

class SalesData(BaseModel):
    date: date
    total_sales: float
    total_records: int
    average_value: float

class PredictionData(BaseModel):
    date: date
    predicted_sales: float
    total_records: int
    average_predicted_value: float

class ComparisonData(BaseModel):
    date: date
    actual_sales: float
    predicted_sales: float
    actual_records: int
    predicted_records: int
    absolute_error: float
    percentage_error: Optional[float]

class AccuracyMetrics(BaseModel):
    total_predictions: int
    mae: float  # Mean Absolute Error
    rmse: float  # Root Mean Square Error
    mape: float  # Mean Absolute Percentage Error
    correlation: float

class RegionData(BaseModel):
    region: str
    country: str
    continent: str
    total_sales: float
    avg_sales: float
    total_records: int

class TimeSeriesData(BaseModel):
    date: date
    region: str
    total_sales: float
    total_records: int

class MonthlyData(BaseModel):
    year: int
    month: int
    total_sales: float
    avg_sales: float
    total_records: int

class QuarterlyData(BaseModel):
    year: int
    quarter: int
    total_sales: float
    avg_sales: float
    total_records: int

# API Routes
@app.get("/")
async def root():
    return {"message": "Welcome to Sales Ninja API"}

@app.get("/api/daily-sales", response_model=List[SalesMetrics])
async def daily_sales_endpoint(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get daily sales data between start_date and end_date
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
        return await get_daily_sales(start, end)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/monthly-sales", response_model=List[SalesMetrics])
async def monthly_sales_endpoint(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get monthly aggregated sales data
    """
    try:
        return await get_daily_sales(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/kpi-metrics", response_model=KPIMetrics)
async def kpi_metrics_endpoint(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get overall KPI metrics for the specified date range
    """
    try:
        return await get_daily_sales(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/promotion-impact", response_model=List[PromotionImpact])
async def promotion_impact_endpoint(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get promotional vs non-promotional sales comparison
    """
    try:
        return await get_daily_sales(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/product-categories", response_model=List[ProductCategorySales])
async def product_category_sales_endpoint(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get sales metrics by product category
    """
    try:
        return await get_daily_sales(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/store-performance", response_model=List[StorePerformance])
async def store_performance_endpoint(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """
    Get sales performance by store
    """
    try:
        return await get_daily_sales(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/actuals", response_model=List[SalesData])
async def get_actuals(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get actual sales data between start_date and end_date
    """
    try:
        return await get_daily_sales(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/predictions", response_model=List[PredictionData])
async def get_predictions(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get sales predictions between start_date and end_date
    """
    try:
        return await get_daily_predictions(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/comparison", response_model=List[ComparisonData])
async def get_comparison(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get comparison between actual sales and predictions
    """
    try:
        return await get_actuals_vs_predictions(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/accuracy", response_model=AccuracyMetrics)
async def get_accuracy(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get prediction accuracy metrics
    """
    try:
        return await get_prediction_accuracy_metrics(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regions", response_model=List[RegionData])
async def get_regions(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get sales data aggregated by region"""
    try:
        return await get_sales_by_region(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/region/{region}/timeseries", response_model=List[TimeSeriesData])
async def get_region_sales(
    region: str,
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """Get daily sales time series for a specific region"""
    try:
        return await get_region_time_series(region, start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/monthly", response_model=List[MonthlyData])
async def get_monthly_data(
    year: Optional[int] = Query(None, description="Filter by year (YYYY)")
):
    """Get monthly aggregated sales data"""
    try:
        return await get_daily_sales(None, None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quarterly", response_model=List[QuarterlyData])
async def get_quarterly_data(
    year: Optional[int] = Query(None, description="Filter by year (YYYY)")
):
    """Get quarterly aggregated sales data"""
    try:
        return await get_daily_sales(None, None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "healthy"} 