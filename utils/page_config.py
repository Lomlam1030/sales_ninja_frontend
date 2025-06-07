import streamlit as st

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
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
        /* Main title styling */
        .main-header {
            background: linear-gradient(90deg, #0A2342 0%, #00B4D8 100%);
            padding: 20px 20px 10px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 2px solid #00B4D8;
        }
        
        .title-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }
        
        .main-title {
            color: white;
            font-size: 48px;
            font-weight: 700;
            margin: 0;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .title-emoji {
            font-size: 40px;
            margin-bottom: 5px;
        }
        
        .subtitle {
            color: #CAF0F8;
            font-size: 20px;
            text-align: center;
            margin-top: 10px;
            font-style: italic;
        }
    </style>
    """, unsafe_allow_html=True)

    # Enhanced header with title and subtitle
    subtitle_html = f'<p class="subtitle">{subtitle}</p>' if subtitle else ''
    st.markdown(f"""
    <div class="main-header">
        <div class="title-container">
            <span class="title-emoji">{emoji}</span>
            <h1 class="main-title">{title}</h1>
            <span class="title-emoji">{emoji}</span>
        </div>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True) 