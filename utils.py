import pandas as pd
import numpy as np
from typing import Union, Optional

def format_number(num: Union[int, float]) -> str:
    """
    Format large numbers for display with appropriate suffixes.
    
    Args:
        num: Number to format
        
    Returns:
        Formatted string with K, M, B suffixes
    """
    try:
        num = float(num)
        
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return f"{int(num)}"
    except (ValueError, TypeError):
        return "0"

def calculate_growth(current: float, previous: float) -> float:
    """
    Calculate percentage growth between two values.
    
    Args:
        current: Current period value
        previous: Previous period value
        
    Returns:
        Growth percentage
    """
    try:
        if previous == 0:
            return 0.0
        return ((current - previous) / previous) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if division by zero.
    
    Args:
        numerator: Number to divide
        denominator: Number to divide by
        default: Default value if division by zero
        
    Returns:
        Division result or default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (ValueError, TypeError):
        return default

def validate_dataframe(df: pd.DataFrame, required_columns: list) -> bool:
    """
    Validate that a DataFrame has required columns and is not empty.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        True if valid, False otherwise
    """
    try:
        if df is None or df.empty:
            return False
        
        return all(col in df.columns for col in required_columns)
    except:
        return False

def get_date_range_label(start_date, end_date) -> str:
    """
    Create a human-readable date range label.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Formatted date range string
    """
    try:
        if pd.isna(start_date) or pd.isna(end_date):
            return "Date range not available"
        
        start_str = pd.to_datetime(start_date).strftime('%b %Y')
        end_str = pd.to_datetime(end_date).strftime('%b %Y')
        
        if start_str == end_str:
            return start_str
        else:
            return f"{start_str} - {end_str}"
    except:
        return "Date range not available"

def calculate_market_share(value: float, total: float) -> float:
    """
    Calculate market share percentage.
    
    Args:
        value: Individual value
        total: Total market value
        
    Returns:
        Market share percentage
    """
    return safe_divide(value, total, 0.0) * 100

def get_growth_color(growth: float) -> str:
    """
    Get color based on growth value for styling.
    
    Args:
        growth: Growth percentage
        
    Returns:
        Color string
    """
    if growth > 0:
        return "green"
    elif growth < 0:
        return "red"
    else:
        return "gray"

def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    try:
        text = str(text)
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    except:
        return ""

def clean_manufacturer_name(name: str) -> str:
    """
    Clean and standardize manufacturer names.
    
    Args:
        name: Raw manufacturer name
        
    Returns:
        Cleaned manufacturer name
    """
    try:
        name = str(name).strip()
        
        # Common standardizations
        replacements = {
            'MARUTI SUZUKI': 'Maruti Suzuki',
            'HERO MOTOCORP': 'Hero MotoCorp',
            'HONDA MOTORCYCLE': 'Honda Motorcycle',
            'BAJAJ AUTO': 'Bajaj Auto',
            'TATA MOTORS': 'Tata Motors',
            'MAHINDRA': 'Mahindra',
            'HYUNDAI': 'Hyundai',
            'TOYOTA': 'Toyota',
            'TVS MOTOR': 'TVS Motor'
        }
        
        name_upper = name.upper()
        for key, value in replacements.items():
            if key in name_upper:
                return value
        
        # Title case for other names
        return name.title()
    except:
        return str(name)

def calculate_compound_growth_rate(start_value: float, end_value: float, periods: int) -> float:
    """
    Calculate compound annual growth rate (CAGR).
    
    Args:
        start_value: Starting value
        end_value: Ending value
        periods: Number of periods
        
    Returns:
        CAGR percentage
    """
    try:
        if start_value <= 0 or end_value <= 0 or periods <= 0:
            return 0.0
        
        cagr = (pow(end_value / start_value, 1.0 / periods) - 1) * 100
        return cagr
    except:
        return 0.0

def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a number as a percentage string.
    
    Args:
        value: Percentage value
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    try:
        return f"{value:.{decimals}f}%"
    except:
        return "0.0%"

def get_quarter_from_date(date) -> str:
    """
    Get quarter string from date.
    
    Args:
        date: Date object
        
    Returns:
        Quarter string (e.g., "2024-Q1")
    """
    try:
        dt = pd.to_datetime(date)
        year = dt.year
        quarter = (dt.month - 1) // 3 + 1
        return f"{year}-Q{quarter}"
    except:
        return "Unknown"

def calculate_moving_average(series: pd.Series, window: int = 3) -> pd.Series:
    """
    Calculate moving average for a series.
    
    Args:
        series: Pandas Series
        window: Moving average window
        
    Returns:
        Moving average series
    """
    try:
        return series.rolling(window=window, min_periods=1).mean()
    except:
        return series

def detect_outliers(series: pd.Series, threshold: float = 2.0) -> pd.Series:
    """
    Detect outliers using z-score method.
    
    Args:
        series: Pandas Series
        threshold: Z-score threshold
        
    Returns:
        Boolean series indicating outliers
    """
    try:
        z_scores = np.abs((series - series.mean()) / series.std())
        return z_scores > threshold
    except:
        return pd.Series([False] * len(series))
