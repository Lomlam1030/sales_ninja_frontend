from google.cloud import bigquery
import pandas as pd
from typing import Optional
from datetime import datetime

# Initialize BigQuery client
client = bigquery.Client()

def get_daily_sales(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Get daily sales data between specified dates.
    """
    query = f"""
        SELECT
            DATE(DateKey) AS date,
            SUM(NetSales) AS total_net_sales,
            SUM(SalesQuantity) AS total_volume,
            COUNT(DISTINCT SalesKey) AS transaction_count,
            SUM(CASE WHEN PromotionKey != 1 THEN NetSales ELSE 0 END) AS promotional_sales,
            SUM(CASE WHEN PromotionKey != 1 THEN SalesQuantity ELSE 0 END) AS promotional_volume
        FROM `sales_data`
        WHERE DATE(DateKey) BETWEEN DATE('{start_date.strftime('%Y-%m-%d')}') 
            AND DATE('{end_date.strftime('%Y-%m-%d')}')
        GROUP BY date
        ORDER BY date
    """
    return client.query(query).to_dataframe()

def get_monthly_sales(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Get monthly aggregated sales data.
    """
    query = f"""
        SELECT
            FORMAT_DATE('%Y-%m', DateKey) AS month,
            SUM(NetSales) AS total_net_sales,
            SUM(SalesQuantity) AS total_volume,
            COUNT(DISTINCT SalesKey) AS transaction_count,
            SUM(CASE WHEN PromotionKey != 1 THEN NetSales ELSE 0 END) AS promotional_sales,
            SUM(CASE WHEN PromotionKey != 1 THEN SalesQuantity ELSE 0 END) AS promotional_volume
        FROM `sales_data`
        WHERE DATE(DateKey) BETWEEN DATE('{start_date.strftime('%Y-%m-%d')}') 
            AND DATE('{end_date.strftime('%Y-%m-%d')}')
        GROUP BY month
        ORDER BY month
    """
    return client.query(query).to_dataframe()

def get_weekly_sales(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Get weekly aggregated sales data.
    """
    query = f"""
        SELECT
            CalendarWeekLabel AS week,
            SUM(NetSales) AS total_net_sales,
            SUM(SalesQuantity) AS total_volume,
            COUNT(DISTINCT SalesKey) AS transaction_count,
            SUM(CASE WHEN PromotionKey != 1 THEN NetSales ELSE 0 END) AS promotional_sales,
            SUM(CASE WHEN PromotionKey != 1 THEN SalesQuantity ELSE 0 END) AS promotional_volume
        FROM `sales_data`
        WHERE DATE(DateKey) BETWEEN DATE('{start_date.strftime('%Y-%m-%d')}') 
            AND DATE('{end_date.strftime('%Y-%m-%d')}')
        GROUP BY week
        ORDER BY week
    """
    return client.query(query).to_dataframe()

def get_kpi_metrics(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Get overall KPI metrics for the specified date range.
    """
    query = f"""
        SELECT
            SUM(NetSales) AS total_net_sales,
            SUM(SalesQuantity) AS total_volume,
            COUNT(DISTINCT SalesKey) AS total_transactions,
            AVG(NetSales) AS avg_transaction_value,
            SUM(CASE WHEN PromotionKey != 1 THEN NetSales ELSE 0 END) AS promotional_sales,
            SUM(CASE WHEN PromotionKey != 1 THEN SalesQuantity ELSE 0 END) AS promotional_volume,
            COUNT(DISTINCT CASE WHEN PromotionKey != 1 THEN SalesKey END) AS promotional_transactions
        FROM `sales_data`
        WHERE DATE(DateKey) BETWEEN DATE('{start_date.strftime('%Y-%m-%d')}') 
            AND DATE('{end_date.strftime('%Y-%m-%d')}')
    """
    return client.query(query).to_dataframe()

def get_promotion_impact(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Get promotional vs non-promotional sales comparison.
    """
    query = f"""
        SELECT
            CASE WHEN PromotionKey != 1 THEN TRUE ELSE FALSE END AS has_promotion,
            SUM(NetSales) AS total_sales,
            AVG(NetSales) AS avg_sale_value,
            SUM(SalesQuantity) AS total_volume,
            AVG(SalesQuantity) AS avg_volume,
            COUNT(DISTINCT SalesKey) AS transaction_count
        FROM `sales_data`
        WHERE DATE(DateKey) BETWEEN DATE('{start_date.strftime('%Y-%m-%d')}') 
            AND DATE('{end_date.strftime('%Y-%m-%d')}')
        GROUP BY has_promotion
    """
    return client.query(query).to_dataframe()

def get_product_category_sales(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Get sales by product category.
    """
    query = f"""
        SELECT
            ProductCategoryName,
            SUM(NetSales) AS total_sales,
            SUM(SalesQuantity) AS total_volume,
            COUNT(DISTINCT SalesKey) AS transaction_count,
            SUM(CASE WHEN PromotionKey != 1 THEN NetSales ELSE 0 END) AS promotional_sales
        FROM `sales_data`
        WHERE DATE(DateKey) BETWEEN DATE('{start_date.strftime('%Y-%m-%d')}') 
            AND DATE('{end_date.strftime('%Y-%m-%d')}')
        GROUP BY ProductCategoryName
        ORDER BY total_sales DESC
    """
    return client.query(query).to_dataframe()

def get_store_performance(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Get sales performance by store.
    """
    query = f"""
        SELECT
            StoreName,
            StoreType,
            RegionCountryName,
            SUM(NetSales) AS total_sales,
            SUM(SalesQuantity) AS total_volume,
            COUNT(DISTINCT SalesKey) AS transaction_count
        FROM `sales_data`
        WHERE DATE(DateKey) BETWEEN DATE('{start_date.strftime('%Y-%m-%d')}') 
            AND DATE('{end_date.strftime('%Y-%m-%d')}')
        GROUP BY StoreName, StoreType, RegionCountryName
        ORDER BY total_sales DESC
    """
    return client.query(query).to_dataframe() 