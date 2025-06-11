from utils.sales_calculations import load_dashboard_data
import pandas as pd
from config.bq_client import client, PROJECT_ID, DATASET, ACTUALS_TABLE, PREDICTIONS_TABLE

def inspect_table_schema(table_id):
    """Get and print the schema of a BigQuery table."""
    table = client.get_table(f"{PROJECT_ID}.{DATASET}.{table_id}")
    print(f"\nSchema for {table_id}:")
    for field in table.schema:
        print(f"- {field.name} ({field.field_type})")

def test_connection():
    print(f"\nTesting BigQuery connection...")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Dataset: {DATASET}")
    print(f"Tables: {ACTUALS_TABLE}, {PREDICTIONS_TABLE}")
    
    # Test if we can list datasets
    try:
        datasets = list(client.list_datasets())
        print(f"\nAvailable datasets:")
        for dataset in datasets:
            print(f"- {dataset.dataset_id}")
    except Exception as e:
        print(f"Error listing datasets: {str(e)}")
        return

    # Test if we can list tables in our dataset
    try:
        tables = list(client.list_tables(f"{PROJECT_ID}.{DATASET}"))
        print(f"\nAvailable tables in {DATASET}:")
        for table in tables:
            print(f"- {table.table_id}")
    except Exception as e:
        print(f"Error listing tables: {str(e)}")
        return

def test_simple_query():
    print("\nTesting simple query...")
    query = f"""
    SELECT 
        MIN(DateKey) as min_date,
        MAX(DateKey) as max_date,
        COUNT(*) as count
    FROM `{PROJECT_ID}.{DATASET}.{ACTUALS_TABLE}`
    """
    try:
        result = client.query(query).result()
        for row in result:
            print(f"Number of rows in {ACTUALS_TABLE}: {row.count:,}")
            print(f"Date range: {row.min_date} to {row.max_date}")
    except Exception as e:
        print(f"Error running simple query: {str(e)}")

def main():
    print("Starting BigQuery tests...")
    
    # Test basic connection and list available data
    test_connection()
    
    # Test simple query to get date range
    test_simple_query()
    
    print("\nTrying to load data for year 2007...")
    try:
        # Load data for 2007 (will use the default)
        actual_data, predicted_data = load_dashboard_data()
        
        print("\nSample data loaded successfully!")
        
        print("\nActual Data Info:")
        print(f"Total rows: {len(actual_data):,}")
        print(f"Columns: {len(actual_data.columns):,}")
        print("\nColumns:")
        print(actual_data.columns.tolist())
        print("\nDate range:")
        print(f"From: {actual_data['date'].min()}")
        print(f"To: {actual_data['date'].max()}")
        
        print("\nPredicted Data Info:")
        print(f"Total rows: {len(predicted_data):,}")
        print(f"Columns: {len(predicted_data.columns):,}")
        print("\nDate range:")
        print(f"From: {predicted_data['date'].min()}")
        print(f"To: {predicted_data['date'].max()}")
        
        # Show sample of data distribution
        print("\nData distribution by month (Actual Data):")
        monthly_counts = actual_data.groupby('month_name').size()
        for month, count in monthly_counts.items():
            print(f"{month}: {count:,} rows")
        
    except Exception as e:
        print(f"\nError loading sample data: {str(e)}")
        import traceback
        print("\nFull error trace:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 