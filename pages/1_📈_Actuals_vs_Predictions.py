import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from utils.page_config import set_page_config, add_page_title
from utils.theme import get_css
from services.data_source import get_data_source
from config.settings import settings

# Page configuration
set_page_config("Actuals vs Predictions")

# Add title
st.title("📈 Actuals vs Predictions")

# Initialize data source if not already done
if 'data_source' not in st.session_state:
    try:
        st.session_state.data_source = get_data_source()
    except Exception as e:
        st.error(f"Failed to initialize data source: {str(e)}")
        st.stop()

def load_data(year=None, quarter=None, month=None, week=None):
    """Load and cache data."""
    @st.cache_data(ttl=3600, show_spinner=False)
    def _load_data(y, q, m, w):
        # Convert month name to number if provided
        month_num = None
        if m:
            month_map = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            month_num = month_map.get(m)
        
        # Convert quarter to number if provided
        quarter_num = None
        if q:
            quarter_num = int(q[1])  # Extract number from "Q1", "Q2", etc.
        
        return st.session_state.data_source.load_dashboard_data(
            year=y,
            quarter=quarter_num,
            month=month_num,
            week=w,
            limit=1000
        )
    
    with st.spinner("Loading sales data..."):
        return _load_data(year, quarter, month, week)

def create_time_series_plot(actual_df, predicted_df, x_col="date", title="Sales Comparison"):
    """Create a time series plot comparing actual vs predicted values."""
    # Create line plot for actual values
    fig = px.line(
        actual_df,
        x=x_col,
        y="net_sales",
        title=title
    )
    
    # Add predicted values line
    fig.add_scatter(
        x=predicted_df[x_col],
        y=predicted_df["net_sales"],
        mode="lines",
        name="Predicted",
        line=dict(dash="dash")
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title=x_col.title(),
        yaxis_title="Net Sales",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

def show_metrics(actual_df, predicted_df):
    """Display key metrics comparing actual vs predicted values."""
    actual_total = actual_df["net_sales"].sum()
    predicted_total = predicted_df["net_sales"].sum()
    
    # Calculate difference and accuracy
    difference = actual_total - predicted_total
    accuracy = (1 - abs(difference) / actual_total) * 100 if actual_total != 0 else 0
    
    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Actual Sales",
            f"${actual_total:,.2f}"
        )
    
    with col2:
        st.metric(
            "Predicted Sales",
            f"${predicted_total:,.2f}"
        )
    
    with col3:
        st.metric(
            "Prediction Accuracy",
            f"{accuracy:.1f}%"
        )

def main():
    # Create tabs for different time views
    tab_names = ["Daily View", "Monthly View", "Quarterly View"]
    current_tab = st.radio("Select View", tab_names, horizontal=True, label_visibility="hidden")
    
    # Sidebar filters
    st.sidebar.header("📅 Date Range")
    
    # Initialize filter values
    year = None
    quarter = None
    month = None
    week = None
    
    # Year selection (always visible)
    year = st.sidebar.selectbox(
        "Year",
        options=[2007, 2008, 2009],
        index=0
    )
    
    # Quarter selection (always visible)
    quarter = st.sidebar.selectbox(
        "Quarter",
        options=["Q1", "Q2", "Q3", "Q4"]
    )
    
    # Month selection (visible for Daily and Monthly views)
    if current_tab in ["Daily View", "Monthly View"]:
        month = st.sidebar.selectbox(
            "Month",
            options=[
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"
            ]
        )
    
    # Week selection (visible only for Daily view)
    if current_tab == "Daily View":
        week = st.sidebar.slider(
            "Week",
            min_value=1,
            max_value=52,
            value=1
        )
    
    try:
        # Load data with filters
        df_actual, df_predicted = load_data(
            year=year,
            quarter=quarter,
            month=month,
            week=week
        )
        
        if df_actual.empty:
            st.warning("No data found for the selected filters.")
            return
        
        # Daily View
        if current_tab == "Daily View":
            st.header("📈 Daily Sales Analysis")
            
            # Daily aggregation
            daily_actual = df_actual.groupby("date")["net_sales"].sum().reset_index()
            daily_predicted = df_predicted.groupby("date")["net_sales"].sum().reset_index()
            
            show_metrics(daily_actual, daily_predicted)
            st.plotly_chart(
                create_time_series_plot(
                    daily_actual, 
                    daily_predicted,
                    x_col="date",
                    title="Daily Sales Comparison"
                ),
                use_container_width=True
            )
        
        # Monthly View
        elif current_tab == "Monthly View":
            st.header("📅 Monthly Sales Analysis")
            
            # Monthly aggregation
            monthly_actual = df_actual.groupby(["year", "month", "month_name"])["net_sales"].sum().reset_index()
            monthly_predicted = df_predicted.groupby(["year", "month", "month_name"])["net_sales"].sum().reset_index()
            
            # Sort by month number
            monthly_actual = monthly_actual.sort_values("month")
            monthly_predicted = monthly_predicted.sort_values("month")
            
            show_metrics(monthly_actual, monthly_predicted)
            st.plotly_chart(
                create_time_series_plot(
                    monthly_actual,
                    monthly_predicted,
                    x_col="month_name",
                    title="Monthly Sales Comparison"
                ),
                use_container_width=True
            )
        
        # Quarterly View
        else:
            st.header("🗓️ Quarterly Sales Analysis")
            
            # Quarterly aggregation
            quarterly_actual = df_actual.groupby(["year", "quarter"])["net_sales"].sum().reset_index()
            quarterly_predicted = df_predicted.groupby(["year", "quarter"])["net_sales"].sum().reset_index()
            
            show_metrics(quarterly_actual, quarterly_predicted)
            st.plotly_chart(
                create_time_series_plot(
                    quarterly_actual,
                    quarterly_predicted,
                    x_col="quarter",
                    title="Quarterly Sales Comparison"
                ),
                use_container_width=True
            )
        
    except Exception as e:
        st.error(f"Error loading or processing data: {str(e)}")
        import traceback
        st.error("Detailed error: " + traceback.format_exc())

if __name__ == "__main__":
    main() 