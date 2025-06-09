import pandas as pd
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict, Any
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define paths to data files
DATA_DIR = "data"
ACTUALS_FILE = os.path.join(DATA_DIR, "data_dashboard_final.csv")
PREDICTIONS_FILE = os.path.join(DATA_DIR, "synthetic_predicted_sales_2007_2010.csv")

def load_actuals_data() -> pd.DataFrame:
    """Load and cache the actuals data"""
    logger.info(f"Loading data from {ACTUALS_FILE}")
    try:
        df = pd.read_csv(ACTUALS_FILE)
        df['date'] = pd.to_datetime(df['DateKey'])
        logger.info(f"Successfully loaded data. Shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        logger.info(f"First few dates: {df['date'].head().tolist()}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def load_predictions_data() -> pd.DataFrame:
    """Load and cache the predictions data"""
    logger.info(f"Loading predictions from {PREDICTIONS_FILE}")
    try:
        df = pd.read_csv(PREDICTIONS_FILE)
        df['date'] = pd.to_datetime(df['DateKey'])
        logger.info(f"Successfully loaded predictions. Shape: {df.shape}")
        logger.info(f"First few dates: {df['date'].head().tolist()}")
        return df
    except Exception as e:
        logger.error(f"Error loading predictions: {str(e)}")
        raise

async def get_daily_sales(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """Get daily sales metrics between start_date and end_date"""
    logger.info(f"Getting daily sales for start_date: {start_date}, end_date: {end_date}")
    
    if not end_date:
        end_date = start_date + timedelta(days=30)
        
    df = load_actuals_data()
    
    # Filter by date range
    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
    filtered_df = df[mask]
    logger.info(f"Filtered data shape: {filtered_df.shape}")
    
    # Group by date and calculate metrics
    daily_metrics = filtered_df.groupby(filtered_df['date'].dt.date).agg({
        'SalesAmount': ['sum', 'count', 'mean']
    }).reset_index()
    
    # Rename columns
    daily_metrics.columns = ['date', 'total_sales', 'total_records', 'average_value']
    logger.info(f"Daily metrics shape: {daily_metrics.shape}")
    logger.info(f"Sample data: {daily_metrics.head().to_dict('records')}")
    
    # Convert date to string format for JSON serialization
    result = []
    for record in daily_metrics.to_dict('records'):
        record['date'] = record['date'].isoformat()
        result.append(record)
    
    return result

async def get_daily_predictions(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """Get daily sales predictions between start_date and end_date"""
    logger.info(f"Getting predictions for start_date: {start_date}, end_date: {end_date}")
    
    if not end_date:
        end_date = start_date + timedelta(days=30)
        
    df = load_predictions_data()
    
    # Filter by date range
    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
    filtered_df = df[mask]
    logger.info(f"Filtered predictions shape: {filtered_df.shape}")
    
    # Group by date and calculate metrics
    daily_predictions = filtered_df.groupby(filtered_df['date'].dt.date).agg({
        'SalesAmount': ['sum', 'count', 'mean']
    }).reset_index()
    
    # Rename columns
    daily_predictions.columns = ['date', 'predicted_sales', 'total_records', 'average_predicted_value']
    logger.info(f"Daily predictions shape: {daily_predictions.shape}")
    
    # Convert date to string format
    result = []
    for record in daily_predictions.to_dict('records'):
        record['date'] = record['date'].isoformat()
        result.append(record)
    
    return result

async def get_actuals_vs_predictions(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """Get comparison of actual sales vs predictions"""
    logger.info(f"Getting comparison for start_date: {start_date}, end_date: {end_date}")
    
    if not end_date:
        end_date = start_date + timedelta(days=30)
        
    actuals_df = load_actuals_data()
    predictions_df = load_predictions_data()
    
    # Filter by date range
    actuals_mask = (actuals_df['date'].dt.date >= start_date) & (actuals_df['date'].dt.date <= end_date)
    predictions_mask = (predictions_df['date'].dt.date >= start_date) & (predictions_df['date'].dt.date <= end_date)
    
    # Group by date
    actuals = actuals_df[actuals_mask].groupby(actuals_df['date'].dt.date)['SalesAmount'].agg(['sum', 'count']).reset_index()
    predictions = predictions_df[predictions_mask].groupby(predictions_df['date'].dt.date)['SalesAmount'].agg(['sum', 'count']).reset_index()
    
    # Rename columns
    actuals.columns = ['date', 'actual_sales', 'actual_records']
    predictions.columns = ['date', 'predicted_sales', 'predicted_records']
    
    # Merge actuals and predictions
    comparison = pd.merge(actuals, predictions, on='date', how='outer').fillna(0)
    logger.info(f"Comparison shape: {comparison.shape}")
    
    # Calculate error metrics
    comparison['absolute_error'] = abs(comparison['actual_sales'] - comparison['predicted_sales'])
    comparison['percentage_error'] = comparison.apply(
        lambda row: (abs(row['actual_sales'] - row['predicted_sales']) / row['actual_sales']) * 100 
        if row['actual_sales'] > 0 else None, 
        axis=1
    )
    
    # Convert date to string format
    result = []
    for record in comparison.to_dict('records'):
        record['date'] = record['date'].isoformat()
        result.append(record)
    
    return result

async def get_prediction_accuracy_metrics(start_date: date, end_date: Optional[date] = None) -> Dict[str, Any]:
    """Get overall prediction accuracy metrics"""
    logger.info(f"Getting accuracy metrics for start_date: {start_date}, end_date: {end_date}")
    
    if not end_date:
        end_date = start_date + timedelta(days=30)
        
    actuals_df = load_actuals_data()
    predictions_df = load_predictions_data()
    
    # Filter by date range
    actuals_mask = (actuals_df['date'].dt.date >= start_date) & (actuals_df['date'].dt.date <= end_date)
    predictions_mask = (predictions_df['date'].dt.date >= start_date) & (predictions_df['date'].dt.date <= end_date)
    
    # Group by date for comparison
    actuals_daily = actuals_df[actuals_mask].groupby(actuals_df['date'].dt.date)['SalesAmount'].sum().reset_index()
    predictions_daily = predictions_df[predictions_mask].groupby(predictions_df['date'].dt.date)['SalesAmount'].sum().reset_index()
    
    # Merge on date
    merged = pd.merge(actuals_daily, predictions_daily, on='date', suffixes=('_actual', '_pred'))
    logger.info(f"Merged data shape for accuracy metrics: {merged.shape}")
    
    if len(merged) == 0:
        logger.warning("No matching data found for accuracy metrics")
        return {
            'total_predictions': 0,
            'mae': 0,
            'rmse': 0,
            'mape': 0,
            'correlation': 0
        }
    
    # Calculate metrics
    metrics = {
        'total_predictions': len(merged),
        'mae': abs(merged['SalesAmount_actual'] - merged['SalesAmount_pred']).mean(),
        'rmse': ((merged['SalesAmount_actual'] - merged['SalesAmount_pred']) ** 2).mean() ** 0.5,
        'mape': (abs(merged['SalesAmount_actual'] - merged['SalesAmount_pred']) / merged['SalesAmount_actual']).mean() * 100,
        'correlation': merged['SalesAmount_actual'].corr(merged['SalesAmount_pred'])
    }
    
    logger.info(f"Computed metrics: {metrics}")
    return metrics

async def get_sales_by_region(start_date: date, end_date: Optional[date] = None) -> List[dict]:
    """Get sales data aggregated by region"""
    if not end_date:
        end_date = start_date + timedelta(days=30)
        
    df = load_actuals_data()
    
    # Filter by date range
    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
    filtered_df = df[mask]
    
    # Group by region and calculate metrics
    region_metrics = filtered_df.groupby(['RegionCountryName', 'ContinentName']).agg({
        'SalesAmount': ['sum', 'mean', 'count']
    }).reset_index()
    
    # Rename columns
    region_metrics.columns = ['region', 'continent', 'total_sales', 'avg_sales', 'total_records']
    region_metrics['country'] = region_metrics['region']  # Using region country as both region and country
    
    # Convert to dict format
    return region_metrics.to_dict('records')

async def get_region_time_series(region: str, start_date: date, end_date: date) -> List[dict]:
    """Get daily sales time series for a specific region"""
    df = load_actuals_data()
    
    # Filter by date range and region
    mask = (
        (df['date'].dt.date >= start_date) & 
        (df['date'].dt.date <= end_date) & 
        (df['RegionCountryName'] == region)
    )
    filtered_df = df[mask]
    
    # Group by date and calculate metrics
    time_series = filtered_df.groupby(filtered_df['date'].dt.date).agg({
        'SalesAmount': ['sum', 'count']
    }).reset_index()
    
    # Rename columns
    time_series.columns = ['date', 'total_sales', 'total_records']
    time_series['region'] = region
    
    # Convert date to string format
    result = []
    for record in time_series.to_dict('records'):
        record['date'] = record['date'].isoformat()
        result.append(record)
    
    return result 