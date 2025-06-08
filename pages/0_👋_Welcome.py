import streamlit as st
from utils.page_config import set_page_config, add_page_title
from utils.theme import COLORS, get_css

# Configure the page
set_page_config(title="Welcome")

# Add the styled title and CSS
st.markdown(get_css(), unsafe_allow_html=True)
add_page_title(
    title="Welcome to Sales Ninja",
    subtitle="Your Advanced Sales Analytics Dashboard",
    emoji="👋"
)

# Main content container
st.markdown("""
<div class="container">
    <h2 style="color: {primary};">About Sales Ninja</h2>
    <p>
        Sales Ninja is your advanced analytics dashboard for tracking and analyzing sales performance 
        across different regions, time periods, and product categories. Our intuitive interface and 
        powerful visualizations help you make data-driven decisions with confidence.
    </p>
</div>
""".format(primary=COLORS['primary']), unsafe_allow_html=True)

# Features section
st.markdown("""
<div class="container">
    <h2 style="color: {primary};">Key Features</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        <div class="metric-container">
            <h3 style="color: {secondary};">📊 Sales Analytics</h3>
            <p>Comprehensive sales data analysis with interactive visualizations and detailed metrics.</p>
        </div>
        <div class="metric-container">
            <h3 style="color: {secondary};">🌍 Geographic Insights</h3>
            <p>Global sales distribution view with detailed country and region-wise performance tracking.</p>
        </div>
        <div class="metric-container">
            <h3 style="color: {secondary};">📈 Trend Analysis</h3>
            <p>Track sales trends over time with advanced filtering and comparison capabilities.</p>
        </div>
    </div>
</div>
""".format(primary=COLORS['primary'], secondary=COLORS['secondary']), unsafe_allow_html=True)

# Getting Started section
st.markdown("""
<div class="container">
    <h2 style="color: {primary};">Getting Started</h2>
    <p>
        Navigate through the different sections using the sidebar menu:
    </p>
    <ul>
        <li><span class="info-text">📈 Actuals vs Predictions</span> - Compare actual sales performance against predictions</li>
        <li><span class="info-text">🌍 Geography</span> - Detailed geographic sales distribution analysis</li>
        <li><span class="info-text">📊 Dashboard</span> - Comprehensive overview of key performance metrics</li>
    </ul>
    <p class="success-text" style="margin-top: 1rem;">
        Tip: Use the filters in each section to drill down into specific time periods, regions, or metrics!
    </p>
</div>
""".format(primary=COLORS['primary']), unsafe_allow_html=True)

# Help section
with st.expander("Need Help? 🤔"):
    st.markdown("""
    <div style="padding: 1rem;">
        <p>
            If you need assistance using the dashboard or have questions about the data:
        </p>
        <ul>
            <li>Check the tooltips (hover over charts and metrics)</li>
            <li>Use the filters to narrow down your analysis</li>
            <li>Contact the support team for technical assistance</li>
        </ul>
    </div>
    """, unsafe_allow_html=True) 