# Vehicle Registration Analytics Dashboard

## Overview

This is a Streamlit-based analytics dashboard that provides investor-focused insights from vehicle registration data sourced from the Vahan Dashboard (vahan.parivahan.gov.in). The application fetches real-time vehicle registration data from India's official transport portal and processes it to generate key performance indicators, growth metrics, and market analysis visualizations for investment decision-making.

The dashboard focuses on delivering actionable insights through data visualization, trend analysis, and comparative metrics that are particularly relevant to investors in the automotive and transportation sectors.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for rapid web application development
- **UI Components**: Native Streamlit widgets and components for dashboard controls
- **Visualization**: Plotly Express and Plotly Graph Objects for interactive charts and graphs
- **Layout**: Wide layout configuration with expandable sidebar for controls
- **State Management**: Streamlit session state for data persistence across user interactions

### Backend Architecture
- **Data Collection Layer**: `VahanDataCollector` class handles data fetching from external sources
- **Data Processing Layer**: `DataProcessor` class performs analytics calculations and data transformations
- **Utility Layer**: Helper functions for number formatting and growth calculations
- **Architecture Pattern**: Modular design with separation of concerns between data collection, processing, and presentation

### Data Processing Pipeline
- **Primary Data Source**: Vahan Dashboard API endpoints
- **Fallback Method**: Web scraping using trafilatura for content extraction
- **Data Structure**: Pandas DataFrames for efficient data manipulation
- **Analytics Engine**: Custom growth metrics, market analysis, and trend calculations
- **Caching Strategy**: Session-based data caching to minimize API calls

### Error Handling and Resilience
- **Graceful Degradation**: Fallback to empty datasets when data sources are unavailable
- **Error Recovery**: Multiple data fetching strategies with fallback mechanisms
- **User Feedback**: Clear error messages and loading indicators

## External Dependencies

### Data Sources
- **Vahan Dashboard API**: Primary data source at vahan.parivahan.gov.in
- **Web Scraping Fallback**: trafilatura library for content extraction when API is unavailable

### Python Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualization (plotly.express and plotly.graph_objects)
- **requests**: HTTP client for API interactions
- **trafilatura**: Web content extraction for scraping fallback

### Development Dependencies
- **datetime**: Date and time handling
- **json**: JSON data processing
- **re**: Regular expressions for data parsing
- **time**: Time-based operations and delays
- **typing**: Type hints for better code documentation

### Infrastructure Requirements
- **Session Management**: Built-in Streamlit session handling
- **HTTP Client**: requests.Session for persistent connections
- **User Agent Spoofing**: Browser headers for web scraping compatibility