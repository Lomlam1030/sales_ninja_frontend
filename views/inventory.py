import streamlit as st
import plotly.express as px
import pandas as pd
from utils.api import APIClient

def show_inventory(api_client: APIClient):
    st.title("Inventory Management")
    
    try:
        # Fetch inventory data
        inventory_data = api_client.get_inventory_status()
        
        # Convert to DataFrame
        df = pd.DataFrame(inventory_data['inventory'])
        
        # Calculate inventory metrics
        total_items = df['quantity'].sum()
        low_stock_items = len(df[df['status'] == 'low_stock'])
        out_of_stock_items = len(df[df['status'] == 'out_of_stock'])
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items in Stock", total_items)
        with col2:
            st.metric("Low Stock Items", low_stock_items)
            if low_stock_items > 0:
                st.warning("Some items need reordering!")
        with col3:
            st.metric("Out of Stock Items", out_of_stock_items)
            if out_of_stock_items > 0:
                st.error("Critical: Items out of stock!")
        
        # Stock level chart
        st.subheader("Stock Levels by Product")
        fig1 = px.bar(
            df,
            x='product_name',
            y='quantity',
            color='status',
            title='Current Stock Levels',
            color_discrete_map={
                'in_stock': 'green',
                'low_stock': 'orange',
                'out_of_stock': 'red'
            }
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Filter options
        status_filter = st.multiselect(
            "Filter by Status",
            options=['in_stock', 'low_stock', 'out_of_stock'],
            default=['low_stock', 'out_of_stock']
        )
        
        # Filtered inventory table
        st.subheader("Inventory Details")
        filtered_df = df[df['status'].isin(status_filter)] if status_filter else df
        st.dataframe(
            filtered_df.sort_values('quantity', ascending=True),
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"Error loading inventory data: {str(e)}")
        st.info("Please check your API connection and try again.") 