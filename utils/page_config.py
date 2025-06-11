"""Page configuration utilities for the Sales Ninja dashboard."""

import streamlit as st

def set_page_config(page_title: str):
    """Configure the page settings."""
    st.set_page_config(
        page_title=f"Sales Ninja - {page_title}",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS for gradient title
    st.markdown("""
        <style>
        .gradient-title {
            background: linear-gradient(45deg, #4169E1, #9370DB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def add_page_title(title: str, subtitle: str = None, emoji: str = None):
    """Add a styled title and optional subtitle to the page.
    
    Args:
        title: The title text to display
        subtitle: Optional subtitle to display below the title
        emoji: Optional emoji to display before the title
    """
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
    st.markdown("---")  # Add a separator line 