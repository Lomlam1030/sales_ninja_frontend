"""Geography data calculations for the Sales Ninja dashboard."""

import pandas as pd
from typing import Dict, List, Optional, Tuple

def prepare_geography_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare geography data for visualization.
    
    Args:
        df: DataFrame with sales data containing geography columns
    
    Returns:
        DataFrame aggregated by geography with sales metrics
    """
    # Group by geography columns and calculate metrics
    geo_data = df.groupby(['country', 'continent']).agg({
        'net_sales': ['sum', 'mean'],
        'SalesQuantity': 'sum',
        'ReturnQuantity': 'sum',
        'DiscountAmount': 'sum'
    }).round(2)
    
    # Flatten column names
    geo_data.columns = [
        f"{col[0]}_{col[1]}" if col[1] != '' else col[0]
        for col in geo_data.columns
    ]
    
    # Reset index to make geography columns regular columns
    geo_data = geo_data.reset_index()
    
    # Calculate additional metrics
    geo_data['return_rate'] = (
        geo_data['ReturnQuantity_sum'] / geo_data['SalesQuantity_sum'] * 100
    ).round(2)
    
    geo_data['discount_rate'] = (
        geo_data['DiscountAmount_sum'] / geo_data['net_sales_sum'] * 100
    ).round(2)
    
    return geo_data

def get_continent_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get sales summary by continent.
    
    Args:
        df: DataFrame with sales data
    
    Returns:
        DataFrame with continent-level metrics
    """
    return df.groupby('continent').agg({
        'net_sales': ['sum', 'mean'],
        'SalesQuantity': 'sum',
        'ReturnQuantity': 'sum',
        'DiscountAmount': 'sum'
    }).round(2)

def get_country_summary(df: pd.DataFrame, continent: Optional[str] = None) -> pd.DataFrame:
    """
    Get sales summary by country, optionally filtered by continent.
    
    Args:
        df: DataFrame with sales data
        continent: Optional continent to filter by
    
    Returns:
        DataFrame with country-level metrics
    """
    if continent:
        df = df[df['continent'] == continent]
    
    return df.groupby('country').agg({
        'net_sales': ['sum', 'mean'],
        'SalesQuantity': 'sum',
        'ReturnQuantity': 'sum',
        'DiscountAmount': 'sum'
    }).round(2)

def calculate_geographic_sales(df: pd.DataFrame, 
                             year: Optional[int] = None,
                             period: str = 'D') -> pd.DataFrame:
    """
    Calculate sales by continent for different time periods.
    
    Args:
        df (pd.DataFrame): Input dashboard data
        year (Optional[int]): Year to filter the data
        period (str): Time period ('D' for daily, 'M' for monthly, 'Q' for quarterly)
    
    Returns:
        pd.DataFrame: Sales data by continent with proper date formatting
    """
    # Filter by year if specified
    if year is not None:
        df = df[df['Year'] == year]
    
    # Group by appropriate time period and continent
    groupby_cols = ['ContinentName']
    if period == 'D':
        groupby_cols = ['DateKey'] + groupby_cols
    elif period == 'M':
        groupby_cols = ['Year', 'Month'] + groupby_cols
    else:  # 'Q'
        groupby_cols = ['Year', 'Quarter'] + groupby_cols
    
    # Calculate sales by continent
    sales_data = df.groupby(groupby_cols)['SalesAmount'].sum().reset_index()
    
    # Format the date/period information
    if period == 'D':
        sales_data['period'] = sales_data['DateKey'].dt.strftime('%Y-%m-%d')
    elif period == 'M':
        sales_data['period'] = pd.to_datetime(
            sales_data[['Year', 'Month']].assign(day=1)
        ).dt.strftime('%B %Y')
    else:  # 'Q'
        sales_data['period'] = sales_data.apply(
            lambda x: f"Q{x['Quarter']} {x['Year']}", axis=1
        )
    
    # Ensure proper column names for the map
    sales_data = sales_data.rename(columns={
        'SalesAmount': 'SalesAmount',  # Keep as is for hover formatting
        'ContinentName': 'ContinentName'  # Keep as is for mapping
    })
    
    return sales_data

def get_available_years(df: pd.DataFrame) -> list:
    """
    Get list of unique years available in the dataset.
    
    Args:
        df (pd.DataFrame): Input dashboard data
    
    Returns:
        list: List of unique years in ascending order
    """
    return sorted(df['Year'].unique().tolist()) 