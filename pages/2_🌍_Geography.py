import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
import json
import branca.colormap as cm
import requests
from pathlib import Path
from utils.page_config import set_page_config, add_page_title

# Configure the page
set_page_config(title="Geography")

# Add the styled title
add_page_title(
    title="Geographic Sales Distribution",
    subtitle="Global Sales Performance by Region",
    emoji="🌍"
)

# Custom color scheme matching the dashboard
COLORS = {
    'primary': '#2ecc71',    # Green from the dashboard
    'secondary': '#3498db',  # Blue from the dashboard
    'background': '#0e1117', # Dark background
    'text': '#fafafa',      # Light text
    'accent': '#95a5a6'     # Subtle accent
}

@st.cache_data
def load_sales_data():
    """Load and prepare sales data from CSV"""
    try:
        # Load the data
        df = pd.read_csv('data/data_dashboard_merged.csv')
        
        # Convert DateKey to datetime and extract year
        df['DateKey'] = pd.to_datetime(df['DateKey'])
        df['year'] = df['DateKey'].dt.year
        
        # Rename columns to match our expected format
        df = df.rename(columns={
            'CountryName': 'country',
            'ContinentName': 'continent',
            'NetSales': 'net_sales'
        })
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

@st.cache_data
def get_geojson_data():
    """Get GeoJSON data - will be replaced with API call in production"""
    try:
        url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to load GeoJSON data")
            return None
    except Exception as e:
        st.error(f"Error loading GeoJSON data: {str(e)}")
        return None

# Load the data
if 'sales_df' not in st.session_state:
    st.session_state.sales_df = load_sales_data()

sales_df = st.session_state.sales_df
if sales_df is None:
    st.error("Failed to load sales data. Please check the data file.")
    st.stop()

geo_data = get_geojson_data()

# Sidebar filters
with st.sidebar:
    st.markdown(f"""
    <style>
    .sidebar-title {{
        font-size: 24px;
        font-weight: bold;
        color: {COLORS['primary']};
        margin-bottom: 20px;
    }}
    .filter-section {{
        background-color: rgba(46, 204, 113, 0.1);
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title">Filters</p>', unsafe_allow_html=True)
    
    # Year selection
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.subheader("📅 Year")
    
    # Get unique years from the actual data
    available_years = sorted(sales_df['year'].astype(int).unique(), reverse=True)
    
    # Default to the most recent year
    default_year = max(available_years)
    
    # Year multiselect with default to most recent year
    selected_years = st.multiselect(
        "Select Years",
        options=available_years,
        default=[default_year],
        key="year_selector",
        help="Select one or more years to view data for. Defaults to the most recent year."
    )
    
    # If no years selected, use the most recent year
    if not selected_years:
        selected_years = [default_year]
        st.info(f"No year selected. Showing data for {default_year}.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Continent selection
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.subheader("🌍 Geography")
    
    # Filter continents based on selected years
    available_continents = sorted(sales_df[sales_df['year'].isin(selected_years)]['continent'].unique())
    selected_continent = st.selectbox(
        "Select Continent",
        options=available_continents,
        key="continent_selector"
    )
    
    # Country selection based on continent and selected years
    available_countries = sorted(
        sales_df[
            (sales_df['continent'] == selected_continent) & 
            (sales_df['year'].isin(selected_years))
        ]['country'].unique()
    )
    
    # Default to top 5 countries by sales for the selected continent and years
    default_countries = (
        sales_df[
            (sales_df['continent'] == selected_continent) & 
            (sales_df['year'].isin(selected_years))
        ]
        .groupby('country')['net_sales']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .index
        .tolist()
    )
    
    selected_countries = st.multiselect(
        "Select Countries",
        options=available_countries,
        default=default_countries,
        key="country_selector",
        help="Select countries to view data for. Defaults to top 5 countries by sales."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Filter data based on selections
filtered_df = sales_df[
    (sales_df['year'].isin(selected_years)) &
    (sales_df['country'].isin(selected_countries))
]

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Daily View", "Monthly View", "Quarterly View"])

def aggregate_by_period(df, freq='D'):
    """Aggregate sales data by the specified frequency"""
    df = df.copy()
    if freq == 'D':
        return df
    
    # For monthly and quarterly views, we'll take the average per period
    if freq == 'M':
        # Monthly average
        return df.groupby(['country', 'continent', 'year', df['DateKey'].dt.month])['net_sales'].mean().reset_index()
    else:  # 'Q'
        # Quarterly average
        return df.groupby(['country', 'continent', 'year', df['DateKey'].dt.quarter])['net_sales'].mean().reset_index()

# Get the appropriate view based on selected tab
if tab1.active:
    display_df = filtered_df
    period_label = "Daily"
elif tab2.active:
    display_df = aggregate_by_period(filtered_df, 'M')
    period_label = "Monthly Average"
else:
    display_df = aggregate_by_period(filtered_df, 'Q')
    period_label = "Quarterly Average"

# Main content styling
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #00B4D8;
    margin-bottom: 20px;
    text-align: center;
}
.map-section {
    background-color: rgba(0,0,0,0);
    padding: 20px;
    border-radius: 5px;
    margin-top: 30px;
    width: 100%;
}
.map-container {
    border: 2px solid rgba(46, 204, 113, 0.3);
    border-radius: 10px;
    overflow: hidden;
    margin: 20px auto;
    width: 100%;
    background: rgba(14, 17, 23, 0.2);
    transition: all 0.3s ease;
}
.map-container:hover {
    border-color: rgba(46, 204, 113, 0.6);
    box-shadow: 0 5px 15px rgba(46, 204, 113, 0.2);
}
.folium-map {
    width: 100% !important;
    height: 500px !important;  /* Match the height of the Home page graph */
}
[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# Map section - use full width
st.markdown('<div class="map-section">', unsafe_allow_html=True)

# Add section header with proper styling
st.markdown("""
<style>
.section-header {
    color: #2ecc71;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    padding-left: 10px;
    border-left: 4px solid #2ecc71;
}
</style>
<h2 class="section-header">📍 Geographic Sales Distribution</h2>
""", unsafe_allow_html=True)

# Create the map
if geo_data:
    # Create a base map
    m = folium.Map(
        location=[30, 0],
        zoom_start=2,
        tiles='cartodbdark_matter',  # Dark theme map
        min_zoom=2,
        max_zoom=6
    )
    
    # Calculate sales by country for the selected years
    country_sales = display_df.groupby(['country', 'continent'])['net_sales'].sum().reset_index()
    
    # Create color scale
    min_sales = country_sales['net_sales'].min()
    max_sales = country_sales['net_sales'].max()
    
    colormap = cm.LinearColormap(
        colors=['#3498db', '#2ecc71'],  # From blue to green
        vmin=min_sales,
        vmax=max_sales
    )
    
    # Format sales values and add them to the GeoJSON properties
    for feature in geo_data['features']:
        country_name = feature['properties']['name']
        country_data = country_sales[country_sales['country'] == country_name]
        if not country_data.empty:
            sales_value = country_data['net_sales'].values[0]
            continent = country_data['continent'].values[0]
            if sales_value >= 1e9:
                formatted_sales = f"${sales_value/1e9:.1f}B"
            elif sales_value >= 1e6:
                formatted_sales = f"${sales_value/1e6:.1f}M"
            else:
                formatted_sales = f"${sales_value:,.0f}"
            feature['properties']['formatted_sales'] = formatted_sales
            feature['properties']['continent'] = continent
        else:
            feature['properties']['formatted_sales'] = "No data"
            feature['properties']['continent'] = "N/A"
    
    # Add the choropleth layer
    choropleth = folium.Choropleth(
        geo_data=geo_data,
        name='choropleth',
        data=country_sales,
        columns=['country', 'net_sales'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Net Sales ({period_label})',
        smooth_factor=0
    ).add_to(m)
    
    # Add hover functionality
    style_function = lambda x: {
        'fillColor': '#000000',
        'color': '#000000',
        'fillOpacity': 0.1,
        'weight': 0.1
    }
    highlight_function = lambda x: {
        'fillColor': '#000000',
        'color': '#2ecc71',
        'fillOpacity': 0.5,
        'weight': 2
    }
    
    # Add GeoJson layer with hover effect
    NIL = folium.features.GeoJson(
        geo_data,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name', 'continent', 'formatted_sales'],
            aliases=['Country', 'Continent', 'Net Sales'],
            style=("background-color: #0e1117; color: #2ecc71; font-family: courier new; font-size: 14px; padding: 10px;")
        )
    )
    m.add_child(NIL)
    m.keep_in_front(NIL)
    
    # Add the map to Streamlit with proper container styling
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    folium_static(m, width=None)  # Let the container control the width
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Unable to load map data. Please try again later.")

st.markdown('</div>', unsafe_allow_html=True)  # Close map-section div

# Display metrics with proper formatting
col1, col2, col3 = st.columns(3)

with col1:
    total_sales = display_df['net_sales'].sum()
    formatted_total = f"${total_sales:,.0f}" if total_sales < 1e9 else f"${total_sales/1e9:.1f}B"
    st.metric(
        "Total Net Sales",
        formatted_total
    )

with col2:
    avg_sales = display_df['net_sales'].mean()
    formatted_avg = f"${avg_sales:,.0f}" if avg_sales < 1e9 else f"${avg_sales/1e9:.1f}B"
    st.metric(
        f"Average Sales per Country",
        formatted_avg
    )

with col3:
    top_country_data = display_df.groupby('country')['net_sales'].sum().sort_values(ascending=False).head(1)
    top_country = top_country_data.index[0]
    st.metric(
        "Top Performing Country",
        top_country
    ) 