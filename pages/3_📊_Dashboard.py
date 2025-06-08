import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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

# Update the color scheme constants
COLOR_SCHEME = {
    'primary': '#FF4B4B',    # Red
    'secondary': '#FF8C00',  # Dark Orange
    'accent': '#FFD700',     # Gold
    'text_primary': '#2C3E50',
    'background': 'rgba(255, 244, 230, 0.1)'  # Light warm background
}

def generate_sample_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    
    data = pd.DataFrame({
        'date': dates,
        'net_sales': np.random.normal(10000, 2000, len(dates)),
        'sales_volume': np.random.normal(500, 100, len(dates)),
        'has_promotion': np.random.choice([True, False], len(dates), p=[0.3, 0.7])
    })
    
    # Increase sales for promotional days
    data.loc[data['has_promotion'], 'net_sales'] *= 1.4
    data.loc[data['has_promotion'], 'sales_volume'] *= 1.5
    
    return data

# Load data
data = generate_sample_data()

# Dashboard Title
st.markdown("""<h1 class="dashboard-header">Sales Performance Dashboard</h1>""", unsafe_allow_html=True)

# Date Range Filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", data['date'].min())
with col2:
    end_date = st.date_input("End Date", data['date'].max())

# Filter data based on date range
filtered_data = data[(data['date'].dt.date >= start_date) & (data['date'].dt.date <= end_date)]

# Update KPI metrics styling
st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.1), rgba(255, 140, 0, 0.1));
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid rgba(255, 140, 0, 0.2);
    ">
    <h2 class="metric-header">Key Performance Indicators</h2>
    </div>
""", unsafe_allow_html=True)

# Calculate KPIs
total_net_sales = filtered_data['net_sales'].sum()
total_volume = filtered_data['sales_volume'].sum()
avg_net_sales = filtered_data['net_sales'].mean()
avg_volume = filtered_data['sales_volume'].mean()

# Display KPIs in columns
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Total Net Sales", f"${total_net_sales:,.2f}")
with kpi2:
    st.metric("Total Sales Volume", f"{total_volume:,.0f}")
with kpi3:
    st.metric("Avg Daily Net Sales", f"${avg_net_sales:,.2f}")
with kpi4:
    st.metric("Avg Daily Volume", f"{avg_volume:,.0f}")

# Promotional Impact Analysis
st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.1), rgba(255, 140, 0, 0.1));
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 1px solid rgba(255, 140, 0, 0.2);
    ">
    <h2 class="analysis-header">Promotional Impact Analysis</h2>
    </div>
""", unsafe_allow_html=True)

# Calculate metrics by promotion status
promo_analysis = filtered_data.groupby('has_promotion').agg({
    'net_sales': ['mean', 'sum', 'count'],
    'sales_volume': ['mean', 'sum']
}).round(2)

# Create comparison metrics
promo_impact = pd.DataFrame({
    'Metric': ['Average Daily Net Sales', 'Average Daily Volume'],
    'With Promotion': [
        promo_analysis.loc[True, ('net_sales', 'mean')],
        promo_analysis.loc[True, ('sales_volume', 'mean')]
    ],
    'Without Promotion': [
        promo_analysis.loc[False, ('net_sales', 'mean')],
        promo_analysis.loc[False, ('sales_volume', 'mean')]
    ]
})

promo_impact['Lift %'] = ((promo_impact['With Promotion'] - promo_impact['Without Promotion']) / 
                         promo_impact['Without Promotion'] * 100).round(2)

# Display promotional impact
col1, col2 = st.columns([2, 1])

with col1:
    # Update the promotional impact chart colors
    fig = go.Figure(data=[
        go.Bar(
            name='With Promotion',
            x=promo_impact['Metric'],
            y=promo_impact['With Promotion'],
            marker_color='#FF4B4B'  # Red
        ),
        go.Bar(
            name='Without Promotion',
            x=promo_impact['Metric'],
            y=promo_impact['Without Promotion'],
            marker_color='#FF8C00'  # Dark Orange
        )
    ])
    
    fig.update_layout(
        title='Sales Metrics: Promotional vs Non-Promotional',
        barmode='group',
        plot_bgcolor='rgba(255, 244, 230, 0.1)',
        paper_bgcolor='rgba(255, 244, 230, 0)',
        height=400,
        font={'color': '#2C3E50'},
        title_font_color='#FF4B4B'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Display impact metrics
    st.markdown("### Promotional Lift")
    for idx, row in promo_impact.iterrows():
        st.metric(
            row['Metric'],
            f"{row['Lift %']:+.2f}%",
            delta_color="normal"
        )

# Time Series Analysis
st.markdown("""<h2 class="analysis-header">Time Series Analysis</h2>""", unsafe_allow_html=True)

# Create time series plots
fig_time = go.Figure()

# Update the time series chart colors
fig_time.add_trace(go.Scatter(
    x=filtered_data['date'],
    y=filtered_data['net_sales'],
    name='Net Sales',
    line=dict(color='#FF4B4B', width=2)  # Red
))

fig_time.add_trace(go.Scatter(
    x=filtered_data['date'],
    y=filtered_data['sales_volume'],
    name='Sales Volume',
    line=dict(color='#FFD700', width=2),  # Gold
    yaxis='y2'
))

fig_time.update_layout(
    title='Net Sales and Volume Over Time',
    xaxis=dict(
        title='Date',
        gridcolor='rgba(255, 140, 0, 0.1)',
        title_font_color='#FF8C00'
    ),
    yaxis=dict(
        title='Net Sales ($)',
        titlefont=dict(color='#FF4B4B'),
        tickfont=dict(color='#FF4B4B'),
        gridcolor='rgba(255, 75, 75, 0.1)'
    ),
    yaxis2=dict(
        title='Sales Volume',
        titlefont=dict(color='#FFD700'),
        tickfont=dict(color='#FFD700'),
        overlaying='y',
        side='right',
        gridcolor='rgba(255, 215, 0, 0.1)'
    ),
    plot_bgcolor='rgba(255, 244, 230, 0.1)',
    paper_bgcolor='rgba(255, 244, 230, 0)',
    height=500,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color='#2C3E50')
    )
)

st.plotly_chart(fig_time, use_container_width=True)

# Update the CSS styling
st.markdown("""
    <style>
    .dashboard-header {
        background: linear-gradient(45deg, #FF4B4B, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 1em;
        text-align: center;
        padding: 20px;
    }
    .metric-header, .analysis-header {
        color: #FF4B4B;
        font-size: 1.8em;
        margin-top: 1em;
        margin-bottom: 0.5em;
        border-left: 5px solid #FF8C00;
        padding-left: 10px;
    }
    div[data-testid="stMetricValue"] {
        color: #FF4B4B !important;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #FF8C00 !important;
    }
    div[data-testid="stMetricDelta"] {
        color: #FFD700 !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        background-color: rgba(255, 244, 230, 0.1);
        border-radius: 10px;
        padding: 10px !important;
        border: 1px solid rgba(255, 140, 0, 0.2);
    }
    div[data-testid="stHorizontalBlock"] > div:hover {
        box-shadow: 0 0 10px rgba(255, 140, 0, 0.2);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    </style>
"""
, unsafe_allow_html=True) 