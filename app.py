import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from typing import Optional
import traceback

from config.settings import settings, DataSource
from services.data_source import get_data_source

# Page config
st.set_page_config(
    page_title="Sales Ninja Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'data_source' not in st.session_state:
    try:
        st.session_state.data_source = get_data_source()
    except Exception as e:
        st.error(f"Failed to initialize data source: {str(e)}")
        st.error("Detailed error: " + traceback.format_exc())
        st.stop()

def load_data(
    year: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> tuple:
    """Load and cache data from the configured data source."""
    try:
        @st.cache_data(ttl=3600)  # Cache for 1 hour
        def _load_data(y: Optional[int], sd: Optional[str], ed: Optional[str]):
            with st.spinner("Loading sales data..."):
                try:
                    return st.session_state.data_source.load_dashboard_data(
                        year=y,
                        start_date=sd,
                        end_date=ed
                    )
                except Exception as e:
                    st.error(f"Error loading data: {str(e)}")
                    st.error("Detailed error: " + traceback.format_exc())
                    raise
        return _load_data(year, start_date, end_date)
    except Exception as e:
        st.error(f"Error in load_data: {str(e)}")
        st.error("Detailed error: " + traceback.format_exc())
        raise

def main():
    try:
        st.title("📊 Sales Ninja Dashboard")
        
        # Data source info
        st.sidebar.info(f"Data Source: {settings.DATA_SOURCE.value}")
        
        # Date filters
        st.sidebar.header("📅 Date Filters")
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
            start_date = None
            end_date = None
        else:
            year = None
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
            start_date = start_date.strftime("%Y-%m-%d") if start_date else None
            end_date = end_date.strftime("%Y-%m-%d") if end_date else None
        
        try:
            # Load data
            df_actual, df_predicted = load_data(year, start_date, end_date)
            
            if df_actual.empty:
                st.warning("No actual sales data found for the selected period.")
                return
            
            # Display data info
            st.sidebar.metric("Actual Data Points", f"{len(df_actual):,}")
            st.sidebar.metric("Predicted Data Points", f"{len(df_predicted):,}")
            
            # Sales Overview
            st.header("📈 Sales Overview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_sales = df_actual["net_sales"].sum()
                st.metric("Total Sales", f"${total_sales:,.2f}")
            
            with col2:
                avg_sales = df_actual["net_sales"].mean()
                st.metric("Average Sales", f"${avg_sales:,.2f}")
            
            with col3:
                total_quantity = df_actual["SalesQuantity"].sum()
                st.metric("Total Units Sold", f"{total_quantity:,}")
            
            # Sales Trend
            st.subheader("Sales Trend")
            if not df_actual.empty:
                daily_sales = df_actual.groupby("date")["net_sales"].sum().reset_index()
                fig = px.line(
                    daily_sales,
                    x="date",
                    y="net_sales",
                    title="Daily Sales Trend",
                    labels={"date": "Date", "net_sales": "Sales Amount ($)"}
                )
                
                if not df_predicted.empty:
                    daily_predicted = df_predicted.groupby("date")["net_sales"].sum().reset_index()
                    fig.add_scatter(
                        x=daily_predicted["date"],
                        y=daily_predicted["net_sales"],
                        name="Predicted",
                        line=dict(dash="dash")
                    )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Product Categories
            if not df_actual.empty and "ProductCategoryName" in df_actual.columns:
                st.subheader("Sales by Product Category")
                category_sales = df_actual.groupby("ProductCategoryName")["net_sales"].sum().sort_values(ascending=True)
                if not category_sales.empty:
                    fig = px.bar(
                        category_sales,
                        orientation="h",
                        title="Sales by Product Category",
                        labels={"value": "Sales Amount ($)", "ProductCategoryName": "Category"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Store Performance
            if not df_actual.empty and all(col in df_actual.columns for col in ["StoreName", "StoreType"]):
                st.subheader("Store Performance")
                store_sales = df_actual.groupby(["StoreName", "StoreType"])[["net_sales", "SalesQuantity"]].sum().reset_index()
                if not store_sales.empty:
                    fig = px.scatter(
                        store_sales,
                        x="net_sales",
                        y="SalesQuantity",
                        color="StoreType",
                        hover_data=["StoreName"],
                        title="Store Performance Analysis",
                        labels={
                            "net_sales": "Total Sales ($)",
                            "SalesQuantity": "Units Sold",
                            "StoreType": "Store Type"
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error("Error loading or processing data")
            st.error(f"Error details: {str(e)}")
            st.error("Full traceback: " + traceback.format_exc())
    
    except Exception as e:
        st.error("Error in main application")
        st.error(f"Error details: {str(e)}")
        st.error("Full traceback: " + traceback.format_exc())

if __name__ == "__main__":
    main() 