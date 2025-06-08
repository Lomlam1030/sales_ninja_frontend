import streamlit as st
from utils.theme import COLORS

def set_page_config(title="Sales Ninja", emoji="📊"):
    """Configure the page with standard settings"""
    st.set_page_config(
        page_title=f"{title} - Sales Ninja",
        page_icon=emoji,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Hide all Streamlit default elements we don't want
    st.markdown("""
        <style>
            /* Hide main menu button and top padding */
            #MainMenu {visibility: hidden;}
            .stApp > header {display: none !important;}
            .stDeployButton {display: none;}
            header[data-testid="stHeader"] {display: none;}
            /* Hide default title */
            .css-10trblm {display: none;}
            .css-1q1n0ol {display: none;}
            /* Remove top padding */
            .main > div {padding-top: 0rem;}
        </style>
    """, unsafe_allow_html=True)

def add_page_title(title, subtitle=None, emoji="📊"):
    """Add a styled title to the page"""
    # Add custom gradient header style
    st.markdown(f"""
        <style>
        .header-container {{
            background: linear-gradient(135deg, #0c1c2c 0%, #1a3a4a 100%);
            padding: 2rem 1rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            border: 2px solid rgba(255, 87, 34, 0.3);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .header-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, 
                rgba(255, 87, 34, 0.1) 0%,
                rgba(244, 81, 30, 0.1) 50%,
                rgba(230, 74, 25, 0.1) 100%
            );
            z-index: 1;
        }}
        .header-title {{
            font-size: 3.5rem;
            font-weight: bold;
            color: {COLORS['primary']};
            margin: 0;
            position: relative;
            z-index: 2;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        .header-subtitle {{
            font-size: 1.5rem;
            color: {COLORS['accent']};
            margin-top: 0.5rem;
            font-style: italic;
            position: relative;
            z-index: 2;
        }}
        .header-emoji {{
            font-size: 2.5rem;
            margin: 0 0.5rem;
            position: relative;
            z-index: 2;
        }}
        </style>
        <div class="header-container">
            <h1 class="header-title">
                {f'<span class="header-emoji">{emoji}</span>' if emoji else ''}
                {title}
                {f'<span class="header-emoji">{emoji}</span>' if emoji else ''}
            </h1>
            {f'<p class="header-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True) 