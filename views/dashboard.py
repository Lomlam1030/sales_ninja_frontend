import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.api import APIClient
from datetime import datetime, timedelta

def generate_dummy_scatter_data(n_points=100):
    """Generate dummy data for scatter plot."""
    np.random.seed(42)  # For reproducibility
    order_quantities = np.random.randint(1, 50, n_points)
    # Generate order values with some correlation to quantity plus some noise
    base_price = np.random.uniform(10, 100, n_points)
    order_values = order_quantities * base_price + np.random.normal(0, 50, n_points)
    order_values = np.maximum(order_values, 0)  # Ensure no negative values
    
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n_points).date
    
    return pd.DataFrame({
        'date': dates,
        'order_quantity': order_quantities,
        'order_value': order_values,
        'customer_id': [f'CUST_{i:03d}' for i in range(n_points)]
    })

def generate_dummy_dashboard_stats():
    """Generate dummy dashboard statistics."""
    return {
        'total_sales': 156789.50,
        'sales_growth': 12.5,
        'total_orders': 1234,
        'orders_growth': 8.3,
        'avg_order_value': 127.06,
        'aov_growth': 4.2,
        'active_customers': 856,
        'customer_growth': 15.7,
        'sales_trend': generate_dummy_sales_trend()
    }

def generate_dummy_sales_trend(days=30):
    """Generate dummy sales trend data."""
    np.random.seed(42)
    dates = [(datetime.now() - timedelta(days=x)).date() for x in range(days)]
    base_amount = 5000
    amounts = [
        base_amount + np.random.normal(0, 500) + (i * 50)  # Slight upward trend
        for i in range(days)
    ]
    amounts = [max(0, amount) for amount in amounts]  # Ensure no negative values
    
    return [{'date': date, 'amount': amount} for date, amount in zip(reversed(dates), reversed(amounts))]

def generate_dummy_top_products():
    """Generate dummy top products data."""
    products = [
        {'name': f'Product {i}', 'sales': np.random.randint(5000, 20000)} 
        for i in range(1, 11)
    ]
    products.sort(key=lambda x: x['sales'], reverse=True)
    return {'products': products}

def show_dashboard(api_client: APIClient):
    st.title("Sales Ninja Dashboard")
    
    try:
        # make api call to get dashboard data
        # dashboard_data = api_client.get_dashboard_stats()
        # Use dummy data instead of API calls
        dashboard_data = generate_dummy_dashboard_stats()
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Sales",
                value=f"${dashboard_data['total_sales']:,.2f}",
                delta=f"{dashboard_data['sales_growth']}%"
            )
            
        with col2:
            st.metric(
                label="Orders",
                value=dashboard_data['total_orders'],
                delta=f"{dashboard_data['orders_growth']}%"
            )
            
        with col3:
            st.metric(
                label="Average Order Value",
                value=f"${dashboard_data['avg_order_value']:,.2f}",
                delta=f"{dashboard_data['aov_growth']}%"
            )
            
        with col4:
            st.metric(
                label="Active Customers",
                value=dashboard_data['active_customers'],
                delta=f"{dashboard_data['customer_growth']}%"
            )
        
        # Create sales trend chart
        st.subheader("Sales Trend")
        sales_df = pd.DataFrame(dashboard_data['sales_trend'])
        fig = px.line(
            sales_df,
            x='date',
            y='amount',
            title='Daily Sales Trend'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add scatter plot section with dummy data
        st.subheader("Order Analysis")
        scatter_data = generate_dummy_scatter_data()
        
        fig_scatter = px.scatter(
            scatter_data,
            x='order_quantity',
            y='order_value',
            title='Order Value vs Quantity',
            hover_data=['customer_id', 'date'],
            labels={
                'order_quantity': 'Order Quantity',
                'order_value': 'Order Value ($)',
            },
            trendline="ols"  # Add trend line
        )
        fig_scatter.update_traces(
            marker=dict(size=8),
            hovertemplate="<br>".join([
                "Order Quantity: %{x}",
                "Order Value: $%{y:.2f}",
                "Customer: %{customdata[0]}",
                "Date: %{customdata[1]}",
            ])
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Display top products with dummy data
        st.subheader("Top Products")
        top_products = generate_dummy_top_products()
        products_df = pd.DataFrame(top_products['products'])
        
        fig2 = px.bar(
            products_df,
            x='name',
            y='sales',
            title='Top 10 Products by Sales'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")
        st.info("Please check your API connection and try again.") 