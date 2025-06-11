from abc import ABC, abstractmethod
from typing import Optional, Tuple
import pandas as pd
from datetime import datetime
import requests
from google.cloud import bigquery

from config.settings import settings, DataSource

class DataSourceInterface(ABC):
    """Abstract interface for data sources."""
    
    @abstractmethod
    def load_dashboard_data(
        self,
        year: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load actual and predicted sales data."""
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
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load data from BigQuery."""
        # Common columns for both actual and predicted data
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
        
        # Load actual data
        actual_query = f"""
        SELECT DISTINCT
            {common_columns},
            RegionCountryName as country
        FROM `{settings.GCP_PROJECT_ID}.{settings.BQ_DATASET}.{settings.BQ_ACTUALS_TABLE}`
        {where_clause}
        ORDER BY DateKey
        """
        
        # Load predicted data
        predicted_query = f"""
        SELECT DISTINCT
            {common_columns}
        FROM `{settings.GCP_PROJECT_ID}.{settings.BQ_DATASET}.{settings.BQ_PREDICTIONS_TABLE}`
        {where_clause}
        ORDER BY DateKey
        """
        
        if limit:
            actual_query += f" LIMIT {limit}"
            predicted_query += f" LIMIT {limit}"
        
        try:
            job_config = bigquery.QueryJobConfig(
                allow_large_results=True,
                use_query_cache=True
            )
            
            df_actual = self.client.query(actual_query, job_config=job_config).to_dataframe()
            df_predicted = self.client.query(predicted_query, job_config=job_config).to_dataframe()
            
            # Convert date columns
            df_actual['date'] = pd.to_datetime(df_actual['DateKey'])
            df_predicted['date'] = pd.to_datetime(df_predicted['DateKey'])
            
            return df_actual, df_predicted
            
        except Exception as e:
            raise Exception(f"Error loading data from BigQuery: {str(e)}")

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
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load data from REST API."""
        params = {}
        if year:
            params['year'] = year
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
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