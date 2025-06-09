from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class DailySalesResponse(BaseModel):
    date: date
    total_sales: float
    total_orders: int
    average_order_value: float

class TopProductsResponse(BaseModel):
    product_id: str
    product_name: str
    total_quantity: int
    total_revenue: float
    average_price: float

class RegionalSalesResponse(BaseModel):
    region: str
    total_sales: float
    total_orders: int
    average_order_value: float
    top_selling_product: str 