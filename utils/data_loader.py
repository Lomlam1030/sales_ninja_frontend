"""Data loading utilities for the Sales Ninja dashboard."""

import streamlit as st
from datetime import datetime
from typing import Optional, Tuple
import pandas as pd

from services.data_source import get_data_source
from config.settings import settings
from .sales_calculations import (
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

def load_dashboard_data(
    year: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and cache dashboard data.
    
    Args:
        year: Optional year filter
        start_date: Optional start date (YYYY-MM-DD)
        end_date: Optional end date (YYYY-MM-DD)
    
    Returns:
        Tuple of (actual_data, predicted_data) DataFrames
    """
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def _load_data(y: Optional[int], sd: Optional[str], ed: Optional[str]):
        if 'data_source' not in st.session_state:
            st.session_state.data_source = get_data_source()
        
        with st.spinner("Loading sales data..."):
            return st.session_state.data_source.load_dashboard_data(
                year=y,
                start_date=sd,
                end_date=ed
            )
    
    return _load_data(year, start_date, end_date)

def get_date_filters() -> Tuple[Optional[int], Optional[str], Optional[str]]:
    """Get date filters from sidebar."""
    st.sidebar.header("📅 Date Range")
    filter_type = st.sidebar.radio(
        "Filter by:",
        ["Year", "Custom Date Range"],
        index=0
    )
    
    if filter_type == "Year":
        year = st.sidebar.selectbox(
            "Select Year",
            options=[2007, 2008, 2009],
            index=0
        )
        return year, None, None
    else:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime(2007, 1, 1),
                min_value=datetime(2007, 1, 1),
                max_value=datetime(2009, 12, 31)
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime(2007, 12, 31),
                min_value=datetime(2007, 1, 1),
                max_value=datetime(2009, 12, 31)
            )
        return None, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d") 