# Sales Ninja Frontend

A comprehensive sales analytics dashboard with promotional impact analysis capabilities. This project provides both a web dashboard and REST API endpoints for analyzing sales performance and promotional effectiveness.

## Features

- 📊 Interactive Sales Dashboard
- 📈 Promotional Impact Analysis
- 📅 Time-based Analytics (Daily/Weekly/Monthly)
- 🏪 Store Performance Metrics
- 📦 Product Category Analysis
- 🌐 REST API Endpoints

## Project Structure

```
sales_ninja_frontend/
├── api/
│   └── sales_api.py         # FastAPI endpoints
├── pages/
│   └── 3_📊_Dashboard.py    # Streamlit dashboard
├── utils/
│   ├── data_queries.py      # BigQuery data access
│   └── page_config.py       # Dashboard configuration
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8+
- Google Cloud Platform account with BigQuery access
- Google Cloud credentials configured

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sales_ninja_frontend.git
cd sales_ninja_frontend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

### Dashboard

Run the Streamlit dashboard:
```bash
streamlit run pages/3_📊_Dashboard.py
```

The dashboard will be available at `http://localhost:8501`

### API Server

Run the FastAPI server:
```bash
uvicorn api.sales_api:app --reload
```

The API will be available at:
- API Endpoints: `http://localhost:8000`
- Swagger Documentation: `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

## API Endpoints

- `GET /sales/daily/` - Daily sales metrics
- `GET /sales/monthly/` - Monthly aggregated metrics
- `GET /sales/weekly/` - Weekly aggregated metrics
- `GET /sales/kpi/` - Overall KPI metrics
- `GET /sales/promotion-impact/` - Promotional analysis
- `GET /sales/product-categories/` - Category-wise sales
- `GET /sales/store-performance/` - Store performance metrics
- `GET /health` - Health check endpoint

## Environment Variables

Create a `.env` file with the following variables:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

## Security

- Ensure your Google Cloud credentials are properly secured
- Never commit `.env` files or credential files to version control
- Use appropriate IAM roles and permissions in Google Cloud

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 