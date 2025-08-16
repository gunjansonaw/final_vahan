import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import plotly.io as pio

# Set Plotly renderer
pio.renderers.default = "browser"

# Set page configuration
st.set_page_config(
    page_title="Vehicle Registration Analytics Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample Data Generator (with proper date handling)
class VahanDataCollector:
    def fetch_vehicle_data(self):
        """Generate realistic sample data"""
        np.random.seed(42)
        date_rng = pd.date_range('2022-01-01', '2023-12-31', freq='D')
        categories = ['2W', '3W', '4W']
        manufacturers = ['Tata', 'Mahindra', 'Maruti', 'Hyundai', 'Kia', 'Toyota', 'Honda']
        
        data = pd.DataFrame({
            'date': np.random.choice(date_rng, 1000),
            'vehicle_category': np.random.choice(categories, 1000, p=[0.6, 0.1, 0.3]),
            'manufacturer': np.random.choice(manufacturers, 1000),
            'registrations': np.random.randint(1, 100, 1000)
        })
        
        # Ensure proper datetime type
        data['date'] = pd.to_datetime(data['date'])
        return data

# Data Processor (with fixed warnings)
class DataProcessor:
    def process_for_analytics(self, df):
        """Process raw data for dashboard analytics"""
        results = {}
        
        # Create a copy to avoid SettingWithCopyWarning
        df = df.copy()
        
        # Total registrations
        results['total_registrations'] = df['registrations'].sum()
        
        # Monthly trend data - using 'ME' instead of deprecated 'M'
        monthly = df.groupby(pd.Grouper(key='date', freq='ME')).agg({'registrations': 'sum'}).reset_index()
        monthly['month'] = monthly['date'].dt.strftime('%Y-%m')
        results['monthly_trend'] = monthly
        
        # Category distribution - ensure column names match what Plotly expects
        category_dist = df.groupby('vehicle_category')['registrations'].sum().reset_index()
        category_dist = category_dist.rename(columns={'vehicle_category': 'category'})
        results['category_distribution'] = category_dist
        
        # Growth calculations
        if len(df['date'].dt.year.unique()) > 1:
            current_year = df[df['date'].dt.year == df['date'].dt.year.max()]['registrations'].sum()
            last_year = df[df['date'].dt.year == df['date'].dt.year.max() - 1]['registrations'].sum()
            results['total_yoy_growth'] = ((current_year - last_year) / last_year) * 100 if last_year != 0 else 0
        else:
            results['total_yoy_growth'] = 0
        
        # Manufacturer analysis
        manufacturer_stats = df.groupby('manufacturer')['registrations'].sum().sort_values(ascending=False).reset_index()
        results['top_manufacturers'] = manufacturer_stats
        
        return results

# Utility functions
def format_number(num):
    """Format large numbers with commas"""
    return f"{int(num):,}" if pd.notna(num) else "0"

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
    """Load and process data"""
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
    """Create interactive filters"""
    st.sidebar.subheader("🔍 Data Filters")
    
    # Create copy to avoid modifying original
    df = df.copy()
    
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
    """Display key performance indicators"""
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
        if len(top_mfg) > 0 and 'total_registrations' in processed_data:
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
                title="Monthly Registration Trends",
                labels={'registrations': 'Number of Registrations'}
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Monthly trend data not available")
    
    with col2:
        st.subheader("🏭 Category Distribution")
        if 'category_distribution' in processed_data:
            fig = px.pie(
                processed_data['category_distribution'],
                values='registrations',
                names='category',  # This now matches the renamed column
                title="Vehicle Category Distribution",
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Category distribution data not available")

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
                title="Top 10 Manufacturers by Registrations",
                labels={'registrations': 'Number of Registrations'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Additional manufacturer analysis can go here
            st.write("Manufacturer Performance Metrics")
            st.dataframe(
                processed_data['top_manufacturers'].head(10),
                use_container_width=True
            )

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
            if load_data():
                st.rerun()
    
    # Load data if not loaded
    if not st.session_state.data_loaded:
        if load_data():
            st.rerun()
        else:
            st.error("Failed to load data. Using sample dataset.")
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

if __name__ == "__main__":
    main()