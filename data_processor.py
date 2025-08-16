import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import plotly.io as pio

# Set Plotly renderer
pio.renderers.default = "browser"  # Ensures Plotly works in all environments

# Set page configuration
st.set_page_config(
    page_title="Vehicle Registration Analytics Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample Data Generator (Replace with your actual data collector)
class VahanDataCollector:
    def fetch_vehicle_data(self):
        """Simulates fetching data from API - REPLACE WITH YOUR ACTUAL IMPLEMENTATION"""
        dates = pd.date_range('2022-01-01', '2023-12-31')
        categories = ['2W', '3W', '4W']
        manufacturers = ['Tata', 'Mahindra', 'Maruti', 'Hyundai', 'Kia', 'Toyota', 'Honda']
        
        data = {
            'date': np.random.choice(dates, 1000),
            'vehicle_category': np.random.choice(categories, 1000),
            'manufacturer': np.random.choice(manufacturers, 1000),
            'registrations': np.random.randint(1, 100, 1000)
        }
        return pd.DataFrame(data)

# Data Processor
class DataProcessor:
    def process_for_analytics(self, df):
        """Process raw data for dashboard analytics"""
        results = {}
        
        # Ensure date is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Total registrations
        results['total_registrations'] = df['registrations'].sum()
        
        # Monthly trend data
        monthly = df.groupby(pd.Grouper(key='date', freq='M')).agg({'registrations': 'sum'}).reset_index()
        monthly['month'] = monthly['date'].dt.strftime('%Y-%m')
        results['monthly_trend'] = monthly
        
        # Category distribution
        results['category_distribution'] = df.groupby('vehicle_category')['registrations'].sum().reset_index()
        
        # Growth calculations (simplified)
        current_year = df[df['date'].dt.year == 2023]['registrations'].sum()
        last_year = df[df['date'].dt.year == 2022]['registrations'].sum()
        results['total_yoy_growth'] = ((current_year - last_year) / last_year) * 100 if last_year != 0 else 0
        
        # Manufacturer analysis
        results['top_manufacturers'] = df.groupby('manufacturer')['registrations'].sum().sort_values(ascending=False).reset_index()
        
        return results

# Utility functions
def format_number(num):
    """Format large numbers with commas"""
    return f"{int(num):,}"

# Initialize session state
def initialize_session_state():
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'vehicle_data' not in st.session_state:
        st.session_state.vehicle_data = None
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = None

def load_data():
    """Load data from API and process it"""
    data_collector = VahanDataCollector()
    data_processor = DataProcessor()
    
    with st.spinner("Fetching latest data..."):
        try:
            raw_data = data_collector.fetch_vehicle_data()
            processed_data = data_processor.process_for_analytics(raw_data)
            
            st.session_state.vehicle_data = raw_data
            st.session_state.processed_data = processed_data
            st.session_state.data_loaded = True
            st.session_state.last_refresh = datetime.now()
            return True
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.session_state.data_loaded = False
            return False

def create_filters(df):
    """Create interactive filters in the sidebar"""
    st.sidebar.subheader("🔍 Data Filters")
    
    # Date range filter
    if 'date' in df.columns:
        min_date = df['date'].min().to_pydatetime()
        max_date = df['date'].max().to_pydatetime()
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['date'] >= pd.to_datetime(start_date)) & 
                   (df['date'] <= pd.to_datetime(end_date))]
    
    # Vehicle category filter
    if 'vehicle_category' in df.columns:
        categories = st.sidebar.multiselect(
            "Vehicle Categories",
            options=sorted(df['vehicle_category'].unique().tolist()),
            default=df['vehicle_category'].unique().tolist()
        )
        df = df[df['vehicle_category'].isin(categories)]
    
    # Manufacturer filter
    if 'manufacturer' in df.columns:
        manufacturers = st.sidebar.multiselect(
            "Manufacturers",
            options=sorted(df['manufacturer'].unique().tolist()),
            default=df['manufacturer'].unique().tolist()[:3]
        )
        df = df[df['manufacturer'].isin(manufacturers)]
    
    return df

def display_kpi_metrics(processed_data):
    """Display the key performance indicator cards"""
    st.subheader("📊 Key Performance Indicators")
    
    cols = st.columns(4)
    
    with cols[0]:
        total = processed_data.get('total_registrations', 0)
        yoy = processed_data.get('total_yoy_growth', 0)
        st.metric(
            "Total Registrations",
            format_number(total),
            f"{yoy:+.1f}% YoY",
            delta_color="normal" if yoy >= 0 else "inverse"
        )
    
    with cols[1]:
        st.metric(
            "Avg Monthly",
            format_number(total // 12) if total else 0,
            "Registrations"
        )
    
    with cols[2]:
        top_mfg = processed_data.get('top_manufacturers', pd.DataFrame())
        leader = top_mfg.iloc[0]['manufacturer'] if len(top_mfg) > 0 else "N/A"
        st.metric(
            "Market Leader",
            leader
        )
    
    with cols[3]:
        if len(top_mfg) > 0:
            total = processed_data['total_registrations']
            leader_count = top_mfg.iloc[0]['registrations']
            share = (leader_count / total) * 100 if total else 0
            st.metric(
                "Market Share",
                f"{share:.1f}%"
            )

def create_trend_charts(processed_data):
    """Create registration trend and distribution charts"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Registration Trends")
        if 'monthly_trend' in processed_data:
            fig = px.line(
                processed_data['monthly_trend'],
                x='month',
                y='registrations',
                title="Monthly Registration Trends"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏭 Category Distribution")
        if 'category_distribution' in processed_data:
            fig = px.pie(
                processed_data['category_distribution'],
                values='registrations',
                names='vehicle_category',
                title="Vehicle Category Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

def create_manufacturer_analysis(processed_data):
    """Create manufacturer performance charts"""
    st.subheader("🏢 Manufacturer Performance")
    
    if 'top_manufacturers' in processed_data:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                processed_data['top_manufacturers'].head(10),
                x='registrations',
                y='manufacturer',
                orientation='h',
                title="Top Manufacturers"
            )
            st.plotly_chart(fig, use_container_width=True)

def main():
    initialize_session_state()
    
    # Header
    st.title("🚗 Vehicle Registration Analytics Dashboard")
    if st.session_state.last_refresh:
        st.caption(f"Last refreshed: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Sidebar controls
    with st.sidebar:
        st.header("Dashboard Controls")
        if st.button("🔄 Refresh Data", type="primary"):
            load_data()
    
    # Load data if not loaded
    if not st.session_state.data_loaded:
        if load_data():
            st.experimental_rerun()
        else:
            st.error("Failed to load data")
            return
    
    # Apply filters
    filtered_df = create_filters(st.session_state.vehicle_data.copy())
    
    # Re-process data if filters changed
    if not filtered_df.equals(st.session_state.vehicle_data):
        processor = DataProcessor()
        st.session_state.processed_data = processor.process_for_analytics(filtered_df)
    
    # Display dashboard
    display_kpi_metrics(st.session_state.processed_data)
    st.markdown("---")
    create_trend_charts(st.session_state.processed_data)
    st.markdown("---")
    create_manufacturer_analysis(st.session_state.processed_data)
    
    # Debug info (can be removed in production)
    with st.expander("Debug Info"):
        st.write("Filtered data shape:", filtered_df.shape)
        st.write("Processed data keys:", st.session_state.processed_data.keys())

if __name__ == "__main__":
    main()