import pandas as pd
import numpy as np
from typing import Optional, Tuple
from datetime import datetime
from google.cloud import bigquery
from config.bq_client import client, PROJECT_ID, DATASET, ACTUALS_TABLE, PREDICTIONS_TABLE

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

def calculate_daily_net_sales(
    df_actual: pd.DataFrame,
    df_predicted: pd.DataFrame,
    year: Optional[int] = None,
    month: Optional[int] = None,
    week: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculate daily net sales for both actual and predicted data.
    
    Args:
        df_actual (pd.DataFrame): Actual sales data
        df_predicted (pd.DataFrame): Predicted sales data
        year (int, optional): Year to filter the data
        month (int, optional): Month to filter the data (1-12)
        week (int, optional): Week number to filter the data (1-53)
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Daily sales data for (actual, predicted)
    """
    def filter_and_aggregate(df):
        # Create a copy of the dataframe
        data = df.copy()
        
        # Apply filters if specified
        if year is not None:
            data = data[data['date'].dt.year == year]
        if month is not None:
            data = data[data['date'].dt.month == month]
        if week is not None:
            data = data[data['date'].dt.isocalendar().week == week]
        
        # Group by date and calculate daily net sales
        daily_sales = data.groupby('date')['net_sales'].sum().reset_index()
        return daily_sales.sort_values('date')
    
    return filter_and_aggregate(df_actual), filter_and_aggregate(df_predicted)

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

def get_sales_summary_stats(
    df_actual: pd.DataFrame,
    df_predicted: pd.DataFrame,
    year: Optional[int] = None,
    month: Optional[int] = None,
    week: Optional[int] = None
) -> Tuple[dict, dict]:
    """Calculate summary statistics for both actual and predicted net sales."""
    daily_actual, daily_predicted = calculate_daily_net_sales(
        df_actual, df_predicted, year, month, week
    )
    
    def calculate_stats(data, prefix):
        return {
            f'{prefix}_total_sales': data['net_sales'].sum(),
            f'{prefix}_average_daily_sales': data['net_sales'].mean(),
            f'{prefix}_max_daily_sales': data['net_sales'].max(),
            f'{prefix}_min_daily_sales': data['net_sales'].min(),
            f'{prefix}_sales_std': data['net_sales'].std(),
            f'{prefix}_total_days': len(data)
        }
    
    actual_stats = calculate_stats(daily_actual, 'actual')
    predicted_stats = calculate_stats(daily_predicted, 'predicted')
    
    return actual_stats, predicted_stats

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