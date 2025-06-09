from google.cloud import bigquery
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict, Any
import os
from config.bq_client import client

PROJECT_ID = "nodal-clock-456815-g3"

# Initialize BigQuery client
# client = bigquery.Client()

async def get_daily_sales(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """
    Get daily sales metrics between start_date and end_date
    """
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = """
    SELECT
        DATE(date) as date,
        SUM(value) as total_sales,
        COUNT(*) as total_records,
        AVG(value) as average_value
    FROM `nodal-clock-456815-g3.sales_data.dashboard_merged_data`
    WHERE DATE(date) BETWEEN @start_date AND @end_date
    GROUP BY date
    ORDER BY date
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

async def get_daily_predictions(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """
    Get daily sales predictions between start_date and end_date
    """
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = """
    SELECT
        DATE(date) as date,
        SUM(value) as predicted_sales,
        COUNT(*) as total_records,
        AVG(value) as average_predicted_value
    FROM `nodal-clock-456815-g3.sales_data.dashboard_prediction_data`
    WHERE DATE(date) BETWEEN @start_date AND @end_date
    GROUP BY date
    ORDER BY date
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

async def get_actuals_vs_predictions(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """
    Get comparison of actual sales vs predictions
    """
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = """
    WITH actuals AS (
        SELECT
            DATE(date) as date,
            SUM(value) as actual_sales,
            COUNT(*) as actual_records
        FROM `nodal-clock-456815-g3.sales_data.dashboard_merged_data`
        WHERE DATE(date) BETWEEN @start_date AND @end_date
        GROUP BY date
    ),
    predictions AS (
        SELECT
            DATE(date) as date,
            SUM(value) as predicted_sales,
            COUNT(*) as predicted_records
        FROM `nodal-clock-456815-g3.sales_data.dashboard_prediction_data`
        WHERE DATE(date) BETWEEN @start_date AND @end_date
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
            THEN ABS(a.actual_sales - COALESCE(p.predicted_sales, 0)) / a.actual_sales 
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
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    return [dict(row) for row in results]

async def get_prediction_accuracy_metrics(start_date: date, end_date: Optional[date] = None) -> Dict[str, Any]:
    """
    Get overall prediction accuracy metrics
    """
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = """
    WITH comparison AS (
        SELECT
            a.date,
            a.value as actual_value,
            p.value as predicted_value,
            ABS(a.value - p.value) as absolute_error,
            POW(a.value - p.value, 2) as squared_error,
            ABS(a.value - p.value) / NULLIF(a.value, 0) as percentage_error
        FROM `nodal-clock-456815-g3.sales_data.dashboard_merged_data` a
        JOIN `nodal-clock-456815-g3.sales_data.dashboard_prediction_data` p 
        ON a.date = p.date
        WHERE DATE(a.date) BETWEEN @start_date AND @end_date
    )
    SELECT
        COUNT(*) as total_predictions,
        AVG(absolute_error) as mae,
        SQRT(AVG(squared_error)) as rmse,
        AVG(percentage_error) * 100 as mape,
        CORR(actual_value, predicted_value) as correlation
    FROM comparison
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    # Return the first (and only) row as a dict
    for row in results:
        return dict(row)
    return {}

async def get_monthly_sales(start_date: date, end_date: date) -> List[dict]:
    """
    Get monthly aggregated sales metrics
    """
    query = """
    SELECT
        FORMAT_DATE('%Y-%m', DateKey) as month,
        SUM(NetSales) as total_sales,
        SUM(SalesQuantity) as total_volume,
        COUNT(DISTINCT SalesKey) as total_orders,
        SUM(amount) / COUNT(DISTINCT SalesKey) as average_order_value,
        COUNT(DISTINCT CustomerKey) as unique_customers,
        SUM(CASE WHEN PromotionKey != 1 THEN NetSales ELSE 0 END) as promotional_sales,
        SUM(CASE WHEN PromotionKey != 1 THEN SalesQuantity ELSE 0 END) as promotional_volume
    FROM `your_project.your_dataset.sales_data`
    WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
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

async def get_kpi_metrics(start_date: date, end_date: date) -> Dict[str, Any]:
    """
    Get overall KPI metrics for the specified date range
    """
    query = """
    SELECT
        SUM(NetSales) as total_sales,
        SUM(SalesQuantity) as total_volume,
        COUNT(DISTINCT SalesKey) as total_orders,
        SUM(NetSales) / COUNT(DISTINCT SalesKey) as average_order_value,
        COUNT(DISTINCT CustomerKey) as unique_customers,
        SUM(CASE WHEN PromotionKey != 1 THEN NetSales ELSE 0 END) as promotional_sales,
        SUM(CASE WHEN PromotionKey != 1 THEN SalesQuantity ELSE 0 END) as promotional_volume,
        COUNT(DISTINCT CASE WHEN PromotionKey != 1 THEN SalesKey END) as promotional_orders
    FROM `your_project.your_dataset.sales_data`
    WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    # Return the first (and only) row as a dict
    for row in results:
        return dict(row)
    return {}

async def get_promotion_impact(start_date: date, end_date: date) -> List[dict]:
    """
    Get promotional vs non-promotional sales comparison
    """
    query = """
    SELECT
        CASE WHEN PromotionKey != 1 THEN TRUE ELSE FALSE END as has_promotion,
        SUM(NetSales) as total_sales,
        AVG(NetSales) as avg_sale_value,
        SUM(SalesQuantity) as total_volume,
        AVG(SalesQuantity) as avg_volume,
        COUNT(DISTINCT SalesKey) as total_orders
    FROM `your_project.your_dataset.sales_data`
    WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
    GROUP BY has_promotion
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

async def get_product_category_sales(start_date: date, end_date: date) -> List[dict]:
    """
    Get sales metrics by product category
    """
    query = """
    SELECT
        ProductCategoryName as category_name,
        SUM(NetSales) as total_sales,
        SUM(SalesQuantity) as total_volume,
        COUNT(DISTINCT SalesKey) as total_orders,
        SUM(CASE WHEN PromotionKey != 1 THEN NetSales ELSE 0 END) as promotional_sales
    FROM `your_project.your_dataset.sales_data`
    WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
    GROUP BY ProductCategoryName
    ORDER BY total_sales DESC
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

async def get_store_performance(start_date: date, end_date: date) -> List[dict]:
    """
    Get sales performance by store
    """
    query = """
    SELECT
        StoreName as store_name,
        StoreType as store_type,
        RegionCountryName as region_country,
        SUM(NetSales) as total_sales,
        SUM(SalesQuantity) as total_volume,
        COUNT(DISTINCT SalesKey) as total_orders
    FROM `your_project.your_dataset.sales_data`
    WHERE DATE(DateKey) BETWEEN @start_date AND @end_date
    GROUP BY StoreName, StoreType, RegionCountryName
    ORDER BY total_sales DESC
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

# Geography Analysis
async def get_sales_by_region(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """Get sales data aggregated by region"""
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = """
    SELECT
        region,
        country,
        continent,
        SUM(value) as total_sales,
        AVG(value) as avg_sales,
        COUNT(*) as total_records
    FROM `nodal-clock-456815-g3.sales_data.dashboard_merged_data`
    WHERE DATE(date) BETWEEN @start_date AND @end_date
    GROUP BY region, country, continent
    ORDER BY total_sales DESC
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
    query = """
    SELECT
        DATE(date) as date,
        region,
        SUM(value) as total_sales,
        COUNT(*) as total_records
    FROM `nodal-clock-456815-g3.sales_data.dashboard_merged_data`
    WHERE 
        DATE(date) BETWEEN @start_date AND @end_date
        AND region = @region
    GROUP BY date, region
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

# Time-based Aggregations
async def get_monthly_aggregates(year: Optional[int] = None) -> List[dict]:
    """Get monthly aggregated sales data"""
    query = """
    SELECT
        EXTRACT(YEAR FROM date) as year,
        EXTRACT(MONTH FROM date) as month,
        SUM(value) as total_sales,
        AVG(value) as avg_sales,
        COUNT(*) as total_records
    FROM `nodal-clock-456815-g3.sales_data.dashboard_merged_data`
    {where_clause}
    GROUP BY year, month
    ORDER BY year, month
    """
    
    where_clause = f"WHERE EXTRACT(YEAR FROM date) = @year" if year else ""
    params = [bigquery.ScalarQueryParameter("year", "INT64", year)] if year else []
    
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    query_job = client.query(query.format(where_clause=where_clause), job_config=job_config)
    results = query_job.result()
    
    return [dict(row) for row in results]

async def get_quarterly_aggregates(year: Optional[int] = None) -> List[dict]:
    """Get quarterly aggregated sales data"""
    query = """
    SELECT
        EXTRACT(YEAR FROM date) as year,
        EXTRACT(QUARTER FROM date) as quarter,
        SUM(value) as total_sales,
        AVG(value) as avg_sales,
        COUNT(*) as total_records
    FROM `nodal-clock-456815-g3.sales_data.dashboard_merged_data`
    {where_clause}
    GROUP BY year, quarter
    ORDER BY year, quarter
    """
    
    where_clause = f"WHERE EXTRACT(YEAR FROM date) = @year" if year else ""
    params = [bigquery.ScalarQueryParameter("year", "INT64", year)] if year else []
    
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    query_job = client.query(query.format(where_clause=where_clause), job_config=job_config)
    results = query_job.result()
    
    return [dict(row) for row in results]

# Add your additional query functions here:
# async def get_customer_metrics(...):
# async def get_product_categories(...):
# etc. 

async def get_top_products(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """
    Get top selling products between start_date and end_date
    """
    if not end_date:
        end_date = start_date + timedelta(days=30)

    query = """
    SELECT
        product_name,
        SUM(value) as total_sales,
        COUNT(*) as total_orders,
        AVG(value) as average_order_value
    FROM `nodal-clock-456815-g3.sales_data.dashboard_merged_data`
    WHERE DATE(date) BETWEEN @start_date AND @end_date
    GROUP BY product_name
    ORDER BY total_sales DESC
    LIMIT 10
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