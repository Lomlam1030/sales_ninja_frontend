import streamlit as st
from utils.page_config import set_page_config, add_page_title
from utils.theme import COLORS, get_css

# Configure the page
set_page_config(title="Sales Ninja | Home")

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
        
        /* Welcome page specific styling */
        .welcome-header {
            color: #4169E1;
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 1em;
            text-align: center;
            padding: 20px;
        }
        
        .feature-box {
            background-color: rgba(65, 105, 225, 0.1);
            border: 1px solid rgba(65, 105, 225, 0.3);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .feature-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(65, 105, 225, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

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