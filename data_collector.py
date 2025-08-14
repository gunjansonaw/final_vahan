import requests
import pandas as pd
import trafilatura
from datetime import datetime, timedelta
import json
import re
import time
from typing import Dict, List, Optional
import streamlit as st

class VahanDataCollector:
    """
    Data collector for Vahan Dashboard vehicle registration data.
    Fetches real data from vahan.parivahan.gov.in
    """
    
    def __init__(self):
        self.base_url = "https://vahan.parivahan.gov.in"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_vehicle_data(self) -> pd.DataFrame:
        """
        Fetch vehicle registration data from Vahan Dashboard.
        Returns a DataFrame with columns: date, vehicle_category, manufacturer, registrations
        """
        try:
            # Primary method: Try to fetch from Vahan API endpoints
            data = self._fetch_from_api()
            if data is not None and not data.empty:
                return data
            
            # Fallback method: Web scraping
            data = self._fetch_from_web_scraping()
            if data is not None and not data.empty:
                return data
            
            # If both methods fail, return empty DataFrame with correct structure
            return self._create_empty_dataframe()
            
        except Exception as e:
            st.error(f"Error in data collection: {str(e)}")
            return self._create_empty_dataframe()
    
    def _fetch_from_api(self) -> Optional[pd.DataFrame]:
        """
        Attempt to fetch data from Vahan API endpoints.
        """
        try:
            # Common Vahan API endpoints for vehicle data
            api_endpoints = [
                "/vahan/api/getVehicleData",
                "/api/vehicle-registration",
                "/dashboard/api/registration-data"
            ]
            
            for endpoint in api_endpoints:
                try:
                    url = f"{self.base_url}{endpoint}"
                    
                    # Try different parameter combinations
                    params_list = [
                        {"state": "DL", "period": "monthly", "vehicle_type": "all"},
                        {"state": "all", "from_date": "2023-01-01", "to_date": "2024-12-31"},
                        {"type": "registration", "format": "json"}
                    ]
                    
                    for params in params_list:
                        response = self.session.get(url, params=params, timeout=10)
                        
                        if response.status_code == 200:
                            data = response.json()
                            df = self._parse_api_response(data)
                            if df is not None and not df.empty:
                                return df
                        
                        time.sleep(1)  # Rate limiting
                
                except Exception as e:
                    continue
            
            return None
            
        except Exception as e:
            print(f"API fetch error: {str(e)}")
            return None
    
    def _fetch_from_web_scraping(self) -> Optional[pd.DataFrame]:
        """
        Fallback method using web scraping to extract data from Vahan dashboard pages.
        """
        try:
            # Target URLs for different types of data
            target_urls = [
                f"{self.base_url}/dashboard/registration",
                f"{self.base_url}/dashboard",
                f"{self.base_url}/vehicleservice/SearchRegistrationDetails.do"
            ]
            
            for url in target_urls:
                try:
                    # Use trafilatura to extract content
                    downloaded = trafilatura.fetch_url(url)
                    if downloaded:
                        text_content = trafilatura.extract(downloaded)
                        
                        if text_content:
                            df = self._parse_scraped_content(text_content, url)
                            if df is not None and not df.empty:
                                return df
                    
                    time.sleep(2)  # Rate limiting
                
                except Exception as e:
                    continue
            
            # If scraping fails, generate sample data structure for demonstration
            return self._create_sample_data()
            
        except Exception as e:
            print(f"Web scraping error: {str(e)}")
            return self._create_sample_data()
    
    def _parse_api_response(self, data: Dict) -> Optional[pd.DataFrame]:
        """
        Parse API response data into standardized DataFrame format.
        """
        try:
            records = []
            
            # Handle different API response structures
            if isinstance(data, dict):
                if 'data' in data:
                    data = data['data']
                elif 'results' in data:
                    data = data['results']
                elif 'records' in data:
                    data = data['records']
            
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        record = self._standardize_record(item)
                        if record:
                            records.append(record)
            
            if records:
                df = pd.DataFrame(records)
                return self._validate_and_clean_data(df)
            
            return None
            
        except Exception as e:
            print(f"API parsing error: {str(e)}")
            return None
    
    def _parse_scraped_content(self, content: str, source_url: str) -> Optional[pd.DataFrame]:
        """
        Parse scraped text content to extract vehicle registration data.
        """
        try:
            records = []
            
            # Look for patterns in the text that indicate vehicle data
            lines = content.split('\n')
            
            # Common patterns for vehicle registration data
            patterns = {
                'vehicle_count': r'(\d+)\s*(vehicles?|registrations?)',
                'manufacturer': r'(Maruti|Honda|Hyundai|Tata|Mahindra|Toyota|Ford|Suzuki|Hero|Bajaj|TVS|Yamaha)',
                'category': r'(2W|3W|4W|Two Wheeler|Three Wheeler|Four Wheeler|Car|Bike|Motorcycle)',
                'date': r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
                'month_year': r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{4})'
            }
            
            current_record = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Extract information using patterns
                for pattern_name, pattern in patterns.items():
                    matches = re.findall(pattern, line, re.IGNORECASE)
                    if matches:
                        if pattern_name == 'vehicle_count':
                            current_record['registrations'] = int(matches[0][0])
                        elif pattern_name == 'manufacturer':
                            current_record['manufacturer'] = matches[0]
                        elif pattern_name == 'category':
                            current_record['vehicle_category'] = self._standardize_category(matches[0])
                        elif pattern_name in ['date', 'month_year']:
                            current_record['date'] = self._parse_date(matches[0])
                
                # If we have enough information, add the record
                if len(current_record) >= 3:
                    records.append(current_record.copy())
                    current_record = {}
            
            if records:
                df = pd.DataFrame(records)
                return self._validate_and_clean_data(df)
            
            return None
            
        except Exception as e:
            print(f"Content parsing error: {str(e)}")
            return None
    
    def _create_sample_data(self) -> pd.DataFrame:
        """
        Create sample data structure that represents the expected format from Vahan Dashboard.
        This is only used when real data cannot be fetched.
        """
        try:
            # Generate dates for the last 24 months
            end_date = datetime.now()
            start_date = end_date - timedelta(days=730)
            
            date_range = pd.date_range(start=start_date, end=end_date, freq='ME')
            
            # Vehicle categories as per Vahan classification
            categories = ['2W', '3W', '4W']
            
            # Major manufacturers in Indian market
            manufacturers = {
                '2W': ['Hero MotoCorp', 'Honda Motorcycle', 'TVS Motor', 'Bajaj Auto', 'Yamaha', 'Royal Enfield'],
                '3W': ['Bajaj Auto', 'Mahindra', 'TVS Motor', 'Atul Auto', 'Piaggio'],
                '4W': ['Maruti Suzuki', 'Hyundai', 'Tata Motors', 'Mahindra', 'Honda Cars', 'Toyota']
            }
            
            records = []
            
            # Note: This creates a realistic data structure but with placeholder values
            # In a real implementation, this would only be used if actual data fetching fails
            
            for date in date_range:
                for category in categories:
                    for manufacturer in manufacturers[category]:
                        # Create record with proper structure but no actual data
                        record = {
                            'date': date,
                            'vehicle_category': category,
                            'manufacturer': manufacturer,
                            'registrations': 0,  # Placeholder - would be real data from Vahan
                            'data_source': 'placeholder'  # Mark as placeholder data
                        }
                        records.append(record)
            
            df = pd.DataFrame(records)
            return self._validate_and_clean_data(df)
            
        except Exception as e:
            print(f"Sample data creation error: {str(e)}")
            return self._create_empty_dataframe()
    
    def _create_empty_dataframe(self) -> pd.DataFrame:
        """
        Create an empty DataFrame with the correct column structure.
        """
        return pd.DataFrame(columns=['date', 'vehicle_category', 'manufacturer', 'registrations'])
    
    def _standardize_record(self, record: Dict) -> Optional[Dict]:
        """
        Standardize a record to match our expected format.
        """
        try:
            standardized = {}
            
            # Map various field names to our standard fields
            field_mappings = {
                'date': ['date', 'registration_date', 'reg_date', 'period', 'month'],
                'vehicle_category': ['vehicle_category', 'category', 'vehicle_type', 'type'],
                'manufacturer': ['manufacturer', 'make', 'brand', 'oem'],
                'registrations': ['registrations', 'count', 'total', 'reg_count', 'vehicles']
            }
            
            for standard_field, possible_fields in field_mappings.items():
                for field in possible_fields:
                    if field in record:
                        if standard_field == 'vehicle_category':
                            standardized[standard_field] = self._standardize_category(record[field])
                        elif standard_field == 'date':
                            standardized[standard_field] = self._parse_date(record[field])
                        else:
                            standardized[standard_field] = record[field]
                        break
            
            # Ensure we have minimum required fields
            required_fields = ['date', 'vehicle_category', 'registrations']
            if all(field in standardized for field in required_fields):
                return standardized
            
            return None
            
        except Exception as e:
            print(f"Record standardization error: {str(e)}")
            return None
    
    def _standardize_category(self, category: str) -> str:
        """
        Standardize vehicle category names.
        """
        category = str(category).upper().strip()
        
        if any(term in category for term in ['2W', 'TWO WHEEL', 'BIKE', 'MOTORCYCLE', 'SCOOTER']):
            return '2W'
        elif any(term in category for term in ['3W', 'THREE WHEEL', 'AUTO', 'RICKSHAW']):
            return '3W'
        elif any(term in category for term in ['4W', 'FOUR WHEEL', 'CAR', 'PASSENGER']):
            return '4W'
        else:
            return category
    
    def _parse_date(self, date_str) -> Optional[datetime]:
        """
        Parse various date formats into datetime object.
        """
        try:
            if isinstance(date_str, datetime):
                return date_str
            
            date_str = str(date_str)
            
            # Common date formats
            formats = [
                '%Y-%m-%d',
                '%d-%m-%Y',
                '%m/%d/%Y',
                '%d/%m/%Y',
                '%Y/%m/%d',
                '%b %Y',
                '%B %Y'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and clean the DataFrame.
        """
        try:
            if df.empty:
                return df
            
            # Ensure required columns exist
            required_columns = ['date', 'vehicle_category', 'registrations']
            for col in required_columns:
                if col not in df.columns:
                    if col == 'registrations':
                        df[col] = 0
                    else:
                        df[col] = 'Unknown'
            
            # Add manufacturer column if missing
            if 'manufacturer' not in df.columns:
                df['manufacturer'] = 'Unknown'
            
            # Convert data types
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['registrations'] = pd.to_numeric(df['registrations'], errors='coerce').fillna(0)
            
            # Remove rows with invalid dates
            df = df.dropna(subset=['date'])
            
            # Sort by date
            df = df.sort_values('date')
            
            # Reset index
            df = df.reset_index(drop=True)
            
            return df
            
        except Exception as e:
            print(f"Data validation error: {str(e)}")
            return pd.DataFrame(columns=['date', 'vehicle_category', 'manufacturer', 'registrations'])
