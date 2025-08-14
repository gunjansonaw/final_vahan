"""
API Information and Configuration for Vahan Dashboard Integration

This module provides comprehensive information about available API endpoints
for accessing vehicle registration data from official and authorized sources.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List

class APIInfo:
    """
    Information about available Vahan data API providers and endpoints.
    """
    
    @staticmethod
    def get_api_providers() -> Dict[str, Dict]:
        """
        Return information about available API providers.
        """
        return {
            "masters_india": {
                "name": "Masters India APIs",
                "description": "Official Vahan data access through government integration",
                "features": [
                    "Vehicle Detail API (RC)",
                    "Insurance verification",
                    "Permit status checking",
                    "Blacklist verification"
                ],
                "pricing": "Credit-based pricing",
                "documentation": "https://docs.mastersindia.co/masters-india-apis/proof-of-delivery-pod-api/vahan-api-vehicle-detail-api-rc",
                "endpoints": {
                    "vehicle_detail": "https://api.mastersindia.co/vahan/vehicle-detail",
                    "bulk_analytics": "https://api.mastersindia.co/bulk/vehicle-statistics"
                },
                "auth_method": "JWT Bearer Token",
                "response_format": "JSON",
                "rate_limits": "Varies by plan"
            },
            
            "surepass": {
                "name": "Surepass Vehicle APIs",
                "description": "Real-time vehicle verification and analytics",
                "features": [
                    "RC Verification API",
                    "Insurance Verification",
                    "Stolen Vehicle Check",
                    "Vehicle Tracking",
                    "FASTag Verification"
                ],
                "pricing": "Pay-per-use or subscription",
                "documentation": "https://surepass.io/vahan-verification-api/",
                "endpoints": {
                    "rc_verification": "https://kyc-api.surepass.io/api/v1/vehicle-rc-verification",
                    "bulk_analytics": "https://kyc-api.surepass.io/api/v1/vehicle/bulk-analytics"
                },
                "auth_method": "API Key",
                "response_format": "JSON",
                "rate_limits": "99.99% uptime, 1-3 second response"
            },
            
            "hyperverge": {
                "name": "HyperVerge Vahan API",
                "description": "AI-powered vehicle verification",
                "features": [
                    "Chassis number verification",
                    "Owner details",
                    "Insurance information",
                    "Fuel type data"
                ],
                "pricing": "Enterprise pricing",
                "documentation": "https://hyperverge.co/in/integrations-marketplace/vahan-api/",
                "endpoints": {
                    "verify": "https://api.hyperverge.co/v1/vahan/verify"
                },
                "auth_method": "API Key",
                "response_format": "JSON",
                "rate_limits": "Less than 1 week integration"
            },
            
            "scriza": {
                "name": "Scriza Vehicle RC API",
                "description": "Advanced vehicle verification with 99.97% accuracy",
                "features": [
                    "RC verification",
                    "Real-time processing",
                    "AI-based validation"
                ],
                "pricing": "Credit-based",
                "documentation": "https://www.scriza.in/vehicle-rc-verification",
                "endpoints": {
                    "rc_verify": "https://api.scriza.in/vehicle/rc-verify"
                },
                "auth_method": "API Key",
                "response_format": "JSON",
                "rate_limits": "Under 30 seconds response"
            }
        }
    
    @staticmethod
    def get_sample_requests() -> Dict[str, Dict]:
        """
        Return sample API request formats for each provider.
        """
        return {
            "masters_india": {
                "individual_vehicle": {
                    "url": "https://api.mastersindia.co/vahan/vehicle-detail",
                    "method": "POST",
                    "headers": {
                        "Authorization": "Bearer YOUR_JWT_TOKEN",
                        "Content-Type": "application/json"
                    },
                    "payload": {
                        "vehiclenumber": "KA05ML1234"
                    }
                },
                "bulk_analytics": {
                    "url": "https://api.mastersindia.co/bulk/vehicle-statistics",
                    "method": "POST", 
                    "headers": {
                        "Authorization": "Bearer YOUR_JWT_TOKEN",
                        "Content-Type": "application/json"
                    },
                    "payload": {
                        "type": "registration_analytics",
                        "period": "monthly",
                        "states": ["DL", "MH", "KA"],
                        "vehicle_types": ["2W", "3W", "4W"],
                        "start_date": "2023-01-01",
                        "end_date": "2024-12-31"
                    }
                }
            },
            
            "surepass": {
                "rc_verification": {
                    "url": "https://kyc-api.surepass.io/api/v1/vehicle-rc-verification",
                    "method": "POST",
                    "headers": {
                        "Authorization": "Bearer YOUR_API_KEY",
                        "Content-Type": "application/json"
                    },
                    "payload": {
                        "rc_number": "KA05ML1234"
                    }
                },
                "bulk_analytics": {
                    "url": "https://kyc-api.surepass.io/api/v1/vehicle/bulk-analytics",
                    "method": "POST",
                    "headers": {
                        "Authorization": "Bearer YOUR_API_KEY",
                        "Content-Type": "application/json"
                    },
                    "payload": {
                        "analytics_type": "registration_trends",
                        "timeframe": "monthly",
                        "categories": ["2W", "3W", "4W"],
                        "manufacturers": True,
                        "geographic_scope": "national"
                    }
                }
            }
        }
    
    @staticmethod
    def get_environment_setup() -> Dict[str, str]:
        """
        Return environment variable setup instructions.
        """
        return {
            "MASTERS_INDIA_API_KEY": "Your Masters India JWT token",
            "SUREPASS_API_KEY": "Your Surepass API key",
            "HYPERVERGE_API_KEY": "Your HyperVerge API key",
            "SCRIZA_API_KEY": "Your Scriza API key",
            "VAHAN_API_KEY": "Generic API key (will try all providers)"
        }
    
    @staticmethod
    def display_api_info():
        """
        Display comprehensive API information in Streamlit.
        """
        st.subheader("🔌 API Integration Information")
        
        st.markdown("""
        **Connect to Real Vehicle Registration Data**
        
        This dashboard is designed to integrate with official Vahan data sources. 
        To access real vehicle registration data for investment analysis, you need API credentials from authorized providers.
        """)
        
        # Provider comparison
        st.subheader("📊 Available API Providers")
        
        providers = APIInfo.get_api_providers()
        
        # Create comparison table
        comparison_data = []
        for provider_id, info in providers.items():
            comparison_data.append({
                "Provider": info["name"],
                "Features": len(info["features"]),
                "Auth Method": info["auth_method"],
                "Response Time": info["rate_limits"],
                "Documentation": f"[Link]({info['documentation']})"
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Detailed provider information
        st.subheader("🔧 Provider Details")
        
        selected_provider = st.selectbox(
            "Select a provider for detailed information:",
            options=list(providers.keys()),
            format_func=lambda x: providers[x]["name"]
        )
        
        if selected_provider:
            provider_info = providers[selected_provider]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{provider_info['name']}**")
                st.write(provider_info["description"])
                
                st.write("**Features:**")
                for feature in provider_info["features"]:
                    st.write(f"• {feature}")
            
            with col2:
                st.write("**Technical Details:**")
                st.write(f"• **Auth Method:** {provider_info['auth_method']}")
                st.write(f"• **Response Format:** {provider_info['response_format']}")
                st.write(f"• **Pricing:** {provider_info['pricing']}")
                st.write(f"• **Performance:** {provider_info['rate_limits']}")
                
                st.write(f"**Documentation:** [View Docs]({provider_info['documentation']})")
        
        # Sample code
        st.subheader("💻 Sample Integration Code")
        
        sample_requests = APIInfo.get_sample_requests()
        
        if selected_provider in sample_requests:
            provider_samples = sample_requests[selected_provider]
            
            for api_type, sample in provider_samples.items():
                st.write(f"**{api_type.replace('_', ' ').title()}**")
                
                code_sample = f"""
import requests

# {api_type.replace('_', ' ').title()} Request
url = "{sample['url']}"
headers = {sample['headers']}
payload = {sample['payload']}

response = requests.{sample['method'].lower()}(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    print("Success:", data)
else:
    print("Error:", response.status_code, response.text)
"""
                
                st.code(code_sample, language="python")
        
        # Environment setup
        st.subheader("⚙️ Environment Setup")
        
        st.markdown("""
        **To connect this dashboard to real data sources:**
        
        1. **Choose an API provider** from the list above
        2. **Sign up** for an account with your chosen provider
        3. **Get your API credentials** (API key or JWT token)
        4. **Add your credentials** to the environment variables
        """)
        
        env_vars = APIInfo.get_environment_setup()
        
        st.write("**Required Environment Variables:**")
        for var_name, description in env_vars.items():
            st.code(f"{var_name}={description}")
        
        st.info("""
        💡 **Tip:** Once you add your API credentials, the dashboard will automatically 
        connect to the real Vahan database and display actual vehicle registration analytics.
        """)
        
        # Cost estimation
        st.subheader("💰 Cost Estimation")
        
        st.markdown("""
        **Typical API Costs:**
        
        • **Individual Vehicle Lookup:** ₹0.50 - ₹2.00 per query
        • **Bulk Analytics Data:** ₹500 - ₹2,000 per month (depending on volume)
        • **Enterprise Plans:** ₹5,000+ per month with unlimited queries
        
        **For Investment Analysis:** Bulk analytics plans are recommended for continuous 
        monitoring of vehicle registration trends and market analysis.
        """)

def show_connection_status():
    """
    Show current API connection status.
    """
    import os
    
    st.subheader("🔗 Connection Status")
    
    env_vars = APIInfo.get_environment_setup()
    
    for var_name, description in env_vars.items():
        api_key = os.getenv(var_name)
        if api_key:
            st.success(f"✅ {var_name}: Connected")
        else:
            st.warning(f"⚠️ {var_name}: Not configured")
    
    # Check if any API key is available
    any_key_available = any(os.getenv(var) for var in env_vars.keys())
    
    if any_key_available:
        st.info("🚀 API credentials detected! The dashboard will attempt to fetch real data.")
    else:
        st.error("❌ No API credentials found. The dashboard will use sample data structure only.")
        
        st.markdown("""
        **To connect to real data:**
        1. Get API credentials from any provider listed above
        2. Add them to your environment variables
        3. Restart the application
        """)