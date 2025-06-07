import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from utils.api import APIClient

def show_sales(api_client: APIClient):
    st.title("Sales Analysis")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now()
        )
    
    try:
        # Fetch sales data for the selected period
        sales_data = api_client.get_sales_data(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        # Convert to DataFrame
        df = pd.DataFrame(sales_data['sales'])
        
        # Summary metrics
        total_sales = df['amount'].sum()
        avg_daily_sales = df['amount'].mean()
        total_orders = len(df)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sales", f"${total_sales:,.2f}")
        with col2:
            st.metric("Average Daily Sales", f"${avg_daily_sales:,.2f}")
        with col3:
            st.metric("Total Orders", total_orders)
        
        # Sales trend chart
        st.subheader("Sales Trend")
        fig1 = px.line(
            df,
            x='date',
            y='amount',
            title='Daily Sales'
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Sales by category
        st.subheader("Sales by Category")
        category_sales = df.groupby('category')['amount'].sum().reset_index()
        fig2 = px.pie(
            category_sales,
            values='amount',
            names='category',
            title='Sales Distribution by Category'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed sales table
        st.subheader("Detailed Sales Data")
        st.dataframe(
            df.sort_values('date', ascending=False),
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"Error loading sales data: {str(e)}")
        st.info("Please check your API connection and try again.") 