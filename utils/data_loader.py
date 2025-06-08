import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data
def load_sales_data():
    """
    Load the real sales data and cache it using streamlit's caching mechanism.
    Returns a DataFrame with the sales data.
    """
    # Create sample DataFrame with the structure you provided
    data = {
        'SalesKey': [1, 2, 3, 4, 5],
        'DateKey': ['2007-01-02', '2007-02-12', '2008-01-24', '2008-01-13', '2008-01-22'],
        'ChannelKey': [1, 4, 1, 2, 2],
        'StoreKey': [209, 308, 156, 306, 306],
        'ProductKey': [956, 766, 1175, 1429, 1133],
        'PromotionKey': [10, 2, 11, 10, 10],
        'UnitCost': [91.05, 10.15, 209.03, 132.90, 144.52],
        'UnitPrice': [198.0, 19.9, 410.0, 289.0, 436.2],
        'SalesQuantity': [8, 4, 9, 8, 24],
        'ReturnQuantity': [0, 0, 0, 0, 0],
        'ProductSubcategoryKey': [23.0, 22.0, 27.0, 31.0, 24.0],
        'ProductSubcategoryName': ['Digital Cameras', 'Computers Accessories', 'Camcorders', 'Touch Screen Phones', 'Digital SLR Cameras'],
        'ProductCategoryKey': [4.0, 3.0, 4.0, 5.0, 4.0],
        'ProductCategoryName': ['Cameras and camcorders', 'Computers', 'Cameras and camcorders', 'Cell phones', 'Cameras and camcorders'],
        'GeographyKey': [738, 693, 449, 586, 586],
        'StoreType': ['Store', 'Reseller', 'Store', 'Online', 'Online'],
        'StoreName': ['Contoso Baildon Store', 'Contoso North America Reseller', 'Contoso Cambridge Store', 'Contoso Europe Online Store', 'Contoso Europe Online Store'],
        'ContinentName': ['Europe', 'North America', 'Europe', 'Europe', 'Europe'],
        'CalendarWeekLabel': ['Week 1', 'Week 7', 'Week 4', 'Week 3', 'Week 4'],
        'RegionCountryName': ['United Kingdom', 'United States', 'United Kingdom', 'Germany', 'Germany']
    }
    
    df = pd.DataFrame(data)
    df['DateKey'] = pd.to_datetime(df['DateKey'])
    return df

@st.cache_data
def load_geography_data():
    """
    Load synthetic geography data for the geography page.
    This maintains the existing synthetic data structure.
    """
    # Generate synthetic data for geography visualization
    current_date = datetime.now()
    start_date = current_date - timedelta(days=3*365)  # 3 years of data
    dates = pd.date_range(start=start_date, end=current_date, freq='D')
    
    # Define regions and countries
    regions = {
        'Europe': ['Germany', 'France', 'United Kingdom', 'Italy', 'Spain'],
        'North America': ['United States', 'Canada', 'Mexico'],
        'Asia': ['Japan', 'China', 'South Korea', 'India', 'Singapore'],
        'Oceania': ['Australia', 'New Zealand'],
        'South America': ['Brazil', 'Argentina', 'Chile'],
        'Africa': ['South Africa', 'Egypt', 'Nigeria']
    }
    
    # Generate data
    data = []
    for date in dates:
        for continent, countries in regions.items():
            for country in countries:
                # Add seasonal variation
                season_factor = 1 + 0.3 * np.sin(2 * np.pi * (date.dayofyear / 365 - 0.25))
                # Add day of week variation
                dow_factor = 0.7 if date.weekday() >= 5 else 1.0
                # Add yearly growth
                year_factor = 1 + 0.1 * ((date - start_date).days / 365)
                
                # Base values with randomization
                sales = np.random.normal(10000, 1000) * season_factor * dow_factor * year_factor
                
                data.append({
                    'date': date,
                    'year': date.year,
                    'month': date.month,
                    'quarter': (date.month-1)//3 + 1,
                    'week': date.isocalendar()[1],
                    'continent': continent,
                    'country': country,
                    'sales': sales
                })
    
    return pd.DataFrame(data)

def initialize_session_state():
    """Initialize the session state with both real and synthetic data if not already present."""
    if 'sales_df' not in st.session_state:
        st.session_state.sales_df = load_sales_data()
    if 'geography_df' not in st.session_state:
        st.session_state.geography_df = load_geography_data()

def get_sales_data():
    """Get the real sales data from session state."""
    initialize_session_state()
    return st.session_state.sales_df

def get_geography_data():
    """Get the synthetic geography data from session state."""
    initialize_session_state()
    return st.session_state.geography_df 