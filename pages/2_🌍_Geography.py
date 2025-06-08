import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json
import branca.colormap as cm
from pathlib import Path
from utils.page_config import set_page_config, add_page_title
import plotly.express as px
import plotly.graph_objects as go

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
st.sidebar.write("Number of Countries:", len(display_df['country'].unique()))
if len(display_df) > 0:
    st.sidebar.write("Sample Countries:", ", ".join(display_df['country'].head().tolist()))

# Add debug information for columns
st.sidebar.write("Available columns:", list(table_df.columns))

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
    
    # Calculate sales by country
    country_sales = display_df.copy()
    
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

# Add filters above the table
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

# Create filtered dataset
filtered_data = table_df.copy()

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
selected_countries = col2.multiselect(
    "Select Countries",
    available_countries,
    default=[],
    key="country_filter"
)

# Apply country filter
if selected_countries:
    filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]

# Format the sales columns for the filtered data
def format_currency(value):
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:,.2f}"

filtered_data['Average Sales'] = filtered_data['avg_sales'].apply(format_currency)
filtered_data['Total Sales'] = filtered_data['total_sales'].apply(format_currency)

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

# Calculate KPIs based on filtered data
def calculate_kpis(data, continent_filter, country_filters):
    if country_filters:
        # Use selected countries
        filtered_data = data[data['country'].isin(country_filters)]
        num_countries = len(country_filters)
        region_type = "Selected Countries"
    elif continent_filter != "All Continents":
        # Use selected continent
        filtered_data = data[data['continent'] == continent_filter]
        num_countries = len(filtered_data['country'].unique())
        region_type = continent_filter
    else:
        # Use all data
        filtered_data = data
        num_countries = len(filtered_data['country'].unique())
        region_type = "All Continents"
    
    avg_sales = filtered_data['avg_sales'].mean()
    total_sales = filtered_data['total_sales'].sum()
    
    # Format the average sales
    if avg_sales >= 1e9:
        formatted_avg = f"${avg_sales/1e9:.2f}B"
    elif avg_sales >= 1e6:
        formatted_avg = f"${avg_sales/1e6:.2f}M"
    else:
        formatted_avg = f"${avg_sales:,.2f}"
    
    # Format the total sales
    if total_sales >= 1e9:
        formatted_total = f"${total_sales/1e9:.2f}B"
    elif total_sales >= 1e6:
        formatted_total = f"${total_sales/1e6:.2f}M"
    else:
        formatted_total = f"${total_sales:,.2f}"
    
    return formatted_avg, formatted_total, num_countries, region_type

# Get KPI values
avg_sales, total_sales, num_countries, region_type = calculate_kpis(
    table_df,
    selected_continent,
    selected_countries
)

# Create three columns for KPIs
col1, col2, col3 = st.columns(3)

# KPI 1: Average Sales
with col1:
    st.metric(
        f"Average Net Sales per {period_label}",
        avg_sales,
        help=region_type
    )

# KPI 2: Total Sales
with col2:
    st.metric(
        f"Total Net Sales (All {period_label}s)",
        total_sales,
        help=region_type
    )

# KPI 3: Number of Countries
with col3:
    st.metric(
        "Number of Countries",
        num_countries,
        help=region_type
    )

# Add bar chart section
st.markdown("""
<h2 class="table-header">📊 Sales Comparison</h2>
""", unsafe_allow_html=True)

# Prepare data for bar chart based on filters
def prepare_bar_chart_data(data, continent_filter, country_filters):
    if country_filters:
        # Show selected countries
        chart_data = data[data['country'].isin(country_filters)].copy()
        group_by = 'country'
        title = f"Average Sales by Country"
    elif continent_filter != "All Continents":
        # Show countries in selected continent
        chart_data = data[data['continent'] == continent_filter].copy()
        group_by = 'country'
        title = f"Average Sales by Country in {continent_filter}"
    else:
        # Show all continents
        chart_data = data.copy()
        group_by = 'continent'
        title = "Average Sales by Continent"
    
    # Group and calculate averages
    agg_data = chart_data.groupby(group_by)['avg_sales'].mean().reset_index()
    agg_data = agg_data.sort_values('avg_sales', ascending=True)  # Sort for better visualization
    
    return agg_data, title, group_by

# Get aggregated data for bar chart
agg_data, chart_title, group_by = prepare_bar_chart_data(
    table_df, 
    selected_continent, 
    selected_countries
)

# Create bar chart
fig = go.Figure()

# Add bars
fig.add_trace(go.Bar(
    x=agg_data['avg_sales'],
    y=agg_data[group_by],
    orientation='h',
    marker_color='#2ecc71',
    text=[f"${x:,.2f}" for x in agg_data['avg_sales']],  # Format as currency
    textposition='auto',
))

# Update layout
fig.update_layout(
    title=dict(
        text=f"{chart_title} (per {period_label})",
        x=0.5,
        xanchor='center'
    ),
    xaxis_title="Average Sales ($)",
    yaxis_title=group_by.title(),
    height=max(len(agg_data) * 50, 400),  # Dynamic height based on number of bars
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#2ecc71'),
    showlegend=False,
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(46, 204, 113, 0.1)',
        tickformat="$,.2f"  # Format as currency
    ),
    yaxis=dict(
        showgrid=False,
        automargin=True
    ),
    bargap=0.2
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Add time comparison table
st.markdown("""
<h2 class="table-header">⏱️ Time Comparison</h2>
""", unsafe_allow_html=True)

# Prepare time comparison data
def prepare_time_comparison(data, continent_filter, country_filters, period):
    if country_filters:
        comparison_data = data[data['country'].isin(country_filters)].copy()
        group_cols = ['country']
    elif continent_filter != "All Continents":
        comparison_data = data[data['continent'] == continent_filter].copy()
        group_cols = ['country']
    else:
        comparison_data = data.copy()
        group_cols = ['continent']
    
    # Calculate period averages
    period_avg = comparison_data.groupby(group_cols)['avg_sales'].mean().reset_index()
    period_total = comparison_data.groupby(group_cols)['total_sales'].sum().reset_index()
    
    # Format currencies
    period_avg['Average per ' + period] = period_avg['avg_sales'].apply(format_currency)
    period_total['Total All ' + period + 's'] = period_total['total_sales'].apply(format_currency)
    
    # Merge and clean up
    final_data = period_avg.merge(period_total, on=group_cols)
    final_data = final_data.drop(['avg_sales', 'total_sales'], axis=1)
    
    # Rename columns
    if 'country' in group_cols:
        final_data = final_data.rename(columns={'country': 'Region'})
    else:
        final_data = final_data.rename(columns={'continent': 'Region'})
    
    return final_data

# Get time comparison data
time_comparison = prepare_time_comparison(
    table_df,
    selected_continent,
    selected_countries,
    period_label
)

# Display time comparison table
st.dataframe(
    time_comparison,
    hide_index=True,
    height=min(max((len(time_comparison) + 1) * 35, 200), 400),
    column_config={
        "Region": st.column_config.TextColumn(
            "Region",
            width="medium"
        ),
        f"Average per {period_label}": st.column_config.TextColumn(
            f"Average per {period_label}",
            width="large"
        ),
        f"Total All {period_label}s": st.column_config.TextColumn(
            f"Total All {period_label}s",
            width="large"
        )
    }
) 