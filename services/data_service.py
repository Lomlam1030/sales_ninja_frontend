from google.cloud import bigquery
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict, Any
import logging
from config.bq_client import client, PROJECT_ID, DATASET, ACTUALS_TABLE, PREDICTIONS_TABLE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_daily_sales(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """Get daily sales metrics between start_date and end_date"""
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = f"""
    SELECT
        DATE(DateKey) as date,
        SUM(SalesAmount) as total_sales,
        COUNT(*) as total_records,
        AVG(SalesAmount) as average_value
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
    GROUP BY date
    ORDER BY date
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        return [
            {
                'date': row.date.isoformat(),
                'total_sales': float(row.total_sales),
                'total_records': int(row.total_records),
                'average_value': float(row.average_value)
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching daily sales: {str(e)}")
        raise

async def get_daily_predictions(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """Get daily sales predictions between start_date and end_date"""
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = f"""
    SELECT
        DATE(DateKey) as date,
        SUM(SalesAmount) as predicted_sales,
        COUNT(*) as total_records,
        AVG(SalesAmount) as average_predicted_value
    FROM `{PROJECT_ID}.{DATASET}.{PREDICTIONS_TABLE}`
    WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
    GROUP BY date
    ORDER BY date
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        return [
            {
                'date': row.date.isoformat(),
                'predicted_sales': float(row.predicted_sales),
                'total_records': int(row.total_records),
                'average_predicted_value': float(row.average_predicted_value)
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching predictions: {str(e)}")
        raise

async def get_actuals_vs_predictions(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """Get comparison of actual sales vs predictions"""
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = f"""
    WITH actuals AS (
        SELECT
            DATE(DateKey) as date,
            SUM(SalesAmount) as actual_sales,
            COUNT(*) as actual_records
        FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
        WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
        GROUP BY date
    ),
    predictions AS (
        SELECT
            DATE(DateKey) as date,
            SUM(SalesAmount) as predicted_sales,
            COUNT(*) as predicted_records
        FROM `{PROJECT_ID}.{DATASET}.{PREDICTIONS_TABLE}`
        WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
        GROUP BY date
    )
    SELECT
        COALESCE(a.date, p.date) as date,
        COALESCE(a.actual_sales, 0) as actual_sales,
        COALESCE(p.predicted_sales, 0) as predicted_sales,
        COALESCE(a.actual_records, 0) as actual_records,
        COALESCE(p.predicted_records, 0) as predicted_records,
        ABS(COALESCE(a.actual_sales, 0) - COALESCE(p.predicted_sales, 0)) as absolute_error,
        CASE 
            WHEN a.actual_sales > 0 
            THEN ABS(a.actual_sales - COALESCE(p.predicted_sales, 0)) / a.actual_sales * 100
            ELSE NULL 
        END as percentage_error
    FROM actuals a
    FULL OUTER JOIN predictions p ON a.date = p.date
    ORDER BY date
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        return [
            {
                'date': row.date.isoformat(),
                'actual_sales': float(row.actual_sales),
                'predicted_sales': float(row.predicted_sales),
                'actual_records': int(row.actual_records),
                'predicted_records': int(row.predicted_records),
                'absolute_error': float(row.absolute_error),
                'percentage_error': float(row.percentage_error) if row.percentage_error is not None else None
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching comparison: {str(e)}")
        raise

async def get_sales_by_region(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """Get sales data aggregated by region"""
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = f"""
    SELECT
        StoreName as region,
        ContinentName as continent,
        SUM(SalesAmount) as total_sales,
        AVG(SalesAmount) as average_sales,
        COUNT(*) as total_records
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
    GROUP BY StoreName, ContinentName
    ORDER BY total_sales DESC
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        return [
            {
                'region': str(row.region),
                'continent': str(row.continent),
                'total_sales': float(row.total_sales),
                'average_sales': float(row.average_sales),
                'total_records': int(row.total_records)
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching region data: {str(e)}")
        raise

async def get_kpi_metrics(start_date: date, end_date: date) -> Dict[str, Any]:
    """Get overall KPI metrics"""
    query = f"""
    SELECT
        SUM(SalesAmount) as total_sales,
        COUNT(*) as total_orders,
        AVG(SalesAmount) as average_order_value,
        COUNT(DISTINCT SalesKey) as unique_orders
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        for row in results:
            return {
                "total_sales": float(row.total_sales),
                "total_orders": int(row.total_orders),
                "average_order_value": float(row.average_order_value),
                "unique_orders": int(row.unique_orders)
            }
        return {}
    except Exception as e:
        logger.error(f"Error fetching KPI metrics: {str(e)}")
        raise

async def get_monthly_sales(start_date: date, end_date: date) -> List[dict]:
    """Get monthly aggregated sales metrics"""
    query = f"""
    SELECT
        FORMAT_DATE('%Y-%m', date) as month,
        SUM(value) as total_sales,
        AVG(value) as average_order_value,
        COUNT(*) as total_records,
        COUNT(DISTINCT customer_id) as unique_customers,
        COUNT(DISTINCT order_id) as total_orders
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    WHERE DATE(date) BETWEEN @start_date AND @end_date
    GROUP BY month
    ORDER BY month
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    return [dict(row) for row in results]

async def get_quarterly_sales(start_date: date, end_date: date) -> List[dict]:
    """Get quarterly aggregated sales metrics"""
    query = f"""
    SELECT
        FORMAT_DATE('%Y-Q%Q', date) as quarter,
        SUM(value) as total_sales,
        AVG(value) as average_order_value,
        COUNT(*) as total_records,
        COUNT(DISTINCT customer_id) as unique_customers,
        COUNT(DISTINCT order_id) as total_orders
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    WHERE DATE(date) BETWEEN @start_date AND @end_date
    GROUP BY quarter
    ORDER BY quarter
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    return [dict(row) for row in results]

async def get_region_time_series(region: str, start_date: date, end_date: date) -> List[dict]:
    """Get daily sales time series for a specific region"""
    query = f"""
    SELECT
        DATE(date) as date,
        SUM(value) as sales,
        COUNT(*) as transactions,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    WHERE 
        DATE(date) BETWEEN @start_date AND @end_date
        AND region = @region
    GROUP BY date
    ORDER BY date
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
            bigquery.ScalarQueryParameter("region", "STRING", region),
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    return [dict(row) for row in results]

async def get_top_products(start_date: date, end_date: Optional[date] = None, limit: int = 10) -> List[dict]:
    """Get top selling products"""
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = f"""
    SELECT
        product_id,
        SUM(value) as total_sales,
        COUNT(*) as total_transactions,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    WHERE DATE(date) BETWEEN @start_date AND @end_date
    GROUP BY product_id
    ORDER BY total_sales DESC
    LIMIT @limit
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    return [dict(row) for row in results] 