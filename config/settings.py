import os
from enum import Enum
from typing import Optional
from pathlib import Path

class DataSource(Enum):
    BIGQUERY = "bigquery"
    REST_API = "rest_api"

class Settings:
    def __init__(self):
        # Data Source Configuration
        self.DATA_SOURCE: DataSource = self._get_data_source()
        
        # BigQuery Settings
        self.GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
        self.BQ_DATASET: str = os.getenv("BQ_DATASET", "dashboard_data")
        self.BQ_ACTUALS_TABLE: str = os.getenv("BQ_ACTUALS_TABLE", "dashboard_merged_data")
        self.BQ_PREDICTIONS_TABLE: str = os.getenv("BQ_PREDICTIONS_TABLE", "dashboard_prediction_data")
        self.GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = self._get_credentials_path()
        
        # REST API Settings
        self.API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
        self.API_VERSION: str = os.getenv("API_VERSION", "v1")
        self.API_KEY: Optional[str] = os.getenv("API_KEY")
        
        # Data Loading Settings
        self.DEFAULT_YEAR: int = int(os.getenv("DEFAULT_YEAR", "2007"))
        self.MAX_ROWS: int = 700  # Fixed at 700 rows
        
        # Validate settings
        self.validate()
    
    def _get_data_source(self) -> DataSource:
        """Get and validate data source from environment."""
        data_source = os.getenv("DATA_SOURCE", "bigquery").lower()
        try:
            return DataSource(data_source)
        except ValueError:
            raise ValueError(
                f"Invalid DATA_SOURCE value: {data_source}. "
                f"Must be one of: {[ds.value for ds in DataSource]}"
            )
    
    def _get_credentials_path(self) -> Optional[str]:
        """Get and validate credentials path."""
        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if creds_path:
            path = Path(creds_path)
            if not path.exists():
                raise ValueError(
                    f"GOOGLE_APPLICATION_CREDENTIALS file not found at: {creds_path}"
                )
            return str(path)
        return None
    
    # Endpoints
    @property
    def actuals_endpoint(self) -> str:
        return f"{self.API_BASE_URL}/api/{self.API_VERSION}/sales/actuals"
    
    @property
    def predictions_endpoint(self) -> str:
        return f"{self.API_BASE_URL}/api/{self.API_VERSION}/sales/predictions"

    def validate(self):
        """Validate the configuration based on the selected data source."""
        try:
            if self.DATA_SOURCE == DataSource.BIGQUERY:
                if not self.GCP_PROJECT_ID:
                    raise ValueError("GCP_PROJECT_ID is required when using BigQuery")
                if not self.GOOGLE_APPLICATION_CREDENTIALS:
                    raise ValueError(
                        "GOOGLE_APPLICATION_CREDENTIALS is required when using BigQuery. "
                        "Please set the environment variable to point to your service account key file."
                    )
            
            elif self.DATA_SOURCE == DataSource.REST_API:
                if not self.API_BASE_URL:
                    raise ValueError("API_BASE_URL is required when using REST API")
                if not self.API_KEY:
                    raise ValueError("API_KEY is required when using REST API")
            
            if self.DEFAULT_YEAR not in [2007, 2008, 2009]:
                raise ValueError("DEFAULT_YEAR must be 2007, 2008, or 2009")
            
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {str(e)}")

# Create a global settings instance
try:
    settings = Settings()
except Exception as e:
    raise ValueError(f"Failed to initialize settings: {str(e)}") 