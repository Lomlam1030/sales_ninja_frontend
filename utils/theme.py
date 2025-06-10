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
                'color': '#191970',  # Midnight Blue
                'size': 12
            },
            'title': {
                'font': {
                    'color': '#191970',  # Midnight Blue
                    'size': 16,
                    'weight': 600
                }
            },
            'xaxis': {
                'title_font': {'color': '#191970', 'size': 14},  # Midnight Blue
                'tickfont': {'color': '#191970', 'size': 12},  # Midnight Blue
                'gridcolor': 'rgba(65, 105, 225, 0.1)',  # Royal Blue with opacity
                'zerolinecolor': 'rgba(65, 105, 225, 0.2)'  # Royal Blue with opacity
            },
            'yaxis': {
                'title_font': {'color': '#191970', 'size': 14},  # Midnight Blue
                'tickfont': {'color': '#191970', 'size': 12},  # Midnight Blue
                'gridcolor': 'rgba(65, 105, 225, 0.1)',  # Royal Blue with opacity
                'zerolinecolor': 'rgba(65, 105, 225, 0.2)'  # Royal Blue with opacity
            },
            'legend': {
                'font': {'color': '#191970', 'size': 12}  # Midnight Blue
            }
        }
    }

# CSS for consistent styling across pages
def get_css():
    """Return CSS styles for consistent page styling"""
    return """
    <style>
        /* Base text colors */
        .stMarkdown, p, .stText {
            color: #9370DB !important;  /* Medium Purple - darker shade of lavender */
        }
        
        /* Metric labels and values */
        [data-testid="stMetricLabel"] {
            color: #4169E1 !important;  /* Royal Blue */
            font-size: 1rem !important;
            font-weight: 600 !important;
        }
        [data-testid="stMetricValue"] {
            color: #191970 !important;  /* Midnight Blue */
            font-size: 1.8rem !important;
            font-weight: 600 !important;
        }
        
        /* Headers */
        .section-header {
            color: #191970 !important;  /* Midnight Blue */
            font-size: 1.5em !important;
            font-weight: 600 !important;
            margin: 1em 0 !important;
            padding: 0.5em 0 !important;
            border-bottom: 2px solid rgba(147, 112, 219, 0.3) !important;
        }
        
        /* Filter area styling */
        .stSelectbox label, .stMultiSelect label, .stSlider label {
            color: #191970 !important;  /* Midnight Blue */
            font-weight: 600 !important;
            font-size: 1rem !important;
        }
        .stSelectbox > div > div[data-baseweb="select"] > div, 
        .stMultiSelect > div > div[data-baseweb="select"] > div,
        .stSelectbox > div > div > div[role="listbox"],
        .stMultiSelect > div > div > div[role="listbox"] {
            color: #191970 !important;  /* Midnight Blue */
            font-weight: 500 !important;
            background-color: rgba(255, 255, 255, 0.9) !important;
        }
        /* Filter options styling */
        div[role="option"] {
            color: #191970 !important;  /* Midnight Blue */
            background-color: rgba(255, 255, 255, 0.9) !important;
        }
        div[role="option"]:hover {
            background-color: rgba(65, 105, 225, 0.1) !important;
        }
        /* Selected option styling */
        div[aria-selected="true"] {
            background-color: rgba(65, 105, 225, 0.2) !important;
            color: #191970 !important;  /* Midnight Blue */
            font-weight: 600 !important;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1em;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 1em;
            border-radius: 0.5em;
        }
        .stTabs [data-baseweb="tab"],
        .stTabs [data-baseweb="tab"] span {
            height: 3em;
            white-space: pre-wrap;
            background-color: #4169E1 !important;  /* Royal Blue */
            border-radius: 0.5em;
            color: #FFFFFF !important;  /* White */
            font-size: 1em;
            font-weight: 600;
            border: none;
            padding: 0 1em;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover,
        .stTabs [data-baseweb="tab"]:hover span {
            background-color: #6A5ACD !important;  /* Slate Blue */
            color: #FFFFFF !important;  /* White */
        }
        .stTabs [aria-selected="true"],
        .stTabs [aria-selected="true"] span {
            background-color: #191970 !important;  /* Midnight Blue */
            color: #FFFFFF !important;  /* White */
            font-weight: 600;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        /* Override any other text colors in tabs */
        .stTabs [data-baseweb="tab"] * {
            color: #FFFFFF !important;
        }
        
        /* Table headers and cells */
        .table-header {
            color: #191970 !important;  /* Midnight Blue */
            font-size: 1.5em !important;
            font-weight: 600 !important;
            margin: 1em 0 !important;
        }
        [data-testid="stDataFrameResizable"] {
            color: #4169E1 !important;  /* Royal Blue */
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(25, 25, 112, 0.3);
            border-right: 1px solid rgba(147, 112, 219, 0.2);
        }
        [data-testid="stSidebar"] .stMarkdown {
            color: #4169E1 !important;  /* Royal Blue */
            font-weight: 600 !important;
        }
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stMultiSelect label {
            color: #4169E1 !important;  /* Royal Blue */
        }
        [data-testid="stSidebar"] .stSelectbox > div > div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] .stMultiSelect > div > div[data-baseweb="select"] > div {
            color: #191970 !important;  /* Midnight Blue */
            background-color: rgba(255, 255, 255, 0.9) !important;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: rgba(65, 105, 225, 0.2) !important;
            color: #191970 !important;  /* Midnight Blue */
            border: 1px solid rgba(147, 112, 219, 0.3) !important;
            font-weight: 600 !important;
        }
        .stButton > button:hover {
            background-color: rgba(65, 105, 225, 0.4) !important;
            border: 1px solid rgba(147, 112, 219, 0.5) !important;
        }
    </style>
    """ 