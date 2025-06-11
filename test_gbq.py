from config.bq_client import client, PROJECT_ID, DATASET, ACTUALS_TABLE
import pandas as pd

def test_connection():
    print("Testing BigQuery Connection...")
    
    # Test query to get a few rows
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    LIMIT 5
    """
    
    try:
        # Execute query
        df = client.query(query).to_dataframe()
        
        # Print results
        print("\nConnection successful!")
        print(f"\nFound {len(df)} rows")
        print("\nColumns in the table:")
        print(df.columns.tolist())
        print("\nFirst few rows:")
        print(df.head())
        
    except Exception as e:
        print(f"Error accessing data: {str(e)}")

if __name__ == "__main__":
    test_connection() 