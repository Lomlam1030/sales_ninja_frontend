import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils.page_config import set_page_config, add_page_title
from utils.sales_calculations import (
    load_dashboard_data,
    calculate_daily_net_sales,
    calculate_monthly_net_sales,
    calculate_quarterly_net_sales,
    get_sales_summary_stats,
    get_monthly_summary_stats,
    get_quarterly_summary_stats,
    get_available_years,
    get_available_months,
    get_available_weeks,
    get_month_name,
    get_quarter_name
)

# Configure the page
set_page_config(title="Home")

# Custom CSS for blue tabs
st.markdown("""
    <style>
        div[data-baseweb="tab-list"] {
            gap: 2px;
        }
        
        button[data-baseweb="tab"] {
            padding: 10px 24px;
            margin: 0px 8px;
            background-color: #1e2f4d;
            border-radius: 4px;
        }
        
        button[data-baseweb="tab"]:hover {
            background-color: #2c446e;
        }
        
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #000080;
        }
        
        div[role="tablist"] button[role="tab"]:hover {
            color: #87CEEB;
        }
    </style>
""", unsafe_allow_html=True)

# Add the styled title
add_page_title(
    title="Sales Performance Dashboard",
    subtitle="Daily, Monthly, and Quarterly Sales Overview",
    emoji="📈"
)

def format_currency(value):
    """Format large numbers in millions/billions with proper currency symbol."""
    if pd.isna(value):
        return "N/A"
    if value >= 1e9:
        return f"${value/1e9:.1f}B"
    elif value >= 1e6:
        return f"${value/1e6:.1f}M"
    else:
        return f"${value:,.0f}"

def plot_sales_data(actual_data, predicted_data, title, freq='D'):
    """Plot actual and predicted sales data using Plotly"""
    fig = go.Figure()
    
    # Add actual sales line
    fig.add_trace(go.Scatter(
        x=actual_data['date'],
        y=actual_data['net_sales'],
        name='Actual Sales',
        line=dict(color='#000080', width=2),  # Navy blue
        hovertemplate='%{x}<br>Actual Sales: %{y:$,.0f}<extra></extra>'
    ))
    
    # Add predicted sales line
    fig.add_trace(go.Scatter(
        x=predicted_data['date'],
        y=predicted_data['net_sales'],
        name='Predicted Sales',
        line=dict(color='#87CEEB', width=2, dash='dot'),  # Light blue
        hovertemplate='%{x}<br>Predicted Sales: %{y:$,.0f}<extra></extra>'
    ))
    
    # Calculate and add average lines
    actual_avg = actual_data['net_sales'].mean()
    predicted_avg = predicted_data['net_sales'].mean()
    
    fig.add_hline(
        y=actual_avg,
        line_dash="dot",
        line_color="rgba(0, 0, 128, 0.5)",  # Semi-transparent navy blue
        annotation_text=f"Actual Avg: {format_currency(actual_avg)}",
        annotation_position="bottom right"
    )
    
    fig.add_hline(
        y=predicted_avg,
        line_dash="dot",
        line_color="rgba(135, 206, 235, 0.5)",  # Semi-transparent light blue
        annotation_text=f"Predicted Avg: {format_currency(predicted_avg)}",
        annotation_position="top right"
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        showlegend=True,
        height=500,
        template="plotly_dark",
        hovermode='x unified'
    )
    
    return fig

def display_kpi_metrics(actual_stats, predicted_stats, freq):
    """Display KPI metrics in a formatted way"""
    period_labels = {
        'D': 'Daily',
        'M': 'Monthly',
        'Q': 'Quarterly'
    }
    
    # Actual Sales Metrics
    st.markdown("#### Actual Sales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=f"Total Sales",
            value=format_currency(actual_stats['actual_total_sales']),
            delta=None
        )
    
    with col2:
        st.metric(
            label=f"Average {period_labels[freq]} Sales",
            value=format_currency(actual_stats[f'actual_average_{period_labels[freq].lower()}_sales']),
            delta=None
        )
    
    with col3:
        st.metric(
            label=f"Maximum {period_labels[freq]} Sales",
            value=format_currency(actual_stats[f'actual_max_{period_labels[freq].lower()}_sales']),
            delta=None
        )
    
    # Predicted Sales Metrics
    st.markdown("#### Predicted Sales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=f"Total Sales",
            value=format_currency(predicted_stats['predicted_total_sales']),
            delta=None
        )
    
    with col2:
        st.metric(
            label=f"Average {period_labels[freq]} Sales",
            value=format_currency(predicted_stats[f'predicted_average_{period_labels[freq].lower()}_sales']),
            delta=None
        )
    
    with col3:
        st.metric(
            label=f"Maximum {period_labels[freq]} Sales",
            value=format_currency(predicted_stats[f'predicted_max_{period_labels[freq].lower()}_sales']),
            delta=None
        )

# Load the data
try:
    df_actual, df_predicted = load_dashboard_data()
    available_years = get_available_years(df_actual)
    
    # Global year filter in sidebar
    st.sidebar.markdown("### Global Year Filter")
    year_filter = st.sidebar.selectbox(
        'Select Year',
        ['All Years'] + [str(year) for year in sorted(available_years, reverse=True)],
        index=0,
        key='global_year'
    )
    selected_year = int(year_filter) if year_filter != 'All Years' else None
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Daily View", "Monthly View", "Quarterly View"])
    
    # Daily View
    with tab1:
        # Additional filters for daily view only
        st.sidebar.markdown("### Daily View Additional Filters")
        
        # Get available months based on selected year
        available_months = get_available_months(df_actual, selected_year)
        month_filter = st.sidebar.selectbox(
            'Filter by Month (Optional)',
            ['All Months'] + [f"{month:02d} - {get_month_name(month)}" for month in available_months],
            index=0
        )
        selected_month = int(month_filter.split(' - ')[0]) if month_filter != 'All Months' else None
        
        # Get available weeks based on selected year and month
        available_weeks = get_available_weeks(df_actual, selected_year, selected_month)
        week_filter = st.sidebar.selectbox(
            'Filter by Week (Optional)',
            ['All Weeks'] + [f"Week {week:02d}" for week in available_weeks],
            index=0
        )
        selected_week = int(week_filter.split(' ')[1]) if week_filter != 'All Weeks' else None
        
        # Calculate and display daily data
        daily_actual, daily_predicted = calculate_daily_net_sales(
            df_actual, df_predicted, selected_year, selected_month, selected_week
        )
        actual_stats, predicted_stats = get_sales_summary_stats(
            df_actual, df_predicted, selected_year, selected_month, selected_week
        )
        
        # Build title based on filters
        title_parts = ["Daily Sales"]
        if selected_year:
            title_parts.append(str(selected_year))
        if selected_month:
            title_parts.append(get_month_name(selected_month))
        if selected_week:
            title_parts.append(f"Week {selected_week}")
        
        display_kpi_metrics(actual_stats, predicted_stats, 'D')
        st.plotly_chart(
            plot_sales_data(daily_actual, daily_predicted, " - ".join(title_parts), freq='D'),
            use_container_width=True
        )
    
    # Monthly View
    with tab2:
        monthly_actual, monthly_predicted = calculate_monthly_net_sales(
            df_actual, df_predicted, selected_year
        )
        actual_stats, predicted_stats = get_monthly_summary_stats(
            df_actual, df_predicted, selected_year
        )
        
        title = "Monthly Sales" + (f" - {selected_year}" if selected_year else "")
        
        display_kpi_metrics(actual_stats, predicted_stats, 'M')
        st.plotly_chart(
            plot_sales_data(monthly_actual, monthly_predicted, title, freq='M'),
            use_container_width=True
        )
    
    # Quarterly View
    with tab3:
        quarterly_actual, quarterly_predicted = calculate_quarterly_net_sales(
            df_actual, df_predicted, selected_year
        )
        actual_stats, predicted_stats = get_quarterly_summary_stats(
            df_actual, df_predicted, selected_year
        )
        
        title = "Quarterly Sales" + (f" - {selected_year}" if selected_year else "")
        
        display_kpi_metrics(actual_stats, predicted_stats, 'Q')
        st.plotly_chart(
            plot_sales_data(quarterly_actual, quarterly_predicted, title, freq='Q'),
            use_container_width=True
        )

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.error("Please make sure the data file exists and is properly formatted.") 