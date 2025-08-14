# Vehicle Registration Analytics Dashboard

## Overview

An investor-focused Streamlit dashboard that provides comprehensive analytics and insights from vehicle registration data sourced from India's official Vahan Dashboard (vahan.parivahan.gov.in). This application delivers real-time vehicle registration analytics with YoY/QoQ growth metrics, market analysis, and manufacturer performance insights.

## Features

### 📊 Key Performance Indicators
- **Total Registrations**: Overall vehicle registration count with YoY growth
- **Quarter Growth**: QoQ percentage change indicators
- **Monthly Averages**: Average monthly registration trends
- **Market Leadership**: Top manufacturers and market share analysis

### 📈 Analytics & Insights
- **YoY/QoQ Growth Analysis**: Year-over-Year and Quarter-over-Quarter growth metrics
- **Vehicle Category Breakdown**: 2W/3W/4W registration analysis
- **Manufacturer Performance**: Top manufacturers by registrations and growth
- **Trend Visualizations**: Interactive charts showing registration patterns
- **Growth Matrix**: Comprehensive manufacturer growth comparison

### 🎛️ Interactive Features
- **Date Range Selection**: Filter data by custom date periods
- **Category Filters**: Focus on specific vehicle categories (2W/3W/4W)
- **Manufacturer Filters**: Analyze specific manufacturer performance
- **Data Export**: Download filtered data as CSV
- **Real-time Updates**: Refresh data from Vahan Dashboard

## Technical Architecture

### Frontend
- **Framework**: Streamlit for rapid web application development
- **Visualization**: Plotly Express/Graph Objects for interactive charts
- **UI**: Responsive design with sidebar controls and expandable sections

### Backend
- **Data Collection**: VahanDataCollector class with API and web scraping capabilities
- **Data Processing**: DataProcessor class for analytics calculations
- **Utilities**: Helper functions for formatting and calculations

### Data Sources
- **Primary**: Vahan Dashboard API endpoints
- **Fallback**: Web scraping using trafilatura for content extraction

## Installation

### Prerequisites
- Python 3.11+
- Required packages (see requirements.txt)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vehicle-registration-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

4. **Access the dashboard**
   Open your browser to `http://localhost:5000`

## Usage

### Dashboard Navigation

1. **Data Loading**: Click "Refresh Data" to fetch latest information from Vahan Dashboard
2. **Filter Selection**: Use sidebar controls to filter by date range, vehicle category, or manufacturer
3. **Analytics Review**: Examine KPIs, growth charts, and manufacturer performance
4. **Data Export**: Export filtered datasets for further analysis

### Key Metrics Explained

- **YoY Growth**: Year-over-Year percentage change in registrations
- **QoQ Growth**: Quarter-over-Quarter percentage change
- **Market Share**: Manufacturer's percentage of total registrations
- **Growth Matrix**: Comparative analysis of YoY vs QoQ performance

## File Structure

```
vehicle-registration-dashboard/
├── app.py                 # Main Streamlit application
├── data_collector.py      # Data collection from Vahan Dashboard
├── data_processor.py      # Analytics and data processing
├── utils.py              # Utility functions
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualization
- **requests**: HTTP client for API calls
- **trafilatura**: Web content extraction

## Data Processing Pipeline

1. **Data Collection**: Fetch from Vahan Dashboard API endpoints
2. **Fallback Handling**: Web scraping if API unavailable
3. **Data Validation**: Clean and standardize data format
4. **Analytics Calculation**: Compute YoY/QoQ growth metrics
5. **Visualization Preparation**: Format data for charts and tables

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Disclaimer

This application uses data from the official Vahan Dashboard (vahan.parivahan.gov.in). Data accuracy and availability depend on the source system. This tool is designed for analytical and educational purposes.