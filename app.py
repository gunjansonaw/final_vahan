import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from data_collector import VahanDataCollector
from data_processor import DataProcessor
from utils import format_number, calculate_growth

# Set page configuration
st.set_page_config(
    page_title="Vehicle Registration Analytics Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'vehicle_data' not in st.session_state:
    st.session_state.vehicle_data = None

def main():
    # Header
    st.title("🚗 Vehicle Registration Analytics Dashboard")
    st.markdown("**Investor-focused insights from Vahan Dashboard data**")
    st.markdown("---")
    
    # Initialize data collector and processor
    data_collector = VahanDataCollector()
    data_processor = DataProcessor()
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Dashboard Controls")
        
        # Data refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            with st.spinner("Fetching latest data from Vahan Dashboard..."):
                try:
                    st.session_state.vehicle_data = data_collector.fetch_vehicle_data()
                    st.session_state.data_loaded = True
                    st.success("Data refreshed successfully!")
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")
                    st.session_state.data_loaded = False
        
        # Load initial data if not loaded
        if not st.session_state.data_loaded:
            with st.spinner("Loading initial data..."):
                try:
                    st.session_state.vehicle_data = data_collector.fetch_vehicle_data()
                    st.session_state.data_loaded = True
                except Exception as e:
                    st.error(f"Error loading initial data: {str(e)}")
                    st.session_state.data_loaded = False
    
    # Main dashboard content
    if st.session_state.data_loaded and st.session_state.vehicle_data is not None:
        df = st.session_state.vehicle_data
        
        # Sidebar filters
        with st.sidebar:
            st.markdown("---")
            st.subheader("Filters")
            
            # Date range selection
            if 'date' in df.columns:
                min_date = df['date'].min()
                max_date = df['date'].max()
                
                date_range = st.date_input(
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
                categories = ['All'] + sorted(df['vehicle_category'].unique().tolist())
                selected_category = st.selectbox("Vehicle Category", categories)
                
                if selected_category != 'All':
                    df = df[df['vehicle_category'] == selected_category]
            
            # Manufacturer filter
            if 'manufacturer' in df.columns:
                manufacturers = ['All'] + sorted(df['manufacturer'].unique().tolist())
                selected_manufacturer = st.selectbox("Manufacturer", manufacturers)
                
                if selected_manufacturer != 'All':
                    df = df[df['manufacturer'] == selected_manufacturer]
        
        # Process data for analytics
        processed_data = data_processor.process_for_analytics(df)
        
        # Key Metrics Row
        st.subheader("📊 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_registrations = processed_data.get('total_registrations', 0)
            yoy_growth = processed_data.get('total_yoy_growth', 0)
            st.metric(
                "Total Registrations",
                format_number(total_registrations),
                f"{yoy_growth:+.1f}% YoY"
            )
        
        with col2:
            qoq_growth = processed_data.get('total_qoq_growth', 0)
            st.metric(
                "Quarter Growth",
                f"{qoq_growth:+.1f}%",
                "QoQ Change"
            )
        
        with col3:
            avg_monthly = processed_data.get('avg_monthly_registrations', 0)
            st.metric(
                "Avg Monthly",
                format_number(avg_monthly),
                "Registrations"
            )
        
        with col4:
            market_leader = processed_data.get('market_leader', 'N/A')
            market_share = processed_data.get('market_leader_share', 0)
            st.metric(
                "Market Leader",
                market_leader,
                f"{market_share:.1f}% share"
            )
        
        st.markdown("---")
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Registration Trends")
            
            # Monthly trend chart
            if 'monthly_trend' in processed_data:
                monthly_data = processed_data['monthly_trend']
                fig = px.line(
                    monthly_data,
                    x='month',
                    y='registrations',
                    title="Monthly Registration Trends",
                    labels={'registrations': 'Registrations', 'month': 'Month'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🏭 Category Distribution")
            
            # Category pie chart
            if 'category_distribution' in processed_data:
                cat_data = processed_data['category_distribution']
                fig = px.pie(
                    cat_data,
                    values='registrations',
                    names='category',
                    title="Vehicle Category Distribution"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Growth Analysis Section
        st.subheader("📊 Growth Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Year-over-Year Growth by Category**")
            if 'yoy_growth_by_category' in processed_data:
                yoy_data = processed_data['yoy_growth_by_category']
                fig = px.bar(
                    yoy_data,
                    x='category',
                    y='yoy_growth',
                    title="YoY Growth by Vehicle Category",
                    labels={'yoy_growth': 'YoY Growth (%)', 'category': 'Category'},
                    color='yoy_growth',
                    color_continuous_scale='RdYlGn'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Quarter-over-Quarter Growth by Category**")
            if 'qoq_growth_by_category' in processed_data:
                qoq_data = processed_data['qoq_growth_by_category']
                fig = px.bar(
                    qoq_data,
                    x='category',
                    y='qoq_growth',
                    title="QoQ Growth by Vehicle Category",
                    labels={'qoq_growth': 'QoQ Growth (%)', 'category': 'Category'},
                    color='qoq_growth',
                    color_continuous_scale='RdYlBu'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Manufacturer Analysis
        st.subheader("🏢 Manufacturer Performance")
        
        if 'top_manufacturers' in processed_data:
            manufacturer_data = processed_data['top_manufacturers']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    manufacturer_data.head(10),
                    x='registrations',
                    y='manufacturer',
                    orientation='h',
                    title="Top 10 Manufacturers by Registrations",
                    labels={'registrations': 'Registrations', 'manufacturer': 'Manufacturer'}
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Manufacturer growth chart
                if 'manufacturer_growth' in processed_data:
                    growth_data = processed_data['manufacturer_growth']
                    fig = px.scatter(
                        growth_data,
                        x='yoy_growth',
                        y='qoq_growth',
                        size='registrations',
                        hover_name='manufacturer',
                        title="Manufacturer Growth Matrix (YoY vs QoQ)",
                        labels={
                            'yoy_growth': 'YoY Growth (%)',
                            'qoq_growth': 'QoQ Growth (%)'
                        }
                    )
                    fig.add_hline(y=0, line_dash="dash", line_color="gray")
                    fig.add_vline(x=0, line_dash="dash", line_color="gray")
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
        
        # Data Table
        st.subheader("📋 Detailed Data")
        
        # Data export
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.button("📄 Export CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"vehicle_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            show_raw_data = st.checkbox("Show Raw Data")
        
        if show_raw_data:
            st.dataframe(df, use_container_width=True)
        else:
            # Show summary table
            if 'summary_table' in processed_data:
                st.dataframe(processed_data['summary_table'], use_container_width=True)
    
    else:
        # Error state or no data
        st.error("⚠️ Unable to load vehicle registration data")
        st.markdown("""
        **Possible reasons:**
        - Vahan Dashboard API is temporarily unavailable
        - Network connectivity issues
        - Data parsing errors
        
        **Try:**
        1. Click the 'Refresh Data' button in the sidebar
        2. Check your internet connection
        3. Try again in a few minutes
        """)
        
        # Show sample structure for development
        st.info("📝 Expected data structure: Date, Vehicle Category (2W/3W/4W), Manufacturer, Registrations")

if __name__ == "__main__":
    main()
