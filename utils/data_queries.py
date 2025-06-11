from .data_loader import get_daily_sales, get_kpi_metrics, get_promotion_impact

# Re-export the functions to maintain backward compatibility
__all__ = ['get_daily_sales', 'get_kpi_metrics', 'get_promotion_impact'] 