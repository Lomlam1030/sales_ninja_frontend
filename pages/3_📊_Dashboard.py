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
    'primary': '#4169E1',    # Royal Blue
    'secondary': '#9370DB',  # Medium Purple
    'accent': '#E6E6FA',     # Lavender
    'text_primary': '#E6E6FA',
    'background': 'rgba(25, 25, 112, 0.1)'  # Midnight Blue with opacity
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
            background: linear-gradient(135deg, #A8C4E9, #E0D3ED);
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            border: 2px solid #4A78B3;
            box-shadow: 0 2px 6px rgba(74, 120, 179, 0.2);
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
            background: linear-gradient(135deg, #A8C4E9, #E0D3ED);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border: 2px solid #4A78B3;
            box-shadow: 0 2px 6px rgba(74, 120, 179, 0.2);
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
        line=dict(color='#2B4C7E', width=2)  # Dark Blue
    ))

    fig_time.add_trace(go.Scatter(
        x=filtered_data['date'],
        y=filtered_data['total_volume'],
        name='Sales Volume',
        line=dict(color='#4A78B3', width=2),  # Medium Blue
        yaxis='y2'
    ))

    fig_time.update_layout(
        title='Net Sales and Volume Over Time',
        xaxis=dict(
            title='Date',
            gridcolor='rgba(74, 120, 179, 0.1)',  # Medium Blue with opacity
            title_font_color='#2B4C7E'
        ),
        yaxis=dict(
            title='Net Sales ($)',
            titlefont=dict(color='#2B4C7E'),
            tickfont=dict(color='#2B4C7E'),
            gridcolor='rgba(74, 120, 179, 0.1)'
        ),
        yaxis2=dict(
            title='Sales Volume',
            titlefont=dict(color='#4A78B3'),
            tickfont=dict(color='#4A78B3'),
            overlaying='y',
            side='right',
            gridcolor='rgba(74, 120, 179, 0.1)'
        ),
        plot_bgcolor='#E6EEF8',  # Light Blue
        paper_bgcolor='#F8FAFC',  # Very Light Blue
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#2B4C7E')
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
        background: linear-gradient(45deg, #4169E1, #9370DB);  /* Royal Blue to Medium Purple */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 1em;
        text-align: center;
        padding: 20px;
    }
    .metric-header, .analysis-header {
        color: #4169E1;  /* Royal Blue */
        font-size: 1.8em;
        margin-top: 1em;
        margin-bottom: 0.5em;
        border-left: 5px solid #9370DB;  /* Medium Purple */
        padding-left: 10px;
    }
    div[data-testid="stMetricValue"] {
        color: #4169E1 !important;  /* Royal Blue */
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #9370DB !important;  /* Medium Purple */
    }
    div[data-testid="stMetricDelta"] {
        color: #E6E6FA !important;  /* Lavender */
    }
    div[data-testid="stHorizontalBlock"] > div {
        background-color: rgba(25, 25, 112, 0.1);  /* Midnight Blue with opacity */
        border-radius: 10px;
        padding: 10px !important;
        border: 1px solid rgba(147, 112, 219, 0.2);  /* Medium Purple with opacity */
    }
    div[data-testid="stHorizontalBlock"] > div:hover {
        box-shadow: 0 0 10px rgba(147, 112, 219, 0.2);  /* Medium Purple with opacity */
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True) 