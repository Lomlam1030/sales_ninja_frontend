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

# Constants
PROJECT_ID = "nodal-clock-456815-g3"
DATASET = "dashboard_data"
ACTUALS_TABLE = "dashboard_merged_data"
PREDICTIONS_TABLE = "dashboard_prediction_data"

def get_bigquery_client():
    """
    Get an authenticated BigQuery client using service account credentials.
    The service account key can be provided either through:
    1. GOOGLE_APPLICATION_CREDENTIALS environment variable pointing to the key file
    2. Direct JSON credentials in GOOGLE_CREDENTIALS environment variable
    """
    try:
        # First try: Check for credentials JSON in environment variable
        if 'GOOGLE_CREDENTIALS' in os.environ:
            try:
                credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                return bigquery.Client(credentials=credentials, project=PROJECT_ID)
            except Exception as e:
                logger.warning(f"Failed to use GOOGLE_CREDENTIALS env var: {e}")

        # Second try: Use GOOGLE_APPLICATION_CREDENTIALS environment variable
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