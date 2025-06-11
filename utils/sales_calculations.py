"""Sales calculation utilities for the Sales Ninja dashboard."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from google.cloud import bigquery
from config.bq_client import client, PROJECT_ID, DATASET, ACTUALS_TABLE, PREDICTIONS_TABLE

from services.data_source import get_data_source
from config.settings import settings

def load_dashboard_data(
    year: Optional[int] = 2007,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and prepare both actual and predicted sales data from BigQuery.
    
    Args:
        year (Optional[int]): Filter data for specific year (defaults to 2007)
        start_date (Optional[str]): Start date in YYYY-MM-DD format (overrides year if provided)
        end_date (Optional[str]): End date in YYYY-MM-DD format (overrides year if provided)
        limit (Optional[int]): If provided, limits the number of rows returned
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Tuple containing (actual_data, predicted_data)
    """
    # Essential columns for the dashboard
    common_columns = """
        DateKey,
        SalesAmount as net_sales,
        ContinentName as continent,
        CalendarYear as year,
        MonthNumber as month,
        CalendarMonthLabel as month_name,
        CalendarQuarterLabel as quarter,
        ProductName,
        ProductCategoryName,
        PromotionName,
        StoreName,
        StoreType,
        SalesQuantity,
        ReturnQuantity,
        DiscountAmount
    """
    
    # Build WHERE clause
    where_conditions = []
    if year:
        where_conditions.append(f"CalendarYear = {year}")
    if start_date:
        where_conditions.append(f"DateKey >= '{start_date}'")
    if end_date:
        where_conditions.append(f"DateKey <= '{end_date}'")
    
    where_clause = ""
    if where_conditions:
        where_clause = "WHERE " + " AND ".join(where_conditions)
    
    # Load actual data with specific columns
    actual_query = f"""
    SELECT DISTINCT
        {common_columns},
        RegionCountryName as country
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    {where_clause}
    ORDER BY DateKey
    """
    
    # Load predicted data with specific columns
    predicted_query = f"""
    SELECT DISTINCT
        {common_columns}
    FROM `{PROJECT_ID}.{DATASET}.{PREDICTIONS_TABLE}`
    {where_clause}
    ORDER BY DateKey
    """
    
    if limit:
        actual_query += f" LIMIT {limit}"
        predicted_query += f" LIMIT {limit}"
    
    try:
        print("Loading actual sales data...")
        print(f"Query filters: {where_clause if where_conditions else 'None'}")
        
        job_config = bigquery.QueryJobConfig(
            allow_large_results=True,
            use_query_cache=True
        )
        
        # Execute queries with job configuration
        df_actual = client.query(actual_query, job_config=job_config).to_dataframe()
        print(f"Loaded {len(df_actual):,} rows of actual data")
        
        print("\nLoading predicted sales data...")
        df_predicted = client.query(predicted_query, job_config=job_config).to_dataframe()
        print(f"Loaded {len(df_predicted):,} rows of predicted data")
        
        # Convert date columns to datetime
        print("\nProcessing dates...")
        df_actual['date'] = pd.to_datetime(df_actual['DateKey'])
        df_predicted['date'] = pd.to_datetime(df_predicted['DateKey'])
        
        return df_actual, df_predicted
        
    except Exception as e:
        print(f"Error loading data from BigQuery: {str(e)}")
        raise

def calculate_daily_net_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily net sales from transaction data."""
    return df.groupby('date')['net_sales'].sum().reset_index()

def get_sales_summary_stats(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate summary statistics for sales data."""
    return {
        'total_sales': df['net_sales'].sum(),
        'avg_daily_sales': df['net_sales'].mean(),
        'max_daily_sales': df['net_sales'].max(),
        'min_daily_sales': df['net_sales'].min(),
        'total_transactions': len(df),
        'total_quantity': df['SalesQuantity'].sum()
    }

def calculate_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales performance by product category."""
    return df.groupby('ProductCategoryName').agg({
        'net_sales': ['sum', 'mean', 'count'],
        'SalesQuantity': 'sum'
    }).round(2)

def calculate_store_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales performance by store."""
    return df.groupby(['StoreName', 'StoreType']).agg({
        'net_sales': ['sum', 'mean', 'count'],
        'SalesQuantity': 'sum'
    }).round(2)

def calculate_promotion_impact(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the impact of promotions on sales."""
    promotion_stats = df.groupby('PromotionName').agg({
        'net_sales': ['mean', 'sum', 'count'],
        'DiscountAmount': ['mean', 'sum']
    }).round(2)
    
    # Calculate ROI
    promotion_stats['ROI'] = (
        (promotion_stats[('net_sales', 'sum')] - promotion_stats[('DiscountAmount', 'sum')]) 
        / promotion_stats[('DiscountAmount', 'sum')]
    ).round(3)
    
    return promotion_stats

def calculate_prediction_accuracy(
    actual: pd.DataFrame,
    predicted: pd.DataFrame,
    group_by: Optional[str] = None
) -> pd.DataFrame:
    """
    Calculate prediction accuracy metrics.
    
    Args:
        actual: Actual sales data
        predicted: Predicted sales data
        group_by: Optional column to group by before calculating accuracy
    
    Returns:
        DataFrame with accuracy metrics
    """
    if group_by:
        actual_grouped = actual.groupby([group_by, 'date'])['net_sales'].sum().reset_index()
        predicted_grouped = predicted.groupby([group_by, 'date'])['net_sales'].sum().reset_index()
        
        # Merge actual and predicted
        comparison = actual_grouped.merge(
            predicted_grouped,
            on=[group_by, 'date'],
            suffixes=('_actual', '_predicted')
        )
        
        # Calculate metrics by group
        metrics = comparison.groupby(group_by).apply(lambda x: pd.Series({
            'MAPE': np.mean(np.abs((x['net_sales_actual'] - x['net_sales_predicted']) / x['net_sales_actual'])) * 100,
            'Accuracy': 100 - np.mean(np.abs((x['net_sales_actual'] - x['net_sales_predicted']) / x['net_sales_actual'])) * 100,
            'Total_Actual': x['net_sales_actual'].sum(),
            'Total_Predicted': x['net_sales_predicted'].sum(),
            'Difference_%': ((x['net_sales_predicted'].sum() - x['net_sales_actual'].sum()) / x['net_sales_actual'].sum()) * 100
        })).round(2)
        
    else:
        # Calculate daily totals
        actual_daily = actual.groupby('date')['net_sales'].sum()
        predicted_daily = predicted.groupby('date')['net_sales'].sum()
        
        # Calculate overall metrics
        mape = np.mean(np.abs((actual_daily - predicted_daily) / actual_daily)) * 100
        accuracy = 100 - mape
        total_actual = actual_daily.sum()
        total_predicted = predicted_daily.sum()
        difference_pct = ((total_predicted - total_actual) / total_actual) * 100
        
        metrics = pd.DataFrame([{
            'MAPE': mape,
            'Accuracy': accuracy,
            'Total_Actual': total_actual,
            'Total_Predicted': total_predicted,
            'Difference_%': difference_pct
        }]).round(2)
    
    return metrics

def calculate_monthly_net_sales(
    df_actual: pd.DataFrame,
    df_predicted: pd.DataFrame,
    year: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculate monthly net sales for both actual and predicted data.
    """
    def process_monthly(df):
        data = df.copy()
        
        if year is not None:
            data = data[data['date'].dt.year == year]
        
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month
        
        monthly_sales = data.groupby(['year', 'month'])['net_sales'].sum().reset_index()
        monthly_sales['date'] = pd.to_datetime(monthly_sales[['year', 'month']].assign(day=1))
        
        return monthly_sales.sort_values('date')
    
    return process_monthly(df_actual), process_monthly(df_predicted)

def calculate_quarterly_net_sales(
    df_actual: pd.DataFrame,
    df_predicted: pd.DataFrame,
    year: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculate quarterly net sales for both actual and predicted data.
    """
    def process_quarterly(df):
        data = df.copy()
        
        if year is not None:
            data = data[data['date'].dt.year == year]
        
        data['year'] = data['date'].dt.year
        data['quarter'] = data['date'].dt.quarter
        
        quarterly_sales = data.groupby(['year', 'quarter'])['net_sales'].sum().reset_index()
        quarterly_sales['month'] = quarterly_sales['quarter'] * 3 - 2
        quarterly_sales['date'] = pd.to_datetime(quarterly_sales[['year', 'month']].assign(day=1))
        
        return quarterly_sales.sort_values('date')
    
    return process_quarterly(df_actual), process_quarterly(df_predicted)

def get_monthly_summary_stats(
    df_actual: pd.DataFrame,
    df_predicted: pd.DataFrame,
    year: Optional[int] = None
) -> Tuple[dict, dict]:
    """Calculate monthly summary statistics for both actual and predicted data."""
    monthly_actual, monthly_predicted = calculate_monthly_net_sales(df_actual, df_predicted, year)
    
    def calculate_stats(data, prefix):
        return {
            f'{prefix}_total_sales': data['net_sales'].sum(),
            f'{prefix}_average_monthly_sales': data['net_sales'].mean(),
            f'{prefix}_max_monthly_sales': data['net_sales'].max(),
            f'{prefix}_min_monthly_sales': data['net_sales'].min(),
            f'{prefix}_sales_std': data['net_sales'].std(),
            f'{prefix}_total_months': len(data)
        }
    
    actual_stats = calculate_stats(monthly_actual, 'actual')
    predicted_stats = calculate_stats(monthly_predicted, 'predicted')
    
    return actual_stats, predicted_stats

def get_quarterly_summary_stats(
    df_actual: pd.DataFrame,
    df_predicted: pd.DataFrame,
    year: Optional[int] = None
) -> Tuple[dict, dict]:
    """Calculate quarterly summary statistics for both actual and predicted data."""
    quarterly_actual, quarterly_predicted = calculate_quarterly_net_sales(df_actual, df_predicted, year)
    
    def calculate_stats(data, prefix):
        return {
            f'{prefix}_total_sales': data['net_sales'].sum(),
            f'{prefix}_average_quarterly_sales': data['net_sales'].mean(),
            f'{prefix}_max_quarterly_sales': data['net_sales'].max(),
            f'{prefix}_min_quarterly_sales': data['net_sales'].min(),
            f'{prefix}_sales_std': data['net_sales'].std(),
            f'{prefix}_total_quarters': len(data)
        }
    
    actual_stats = calculate_stats(quarterly_actual, 'actual')
    predicted_stats = calculate_stats(quarterly_predicted, 'predicted')
    
    return actual_stats, predicted_stats

def get_available_years(df: pd.DataFrame) -> list:
    """Get list of unique years available in the dataset."""
    return sorted(df['date'].dt.year.unique().tolist())

def get_available_months(df: pd.DataFrame, year: Optional[int] = None) -> list:
    """Get list of available months, optionally filtered by year."""
    data = df.copy()
    if year is not None:
        data = data[data['date'].dt.year == year]
    return sorted(data['date'].dt.month.unique().tolist())

def get_available_weeks(df: pd.DataFrame, year: Optional[int] = None, month: Optional[int] = None) -> list:
    """Get list of available weeks, optionally filtered by year and month."""
    data = df.copy()
    if year is not None:
        data = data[data['date'].dt.year == year]
    if month is not None:
        data = data[data['date'].dt.month == month]
    return sorted(data['date'].dt.isocalendar().week.unique().tolist())

def get_month_name(month: int) -> str:
    """Get month name from month number."""
    return datetime(2000, month, 1).strftime('%B')

def get_quarter_name(quarter: int) -> str:
    """Get quarter name from quarter number."""
    return f"Q{quarter}" 