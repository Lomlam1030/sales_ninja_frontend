import streamlit as st

# Updated color scheme with more blue shades
COLOR_SCHEME = {
    'primary': '#1E3D59',      # Navy Blue
    'secondary': '#E6EEF8',    # Light Blue
    'accent': '#E0D3ED',       # Lilac
    'blue_light': '#A8C4E9',   # Lighter Blue
    'blue_medium': '#4A78B3',  # Medium Blue
    'blue_dark': '#2B4C7E',    # Dark Blue
    'text_primary': '#1E3D59', # Navy Blue for text
    'background': '#F8FAFC',   # Very Light Blue background
    'border': '#4A78B3'        # Medium Blue for borders
}

def set_page_config(title="Sales Ninja", layout="wide"):
    """Configure the page with standard settings"""
    st.set_page_config(
        page_title=title,
        page_icon="🥷",
        layout=layout
    )
    
    # Apply the new color scheme to the entire app
    st.markdown(f"""
        <style>
        /* Main background and text colors */
        .stApp {{
            background-color: {COLOR_SCHEME['background']};
            color: {COLOR_SCHEME['text_primary']};
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLOR_SCHEME['primary']} !important;
        }}
        
        /* Metric containers */
        div[data-testid="stMetricValue"] {{
            color: {COLOR_SCHEME['primary']} !important;
            background: {COLOR_SCHEME['secondary']};
            padding: 10px;
            border-radius: 5px;
            border: 2px solid {COLOR_SCHEME['border']};
        }}
        
        /* Sidebar */
        .css-1d391kg {{
            background-color: {COLOR_SCHEME['primary']};
        }}
        
        /* Buttons */
        .stButton>button {{
            background-color: {COLOR_SCHEME['primary']};
            color: white;
            border: 2px solid {COLOR_SCHEME['border']};
            border-radius: 5px;
            padding: 0.5rem 1rem;
        }}
        
        .stButton>button:hover {{
            background-color: {COLOR_SCHEME['accent']};
            color: {COLOR_SCHEME['primary']};
            border-color: {COLOR_SCHEME['primary']};
        }}
        
        /* Cards and containers */
        .metric-container {{
            background: linear-gradient(135deg, {COLOR_SCHEME['blue_light']}, {COLOR_SCHEME['accent']});
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            border: 2px solid {COLOR_SCHEME['border']};
            box-shadow: 0 2px 6px rgba(74, 120, 179, 0.2);
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2px;
            background-color: {COLOR_SCHEME['secondary']};
            border: 2px solid {COLOR_SCHEME['border']};
            border-radius: 5px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: {COLOR_SCHEME['blue_light']};
            color: {COLOR_SCHEME['primary']};
            padding: 10px 20px;
            border-radius: 5px 5px 0 0;
            border: 1px solid {COLOR_SCHEME['border']};
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {COLOR_SCHEME['primary']};
            color: white;
            border-color: {COLOR_SCHEME['primary']};
        }}
        
        /* DataFrames */
        .dataframe {{
            background-color: {COLOR_SCHEME['secondary']};
            border-radius: 5px;
            border: 2px solid {COLOR_SCHEME['border']};
        }}
        
        /* Plots */
        .js-plotly-plot {{
            background-color: {COLOR_SCHEME['secondary']};
            border-radius: 10px;
            padding: 15px;
            border: 2px solid {COLOR_SCHEME['border']};
            box-shadow: 0 2px 6px rgba(74, 120, 179, 0.2);
        }}

        /* Cards */
        .stCard {{
            border: 2px solid {COLOR_SCHEME['border']};
            box-shadow: 0 2px 6px rgba(74, 120, 179, 0.2);
        }}
        </style>
    """, unsafe_allow_html=True)

def add_page_title(title, subtitle=None, emoji=None):
    """Add a styled title and optional subtitle to the page"""
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(65, 105, 225, 0.1), rgba(147, 112, 219, 0.1));
            padding: 2rem;
            margin: -1rem -1rem 1rem -1rem;
            border-radius: 0.5rem;
            border: 1px solid rgba(147, 112, 219, 0.2);
        ">
            <h1 style="
                font-size: 2.5em;
                font-weight: bold;
                margin: 0;
                display: flex;
                align-items: center;
                gap: 0.3em;
            ">
                {f'<span style="font-size: 1em;">{emoji}</span>' if emoji else ''}
                <span style="
                    background: linear-gradient(45deg, #4169E1, #9370DB);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                ">{title}</span>
            </h1>
            {f'<p style="color: #9370DB; margin: 0.5rem 0 0 0; font-size: 1.2em; opacity: 0.8;">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True) 