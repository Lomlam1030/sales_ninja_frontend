import pandas as pd

# Read just the first few rows to check the structure
df = pd.read_csv('data/data_dashboard_merged.csv', nrows=5)
print("Column names:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head()) 