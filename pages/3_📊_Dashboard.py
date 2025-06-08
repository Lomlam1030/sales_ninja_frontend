import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.page_config import set_page_config, add_page_title

# Configure the page
set_page_config(title="Dashboard")

# Add the styled title
add_page_title(
    title="Sales Performance Dashboard",
    subtitle="Revenue, Costs, and Profit Analysis",
    emoji="📊"
)

def generate_dummy_data():
    """Generate dummy data with revenues, costs, sales volume, and profits"""
    current_date = datetime.now()
    start_date = current_date - timedelta(days=3*365)  # 3 years of data
    dates = pd.date_range(start=start_date, end=current_date, freq='D')
    
    # Product categories and subcategories
    categories = {
        'Electronics': ['Smartphones', 'Laptops', 'Accessories'],
        'Fashion': ['Clothing', 'Shoes', 'Accessories'],
        'Home & Living': ['Furniture', 'Decor', 'Kitchen'],
        'Sports': ['Equipment', 'Apparel', 'Accessories']
    }
    
    # Base values
    base_volume = 1000  # base daily sales volume
    base_price = 100    # average price per unit
    base_cost = 70      # average cost per unit
    
    # Generate daily data with some randomness and trends
    data = []
    for date in dates:
        # For each date, generate data for different categories and subcategories
        for category, subcategories in categories.items():
            for subcategory in subcategories:
                # Add seasonal variation (higher in Q4, lower in Q1)
                season_factor = 1 + 0.3 * np.sin(2 * np.pi * (date.dayofyear / 365 - 0.25))
                # Add day of week variation (lower on weekends)
                dow_factor = 0.7 if date.weekday() >= 5 else 1.0
                # Add yearly growth (10% per year)
                year_factor = 1 + 0.1 * ((date - start_date).days / 365)
                
                # Randomly determine if product is on promotion
                is_promotion = np.random.choice([True, False], p=[0.2, 0.8])  # 20% chance of promotion
                
                # Adjust price and volume based on promotion
                promotion_price_factor = 0.8 if is_promotion else 1.0  # 20% discount on promotion
                promotion_volume_factor = 1.5 if is_promotion else 1.0  # 50% more volume on promotion
                
                # Calculate base metrics with variations
                volume = int(base_volume * season_factor * dow_factor * year_factor * 
                           promotion_volume_factor * np.random.normal(1, 0.1))
                price_per_unit = base_price * promotion_price_factor * np.random.normal(1, 0.05)
                cost_per_unit = base_cost * np.random.normal(1, 0.03)
                
                revenue = volume * price_per_unit
                cost = volume * cost_per_unit
                profit = revenue - cost
                
                data.append({
                    'date': date,
                    'year': date.year,
                    'category': category,
                    'subcategory': subcategory,
                    'is_promotion': is_promotion,
                    'volume': volume,
                    'revenue': revenue,
                    'cost': cost,
                    'profit': profit
                })
    
    return pd.DataFrame(data)

def aggregate_data(df, freq='D'):
    """Aggregate data by the specified frequency"""
    if freq == 'D':
        return df
    
    agg_cols = {
        'volume': 'sum',
        'revenue': 'sum',
        'cost': 'sum',
        'profit': 'sum',
        'year': 'first',
        'category': 'first',
        'subcategory': 'first',
        'is_promotion': 'first'
    }
    
    # Group by the appropriate frequency
    if freq == 'M':
        return df.resample('M', on='date').agg(agg_cols).reset_index()
    else:  # 'Q'
        return df.resample('Q', on='date').agg(agg_cols).reset_index()

# Generate fresh data
st.session_state.dashboard_df = generate_dummy_data()

# Sidebar filters
st.sidebar.header('Filters')

# Year filter
selected_year = st.sidebar.selectbox(
    'Select Year',
    sorted(st.session_state.dashboard_df['year'].unique(), reverse=True)
)

# Category and subcategory filter
categories = st.session_state.dashboard_df['category'].unique()
selected_category = st.sidebar.selectbox('Product Category', ['All'] + list(categories))

if selected_category != 'All':
    subcategories = st.session_state.dashboard_df[
        st.session_state.dashboard_df['category'] == selected_category
    ]['subcategory'].unique()
    selected_subcategory = st.sidebar.selectbox('Product Subcategory', ['All'] + list(subcategories))
else:
    selected_subcategory = 'All'

# Promotion filter
selected_promotion = st.sidebar.selectbox('Promotion', ['All', 'Yes', 'No'])

# Filter data based on all selections
filtered_df = st.session_state.dashboard_df[
    st.session_state.dashboard_df['year'] == selected_year
]

if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
if selected_subcategory != 'All':
    filtered_df = filtered_df[filtered_df['subcategory'] == selected_subcategory]

if selected_promotion != 'All':
    is_promotion = True if selected_promotion == 'Yes' else False
    filtered_df = filtered_df[filtered_df['is_promotion'] == is_promotion]

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Daily View", "Monthly View", "Quarterly View"])

# Get the appropriate view based on selected tab
if tab1.active:
    display_df = filtered_df
    period_label = "Daily"
elif tab2.active:
    display_df = aggregate_data(filtered_df, 'M')
    period_label = "Monthly"
else:
    display_df = aggregate_data(filtered_df, 'Q')
    period_label = "Quarterly"

# Style for KPI containers
st.markdown("""
<style>
.kpi-container {
    padding: 1rem;
    border-radius: 10px;
    margin-top: 2rem;
    background-color: rgba(14, 17, 23, 0.2);
}
[data-testid="stHorizontalBlock"] > div {
    padding: 0 !important;
    gap: 1rem !important;
}
[data-testid="stHorizontalBlock"] {
    gap: 1rem !important;
    padding: 0 0.5rem !important;
}
.kpi-metric {
    background: linear-gradient(135deg, rgba(255, 87, 34, 0.1) 0%, rgba(255, 167, 38, 0.1) 100%);
    border: 2px solid rgba(255, 87, 34, 0.3);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 0.5rem;
}
.kpi-metric:hover {
    border-color: rgba(255, 87, 34, 0.6);
    box-shadow: 0 5px 15px rgba(255, 87, 34, 0.2);
}
.kpi-value-container {
    padding: 0.5rem;
    background-color: rgba(255, 87, 34, 0.1);
    border-radius: 8px;
    margin-bottom: 0.5rem;
}
.kpi-value {
    color: #ff5722;
    font-size: 2rem;
    font-weight: bold;
    line-height: 1.2;
    margin: 0;
    padding: 0.5rem;
}
.kpi-label {
    color: #fafafa;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 0.5rem;
    background-color: rgba(255, 167, 38, 0.1);
    border-radius: 8px;
    margin-top: auto;
}
div[data-testid="stMetricValue"] {
    display: none;
}
div[data-testid="stMetricLabel"] {
    display: none;
}
div[data-testid="stMetricDelta"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Display KPIs
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

# Calculate KPI values
total_revenue = display_df['revenue'].sum()
total_costs = display_df['cost'].sum()
total_volume = display_df['volume'].sum()
total_profit = display_df['profit'].sum()

# Format values
def format_currency(value):
    if value >= 1e9:
        return f"${value/1e9:.1f}B"
    elif value >= 1e6:
        return f"${value/1e6:.1f}M"
    else:
        return f"${value:,.0f}"

def format_volume(value):
    if value >= 1e9:
        return f"{value/1e9:.1f}B"
    elif value >= 1e6:
        return f"{value/1e6:.1f}M"
    else:
        return f"{value:,.0f}"

def create_kpi_html(label, value, tooltip):
    return f"""
    <div class="kpi-metric" title="{tooltip}">
        <div class="kpi-value-container">
            <div class="kpi-value">{value}</div>
        </div>
        <div class="kpi-label">{label}</div>
    </div>
    """

# Display metrics in columns
with col1:
    st.markdown(
        create_kpi_html(
            "Total Revenue",
            format_currency(total_revenue),
            "Total revenue for the selected period"
        ),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        create_kpi_html(
            "Total Costs",
            format_currency(total_costs),
            "Total costs for the selected period"
        ),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        create_kpi_html(
            "Sales Volume",
            format_volume(total_volume),
            "Total units sold in the selected period"
        ),
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        create_kpi_html(
            "Total Profit",
            format_currency(total_profit),
            "Total profit for the selected period"
        ),
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# Add charts section
st.markdown("""
<style>
.chart-container {
    background-color: rgba(14, 17, 23, 0.2);
    border-radius: 10px;
    padding: 1rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)

# Create 2x2 grid for charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Revenue Chart
    revenue_chart = px.bar(
        display_df,
        x='date',
        y='revenue',
        title=f'{period_label} Revenue',
        color_discrete_sequence=['#ff5722'],  # Deep orange
        template='plotly_dark'
    )
    revenue_chart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='',
        yaxis_title='Revenue ($)',
        showlegend=False
    )
    st.plotly_chart(revenue_chart, use_container_width=True)

    # Sales Volume Chart
    volume_chart = px.bar(
        display_df,
        x='date',
        y='volume',
        title=f'{period_label} Sales Volume',
        color_discrete_sequence=['#ffa726'],  # Yellow-orange
        template='plotly_dark'
    )
    volume_chart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='',
        yaxis_title='Units Sold',
        showlegend=False
    )
    st.plotly_chart(volume_chart, use_container_width=True)

with chart_col2:
    # Costs Chart
    costs_chart = px.bar(
        display_df,
        x='date',
        y='cost',
        title=f'{period_label} Costs',
        color_discrete_sequence=['#f4511e'],  # Darker orange
        template='plotly_dark'
    )
    costs_chart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='',
        yaxis_title='Costs ($)',
        showlegend=False
    )
    st.plotly_chart(costs_chart, use_container_width=True)

    # Profit Chart
    profit_chart = px.bar(
        display_df,
        x='date',
        y='profit',
        title=f'{period_label} Profit',
        color_discrete_sequence=['#e64a19'],  # Reddish-orange
        template='plotly_dark'
    )
    profit_chart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title='',
        yaxis_title='Profit ($)',
        showlegend=False
    )
    st.plotly_chart(profit_chart, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ... rest of the code ... 