from google.cloud import bigquery
import os

def get_bigquery_client():
    """
    Initialize and return a BigQuery client.
    Assumes Google Cloud credentials are properly set up in the environment.
    """
    return bigquery.Client()

# Create a singleton client instance
client = get_bigquery_client() 