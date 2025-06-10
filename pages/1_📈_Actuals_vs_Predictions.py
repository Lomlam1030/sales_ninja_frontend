import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils.page_config import set_page_config, add_page_title
from utils.theme import get_css, get_chart_template
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
import calendar

# Configure the page
set_page_config(title="Sales Ninja | Analytics | Actuals vs Predictions")

# Add CSS and title
st.markdown(get_css(), unsafe_allow_html=True)
add_page_title(
    title="Actuals vs Predictions",
    subtitle="Daily, Monthly, and Quarterly Sales Overview",
    emoji="📈"
)

# Custom CSS for styling
st.markdown("""
    <style>
        /* Markdown text styling */
        .element-container div.stMarkdown p {
            color: #4169E1 !important;  /* Royal Blue */
        }
        
        .element-container div.stMarkdown h1,
        .element-container div.stMarkdown h2,
        .element-container div.stMarkdown h3,
        .element-container div.stMarkdown h4,
        .element-container div.stMarkdown h5,
        .element-container div.stMarkdown h6 {
            color: #4169E1 !important;  /* Royal Blue */
        }
        
        .element-container div.stMarkdown a {
            color: #1E90FF !important;  /* Dodger Blue for links */
        }
        
        .element-container div.stMarkdown li {
            color: #4169E1 !important;  /* Royal Blue */
        }
        
        /* Tab styling */
        div[data-baseweb="tab-list"] {
            gap: 2px;
        }
        
        button[data-baseweb="tab"] {
            padding: 10px 24px;
            margin: 0px 8px;
            background-color: rgba(65, 105, 225, 0.8);  /* Royal Blue */
            border-radius: 4px;
            border: 1px solid rgba(147, 112, 219, 0.2);  /* Medium Purple */
            transition: all 0.3s ease;
            color: white;
        }
        
        button[data-baseweb="tab"]:hover {
            background-color: rgba(147, 112, 219, 0.8);  /* Medium Purple */
            border-color: rgba(65, 105, 225, 0.4);  /* Royal Blue */
        }
        
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #9370DB;  /* Medium Purple */
            border-color: #4169E1;  /* Royal Blue */
            box-shadow: 0 2px 4px rgba(65, 105, 225, 0.3);
        }
        
        /* Metric containers */
        div[data-testid="metric-container"] {
            background-color: rgba(65, 105, 225, 0.1);  /* Royal Blue */
            border: 1px solid rgba(147, 112, 219, 0.2);  /* Medium Purple */
            padding: 10px;
            border-radius: 5px;
        }
        
        div[data-testid="metric-container"] label {
            color: #E6E6FA !important;  /* Lavender */
        }
        
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #B0C4DE !important;  /* Light Steel Blue */
        }
        
        /* Section headers */
        .section-header {
            color: #E6E6FA;  /* Lavender */
            font-size: 1.5em;
            font-weight: bold;
            margin: 20px 0;
            padding: 10px;
            border-left: 4px solid #9370DB;  /* Medium Purple */
            background-color: rgba(65, 105, 225, 0.1);  /* Royal Blue with opacity */
        }
        
        /* Add custom CSS to style the selectbox */
        div[data-baseweb="select"] > div {
            border-color: #4169E1 !important;
        }
        
        /* Style for hover and focus states */
        div[data-baseweb="select"]:hover > div,
        div[data-baseweb="select"] > div:focus {
            border-color: #6495ED !important;
            box-shadow: 0 0 0 2px rgba(100, 149, 237, 0.2) !important;
        }
        
        /* Style for the dropdown items */
        div[role="listbox"] div[role="option"]:hover {
            background-color: rgba(100, 149, 237, 0.1) !important;
        }
        
        /* Create container with proper padding */
        .block-container {
            padding: 2rem 1rem;
            max-width: 100% !important;
        }
        [data-testid="stMetricValue"] {
            color: #E6E6FA !important;
        }
        .stPlotlyChart {
            width: 100% !important;
        }
        /* Ensure the plot container takes full width */
        .element-container {
            width: 100% !important;
        }
        /* Remove default padding from Streamlit */
        .main > div {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Container styling */
        .block-container {
            padding: 1rem !important;
        }
        
        /* Plot container styling */
        [data-testid="stMetricValue"] {
            color: #E6E6FA !important;
        }
        
        /* Ensure plot stays within bounds */
        .stPlotlyChart > div {
            width: 100% !important;
            max-width: 100% !important;
            min-width: auto !important;
        }
        
        /* Remove any margin/padding that might cause overflow */
        .element-container, .stPlotlyChart, .js-plotly-plot {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Ensure main content area doesn't overflow */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 5% !important;
            padding-right: 5% !important;
            width: 90% !important;
        }
        
        /* Main container styling */
        .main .block-container {
            padding: 2rem 1rem !important;
            max-width: 100% !important;
        }
        
        /* Section headers */
        h2.table-header {
            color: #2F4F4F;
            padding: 1rem 0;
            font-size: 1.5em;
            font-weight: 600;
            margin-top: 2rem;
        }
        
        /* Plot container styling */
        [data-testid="stMetricValue"] {
            color: #E6E6FA !important;
        }
        
        /* Chart container */
        .stPlotlyChart {
            background: rgba(230, 230, 250, 0.1);
            border: 1px solid rgba(230, 230, 250, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 2rem 0;
        }
        
        /* Filter section styling */
        [data-testid="stHorizontalBlock"] {
            background: rgba(230, 230, 250, 0.1);
            border: 1px solid rgba(230, 230, 250, 0.1);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 2rem 0;
        }
        
        /* Metric container styling */
        div[data-testid="metric-container"] {
            background: rgba(230, 230, 250, 0.1);
            border: 1px solid rgba(230, 230, 250, 0.1);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        /* Selectbox styling */
        div[data-baseweb="select"] {
            margin-bottom: 1rem;
        }

        /* Add spacing after title */
        [data-testid="stAppViewContainer"] > div:first-child {
            margin-bottom: 2rem;
        }

        /* View selector container */
        .view-selector {
            margin: 2rem 0;
            padding: 1rem;
            background: rgba(230, 230, 250, 0.1);
            border-radius: 0.5rem;
            border: 1px solid rgba(230, 230, 250, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

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
        line=dict(color='#4169E1', width=2),  # Royal Blue
        hovertemplate='%{x}<br>Actual Sales: %{y:$,.0f}<extra></extra>'
    ))
    
    # Add predicted sales line
    fig.add_trace(go.Scatter(
        x=predicted_data['date'],
        y=predicted_data['net_sales'],
        name='Predicted Sales',
        line=dict(color='#9370DB', width=2, dash='dot'),  # Medium Purple
        hovertemplate='%{x}<br>Predicted Sales: %{y:$,.0f}<extra></extra>'
    ))
    
    # Calculate and add average lines
    actual_avg = actual_data['net_sales'].mean()
    predicted_avg = predicted_data['net_sales'].mean()
    
    fig.add_hline(
        y=actual_avg,
        line_dash="dot",
        line_color="rgba(65, 105, 225, 0.5)",  # Royal Blue
        annotation=dict(
            text=f"Actual Avg: {format_currency(actual_avg)}",
            font=dict(color='#FFFFFF'),  # White text
            xref="paper",
            x=1,
            showarrow=False,
            yshift=10
        )
    )
    
    fig.add_hline(
        y=predicted_avg,
        line_dash="dot",
        line_color="rgba(147, 112, 219, 0.5)",  # Medium Purple
        annotation=dict(
            text=f"Predicted Avg: {format_currency(predicted_avg)}",
            font=dict(color='#FFFFFF'),  # White text
            xref="paper",
            x=1,
            showarrow=False,
            yshift=-10
        )
    )
    
    # Update layout with strict container bounds and adjusted margins
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(color='#FFFFFF', size=16),  # White text
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        xaxis=dict(
            title='Date',
            gridcolor='rgba(176, 196, 222, 0.1)',
            title_font=dict(color='#FFFFFF', size=14),  # White text
            tickfont=dict(color='#FFFFFF', size=12),  # White text
            rangeslider=dict(visible=False),
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='Sales ($)',
            gridcolor='rgba(176, 196, 222, 0.1)',
            title_font=dict(color='#FFFFFF', size=14),  # White text
            tickfont=dict(color='#FFFFFF', size=12),  # White text
            tickprefix='$',
            showgrid=True,
            zeroline=False
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='#FFFFFF', size=12),  # White text
            bgcolor='rgba(25, 25, 112, 0.3)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=60, t=60, b=60, pad=10),  # Increased margins
        height=450,
        autosize=True,
        width=None,
        plot_bgcolor='rgba(25, 25, 112, 0.3)',
        paper_bgcolor='rgba(25, 25, 112, 0.3)',
        template="plotly_dark",
        hovermode='x unified',
        shapes=[
            # Add border
            dict(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color='rgba(255, 255, 255, 0.2)',
                    width=1
                ),
                fillcolor='rgba(0, 0, 0, 0)'
            )
        ]
    )
    
    # Ensure the plot stays within bounds
    fig.update_xaxes(
        automargin=True,
        constrain='domain',
        fixedrange=True  # Disable zoom
    )
    fig.update_yaxes(
        automargin=True,
        constrain='domain',
        fixedrange=True  # Disable zoom
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
    st.markdown('<div class="section-header">Actual Sales</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-header">Predicted Sales</div>', unsafe_allow_html=True)
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
            use_container_width=True,
            config={
                'displayModeBar': False,
                'responsive': True,
                'scrollZoom': False,
                'staticPlot': True  # This prevents any interactive resizing
            }
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