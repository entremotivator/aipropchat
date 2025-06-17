import streamlit as st
import openai
from openai import OpenAI
from datetime import datetime
import requests
import pandas as pd
import json

# ------------------ Streamlit Config ------------------
st.set_page_config(
    page_title="AI Prop Chat", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ Custom CSS ------------------
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ Session State Initialization ------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "property_data" not in st.session_state:
    st.session_state.property_data = None

# ------------------ Authentication ------------------
def authenticate():
    with st.sidebar.expander("🔐 Login", expanded=not st.session_state.authenticated):
        if not st.session_state.authenticated:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Login")
                if login_button:
                    if username == "admin" and password == "password":  # Replace with real auth
                        st.session_state.authenticated = True
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
        else:
            st.success("✅ Logged in as admin")
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()

# ------------------ API Configuration ------------------
def setup_apis():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 API Configuration")
    
    api_key = st.sidebar.text_input(
        "OpenAI API Key", 
        type="password",
        help="Required for AI chat functionality"
    )
    
    rentcast_key = st.sidebar.text_input(
        "RentCast API Key", 
        type="password",
        help="Required for property data lookup"
    )
    
    st.sidebar.markdown("ℹ️ *Keys are secure and not stored*")
    return api_key, rentcast_key

# ------------------ Property Lookup Function ------------------
def fetch_property_data(address, api_key):
    """Fetch property data from RentCast API"""
    try:
        response = requests.get(
            "https://api.rentcast.io/v1/properties",
            params={"address": address},
            headers={"X-Api-Key": api_key},
            timeout=10
        )
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code}"
    except Exception as e:
        return None, f"Request failed: {str(e)}"

# ------------------ AI Chat Function ------------------
def get_ai_response(prompt, api_key, property_context=None):
    """Get response from OpenAI"""
    try:
        client = OpenAI(api_key=api_key)
        
        system_message = """You are AI Prop Chat, an expert real estate investment assistant. 
        Help users analyze properties, calculate ROI, estimate ARV, provide market insights, 
        and explain real estate concepts clearly. Be concise but thorough."""
        
        if property_context:
            system_message += f"\n\nCurrent property context: {json.dumps(property_context, indent=2)}"
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# ------------------ Main App ------------------
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏡 AI Prop Chat</h1>
        <p>Intelligent Real Estate Analysis Platform</p>
        <p><em>Your AI-powered property investment assistant</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Authentication
    authenticate()
    
    if not st.session_state.authenticated:
        st.warning("🔐 Please login to access the full platform")
        return
    
    # API Setup
    openai_key, rentcast_key = setup_apis()
    
    # Main Content Layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🏠 Property Lookup & Analysis")
        
        # Property Address Input
        address = st.text_input(
            "Enter Property Address",
            placeholder="123 Main St, Atlanta, GA 30309",
            help="Enter full address for best results"
        )
        
        # Lookup Button
        if st.button("🔍 Analyze Property", type="primary") and address and rentcast_key:
            with st.spinner("Fetching property data..."):
                prop_data, error = fetch_property_data(address, rentcast_key)
                
                if prop_data:
                    st.session_state.property_data = prop_data
                    st.success("✅ Property data retrieved!")
                else:
                    st.error(f"❌ {error}")
        
        # Display Property Data
        if st.session_state.property_data:
            st.markdown("### 📊 Property Details")
            
            data = st.session_state.property_data
            
            # Key metrics in columns
            if isinstance(data, list) and len(data) > 0:
                prop = data[0]
            else:
                prop = data
            
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric(
                    "Estimated Value",
                    f"${prop.get('propertyValue', 'N/A'):,}" if isinstance(prop.get('propertyValue'), (int, float)) else "N/A"
                )
            
            with metric_col2:
                st.metric(
                    "Bedrooms",
                    prop.get('bedrooms', 'N/A')
                )
            
            with metric_col3:
                st.metric(
                    "Bathrooms",
                    prop.get('bathrooms', 'N/A')
                )
            
            # Detailed information
            with st.expander("📋 Detailed Property Information"):
                st.json(prop)
            
            # Export option
            if st.button("📥 Export Property Data"):
                df = pd.json_normalize([prop])
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    f"property_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
    
    with col2:
        st.subheader("🤖 AI Property Assistant")
        
        # Chat Interface
        chat_container = st.container()
        
        with chat_container:
            # Display chat history
            for role, message in st.session_state.chat_history[-6:]:  # Show last 6 messages
                with st.chat_message("user" if role == "user" else "assistant"):
                    st.markdown(message)
        
        # Chat input
        user_input = st.chat_input("Ask about properties, investments, or real estate strategies...")
        
        if user_input and openai_key:
            # Add user message to history
            st.session_state.chat_history.append(("user", user_input))
            
            # Get AI response
            with st.spinner("AI is thinking..."):
                ai_response = get_ai_response(
                    user_input, 
                    openai_key, 
                    st.session_state.property_data
                )
                st.session_state.chat_history.append(("ai", ai_response))
            
            st.rerun()
        
        # Quick action buttons
        st.markdown("### ⚡ Quick Actions")
        
        quick_col1, quick_col2 = st.columns(2)
        
        with quick_col1:
            if st.button("💰 Calculate ROI") and openai_key:
                if st.session_state.property_data:
                    prompt = "Calculate potential ROI for this property assuming different investment strategies (fix & flip, rental, wholesale)"
                    response = get_ai_response(prompt, openai_key, st.session_state.property_data)
                    st.session_state.chat_history.append(("user", "Calculate ROI"))
                    st.session_state.chat_history.append(("ai", response))
                    st.rerun()
                else:
                    st.warning("Please lookup a property first")
        
        with quick_col2:
            if st.button("🏘️ Market Analysis") and openai_key:
                if address:
                    prompt = f"Provide market analysis for properties in the area of {address}"
                    response = get_ai_response(prompt, openai_key)
                    st.session_state.chat_history.append(("user", "Market Analysis"))
                    st.session_state.chat_history.append(("ai", response))
                    st.rerun()
                else:
                    st.warning("Please enter an address first")
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Bulk Upload Section
    st.markdown("---")
    st.subheader("📤 Bulk Property Analysis")
    
    uploaded_file = st.file_uploader(
        "Upload CSV with property addresses",
        type=["csv"],
        help="CSV should have addresses in the first column"
    )
    
    if uploaded_file and rentcast_key:
        df = pd.read_csv(uploaded_file)
        st.write("📋 Uploaded Properties:", df.head())
        
        if st.button("🚀 Analyze All Properties"):
            progress_bar = st.progress(0)
            results = []
            
            for idx, row in df.iterrows():
                address = str(row.iloc[0])  # First column
                prop_data, error = fetch_property_data(address, rentcast_key)
                
                if prop_data:
                    if isinstance(prop_data, list) and len(prop_data) > 0:
                        results.append(prop_data[0])
                    else:
                        results.append(prop_data)
                
                progress_bar.progress((idx + 1) / len(df))
            
            if results:
                st.success(f"✅ Analyzed {len(results)} properties")
                results_df = pd.json_normalize(results)
                st.dataframe(results_df)
                
                csv_data = results_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Results",
                    csv_data,
                    f"bulk_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )

# ------------------ Footer ------------------
def footer():
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>© {datetime.now().year} AI Prop Chat - Powered by AI for Real Estate Professionals</p>
        <p>
            <a href="https://vipbusinesscredit.com" target="_blank">🌐 Website</a> | 
            <a href="mailto:support@aipropchat.com">📧 Support</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ------------------ Run App ------------------
if __name__ == "__main__":
    main()
    footer()
