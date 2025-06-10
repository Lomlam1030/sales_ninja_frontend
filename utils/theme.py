"""
Central theme configuration for the Sales Ninja application.
This file contains all color schemes and styling constants used across the app.
"""

# Main color scheme


# Main color scheme - Blue & Purple Professional Theme
COLORS = {
    # --- Base & Text ---
    'background': '#191970', # Midnight Blue - a deep, rich background
    'text': '#E6E6FA',      # Lavender - for high contrast and a soft feel

    # --- Primary UI Elements ---
    'primary': '#4169E1',    # Royal Blue - a strong, confident primary color for buttons/actions
    'secondary': '#7B68EE',  # Medium Slate Blue - a vibrant secondary color for accents
    'accent': '#9370DB',     # Medium Purple - for highlights, active states, or special elements

    # --- Semantic / Status Colors (Best Practice) ---
    'success': '#4DB6AC',   # Teal - a calming, positive color that complements blues
    'warning': '#FFCA28',   # Amber/Yellow - standard, universally understood warning color
    'error': '#EF5350',     # Red - standard, universally understood error color
    'info': '#82B1FF',      # Light Blue - a clear and friendly color for informational alerts
}

# Chart color sequences
CHART_COLORS = [
    '#4169E1',  # Royal Blue
    '#6A5ACD',  # Slate Blue
    '#9370DB',  # Medium Purple
    '#8A2BE2',  # Blue Violet
    '#E6E6FA',  # Lavender
    '#B0C4DE',  # Light Steel Blue
    '#7B68EE',  # Medium Slate Blue
    '#A8C4E9',  # Light Blue
]

# Common CSS styles
STYLES = {
    'container': """
        background-color: rgba(14, 17, 23, 0.2);
        border: 2px solid rgba(255, 87, 34, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 2rem;
    """,
    'container_hover': """
        border-color: rgba(230, 74, 25, 0.6);
        box-shadow: 0 5px 15px rgba(255, 87, 34, 0.2);
    """,
    'metric': """
        background: linear-gradient(135deg, rgba(244, 81, 30, 0.1) 0%, rgba(255, 87, 34, 0.1) 100%);
        border: 2px solid rgba(230, 74, 25, 0.3);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    """,
    'metric_hover': """
        border-color: rgba(216, 67, 21, 0.6);
        box-shadow: 0 5px 15px rgba(255, 87, 34, 0.2);
    """,
}

# Chart templates
def get_chart_template():
    """Return a consistent chart template for use with plotly"""
    return {
        'layout': {
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': {
                'color': COLORS['text']
            },
            'xaxis': {
                'gridcolor': 'rgba(255,255,255,0.1)',
                'zerolinecolor': 'rgba(255,255,255,0.2)'
            },
            'yaxis': {
                'gridcolor': 'rgba(255,255,255,0.1)',
                'zerolinecolor': 'rgba(255,255,255,0.2)'
            }
        }
    }

# CSS for consistent styling across pages
def get_css():
    """Return CSS styles for consistent page styling"""
    return f"""
    <style>
    .container {{
        {STYLES['container']}
    }}
    .container:hover {{
        {STYLES['container_hover']}
    }}
    .metric-container {{
        {STYLES['metric']}
    }}
    .metric-container:hover {{
        {STYLES['metric_hover']}
    }}
    .title {{
        color: {COLORS['primary']};
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 20px;
    }}
    .subtitle {{
        color: {COLORS['text']};
        font-size: 20px;
        margin-bottom: 30px;
    }}
    .info-text {{
        color: {COLORS['info']};
    }}
    .success-text {{
        color: {COLORS['success']};
    }}
    .warning-text {{
        color: {COLORS['warning']};
    }}
    .error-text {{
        color: {COLORS['error']};
    }}
    /* Remove all vertical lines */
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebarNav"] > ul,
    [data-testid="stSidebarNav"] > ul > li > div,
    [data-testid="stSidebarNav"] > ul > li > a,
    .block-container,
    .element-container,
    .stMarkdown,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    section[data-testid="stSidebar"],
    .main .block-container {{
        border-left: none !important;
        border-right: none !important;
        padding-left: 0 !important;
    }}
    /* Add spacing between sidebar and main content */
    section[data-testid="stSidebar"] {{
        padding-right: 1rem !important;
        margin-right: 1rem !important;
    }}
    .main .block-container {{
        padding-left: 2rem !important;
        margin-left: 1rem !important;
    }}
    </style>
    """ 