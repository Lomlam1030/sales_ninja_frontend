"""
Central theme configuration for the Sales Ninja application.
This file contains all color schemes and styling constants used across the app.
"""

# Main color scheme
COLORS = {
    'primary': '#ff5722',    # Deep orange - main accent color
    'secondary': '#f4511e',  # Darker orange - secondary accent color
    'background': '#0e1117', # Dark background
    'text': '#fafafa',      # Light text
    'accent': '#ffa726',    # Yellow-orange accent
    'success': '#e64a19',   # Reddish-orange for positive values
    'warning': '#ff7043',   # Light orange for warnings
    'error': '#d84315',     # Deep reddish-orange for errors
    'info': '#ffb74d',      # Light orange for information
}

# Chart color sequences
CHART_COLORS = [
    COLORS['primary'],      # Deep orange
    COLORS['secondary'],    # Darker orange
    '#e64a19',             # Reddish-orange
    '#d84315',             # Deep reddish-orange
    '#ffa726',             # Yellow-orange
    '#ff7043',             # Light orange
    '#ffb74d',             # Light orange
    '#ff9800',             # Orange
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