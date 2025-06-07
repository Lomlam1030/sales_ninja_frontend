# Sales Ninja Dashboard

A modern dashboard application built with Streamlit that connects to backend REST APIs to display sales, inventory, and business metrics.

## Features

- Real-time dashboard with key performance indicators
- Sales analysis with date range filtering
- Inventory management with stock level alerts
- Interactive charts and data visualization
- Responsive and modern UI

## Setup

### Using Make (Recommended)

The project includes a Makefile for easy setup and management:

```bash
# Setup environment and run application
make all

# Or setup steps individually:
make setup    # Create virtual environment and install dependencies
make run      # Run the Streamlit application

# Other available commands:
make install  # Install dependencies (if venv exists)
make clean    # Remove virtual environment and cache files
make help     # Show all available commands
```

### Manual Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the API configuration in `.env`:
  ```
  API_BASE_URL=http://your-backend-api-url
  API_KEY=your-api-key
  ```

## Running the Application

Using Make:
```bash
make run
```

Or manually:
```bash
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

## Project Structure

```
sales_ninja_frontend/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── .env                  # Environment configuration
├── Makefile              # Build and management scripts
├── README.md             # Project documentation
├── pages/                # Page components
│   ├── dashboard.py      # Main dashboard view
│   ├── sales.py         # Sales analysis
│   └── inventory.py      # Inventory management
└── utils/                # Utility modules
    └── api.py           # API client
```

## API Endpoints

The dashboard expects the following REST API endpoints:

- `/api/dashboard/stats` - Dashboard statistics and metrics
- `/api/sales` - Sales data with date range filtering
- `/api/inventory/status` - Current inventory status
- `/api/products/top` - Top selling products

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 