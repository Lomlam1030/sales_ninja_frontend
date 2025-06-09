import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Define sample data parameters
start_date = datetime(2007, 1, 1)
end_date = datetime(2009, 12, 31)
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Define countries by continent with realistic market sizes
country_data = {
    'North America': {
        'United States': 1.0,  # Base market size multiplier
        'Canada': 0.7,
        'Mexico': 0.6,
        'Costa Rica': 0.3,
        'Panama': 0.3,
        'Guatemala': 0.25,
        'Honduras': 0.2,
        'Nicaragua': 0.2,
        'El Salvador': 0.2,
        'Belize': 0.15
    },
    'Europe': {
        'Germany': 0.9,
        'United Kingdom': 0.85,
        'France': 0.8,
        'Italy': 0.75,
        'Spain': 0.7,
        'Netherlands': 0.65,
        'Belgium': 0.6,
        'Switzerland': 0.6,
        'Austria': 0.55,
        'Sweden': 0.55,
        'Norway': 0.5,
        'Denmark': 0.5,
        'Finland': 0.45,
        'Ireland': 0.45,
        'Poland': 0.4,
        'Greece': 0.35
    },
    'Asia': {
        'Japan': 0.95,
        'China': 0.9,
        'South Korea': 0.8,
        'India': 0.75,
        'Singapore': 0.7,
        'Taiwan': 0.65,
        'Thailand': 0.5,
        'Malaysia': 0.45,
        'Vietnam': 0.4
    }
}

# Create empty lists to store data
records = []

# Define economic trend factors for each year (2007-2009 including financial crisis)
year_factors = {
    2007: 1.0,      # Pre-crisis normal
    2008: 0.85,     # Crisis impact
    2009: 0.75      # Deep recession
}

# Generate synthetic sales data
for date in dates:
    year_factor = year_factors[date.year]
    week_num = date.isocalendar()[1]
    
    for continent, countries in country_data.items():
        for country, market_size in countries.items():
            # Base sales with market size and seasonality
            base_sales = np.random.normal(10000, 2000)  # Base sales around 10,000
            
            # Add seasonal patterns
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.month / 12)  # General seasonality
            
            # Add continent-specific seasonal patterns
            if continent == 'North America':
                # Stronger summer and winter peaks
                seasonal_factor *= 1 + 0.2 * np.sin(4 * np.pi * date.month / 12)
            elif continent == 'Europe':
                # Stronger summer peak
                seasonal_factor *= 1 + 0.25 * np.sin(2 * np.pi * (date.month - 2) / 12)
            elif continent == 'Asia':
                # Different seasonal pattern
                seasonal_factor *= 1 + 0.15 * np.sin(2 * np.pi * (date.month - 1) / 12)
            
            # Add some randomness
            daily_variation = np.random.normal(1, 0.1)
            
            # Calculate final sales amount with year factor
            sales_amount = base_sales * seasonal_factor * market_size * daily_variation * year_factor
            
            # Add some special event spikes (e.g., holidays, sales events)
            if (date.month == 12 and date.day >= 15) or (date.month == 1 and date.day <= 15):  # Holiday season
                sales_amount *= np.random.uniform(1.2, 1.5)
            elif date.month == 11 and date.day >= 20:  # Black Friday period
                sales_amount *= np.random.uniform(1.3, 1.8)
            
            # Add weekly patterns
            if date.weekday() >= 5:  # Weekend
                sales_amount *= 0.7  # Lower sales on weekends
            
            records.append({
                'DateKey': date,
                'SalesAmount': round(sales_amount, 2),
                'CalendarYear': date.year,
                'CalendarMonth': date.month,
                'CalendarWeek': week_num,
                'ContinentName': continent,
                'RegionCountryName': country
            })

# Create DataFrame
df = pd.DataFrame(records)

# Add market dynamics (trends, competition effects)
for country in df['RegionCountryName'].unique():
    mask = df['RegionCountryName'] == country
    
    # Calculate days since start for this country
    days = (df.loc[mask, 'DateKey'] - df.loc[mask, 'DateKey'].min()).dt.days
    
    # Create unique growth pattern for each country
    base_growth = np.random.uniform(0.0001, 0.0003)
    growth_factor = 1 + (days * base_growth)
    
    # Add some market competition effects
    competition_factor = 1 + np.sin(days * 2 * np.pi / 365) * 0.1
    
    # Apply both factors
    df.loc[mask, 'SalesAmount'] *= growth_factor * competition_factor

# Round final sales amounts
df['SalesAmount'] = df['SalesAmount'].round(2)

# Save to CSV
df.to_csv('data/sample_data_geography.csv', index=False)

# Print summary statistics
print("Sample data generated successfully!")
print("\nData Range:")
print(f"Years: 2007-2009")
print(f"Months: 12 per year")
print(f"Weeks: {df['CalendarWeek'].nunique()} total")
print("\nCountry distribution:")
for continent, countries in country_data.items():
    print(f"\n{continent} ({len(countries)} countries):")
    for country in countries.keys():
        print(f"  - {country}")

# Print some basic statistics
print("\nBasic Statistics:")
print(f"Total Records: {len(df):,}")
print(f"Date Range: {df['DateKey'].min().strftime('%Y-%m-%d')} to {df['DateKey'].max().strftime('%Y-%m-%d')}")
print(f"Average Sales: ${df['SalesAmount'].mean():,.2f}")
print(f"Max Sales: ${df['SalesAmount'].max():,.2f}")
print(f"Min Sales: ${df['SalesAmount'].min():,.2f}") 