import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import streamlit as st

class DataProcessor:
    """
    Processes vehicle registration data for analytics and visualization.
    Calculates YoY, QoQ growth and other investor-relevant metrics.
    """
    
    def __init__(self):
        pass
    
    def process_for_analytics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Process the raw data for analytics dashboard.
        Returns a dictionary with all calculated metrics and processed data.
        """
        try:
            if df.empty:
                return self._empty_analytics_result()
            
            # Ensure data is properly formatted
            df = self._prepare_data(df)
            
            if df.empty:
                return self._empty_analytics_result()
            
            # Calculate all analytics
            result = {}
            
            # Basic aggregations
            result['total_registrations'] = int(df['registrations'].sum())
            result['avg_monthly_registrations'] = int(df.groupby(df['date'].dt.to_period('M'))['registrations'].sum().mean())
            
            # Growth calculations
            result.update(self._calculate_growth_metrics(df))
            
            # Market analysis
            result.update(self._calculate_market_metrics(df))
            
            # Trend data for charts
            result.update(self._prepare_chart_data(df))
            
            # Summary table
            result['summary_table'] = self._create_summary_table(df)
            
            return result
            
        except Exception as e:
            st.error(f"Error in data processing: {str(e)}")
            return self._empty_analytics_result()
    
    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare and validate data for processing.
        """
        try:
            # Make a copy to avoid modifying original
            df = df.copy()
            
            # Ensure required columns exist
            required_columns = ['date', 'vehicle_category', 'registrations']
            for col in required_columns:
                if col not in df.columns:
                    return pd.DataFrame()
            
            # Convert data types
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['registrations'] = pd.to_numeric(df['registrations'], errors='coerce').fillna(0)
            
            # Remove invalid dates
            df = df.dropna(subset=['date'])
            
            # Ensure manufacturer column exists
            if 'manufacturer' not in df.columns:
                df['manufacturer'] = 'Unknown'
            
            # Add time period columns
            df['year'] = df['date'].dt.year
            df['quarter'] = df['date'].dt.quarter
            df['month'] = df['date'].dt.month
            df['year_quarter'] = df['year'].astype(str) + '-Q' + df['quarter'].astype(str)
            df['year_month'] = df['date'].dt.to_period('M')
            
            return df
            
        except Exception as e:
            print(f"Data preparation error: {str(e)}")
            return pd.DataFrame()
    
    def _calculate_growth_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate YoY and QoQ growth metrics.
        """
        result = {}
        
        try:
            # Total YoY growth
            yearly_totals = df.groupby('year')['registrations'].sum().reset_index()
            if len(yearly_totals) >= 2:
                current_year = yearly_totals['registrations'].iloc[-1]
                previous_year = yearly_totals['registrations'].iloc[-2]
                result['total_yoy_growth'] = ((current_year - previous_year) / previous_year * 100) if previous_year > 0 else 0
            else:
                result['total_yoy_growth'] = 0
            
            # Total QoQ growth
            quarterly_totals = df.groupby('year_quarter')['registrations'].sum().reset_index()
            if len(quarterly_totals) >= 2:
                current_quarter = quarterly_totals['registrations'].iloc[-1]
                previous_quarter = quarterly_totals['registrations'].iloc[-2]
                result['total_qoq_growth'] = ((current_quarter - previous_quarter) / previous_quarter * 100) if previous_quarter > 0 else 0
            else:
                result['total_qoq_growth'] = 0
            
            # YoY growth by category
            category_yoy = []
            for category in df['vehicle_category'].unique():
                cat_data = df[df['vehicle_category'] == category]
                cat_yearly = cat_data.groupby('year')['registrations'].sum().reset_index()
                
                if len(cat_yearly) >= 2:
                    current = cat_yearly['registrations'].iloc[-1]
                    previous = cat_yearly['registrations'].iloc[-2]
                    growth = ((current - previous) / previous * 100) if previous > 0 else 0
                else:
                    growth = 0
                
                category_yoy.append({
                    'category': category,
                    'yoy_growth': growth
                })
            
            result['yoy_growth_by_category'] = pd.DataFrame(category_yoy)
            
            # QoQ growth by category
            category_qoq = []
            for category in df['vehicle_category'].unique():
                cat_data = df[df['vehicle_category'] == category]
                cat_quarterly = cat_data.groupby('year_quarter')['registrations'].sum().reset_index()
                
                if len(cat_quarterly) >= 2:
                    current = cat_quarterly['registrations'].iloc[-1]
                    previous = cat_quarterly['registrations'].iloc[-2]
                    growth = ((current - previous) / previous * 100) if previous > 0 else 0
                else:
                    growth = 0
                
                category_qoq.append({
                    'category': category,
                    'qoq_growth': growth
                })
            
            result['qoq_growth_by_category'] = pd.DataFrame(category_qoq)
            
        except Exception as e:
            print(f"Growth calculation error: {str(e)}")
            result.update({
                'total_yoy_growth': 0,
                'total_qoq_growth': 0,
                'yoy_growth_by_category': pd.DataFrame(columns=['category', 'yoy_growth']),
                'qoq_growth_by_category': pd.DataFrame(columns=['category', 'qoq_growth'])
            })
        
        return result
    
    def _calculate_market_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate market analysis metrics.
        """
        result = {}
        
        try:
            # Market leader
            manufacturer_totals = df.groupby('manufacturer')['registrations'].sum().sort_values(ascending=False)
            if not manufacturer_totals.empty:
                result['market_leader'] = manufacturer_totals.index[0]
                total_market = manufacturer_totals.sum()
                result['market_leader_share'] = (manufacturer_totals.iloc[0] / total_market * 100) if total_market > 0 else 0
            else:
                result['market_leader'] = 'Unknown'
                result['market_leader_share'] = 0
            
            # Top manufacturers
            top_manufacturers = manufacturer_totals.head(15).reset_index()
            top_manufacturers.columns = ['manufacturer', 'registrations']
            result['top_manufacturers'] = top_manufacturers
            
            # Manufacturer growth analysis
            manufacturer_growth = []
            for manufacturer in top_manufacturers['manufacturer'].head(10):  # Top 10 for growth analysis
                mfr_data = df[df['manufacturer'] == manufacturer]
                
                # YoY growth
                mfr_yearly = mfr_data.groupby('year')['registrations'].sum().reset_index()
                yoy_growth = 0
                if len(mfr_yearly) >= 2:
                    current = mfr_yearly['registrations'].iloc[-1]
                    previous = mfr_yearly['registrations'].iloc[-2]
                    yoy_growth = ((current - previous) / previous * 100) if previous > 0 else 0
                
                # QoQ growth
                mfr_quarterly = mfr_data.groupby('year_quarter')['registrations'].sum().reset_index()
                qoq_growth = 0
                if len(mfr_quarterly) >= 2:
                    current = mfr_quarterly['registrations'].iloc[-1]
                    previous = mfr_quarterly['registrations'].iloc[-2]
                    qoq_growth = ((current - previous) / previous * 100) if previous > 0 else 0
                
                manufacturer_growth.append({
                    'manufacturer': manufacturer,
                    'registrations': int(mfr_data['registrations'].sum()),
                    'yoy_growth': yoy_growth,
                    'qoq_growth': qoq_growth
                })
            
            result['manufacturer_growth'] = pd.DataFrame(manufacturer_growth)
            
        except Exception as e:
            print(f"Market metrics calculation error: {str(e)}")
            result.update({
                'market_leader': 'Unknown',
                'market_leader_share': 0,
                'top_manufacturers': pd.DataFrame(columns=['manufacturer', 'registrations']),
                'manufacturer_growth': pd.DataFrame(columns=['manufacturer', 'registrations', 'yoy_growth', 'qoq_growth'])
            })
        
        return result
    
    def _prepare_chart_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Prepare data for charts and visualizations.
        """
        result = {}
        
        try:
            # Monthly trend data
            monthly_trend = df.groupby('year_month')['registrations'].sum().reset_index()
            monthly_trend['month'] = monthly_trend['year_month'].dt.strftime('%Y-%m')
            monthly_trend = monthly_trend[['month', 'registrations']]
            result['monthly_trend'] = monthly_trend
            
            # Category distribution
            category_dist = df.groupby('vehicle_category')['registrations'].sum().reset_index()
            category_dist.columns = ['category', 'registrations']
            result['category_distribution'] = category_dist
            
        except Exception as e:
            print(f"Chart data preparation error: {str(e)}")
            result.update({
                'monthly_trend': pd.DataFrame(columns=['month', 'registrations']),
                'category_distribution': pd.DataFrame(columns=['category', 'registrations'])
            })
        
        return result
    
    def _create_summary_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a summary table for the dashboard.
        """
        try:
            # Create monthly summary by category
            summary = df.groupby(['year_month', 'vehicle_category']).agg({
                'registrations': 'sum',
                'manufacturer': 'nunique'
            }).reset_index()
            
            summary.columns = ['Month', 'Category', 'Total Registrations', 'Number of Manufacturers']
            summary['Month'] = summary['Month'].dt.strftime('%Y-%m')
            
            # Sort by month descending
            summary = summary.sort_values(['Month', 'Category'], ascending=[False, True])
            
            return summary.head(50)  # Limit to 50 rows for display
            
        except Exception as e:
            print(f"Summary table creation error: {str(e)}")
            return pd.DataFrame(columns=['Month', 'Category', 'Total Registrations', 'Number of Manufacturers'])
    
    def _empty_analytics_result(self) -> Dict[str, Any]:
        """
        Return empty analytics result structure.
        """
        return {
            'total_registrations': 0,
            'total_yoy_growth': 0,
            'total_qoq_growth': 0,
            'avg_monthly_registrations': 0,
            'market_leader': 'No Data',
            'market_leader_share': 0,
            'yoy_growth_by_category': pd.DataFrame(columns=['category', 'yoy_growth']),
            'qoq_growth_by_category': pd.DataFrame(columns=['category', 'qoq_growth']),
            'top_manufacturers': pd.DataFrame(columns=['manufacturer', 'registrations']),
            'manufacturer_growth': pd.DataFrame(columns=['manufacturer', 'registrations', 'yoy_growth', 'qoq_growth']),
            'monthly_trend': pd.DataFrame(columns=['month', 'registrations']),
            'category_distribution': pd.DataFrame(columns=['category', 'registrations']),
            'summary_table': pd.DataFrame(columns=['Month', 'Category', 'Total Registrations', 'Number of Manufacturers'])
        }
