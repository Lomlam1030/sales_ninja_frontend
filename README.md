# Sales Ninja Frontend

A Streamlit dashboard for visualizing sales data with support for both BigQuery and REST API data sources.

## Features

- Flexible data source configuration (BigQuery or REST API)
- Sales data visualization and analysis
- Configurable data loading with filters
- Secure credential management

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sales_ninja_frontend.git
cd sales_ninja_frontend
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure your environment:
   - Copy `.env.example` to `.env`
   - Edit `.env` with your configuration:

```ini
# Data Source Configuration
# Options: bigquery, rest_api
DATA_SOURCE=bigquery

# BigQuery Settings (required if using BigQuery)
GCP_PROJECT_ID=your-project-id
BQ_DATASET=dashboard_data
BQ_ACTUALS_TABLE=dashboard_merged_data
BQ_PREDICTIONS_TABLE=dashboard_prediction_data
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json

# REST API Settings (required if using REST API)
API_BASE_URL=http://localhost:8000
API_VERSION=v1
API_KEY=your-api-key

# Data Loading Settings
DEFAULT_YEAR=2007
MAX_ROWS=1000  # Set to 0 for no limit
```

4. Run the application:
```bash
streamlit run app.py
```

## Configuration

### BigQuery Setup

1. Create a service account in Google Cloud Console
2. Download the service account key JSON file
3. Set `GOOGLE_APPLICATION_CREDENTIALS` to point to your key file
4. Set `DATA_SOURCE=bigquery` in your `.env` file

### REST API Setup

1. Ensure you have access to the backend API
2. Get your API key from the backend team
3. Set `DATA_SOURCE=rest_api` in your `.env` file
4. Configure the API endpoint and key in your `.env` file

## Development

### Project Structure

```
sales_ninja_frontend/
├── app.py                 # Main Streamlit application
├── config/
│   ├── settings.py       # Configuration management
│   └── __init__.py
├── services/
│   ├── data_source.py    # Data source implementations
│   └── __init__.py
├── utils/
│   └── sales_calculations.py  # Data processing utilities
├── pages/                # Streamlit pages
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (not in git)
```

### Adding a New Data Source

1. Add a new enum value in `config/settings.py`
2. Create a new class implementing `DataSourceInterface` in `services/data_source.py`
3. Update the factory function `get_data_source()`

## Security

- Never commit sensitive credentials to git
- Use environment variables for all sensitive configuration
- Keep your API keys and service account files secure
- Regularly rotate your credentials

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 