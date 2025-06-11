import os
from enum import Enum
from typing import Optional

class DataSource(Enum):
    BIGQUERY = "bigquery"
    REST_API = "rest_api"

class Settings:
    # Data Source Configuration
    DATA_SOURCE: DataSource = DataSource(os.getenv("DATA_SOURCE", "bigquery"))
    
    # BigQuery Settings
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    BQ_DATASET: str = os.getenv("BQ_DATASET", "dashboard_data")
    BQ_ACTUALS_TABLE: str = os.getenv("BQ_ACTUALS_TABLE", "dashboard_merged_data")
    BQ_PREDICTIONS_TABLE: str = os.getenv("BQ_PREDICTIONS_TABLE", "dashboard_prediction_data")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # REST API Settings
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    API_KEY: Optional[str] = os.getenv("API_KEY")
    
    # Data Loading Settings
    DEFAULT_YEAR: int = int(os.getenv("DEFAULT_YEAR", "2007"))
    MAX_ROWS: Optional[int] = int(os.getenv("MAX_ROWS", "0")) or None
    
    # Endpoints
    @property
    def actuals_endpoint(self) -> str:
        return f"{self.API_BASE_URL}/api/{self.API_VERSION}/sales/actuals"
    
    @property
    def predictions_endpoint(self) -> str:
        return f"{self.API_BASE_URL}/api/{self.API_VERSION}/sales/predictions"

    def validate(self):
        """Validate the configuration based on the selected data source."""
        if self.DATA_SOURCE == DataSource.BIGQUERY:
            if not self.GCP_PROJECT_ID:
                raise ValueError("GCP_PROJECT_ID is required when using BigQuery")
            if not self.GOOGLE_APPLICATION_CREDENTIALS:
                raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is required when using BigQuery")
        
        elif self.DATA_SOURCE == DataSource.REST_API:
            if not self.API_BASE_URL:
                raise ValueError("API_BASE_URL is required when using REST API")
            if not self.API_KEY:
                raise ValueError("API_KEY is required when using REST API")

# Create a global settings instance
settings = Settings() 