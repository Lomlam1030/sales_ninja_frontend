from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
import pandas as pd
from datetime import datetime
import requests
from google.cloud import bigquery
import streamlit as st
import logging

from config.settings import settings, DataSource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataSourceInterface(ABC):
    """Abstract interface for data sources."""
    
    @abstractmethod
    def load_dashboard_data(
        self,
        year: Optional[int] = None,
        quarter: Optional[int] = None,
        month: Optional[int] = None,
        week: Optional[int] = None,
        limit: Optional[int] = 700
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load data for the dashboard with various time filters."""
        pass

class BigQueryDataSource(DataSourceInterface):
    """BigQuery implementation of the data source interface."""
    
    def __init__(self):
        self.client = bigquery.Client()
        self._validate_connection()
    
    def _validate_connection(self):
        """Validate BigQuery connection and dataset/table existence."""
        try:
            dataset_ref = self.client.dataset(settings.BQ_DATASET)
            self.client.get_dataset(dataset_ref)
            
            # Check if tables exist
            self.client.get_table(f"{dataset_ref}.{settings.BQ_ACTUALS_TABLE}")
            self.client.get_table(f"{dataset_ref}.{settings.BQ_PREDICTIONS_TABLE}")
        except Exception as e:
            raise ConnectionError(f"Failed to validate BigQuery connection: {str(e)}")
    
    def load_dashboard_data(
        self,
        year: Optional[int] = None,
        quarter: Optional[int] = None,
        month: Optional[int] = None,
        week: Optional[int] = None,
        limit: Optional[int] = 700
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load data from BigQuery with time-based filtering."""
        
        # Build WHERE clause based on filters
        conditions = []
        if year:
            conditions.append(f"EXTRACT(YEAR FROM DateKey) = {year}")
        if quarter:
            conditions.append(f"EXTRACT(QUARTER FROM DateKey) = {quarter}")
        if month:
            conditions.append(f"EXTRACT(MONTH FROM DateKey) = {month}")
        if week:
            conditions.append(f"EXTRACT(WEEK FROM DateKey) = {week}")
            
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        limit_clause = f"LIMIT {limit}" if limit else ""
        
        logger.debug(f"Applying filters: {conditions}")
        
        # Actual data query with daily aggregation
        actual_query = f"""
        WITH daily_aggregates AS (
            SELECT
                DateKey,
                EXTRACT(YEAR FROM DateKey) as year,
                EXTRACT(MONTH FROM DateKey) as month,
                FORMAT_DATE('%B', DateKey) as month_name,
                CONCAT('Q', CAST(EXTRACT(QUARTER FROM DateKey) AS STRING)) as quarter,
                EXTRACT(WEEK FROM DateKey) as week,
                ProductCategoryName,
                SUM(SalesAmount) as net_sales,
                SUM(SalesQuantity) as SalesQuantity,
                SUM(ReturnQuantity) as ReturnQuantity,
                SUM(DiscountAmount) as DiscountAmount,
                COUNT(*) as transaction_count
            FROM `{settings.GCP_PROJECT_ID}.{settings.BQ_DATASET}.{settings.BQ_ACTUALS_TABLE}`
            {where_clause}
            GROUP BY 
                DateKey, ProductCategoryName
            {limit_clause}
        )
        SELECT *
        FROM daily_aggregates
        ORDER BY DateKey
        """
        
        # Predicted data query
        predicted_query = f"""
        SELECT
            DateKey,
            EXTRACT(YEAR FROM DateKey) as year,
            EXTRACT(MONTH FROM DateKey) as month,
            FORMAT_DATE('%B', DateKey) as month_name,
            CONCAT('Q', CAST(EXTRACT(QUARTER FROM DateKey) AS STRING)) as quarter,
            EXTRACT(WEEK FROM DateKey) as week,
            ProductCategoryName,
            SUM(SalesAmount) as net_sales,
            SUM(SalesQuantity) as SalesQuantity,
            SUM(ReturnQuantity) as ReturnQuantity,
            SUM(DiscountAmount) as DiscountAmount
        FROM `{settings.GCP_PROJECT_ID}.{settings.BQ_DATASET}.{settings.BQ_PREDICTIONS_TABLE}`
        {where_clause}
        GROUP BY 
            DateKey, ProductCategoryName
        ORDER BY DateKey
        {limit_clause}
        """
        
        try:
            # Execute queries with job configuration
            job_config = bigquery.QueryJobConfig(
                use_query_cache=True,
                priority=bigquery.QueryPriority.BATCH
            )
            
            # Execute queries
            logger.debug("Executing actual data query...")
            df_actual = self.client.query(actual_query, job_config=job_config).to_dataframe()
            logger.debug(f"Retrieved {len(df_actual)} actual records")
            
            logger.debug("Executing predicted data query...")
            df_predicted = self.client.query(predicted_query, job_config=job_config).to_dataframe()
            logger.debug(f"Retrieved {len(df_predicted)} predicted records")
            
            # Convert date columns
            df_actual['date'] = pd.to_datetime(df_actual['DateKey'])
            df_predicted['date'] = pd.to_datetime(df_predicted['DateKey'])
            
            # Sort by date
            df_actual = df_actual.sort_values('date')
            df_predicted = df_predicted.sort_values('date')
            
            return df_actual, df_predicted
            
        except Exception as e:
            logger.error(f"Error in query execution: {str(e)}")
            logger.debug(f"Actual query: {actual_query}")
            logger.debug(f"Predicted query: {predicted_query}")
            return pd.DataFrame(), pd.DataFrame()

class RestApiDataSource(DataSourceInterface):
    """REST API implementation of the data source interface."""
    
    def __init__(self):
        self.session = requests.Session()
        if settings.API_KEY:
            self.session.headers.update({"Authorization": f"Bearer {settings.API_KEY}"})
    
    def _fetch_data(self, endpoint: str, params: dict) -> pd.DataFrame:
        """Helper method to fetch data from API endpoint."""
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return pd.DataFrame(response.json())
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch data from API: {str(e)}")
    
    def load_dashboard_data(
        self,
        year: Optional[int] = None,
        quarter: Optional[int] = None,
        month: Optional[int] = None,
        week: Optional[int] = None,
        limit: Optional[int] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load data from REST API."""
        params = {}
        if year:
            params['year'] = year
        if quarter:
            params['quarter'] = quarter
        if month:
            params['month'] = month
        if week:
            params['week'] = week
        if limit:
            params['limit'] = limit
        
        df_actual = self._fetch_data(settings.actuals_endpoint, params)
        df_predicted = self._fetch_data(settings.predictions_endpoint, params)
        
        # Convert date columns
        for df in [df_actual, df_predicted]:
            df['date'] = pd.to_datetime(df['DateKey'])
        
        return df_actual, df_predicted

def get_data_source() -> DataSourceInterface:
    """Factory function to get the configured data source."""
    if settings.DATA_SOURCE == DataSource.BIGQUERY:
        return BigQueryDataSource()
    elif settings.DATA_SOURCE == DataSource.REST_API:
        return RestApiDataSource()
    else:
        raise ValueError(f"Unsupported data source: {settings.DATA_SOURCE}") 