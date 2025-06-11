import streamlit as st
from .sales_calculations import (
    load_dashboard_data,
    calculate_daily_net_sales,
    get_sales_summary_stats,
    get_available_years,
    get_available_months,
    get_available_weeks
)

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'actual_data' not in st.session_state or 'predicted_data' not in st.session_state:
        actual_data, predicted_data = load_dashboard_data()
        st.session_state['actual_data'] = actual_data
        st.session_state['predicted_data'] = predicted_data

def get_geography_data():
    """Get geography-related data from the loaded dataset."""
    initialize_session_state()
    df = st.session_state['actual_data']
    
    # Group by continent and calculate total sales
    geography_data = df.groupby('continent')['net_sales'].sum().reset_index()
    return geography_data

def get_daily_sales(year=None, month=None, week=None):
    """Get daily sales data for both actual and predicted."""
    initialize_session_state()
    return calculate_daily_net_sales(
        st.session_state['actual_data'],
        st.session_state['predicted_data'],
        year, month, week
    )

def get_kpi_metrics(year=None, month=None, week=None):
    """Get KPI metrics for the dashboard."""
    initialize_session_state()
    actual_stats, predicted_stats = get_sales_summary_stats(
        st.session_state['actual_data'],
        st.session_state['predicted_data'],
        year, month, week
    )
    return actual_stats, predicted_stats

def get_promotion_impact():
    """Get promotion impact data."""
    initialize_session_state()
    df = st.session_state['actual_data']
    
    # Group by promotion flag and calculate average sales
    promotion_data = df.groupby('PromotionKey')['net_sales'].agg(['mean', 'count']).reset_index()
    promotion_data.columns = ['promotion_id', 'avg_sales', 'count']
    return promotion_data 