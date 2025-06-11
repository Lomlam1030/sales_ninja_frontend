"""Utility functions for the Sales Ninja dashboard."""

from .sales_calculations import get_data_source
from .theme import get_css
from .page_config import set_page_config, add_page_title

__all__ = [
    'get_data_source',
    'get_css',
    'set_page_config',
    'add_page_title'
] 