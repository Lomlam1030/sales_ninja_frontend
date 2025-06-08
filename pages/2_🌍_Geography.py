import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json
import branca.colormap as cm
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

@st.cache_data
def load_geojson():
    """Load GeoJSON data for the world map"""
    try:
        with open('data/world-countries.json') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading GeoJSON data: {str(e)}")
        return None

def aggregate_by_period(df, freq='D'):
    """
    Aggregate sales data by the specified frequency.
    Returns the average sales per period (day/month/quarter) for each country.
    """
    df = df.copy()
    
    if freq == 'D':
        # Daily average - first get total sales per day per country
        daily_totals = df.groupby(['DateKey', 'country_geojson', 'country', 'continent'])['net_sales'].sum().reset_index()
        # Then get the average daily sales for each country
        return daily_totals.groupby(['country_geojson', 'country', 'continent'])['net_sales'].mean().reset_index()
            
    elif freq == 'M':
        # Monthly average
        df['year_month'] = df['DateKey'].dt.to_period('M')
        monthly_totals = df.groupby(['year_month', 'country_geojson', 'country', 'continent'])['net_sales'].sum().reset_index()
        return monthly_totals.groupby(['country_geojson', 'country', 'continent'])['net_sales'].mean().reset_index()
            
    else:  # 'Q'
        # Quarterly average
        df['year_quarter'] = df['DateKey'].dt.to_period('Q')
        quarterly_totals = df.groupby(['year_quarter', 'country_geojson', 'country', 'continent'])['net_sales'].sum().reset_index()
        return quarterly_totals.groupby(['country_geojson', 'country', 'continent'])['net_sales'].mean().reset_index()

def aggregate_by_period_with_totals(df, freq='D'):
    """
    Aggregate sales data by the specified frequency.
    Returns both average and total sales per period for each country.
    """
    df = df.copy()
    
    if freq == 'D':
        # Daily aggregation
        daily_totals = df.groupby(['DateKey', 'country_geojson', 'country', 'continent'])['net_sales'].sum().reset_index()
        result = daily_totals.groupby(['country_geojson', 'country', 'continent']).agg({
            'net_sales': ['mean', 'sum']
        }).reset_index()
        result.columns = ['country_geojson', 'country', 'continent', 'avg_sales', 'total_sales']
        return result
            
    elif freq == 'M':
        # Monthly aggregation
        df['year_month'] = df['DateKey'].dt.to_period('M')
        monthly_totals = df.groupby(['year_month', 'country_geojson', 'country', 'continent'])['net_sales'].sum().reset_index()
        result = monthly_totals.groupby(['country_geojson', 'country', 'continent']).agg({
            'net_sales': ['mean', 'sum']
        }).reset_index()
        result.columns = ['country_geojson', 'country', 'continent', 'avg_sales', 'total_sales']
        return result
            
    else:  # 'Q'
        # Quarterly aggregation
        df['year_quarter'] = df['DateKey'].dt.to_period('Q')
        quarterly_totals = df.groupby(['year_quarter', 'country_geojson', 'country', 'continent'])['net_sales'].sum().reset_index()
        result = quarterly_totals.groupby(['country_geojson', 'country', 'continent']).agg({
            'net_sales': ['mean', 'sum']
        }).reset_index()
        result.columns = ['country_geojson', 'country', 'continent', 'avg_sales', 'total_sales']
        return result

# Custom color scheme matching the dashboard
COLORS = {
    'primary': '#2ecc71',    # Green from the dashboard
    'secondary': '#3498db',  # Blue from the dashboard
    'background': '#0e1117', # Dark background
    'text': '#fafafa',      # Light text
    'accent': '#95a5a6'     # Subtle accent
}

@st.cache_data
def get_country_name_mapping():
    """Return mapping of country names to GeoJSON country names"""
    return {
        'United States': 'United States of America',
        'UK': 'United Kingdom',
        'United Kingdom': 'United Kingdom',
        'Germany': 'Germany',
        'Germany ': 'Germany',
        'France': 'France',
        'Australia': 'Australia',
        'Canada': 'Canada',
        'Mexico': 'Mexico',
        'Brazil': 'Brazil',
        'Spain': 'Spain',
        'Italy': 'Italy',
        'Italy ': 'Italy',
        'Netherlands': 'Netherlands',
        'the Netherlands': 'Netherlands',
        'Belgium': 'Belgium',
        'Switzerland': 'Switzerland',
        'Austria': 'Austria',
        'Sweden': 'Sweden',
        'Sweden ': 'Sweden',
        'Norway': 'Norway',
        'Denmark': 'Denmark',
        'Denmark ': 'Denmark',
        'Finland': 'Finland',
        'Japan': 'Japan',
        'China': 'China',
        'India': 'India',
        'South Korea': 'Korea, Republic of',
        'Singapore': 'Singapore',
        'New Zealand': 'New Zealand',
        'Bhutan': 'Bhutan',
        'Russia': 'Russia',
        'Taiwan': 'Taiwan',
        'Syria': 'Syria',
        'Kyrgyzstan': 'Kyrgyzstan',
        'Iran': 'Iran',
        'Ireland': 'Ireland',
        'Ireland ': 'Ireland',
        'Slovenia': 'Slovenia',
        'Thailand': 'Thailand',
        'Turkmenistan': 'Turkmenistan',
        'Romania': 'Romania',
        'Romania ': 'Romania',
        'Portugal': 'Portugal',
        'Pakistan': 'Pakistan',
        'Armenia': 'Armenia',
        'Greece': 'Greece',
        'Greece ': 'Greece',
        'Malta': 'Malta',
        'Poland': 'Poland',
        'Poland ': 'Poland'
    }

@st.cache_data
def load_sales_data():
    """Load and prepare sales data from CSV"""
    try:
        file_path = 'data/data_dashboard_final.csv'
        if not Path(file_path).exists():
            st.error(f"Data file not found at: {file_path}")
            return None

        df = pd.read_csv(file_path, usecols=[
            'DateKey', 'SalesAmount', 'CalendarYear', 'CalendarQuarterLabel',
            'CalendarMonthLabel', 'ContinentName', 'RegionCountryName'
        ])
        
        df['DateKey'] = pd.to_datetime(df['DateKey'])
        df['year'] = df['DateKey'].dt.year
        
        # Clean country names by trimming whitespace
        df['RegionCountryName'] = df['RegionCountryName'].str.strip()
        
        # Get country name mapping
        country_mapping = get_country_name_mapping()
        
        # Map country names to GeoJSON country names
        df['country_geojson'] = df['RegionCountryName'].map(country_mapping)
        
        # Log unmapped countries
        unmapped_countries = df[df['country_geojson'].isna()]['RegionCountryName'].unique()
        if len(unmapped_countries) > 0:
            st.warning(f"Some countries could not be mapped: {', '.join(sorted(unmapped_countries))}")
        
        # Remove rows with unmapped countries
        df = df[df['country_geojson'].notna()]
        
        if len(df) == 0:
            st.error("No data available after mapping countries. Please check the country mapping.")
            return None
        
        # Rename columns to match our expected format
        df = df.rename(columns={
            'RegionCountryName': 'country',
            'ContinentName': 'continent',
            'SalesAmount': 'net_sales'
        })
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load the data
if 'sales_df' not in st.session_state:
    st.session_state.sales_df = load_sales_data()

sales_df = st.session_state.sales_df
if sales_df is None:
    st.error("Failed to load sales data. Please check the data file.")
    st.stop()

geo_data = load_geojson()

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
    height: 500px !important;
}
[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# Create radio buttons for view selection
view_options = ["Daily View", "Monthly View", "Quarterly View"]
selected_view = st.radio("Select View", view_options, horizontal=True)

# Get the appropriate view based on selection
if selected_view == "Daily View":
    display_df = aggregate_by_period(sales_df, 'D')
    table_df = aggregate_by_period_with_totals(sales_df, 'D')
    period_label = "Day"
elif selected_view == "Monthly View":
    display_df = aggregate_by_period(sales_df, 'M')
    table_df = aggregate_by_period_with_totals(sales_df, 'M')
    period_label = "Month"
else:  # Quarterly View
    display_df = aggregate_by_period(sales_df, 'Q')
    table_df = aggregate_by_period_with_totals(sales_df, 'Q')
    period_label = "Quarter"

# Debug information in sidebar
st.sidebar.write("Current view:", period_label)
st.sidebar.write("Number of records:", len(display_df))
if len(display_df) > 0:
    st.sidebar.write("Sample values:", display_df['net_sales'].head())

# Map section
st.markdown('<div class="map-section">', unsafe_allow_html=True)

# Add section header
st.markdown(f"""
<style>
.section-header {{
    color: #2ecc71;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    padding-left: 10px;
    border-left: 4px solid #2ecc71;
}}
</style>
<h2 class="section-header">📍 Geographic Sales Distribution (per {period_label})</h2>
""", unsafe_allow_html=True)

if geo_data:
    # Create a base map
    m = folium.Map(
        location=[30, 0],
        zoom_start=2,
        tiles='cartodbdark_matter',
        min_zoom=2,
        max_zoom=6
    )
    
    # Use display_df directly since it's already aggregated properly
    country_sales = display_df
    
    # Create color scale
    min_sales = country_sales['net_sales'].min()
    max_sales = country_sales['net_sales'].max()
    
    colormap = cm.LinearColormap(
        colors=['#3498db', '#2ecc71'],  # From blue to green
        vmin=min_sales,
        vmax=max_sales
    )
    
    # Format sales values for GeoJSON
    for feature in geo_data['features']:
        country_name = feature['properties']['name']
        country_data = country_sales[country_sales['country_geojson'] == country_name]
        if not country_data.empty:
            sales_value = country_data['net_sales'].values[0]
            continent = country_data['continent'].values[0]
            if sales_value >= 1e9:
                formatted_sales = f"${sales_value/1e9:.2f}B"
            elif sales_value >= 1e6:
                formatted_sales = f"${sales_value/1e6:.2f}M"
            else:
                formatted_sales = f"${sales_value:,.2f}"
            feature['properties']['formatted_sales'] = f"{formatted_sales} per {period_label.lower()}"
            feature['properties']['continent'] = continent
        else:
            feature['properties']['formatted_sales'] = "No data"
            feature['properties']['continent'] = "N/A"

    # Add choropleth layer
    choropleth = folium.Choropleth(
        geo_data=geo_data,
        name='choropleth',
        data=country_sales,
        columns=['country_geojson', 'net_sales'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Average Net Sales per {period_label}',
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
    
    # Add the map to Streamlit
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    folium_static(m, width=None)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Unable to load map data. Please try again later.")

st.markdown('</div>', unsafe_allow_html=True)

# Add table section after the map
st.markdown("""
<style>
.table-header {
    color: #2ecc71;
    font-size: 24px;
    font-weight: bold;
    margin: 30px 0 20px 0;
    padding-left: 10px;
    border-left: 4px solid #2ecc71;
}
.filter-section {
    background-color: rgba(46, 204, 113, 0.05);
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
}
.stDataFrame {
    font-size: 16px !important;
}
[data-testid="stDataFrameResizable"] {
    background-color: rgba(46, 204, 113, 0.05);
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
}
[data-testid="stDataFrameResizable"] td {
    background-color: transparent !important;
}
[data-testid="stDataFrameResizable"] th {
    background-color: rgba(46, 204, 113, 0.1) !important;
    color: #2ecc71 !important;
}
</style>
<h2 class="table-header">📊 Sales by Country</h2>
""", unsafe_allow_html=True)

# Prepare the table data
table_data = table_df.copy()
table_data = table_data.sort_values('avg_sales', ascending=False)

# Format the sales columns
def format_currency(value):
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:,.2f}"

table_data['Average Sales'] = table_data['avg_sales'].apply(format_currency)
table_data['Total Sales'] = table_data['total_sales'].apply(format_currency)

# Add filters above the table
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

# Create filtered dataset
filtered_data = table_data.copy()

# Get unique continents and sort them
continents = sorted(filtered_data['continent'].unique())
selected_continent = col1.selectbox(
    "Select Continent",
    ["All Continents"] + continents,
    key="continent_filter"
)

# Apply continent filter and get available countries
if selected_continent != "All Continents":
    filtered_data = filtered_data[filtered_data['continent'] == selected_continent]

# Get available countries based on current filter
available_countries = sorted(filtered_data['country'].unique())
selected_country = col2.selectbox(
    "Select Country",
    ["All Countries"] + available_countries,
    key="country_filter"
)

# Apply country filter
if selected_country != "All Countries":
    filtered_data = filtered_data[filtered_data['country'] == selected_country]

# Format the sales columns for the filtered data
filtered_data['Average Sales'] = filtered_data['avg_sales'].apply(format_currency)
filtered_data['Total Sales'] = filtered_data['total_sales'].apply(format_currency)

# Debug information
with st.expander("Debug Information"):
    st.write("Selected continent:", selected_continent)
    st.write("Selected country:", selected_country)
    st.write("Number of records after filtering:", len(filtered_data))
    if len(filtered_data) > 0:
        st.write("Sample of filtered data:")
        st.write(filtered_data[['continent', 'country', 'avg_sales', 'total_sales']].head())

st.markdown('</div>', unsafe_allow_html=True)

# Prepare final table with selected columns and renamed
final_table = filtered_data[[
    'continent',
    'country', 
    'Average Sales',
    'Total Sales'
]].rename(columns={
    'country': 'Country',
    'continent': 'Continent'
})

# Add period information to column headers
final_table = final_table.rename(columns={
    'Average Sales': f'Average Sales per {period_label}',
    'Total Sales': f'Total Sales (All {period_label}s)'
})

# Calculate height based on number of rows
# Add 3 for header and padding
num_rows = len(final_table) + 3
# If less than 10 rows, show all without scrolling
height = min(max(num_rows * 35, 200), 400) if len(final_table) <= 10 else 400

# Display the table with custom formatting
st.dataframe(
    final_table,
    hide_index=True,
    height=height,
    column_config={
        "Continent": st.column_config.TextColumn(
            "Continent",
            width="medium"
        ),
        "Country": st.column_config.TextColumn(
            "Country",
            width="medium"
        ),
        f"Average Sales per {period_label}": st.column_config.TextColumn(
            f"Average Sales per {period_label}",
            width="large"
        ),
        f"Total Sales (All {period_label}s)": st.column_config.TextColumn(
            f"Total Sales (All {period_label}s)",
            width="large"
        )
    }
)

# Display metrics with proper formatting
col1, col2, col3 = st.columns(3)

with col1:
    avg_total_sales = display_df['net_sales'].mean()
    formatted_total = f"${avg_total_sales/1e9:.2f}B" if avg_total_sales >= 1e9 else (
        f"${avg_total_sales/1e6:.2f}M" if avg_total_sales >= 1e6 else f"${avg_total_sales:,.2f}"
    )
    st.metric(
        f"Average Net Sales per {period_label}",
        formatted_total
    )

with col2:
    num_countries = len(display_df['country'].unique())
    st.metric(
        "Number of Countries",
        f"{num_countries:,}"
    )

with col3:
    top_country_data = display_df.nlargest(1, 'net_sales')
    top_country = top_country_data['country'].iloc[0]
    top_sales = top_country_data['net_sales'].iloc[0]
    formatted_top = f"${top_sales/1e9:.2f}B" if top_sales >= 1e9 else (
        f"${top_sales/1e6:.2f}M" if top_sales >= 1e6 else f"${top_sales:,.2f}"
    )
    st.metric(
        f"Top Country (per {period_label})",
        f"{top_country}",
        f"{formatted_top}"
    ) 