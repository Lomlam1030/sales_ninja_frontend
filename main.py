import uvicorn
from api.sales_api import app

if __name__ == "__main__":
    uvicorn.run(
        "api.sales_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 