"""Environment configuration for the Sales Ninja dashboard."""

import os
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file or set defaults."""
    # Try to load from .env file if it exists
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Set required environment variables with defaults
    os.environ.setdefault('DATA_SOURCE', 'bigquery')
    os.environ.setdefault('GCP_PROJECT_ID', 'sales-ninja-analytics')
    os.environ.setdefault('BQ_DATASET', 'dashboard_data')
    os.environ.setdefault('BQ_ACTUALS_TABLE', 'sales_actuals')
    os.environ.setdefault('BQ_PREDICTIONS_TABLE', 'sales_predictions')
    os.environ.setdefault('DEFAULT_YEAR', '2007')
    
    # Validate Google credentials
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        creds_path = Path(__file__).parent / 'service-account.json'
        if creds_path.exists():
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(creds_path)
        else:
            raise ValueError(
                "Google Cloud credentials not found. Please set GOOGLE_APPLICATION_CREDENTIALS "
                "environment variable or place service-account.json in the config directory."
            ) 