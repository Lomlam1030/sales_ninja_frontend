import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_dummy_sales_data(days=365):
    """Generate dummy sales data for the past year."""
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days)
    
    # Create base trend with seasonal component
    t = np.arange(days)
    seasonal = 1000 * np.sin(2 * np.pi * t / 365) + 500 * np.sin(2 * np.pi * t / 30)
    trend = 50 * t + 10000
    
    # Add random noise
    noise = np.random.normal(0, 1000, days)
    sales = trend + seasonal + noise
    
    # Ensure no negative values
    sales = np.maximum(sales, 0)
    
    return pd.DataFrame({
        'date': dates,
        'net_sales': sales
    })

def aggregate_sales_data(df, period='D'):
    """Aggregate sales data by specified period."""
    period_map = {
        'D': 'Daily',
        'M': 'Monthly',
        'Q': 'Quarterly'
    }
    
    agg_df = df.set_index('date').resample(period)['net_sales'].mean().reset_index()
    agg_df['period'] = period_map[period]
    return agg_df

def show_home():
    # Page title and description with custom styling
    st.markdown("""
    <style>
    .title {
        font-size: 42px;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 20px;
    }
    .description {
        font-size: 20px;
        color: #424242;
        margin-bottom: 30px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="title">Sales Ninja Analytics Dashboard</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="description">
    Welcome to Sales Ninja Analytics! This intelligent dashboard provides comprehensive insights 
    into your sales performance and predicts future trends. Leverage advanced analytics and 
    machine learning to make data-driven decisions and optimize your sales strategy.
    </p>
    """, unsafe_allow_html=True)
    
    # Generate dummy sales data
    sales_data = generate_dummy_sales_data()
    
    # Time period selector
    period = st.selectbox(
        "Select Time Period",
        ["Daily", "Monthly", "Quarterly"],
        index=1
    )
    
    # Map selection to pandas period codes
    period_map = {
        "Daily": "D",
        "Monthly": "M",
        "Quarterly": "Q"
    }
    
    # Aggregate data based on selected period
    agg_data = aggregate_sales_data(sales_data, period_map[period])
    
    # Create line chart
    fig = px.line(
        agg_data,
        x='date',
        y='net_sales',
        title=f'{period} Net Sales Overview',
        labels={
            'date': 'Time Period',
            'net_sales': 'Net Sales ($)'
        }
    )
    
    # Customize the chart
    fig.update_traces(
        line=dict(width=2),
        hovertemplate="<br>".join([
            "Date: %{x}",
            "Net Sales: $%{y:,.2f}",
            "<extra></extra>"
        ])
    )
    
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f0f0f0'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f0f0f0',
            tickprefix='$'
        )
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add key insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_sales = agg_data['net_sales'].mean()
        st.metric(
            "Average Sales",
            f"${avg_sales:,.2f}",
            delta=f"{((avg_sales / agg_data['net_sales'].iloc[0]) - 1) * 100:.1f}%"
        )
    
    with col2:
        peak_sales = agg_data['net_sales'].max()
        st.metric(
            "Peak Sales",
            f"${peak_sales:,.2f}",
            delta=f"{((peak_sales / avg_sales) - 1) * 100:.1f}%"
        )
    
    with col3:
        current_trend = (
            (agg_data['net_sales'].iloc[-1] / agg_data['net_sales'].iloc[-2]) - 1
        ) * 100
        st.metric(
            "Current Trend",
            f"${agg_data['net_sales'].iloc[-1]:,.2f}",
            delta=f"{current_trend:.1f}%"
        ) 