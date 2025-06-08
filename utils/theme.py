"""
Central theme configuration for the Sales Ninja application.
This file contains all color schemes and styling constants used across the app.
"""

# Main color scheme
COLORS = {
    'primary': '#2ecc71',    # Green - main accent color
    'secondary': '#3498db',  # Blue - secondary accent color
    'background': '#0e1117', # Dark background
    'text': '#fafafa',      # Light text
    'accent': '#95a5a6',    # Subtle accent
    'success': '#27ae60',   # Dark green for positive values
    'warning': '#f39c12',   # Orange for warnings
    'error': '#e74c3c',     # Red for errors
    'info': '#3498db',      # Blue for information
}

# Chart color sequences
CHART_COLORS = [
    COLORS['primary'],
    COLORS['secondary'],
    '#e74c3c',  # Red
    '#f1c40f',  # Yellow
    '#9b59b6',  # Purple
    '#1abc9c',  # Turquoise
    '#e67e22',  # Orange
    '#34495e',  # Navy
]

# Common CSS styles
STYLES = {
    'container': """
        background-color: rgba(14, 17, 23, 0.2);
        border: 2px solid rgba(46, 204, 113, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 2rem;
    """,
    'container_hover': """
        border-color: rgba(46, 204, 113, 0.6);
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.2);
    """,
    'metric': """
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(52, 152, 219, 0.1) 100%);
        border: 2px solid rgba(46, 204, 113, 0.3);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    """,
    'metric_hover': """
        border-color: rgba(46, 204, 113, 0.6);
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.2);
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
    </style>
    """ 