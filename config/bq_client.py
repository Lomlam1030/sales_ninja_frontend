from google.cloud import bigquery
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Constants - load from environment variables with fallbacks
PROJECT_ID = os.getenv('PROJECT_ID', 'nodal-clock-456815-g3')
DATASET = os.getenv('DATASET', 'dashboard_data')
ACTUALS_TABLE = os.getenv('ACTUALS_TABLE', 'dashboard_merged_data')
PREDICTIONS_TABLE = os.getenv('PREDICTIONS_TABLE', 'dashboard_prediction_data')

def get_bigquery_client():
    """
    Get an authenticated BigQuery client using service account credentials.
    Credentials should be provided through GOOGLE_APPLICATION_CREDENTIALS
    environment variable pointing to the key file location.
    """
    try:
        # Use GOOGLE_APPLICATION_CREDENTIALS environment variable
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            logger.error("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")
            raise ValueError("Missing Google Cloud credentials")
            
        return bigquery.Client(project=PROJECT_ID)

    except Exception as e:
        logger.error(f"Failed to initialize BigQuery client: {e}")
        raise

# Initialize the client
try:
    client = get_bigquery_client()
    logger.info("Successfully initialized BigQuery client")
except Exception as e:
    logger.error(f"Error initializing BigQuery client: {e}")
    raise 