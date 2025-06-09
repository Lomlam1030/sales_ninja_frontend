import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json
import branca.colormap as cm
from utils.page_config import set_page_config, add_page_title
from utils.theme import get_css, get_chart_template
import plotly.graph_objects as go
import numpy as np
import calendar
import plotly.express as px
from utils.data_loader import initialize_session_state, get_geography_data

# Configure the page
st.set_page_config(layout="wide", page_title="Geography - Sales Ninja")

# Add CSS and title
st.markdown(get_css(), unsafe_allow_html=True)
add_page_title(
    title="Geographic Sales Distribution",
    subtitle="Global Sales Performance by Region",
    emoji="🌍"
)

# Define warm color palette at the top of the file
warm_colors = ["#FF4B4B", "#FF8C00", "#FFD700"]  # Red, Dark Orange, Gold

# Helper Functions
def format_currency(value):
    """Format a numeric value as currency"""
    if pd.isna(value):
        return "$0.00"
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:,.2f}"

@st.cache_data
def get_country_name_mapping():
    """Return mapping of country names to GeoJSON country names"""
    return {
        'United States': 'United States of America',
        'United Kingdom': 'United Kingdom',
        'Germany': 'Germany',
        'France': 'France',
        'Canada': 'Canada',
        'Mexico': 'Mexico',
        'Spain': 'Spain',
        'Italy': 'Italy',
        'Netherlands': 'Netherlands',
        'Belgium': 'Belgium',
        'Switzerland': 'Switzerland',
        'Austria': 'Austria',
        'Sweden': 'Sweden',
        'Norway': 'Norway',
        'Denmark': 'Denmark',
        'Finland': 'Finland',
        'Ireland': 'Ireland',
        'Poland': 'Poland',
        'Greece': 'Greece',
        'Japan': 'Japan',
        'China': 'China',
        'India': 'India',
        'South Korea': 'Korea, Republic of',
        'Singapore': 'Singapore',
        'Taiwan': 'Taiwan',
        'Thailand': 'Thailand',
        'Malaysia': 'Malaysia',
        'Vietnam': 'Vietnam',
        'Costa Rica': 'Costa Rica',
        'Panama': 'Panama',
        'Guatemala': 'Guatemala',
        'Honduras': 'Honduras',
        'Nicaragua': 'Nicaragua',
        'El Salvador': 'El Salvador',
        'Belize': 'Belize'
    }

@st.cache_data
def load_geojson():
    """Load and cache the GeoJSON data"""
    try:
        with open('data/world-countries.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Could not find GeoJSON file.")
        return None

@st.cache_data(ttl=None, show_spinner=True)
def load_sales_data():
    """Load and prepare sales data"""
    try:
        df = pd.read_csv('data/sample_data_geography.csv',
            parse_dates=['DateKey'])
        
        # Clean and prepare data
        df['RegionCountryName'] = df['RegionCountryName'].str.strip()
        
        # Map country names
        country_mapping = get_country_name_mapping()
        df['country_geojson'] = df['RegionCountryName'].map(country_mapping)
        df = df[df['country_geojson'].notna()]
        
        # Rename columns
        df = df.rename(columns={
            'RegionCountryName': 'country',
            'ContinentName': 'continent',
            'SalesAmount': 'sales',
            'CalendarYear': 'year',
            'CalendarMonth': 'month',
            'CalendarWeek': 'week'
        })
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

@st.cache_data
def get_aggregated_data(df, selected_year=None):
    """Get aggregated data by country"""
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=['country_geojson', 'country', 'continent', 'sales_mean', 'sales_sum'])
    
    # Filter by year if specified
    if selected_year and selected_year != "All Years":
        df = df[df['year'] == int(selected_year)]
        
    agg_data = df.groupby(['country_geojson', 'country', 'continent']).agg({
        'sales': ['mean', 'sum', 'count']
    }).reset_index()
    
    # Flatten the column names
    agg_data.columns = ['country_geojson', 'country', 'continent', 'sales_mean', 'sales_sum', 'sales_count']
    return agg_data

def create_map(data, geojson_data, metric='sales_sum'):
    """Create the choropleth map"""
    if data is None or len(data) == 0:
        st.warning("No data available for the selected filters.")
        return None
        
    m = folium.Map(location=[20, 0], zoom_start=2, scrollWheelZoom=False)
    
    # Create colormap
    sales_values = data[metric].values
    if len(sales_values) > 0:
        vmin = sales_values.min()
        vmax = sales_values.max()
    else:
        vmin = 0
        vmax = 1
    
    colormap = cm.LinearColormap(
        colors=['#FFE5B4', '#FFD700', '#FFA500', '#FF4500'],
        vmin=vmin,
        vmax=vmax
    )
    
    colormap.add_to(m)
    colormap.caption = 'Total Sales' if metric == 'sales_sum' else 'Average Sales'
    
    # Create lookup dictionary
    country_data = data.set_index('country_geojson').to_dict('index')
    
    # Add country polygons
    for feature in geojson_data['features']:
        country_name = feature['properties']['name']
        if country_name in country_data:
            data = country_data[country_name]
            color = colormap(data[metric])
            
            tooltip = f"""
            <b>{country_name}</b><br>
            Total Sales: {format_currency(data['sales_sum'])}<br>
            Average Sales: {format_currency(data['sales_mean'])}<br>
            Number of Sales: {data['sales_count']:,}<br>
            Continent: {data['continent']}
            """
            
            folium.GeoJson(
                feature,
                style_function=lambda x, color=color: {
                    'fillColor': color,
                    'fillOpacity': 0.7,
                    'color': 'black',
                    'weight': 1,
                    'dashArray': '5, 5'
                },
                tooltip=folium.Tooltip(tooltip)
            ).add_to(m)
    
    return m

def create_bar_chart(data, metric='sales_sum', title=None):
    """Create bar chart of sales by country"""
    if data is None or len(data) == 0:
        st.warning("No data available for visualization.")
        return None
    
    if title is None:
        title = "Total Sales by Country" if metric == 'sales_sum' else "Average Sales by Country"
        
    fig = go.Figure(data=[
        go.Bar(
            name='Sales',
            x=data['country'],
            y=data[metric],
            text=[format_currency(val) for val in data[metric]],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Country",
        yaxis_title="Sales Amount",
        template=get_chart_template(),
        height=500
    )
    
    return fig

def create_time_series_chart(data, time_cols, region_col, metric='Total Sales', title=None):
    """Create time series chart of sales over time"""
    if data is None or len(data) == 0:
        st.warning("No data available for visualization.")
        return None
    
    # Create a date-like string for x-axis ordering
    if 'week' in time_cols:
        data['period'] = data.apply(
            lambda x: f"{x['year']}-{x['month']:02d}-W{x['week']:02d}", 
            axis=1
        )
    elif 'month' in time_cols:
        data['period'] = data.apply(
            lambda x: f"{x['year']}-{x['month']:02d}", 
            axis=1
        )
    elif 'quarter' in time_cols:
        data['period'] = data.apply(
            lambda x: f"{x['year']}-{x['quarter']}", 
            axis=1
        )
    else:
        data['period'] = data['year'].astype(str)

    # Create traces for each region
    fig = go.Figure()
    
    for region in sorted(data[region_col].unique()):
        region_data = data[data[region_col] == region]
        
        # Extract numeric values from currency strings
        if metric in ['Total Sales', 'Average Sales']:
            y_values = region_data[metric].str.replace('$', '').str.replace(',', '')
            y_values = y_values.str.replace('B', '000000000').str.replace('M', '000000')
            y_values = y_values.astype(float)
            hover_template = f"{region}<br>Period: %{{x}}<br>{metric}: %{{y:$,.2f}}<extra></extra>"
        else:
            y_values = region_data[metric].str.replace(',', '').astype(float)
            hover_template = f"{region}<br>Period: %{{x}}<br>{metric}: %{{y:,.0f}}<extra></extra>"
        
        fig.add_trace(go.Scatter(
            x=region_data['period'],
            y=y_values,
            name=region,
            mode='lines+markers',
            hovertemplate=hover_template
        ))
    
    # Update layout
    if title is None:
        if len(time_cols) > 1:
            period_type = time_cols[-1].capitalize()
        else:
            period_type = time_cols[0].capitalize()
        title = f"{metric} by {period_type}"

    fig.update_layout(
        title=title,
        xaxis_title="Time Period",
        yaxis_title=metric,
        template=get_chart_template(),
        height=500,
        showlegend=True,
        legend_title=region_col.capitalize(),
        hovermode='x unified'
    )
    
    return fig

# Initialize session state
initialize_session_state()

# Get the synthetic geography data
map_df = get_geography_data()

# Load Data
sales_df = load_sales_data()
if sales_df is None:
    st.error("Failed to load sales data. Please check the data file.")
    st.stop()

# Load GeoJSON
geojson_data = load_geojson()
if geojson_data is None:
    st.error("Failed to load GeoJSON data. Please check the file.")
    st.stop()

# 1. Map Section with its own filters
st.markdown("""<h2 class="table-header">🗺️ Sales Distribution Map</h2>""", unsafe_allow_html=True)

# Map filters
map_col1, map_col2 = st.columns(2)

with map_col1:
    available_continents = sorted(sales_df['continent'].unique())
    selected_continent = st.selectbox(
        "Select Continent",
        ["All Continents"] + available_continents,
        key="map_continent"
    )

with map_col2:
    if selected_continent != "All Continents":
        available_countries = sorted(sales_df[sales_df['continent'] == selected_continent]['country'].unique())
    else:
        available_countries = sorted(sales_df['country'].unique())
    
    selected_countries = st.multiselect(
        "Select Countries",
        options=["All Countries"] + available_countries,
        default=None,
        key="map_countries"
    )

# Add metric selector for map
map_metric = st.radio(
    "Select Map Metric",
    ["Total Sales", "Average Sales"],
    horizontal=True,
    key="map_metric"
)

# Filter data for map and summary
map_df = sales_df.copy()

if selected_continent != "All Continents":
    map_df = map_df[map_df['continent'] == selected_continent]
if selected_countries and "All Countries" not in selected_countries:
    map_df = map_df[map_df['country'].isin(selected_countries)]

# Aggregate data for both map and summary
map_aggregated_data = get_aggregated_data(map_df)
metric_col = 'sales_sum' if map_metric == "Total Sales" else 'sales_mean'

# Display map
m = create_map(map_aggregated_data, geojson_data, metric=metric_col)
if m is not None:
    folium_static(m, width=1200)

# 2. Summary Section
st.markdown("""<h2 class="table-header">📊 Sales Summary</h2>""", unsafe_allow_html=True)

if len(map_aggregated_data) > 0:
    # Create summary based on selected filters
    if selected_continent != "All Continents":
        summary = map_aggregated_data.groupby('country').agg({
            'sales_mean': 'mean',
            'sales_sum': 'sum',
            'sales_count': 'sum'
        }).reset_index()
        summary.columns = ['Country', 'Average Sales', 'Total Sales', 'Number of Sales']
    else:
        summary = map_aggregated_data.groupby('continent').agg({
            'sales_mean': 'mean',
            'sales_sum': 'sum',
            'sales_count': 'sum'
        }).reset_index()
        summary.columns = ['Continent', 'Average Sales', 'Total Sales', 'Number of Sales']

    summary['Average Sales'] = summary['Average Sales'].apply(format_currency)
    summary['Total Sales'] = summary['Total Sales'].apply(format_currency)
    summary['Number of Sales'] = summary['Number of Sales'].apply(lambda x: f"{x:,}")

    # Display summary table
    st.dataframe(
        summary,
        hide_index=True,
        column_config={
            "Country" if selected_continent != "All Continents" else "Continent": st.column_config.TextColumn("Region", width="medium"),
            "Average Sales": st.column_config.TextColumn("Average Sales", width="large"),
            "Total Sales": st.column_config.TextColumn("Total Sales", width="large"),
            "Number of Sales": st.column_config.TextColumn("Number of Sales", width="medium")
        }
    )

    # Display KPIs with context
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

    # Create context string for metrics
    context = ""
    if selected_continent != "All Continents":
        context += f" in {selected_continent}"
        if selected_countries and "All Countries" not in selected_countries:
            country_list = ", ".join(selected_countries)
            context += f" ({country_list})"

    with kpi_col1:
        st.metric(
            f"Total Sales{context}",
            format_currency(map_aggregated_data['sales_sum'].sum()),
            help=f"Total sales across selected regions{context}"
        )

    with kpi_col2:
        st.metric(
            f"Average Sales{context}",
            format_currency(map_aggregated_data['sales_mean'].mean()),
            help=f"Average sales across selected regions{context}"
        )

    with kpi_col3:
        region_type = "Countries" if selected_continent != "All Continents" else "Continents"
        st.metric(
            f"Number of {region_type}{context}",
            str(len(map_aggregated_data)),
            help=f"Number of {region_type.lower()} in the current selection"
        )

    # Bar Chart Visualization
    st.markdown("""<h2 class="table-header">📊 Sales by Region</h2>""", unsafe_allow_html=True)
    
    # Add metric selector for bar chart
    chart_metric = st.radio(
        "Select Chart Metric",
        ["Total Sales", "Average Sales"],
        horizontal=True,
        key="chart_metric"
    )
    
    # Create bar chart title with context
    chart_title = f"{chart_metric} by {'Country' if selected_continent != 'All Continents' else 'Continent'}"
    if context:
        chart_title += context
    
    # Create and display bar chart
    bar_metric_col = 'sales_sum' if chart_metric == "Total Sales" else 'sales_mean'

    # Determine which column to use for regions
    region_col = 'country' if selected_continent != "All Continents" else 'continent'

    fig = px.bar(
        map_aggregated_data,
        x=region_col,  # Use region_col which is either 'country' or 'continent'
        y=bar_metric_col,
        title=chart_title,
        labels={
            region_col: 'Region',  # Label it as Region in the display
            bar_metric_col: chart_metric
        },
        color_discrete_sequence=['#DAA520'],  # Dark golden yellow
        height=400
    )

    # Customize layout
    fig.update_layout(
        xaxis_title="Region",
        yaxis_title=chart_metric,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent surrounding
        bargap=0.3,  # Adjust gap between bars
        showlegend=False
    )

    # Format y-axis for currency values
    if bar_metric_col in ['sales_sum', 'sales_mean']:
        fig.update_layout(
            yaxis=dict(
                tickformat="$,.0f",
                gridcolor='rgba(128,128,128,0.1)'  # Light grid lines
            )
        )
    else:
        fig.update_layout(
            yaxis=dict(
                tickformat=",d",
                gridcolor='rgba(128,128,128,0.1)'  # Light grid lines
            )
        )

    # Update x-axis style
    fig.update_xaxes(
        gridcolor='rgba(128,128,128,0.1)',  # Light grid lines
        tickangle=45  # Angle the labels for better readability
    )

    st.plotly_chart(fig, use_container_width=True)

    # Time Analysis Section
    st.markdown("""<h2 class="table-header">📊 Time Series Analysis</h2>""", unsafe_allow_html=True)

    # Metric selection
    metric_options = {
        'sales_sum': 'Total Sales',
        'sales_mean': 'Average Sales',
        'sales_count': 'Number of Sales'
    }
    selected_metric = st.selectbox(
        "Select Metric",
        options=list(metric_options.keys()),
        format_func=lambda x: metric_options[x],
        key="time_metric"
    )
    time_metric = metric_options[selected_metric]

    # Start with data filtered by continent and country selections
    time_df = map_df.copy()
    if selected_continent != "All Continents":
        time_df = time_df[time_df['continent'] == selected_continent]
    if selected_countries and "All Countries" not in selected_countries:
        time_df = time_df[time_df['country'].isin(selected_countries)]

    # Calculate quarter from DateKey
    time_df['quarter'] = time_df['DateKey'].dt.quarter

    # Time filters in a single row
    time_col1, time_col2, time_col3, time_col4 = st.columns(4)

    # Year selection
    with time_col1:
        available_years = sorted(time_df['year'].unique())
        selected_year = st.selectbox(
            "Year",
            options=["All Years"] + available_years,
            key="time_year"
        )

    # Filter data by year if selected
    year_df = time_df
    if selected_year != "All Years":
        year_df = time_df[time_df['year'] == int(selected_year)]

    # Quarter selection
    with time_col2:
        available_quarters = sorted(year_df['quarter'].unique())
        selected_quarter = st.selectbox(
            "Quarter",
            options=["All Quarters"] + [f"Q{q}" for q in available_quarters],
            key="time_quarter"
        )

    # Filter data by quarter if selected and get available months
    quarter_df = year_df
    if selected_quarter != "All Quarters":
        quarter_num = int(selected_quarter[1])
        quarter_df = year_df[year_df['quarter'] == quarter_num]
        # Get months for this quarter
        quarter_months = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12]
        }
        available_months = sorted(set(quarter_df['month'].unique()) & set(quarter_months[quarter_num]))
    else:
        available_months = sorted(quarter_df['month'].unique())

    # Month selection
    with time_col3:
        selected_month = st.selectbox(
            "Month",
            options=["All Months"] + [calendar.month_abbr[m] for m in available_months],
            key="time_month"
        )

    # Filter data by month if selected and get available weeks
    month_df = quarter_df
    if selected_month != "All Months":
        month_num = list(calendar.month_abbr).index(selected_month)
        month_df = quarter_df[quarter_df['month'] == month_num]
        available_weeks = sorted(month_df['week'].unique())
    else:
        available_weeks = sorted(quarter_df['week'].unique())

    # Week selection
    with time_col4:
        selected_week = st.selectbox(
            "Week",
            options=["All Weeks"] + [f"Week {w}" for w in available_weeks],
            key="time_week"
        )

    # Final filtering based on week selection
    if selected_week != "All Weeks":
        week_num = int(selected_week.split()[1])
        time_df = month_df[month_df['week'] == week_num]
    elif selected_month != "All Months":
        month_num = list(calendar.month_abbr).index(selected_month)
        time_df = quarter_df[quarter_df['month'] == month_num]
    elif selected_quarter != "All Quarters":
        time_df = quarter_df
    elif selected_year != "All Years":
        time_df = year_df

    # Only proceed with visualization if we have data
    if len(time_df) > 0:
        # Determine x-axis based on selections
        if selected_week != "All Weeks":
            x_col = 'week'
            time_format = lambda x: f"Week {int(x)}"
            title_period = f"Week {week_num}"
        elif selected_month != "All Months":
            x_col = 'month'
            time_format = lambda x: calendar.month_abbr[int(x)]
            title_period = selected_month
        elif selected_quarter != "All Quarters":
            x_col = 'quarter'
            time_format = lambda x: f"Q{int(x)}"
            title_period = selected_quarter
        else:
            x_col = 'year'
            time_format = lambda x: str(int(x))
            title_period = "Year"

        # Get unique regions
        regions = sorted(time_df[region_col].unique())

        # Create a visualization for each region
        for region in regions:
            # Filter data for the current region
            region_df = time_df[time_df[region_col] == region]
            
            # Prepare data for visualization
            if selected_year != "All Years":
                # If specific year selected, show only that year's data
                groupby_cols = [x_col]
                title_year = f" ({selected_year})"
            else:
                # If all years, include year in grouping
                groupby_cols = ['year', x_col] if x_col != 'year' else ['year']
                title_year = ""

            # Aggregate data
            region_summary = region_df.groupby(groupby_cols).agg({
                'sales': ['mean', 'sum', 'count']
            }).reset_index()

            # Flatten column names
            if len(groupby_cols) > 1:
                region_summary.columns = groupby_cols + ['sales_mean', 'sales_sum', 'sales_count']
            else:
                region_summary.columns = [groupby_cols[0], 'sales_mean', 'sales_sum', 'sales_count']

            # Create x-axis labels
            if selected_year == "All Years" and x_col != 'year':
                region_summary['x_label'] = region_summary.apply(
                    lambda row: f"Y{int(row['year'])}-{time_format(row[x_col])}", axis=1
                )
            else:
                region_summary['x_label'] = region_summary[x_col].apply(time_format)

            # Create bar chart for the region
            fig = px.bar(
                region_summary,
                x='x_label',
                y=selected_metric,
                title=f"{time_metric} by {title_period} for {region}{title_year}",
                labels={
                    'x_label': title_period,
                    selected_metric: time_metric
                },
                color_discrete_sequence=['#DAA520'],  # Dark golden yellow
                height=400
            )

            # Customize layout
            fig.update_layout(
                xaxis_title=title_period,
                yaxis_title=time_metric,
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent surrounding
                bargap=0.3,  # Adjust gap between bars
                showlegend=False
            )

            # Format y-axis for currency values
            if selected_metric in ['sales_sum', 'sales_mean']:
                fig.update_layout(
                    yaxis=dict(
                        tickformat="$,.0f",
                        gridcolor='rgba(128,128,128,0.1)'  # Light grid lines
                    )
                )
            else:
                fig.update_layout(
                    yaxis=dict(
                        tickformat=",d",
                        gridcolor='rgba(128,128,128,0.1)'  # Light grid lines
                    )
                )

            # Update x-axis style
            fig.update_xaxes(
                gridcolor='rgba(128,128,128,0.1)',  # Light grid lines
                tickangle=45 if len(region_summary) > 6 else 0  # Angle labels only if many bars
            )

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")
        st.warning("Need both promotional and non-promotional data for comparison. Current distribution:\n\nPromotional transactions: 5\nNon-promotional transactions: 0\nUnable to calculate promotional impact. Please check the data or filters.")