import streamlit as st

# Configure the page with dark theme
st.set_page_config(
    page_title="Sales Ninja",
    page_icon="🥷",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/sales_ninja_frontend',
        'Report a bug': "https://github.com/yourusername/sales_ninja_frontend/issues",
        'About': "# Sales Ninja Analytics\nYour intelligent sales analytics platform."
    }
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 4em !important;
        font-weight: bold;
        background: linear-gradient(45deg, #4169E1, #9370DB);  /* Royal Blue to Medium Purple */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 20px;
    }
    .subtitle {
        font-size: 1.5em !important;
        color: #E6E6FA;  /* Lavender */
        margin-bottom: 2em;
    }
    .feature-header {
        font-size: 1.8em !important;
        color: #4169E1;  /* Royal Blue */
        margin-bottom: 1em;
    }
    .feature-text {
        font-size: 1.2em !important;
        color: #E6E6FA;  /* Lavender */
    }
    .centered {
        text-align: center;
    }
    .feature-box {
        background: rgba(65, 105, 225, 0.1);  /* Royal Blue with opacity */
        border: 1px solid rgba(147, 112, 219, 0.3);  /* Medium Purple with opacity */
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(65, 105, 225, 0.2);  /* Royal Blue with opacity */
    }
</style>
""", unsafe_allow_html=True)

# Main content with centered layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Title and Logo
    st.markdown('<div class="centered"><h1 class="main-title">🥷 Sales Ninja</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="centered"><p class="subtitle">Your Intelligent Sales Analytics Platform</p></div>', unsafe_allow_html=True)

    # Description
    st.markdown("""
    <div class="centered">
        <p class="feature-text">
            Welcome to Sales Ninja, your advanced analytics platform for sales performance monitoring and prediction.
            Leverage the power of data-driven insights to optimize your business decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Spacer
    st.write("")
    st.write("")

    # Features
    st.markdown('<h2 class="feature-header centered">Key Features</h2>', unsafe_allow_html=True)

    # Feature columns
    feat_col1, feat_col2, feat_col3 = st.columns(3)

    with feat_col1:
        st.markdown("""
        <div class="feature-box centered">
            <h3>📈 Sales Analytics</h3>
            <p class="feature-text">Track daily, monthly, and quarterly sales performance with interactive visualizations</p>
        </div>
        """, unsafe_allow_html=True)

    with feat_col2:
        st.markdown("""
        <div class="feature-box centered">
            <h3>🌍 Geographic Insights</h3>
            <p class="feature-text">Analyze sales distribution across regions with interactive maps</p>
        </div>
        """, unsafe_allow_html=True)

    with feat_col3:
        st.markdown("""
        <div class="feature-box centered">
            <h3>📊 Detailed Dashboard</h3>
            <p class="feature-text">Deep dive into sales metrics and performance indicators</p>
        </div>
        """, unsafe_allow_html=True)

    # Spacer
    st.write("")
    st.write("")

    # Navigation Instructions
    st.markdown("""
    <div class="centered">
        <p class="feature-text">
            👈 Use the sidebar to navigate through the analytics pages
        </p>
    </div>
    """, unsafe_allow_html=True) 