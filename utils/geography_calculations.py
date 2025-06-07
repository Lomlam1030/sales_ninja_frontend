import pandas as pd
from typing import Optional, Dict
from datetime import datetime

def get_geography_data() -> pd.DataFrame:
    """
    Load and prepare the geographic sales data.
    
    Returns:
        pd.DataFrame: Processed dashboard data with geographic information
    """
    df = pd.read_csv('data/data_dashboard_merged.csv')
    
    # Convert date for filtering
    df['DateKey'] = pd.to_datetime(df['DateKey'])
    df['Year'] = df['DateKey'].dt.year
    df['Month'] = df['DateKey'].dt.month
    df['Quarter'] = df['DateKey'].dt.quarter
    
    return df

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