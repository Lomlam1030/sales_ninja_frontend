import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.page_config import set_page_config, add_page_title
from utils.data_queries import get_daily_sales, get_kpi_metrics, get_promotion_impact
from google.cloud import bigquery

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

# Initialize BigQuery client
client = bigquery.Client()

# Dashboard Title
st.markdown("""<h1 class="dashboard-header">Sales Performance Dashboard</h1>""", unsafe_allow_html=True)

# Date Range Filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(2007, 1, 1))
with col2:
    end_date = st.date_input("End Date", datetime(2009, 12, 31))

try:
    # Get data from BigQuery
    filtered_data = get_daily_sales(start_date, end_date)
    kpi_data = get_kpi_metrics(start_date, end_date)
    promo_data = get_promotion_impact(start_date, end_date)

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

    # Display KPIs in columns
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric("Total Net Sales", f"${kpi_data['total_net_sales'].iloc[0]:,.2f}")
    with kpi2:
        st.metric("Total Sales Volume", f"{kpi_data['total_volume'].iloc[0]:,.0f}")
    with kpi3:
        st.metric("Total Transactions", f"{kpi_data['total_transactions'].iloc[0]:,.0f}")
    with kpi4:
        st.metric("Avg Transaction Value", f"${kpi_data['avg_transaction_value'].iloc[0]:,.2f}")

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

    # Calculate promotional impact
    promo_metrics = []
    for metric in ['total_sales', 'avg_sale_value', 'total_volume', 'avg_volume', 'transaction_count']:
        promo_val = promo_data[promo_data['has_promotion']][metric].iloc[0]
        non_promo_val = promo_data[~promo_data['has_promotion']][metric].iloc[0]
        lift = ((promo_val - non_promo_val) / non_promo_val) * 100
        promo_metrics.append({
            'Metric': metric.replace('_', ' ').title(),
            'Promotional': promo_val,
            'Non-Promotional': non_promo_val,
            'Lift %': lift
        })

    promo_impact = pd.DataFrame(promo_metrics)

    # Display promotional metrics
    col1, col2 = st.columns(2)

    with col1:
        # Create comparison table
        fig_table = go.Figure(data=[go.Table(
            header=dict(
                values=['Metric', 'Promotional', 'Non-Promotional'],
                fill_color='rgba(255, 140, 0, 0.1)',
                align='left'
            ),
            cells=dict(
                values=[
                    promo_impact['Metric'],
                    promo_impact['Promotional'].apply(lambda x: f"${x:,.2f}" if 'value' in str(promo_impact['Metric']).lower() else f"{x:,.0f}"),
                    promo_impact['Non-Promotional'].apply(lambda x: f"${x:,.2f}" if 'value' in str(promo_impact['Metric']).lower() else f"{x:,.0f}")
                ],
                align='left'
            )
        )])
        st.plotly_chart(fig_table, use_container_width=True)

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
        y=filtered_data['total_net_sales'],
        name='Net Sales',
        line=dict(color='#FF4B4B', width=2)  # Red
    ))

    fig_time.add_trace(go.Scatter(
        x=filtered_data['date'],
        y=filtered_data['total_volume'],
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

except Exception as e:
    st.error(f"Error loading dashboard data: {str(e)}")
    st.info("Please check your BigQuery connection and try again.")

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