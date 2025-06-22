import streamlit as st
import requests
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="📈 Stock Analyzer Pro",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling with glassmorphism and gradients
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-bg: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --card-bg: rgba(255, 255, 255, 0.1);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --text-primary: #ffffff;
        --text-secondary: #e2e8f0;
        --accent-color: #fbbf24;
        --accent-hover: #f59e0b;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --border-radius: 16px;
        --shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        --shadow-hover: 0 12px 48px rgba(0, 0, 0, 0.15);
    }
    
    /* Main app container */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* App view container */
    [data-testid="stAppViewContainer"] {
        background: transparent;
        padding: 1rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(145deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: var(--border-radius);
        margin: 1rem;
        padding: 1rem;
        box-shadow: var(--shadow);
    }
    
    /* Sidebar toggle button */
    .sidebar-toggle {
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 1000;
        background: linear-gradient(45deg, var(--accent-color), var(--accent-hover));
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow);
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1.2rem;
    }
    
    .sidebar-toggle:hover {
        transform: scale(1.1);
        box-shadow: var(--shadow-hover);
    }
    
    /* Enhanced company card */
    .company-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(25px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .company-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-color), #667eea, #764ba2);
    }
    
    .company-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 80px rgba(0,0,0,0.2);
        border-color: rgba(255,255,255,0.3);
    }
    
    .company-logo {
        width: 120px;
        height: 120px;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .company-logo:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }
    
    .company-logo img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .company-logo-placeholder {
        width: 120px;
        height: 120px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .company-title {
        font-size: 3rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        background: linear-gradient(45deg, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }
    
    .company-subtitle {
        font-size: 1.3rem;
        color: var(--accent-color);
        font-weight: 600;
        margin: 0 0 2rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .company-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .detail-item {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.2rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .detail-item:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }
    
    .detail-label {
        font-weight: 600;
        color: var(--accent-color);
        margin-bottom: 0.3rem;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .detail-value {
        font-size: 1.1rem;
        color: var(--text-primary);
        font-weight: 500;
    }
    
    /* Enhanced buttons */
    [data-testid="stButton"] button {
        background: linear-gradient(45deg, var(--accent-color), var(--accent-hover));
        color: #1a1a2e;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(251, 191, 36, 0.4);
        background: linear-gradient(45deg, var(--accent-hover), var(--accent-color));
    }
    
    /* Modern metrics */
    [data-testid="metric-container"] {
        background: var(--glass-bg);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
        border-color: rgba(255,255,255,0.2);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Input fields */
    [data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 12px;
        color: var(--text-primary);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTextInput"] input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.1);
        outline: none;
    }
    
    /* Multiselect styling */
    [data-testid="stMultiSelect"] {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 0.5rem;
    }
    
    /* Expander styling */
    [data-testid="stExpander"] {
        background: var(--glass-bg);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: var(--border-radius);
        backdrop-filter: blur(20px);
        box-shadow: var(--shadow);
        margin: 1rem 0;
    }
    
    /* Chart container */
    [data-testid="stLineChart"] {
        background: rgba(255,255,255,0.02);
        border-radius: var(--border-radius);
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* News cards */
    .news-card {
        background: var(--glass-bg);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .news-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
        border-color: rgba(255,255,255,0.2);
    }
    
    /* Links */
    a {
        color: var(--accent-color);
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    a:hover {
        color: var(--accent-hover);
        text-shadow: 0 0 8px rgba(251, 191, 36, 0.3);
    }
    
    /* Section headers */
    .section-header {
        text-align: center;
        margin: 4rem 0 2rem 0;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(45deg, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Section dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 3rem 0;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, var(--accent-color), var(--accent-hover));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-hover);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .company-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .company-title {
            font-size: 2rem;
        }
        
        .company-details {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add sidebar toggle functionality
st.markdown("""
<script>
function toggleSidebar() {
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        if (sidebar.style.display === 'none') {
            sidebar.style.display = 'block';
        } else {
            sidebar.style.display = 'none';
        }
    }
}
</script>
""", unsafe_allow_html=True)

# Sidebar toggle button
if st.button("☰", help="Toggle Sidebar"):
    st.rerun()

# Enhanced sidebar with modern styling
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 1.8rem; margin: 0; background: linear-gradient(45deg, #fbbf24, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🔍 Stock Lookup
    </h1>
    <p style="color: #e2e8f0; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        Analyze any stock with real-time data
    </p>
</div>
""", unsafe_allow_html=True)

ticker = st.sidebar.text_input("Enter ticker symbol", "AAPL", help="Type any stock symbol (e.g., AAPL, GOOGL, TSLA)").upper()
api_url = st.sidebar.text_input("API URL", "http://localhost:8000/analyze", help="Your backend API endpoint")

# Initialize session_state
if "data" not in st.session_state:
    st.session_state.data = None
if "error" not in st.session_state:
    st.session_state.error = None

# Enhanced fetch button with loading state
if st.sidebar.button("🚀 Run Analysis", help="Fetch and analyze the stock data"):
    with st.sidebar:
        with st.spinner("Fetching data..."):
            st.session_state.error = None
            try:
                r = requests.post(api_url, json={"ticker": ticker})
                r.raise_for_status()
                st.session_state.data = r.json()
                st.success("✅ Data loaded successfully!")
            except Exception as e:
                st.session_state.error = str(e)
                st.session_state.data = None

# Show any fetch error with enhanced styling
if st.session_state.error:
    st.sidebar.error(f"❌ API error: {st.session_state.error}")

# Main content area
if st.session_state.data:
    data = st.session_state.data
    
    # Modern header with gradient background
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <h1 style="font-size: 3.5rem; margin: 0; background: linear-gradient(45deg, #667eea, #764ba2, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">
            📈 Stock Analyzer Pro
        </h1>
        <p style="color: #e2e8f0; font-size: 1.2rem; margin: 1rem 0 0 0;">
            Advanced stock analysis with real-time insights
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced Company Profile Card
    profile = data["company_data"]["profile"]
    
    st.markdown('<div class="company-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if logo := profile.get("logo"):
            st.markdown(f'''
            <div class="company-logo">
                <img src="{logo}" alt="{profile['name']} logo">
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="company-logo-placeholder">
                📊
            </div>
            ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div class="company-title">{profile['name']}</div>
        <div class="company-subtitle">{profile['ticker']} • {profile['exchange']} - GLOBAL MARKET</div>
        
        <div class="company-details">
            <div class="detail-item">
                <div class="detail-label">🏭 Industry</div>
                <div class="detail-value">{profile['finnhubIndustry']}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">💰 Market Cap</div>
                <div class="detail-value">${profile['marketCapitalization']:,}M</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">🌍 Country</div>
                <div class="detail-value">{profile.get('country','—')}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">💱 Currency</div>
                <div class="detail-value">{profile.get('currency','—')}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">📅 IPO Date</div>
                <div class="detail-value">{profile.get('ipo','—')}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">🌐 Website</div>
                <div class="detail-value">
                    <a href="{profile.get('weburl','')}" target="_blank">{profile.get('weburl','—')}</a>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Price data with enhanced metrics display
    sd = data["stock_data"]
    
    st.markdown('<div class="section-header">💹 Live Market Data</div>', unsafe_allow_html=True)

    # Row 1: Core price metrics
    r1 = st.columns(6)
    with r1[0]:
        st.metric("🟢 Open", f"${sd['open']:.2f}")
    with r1[1]:
        st.metric("🔺 Day High", f"${sd['dayHigh']:.2f}")
    with r1[2]:
        st.metric("🔻 Day Low", f"${sd['dayLow']:.2f}")
    with r1[3]:
        st.metric("🔵 Close", f"${sd['close']:.2f}")
    with r1[4]:
        change = sd['close'] - sd['previousClose']
        st.metric("🔄 Prev Close", f"${sd['previousClose']:.2f}", delta=f"{change:.2f}")
    with r1[5]:
        st.metric("⚫ Last Price", f"${sd['lastPrice']:.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Volume and market metrics
    r2 = st.columns(7)
    with r2[0]:
        st.metric("📊 Volume", f"{sd['volume']:,}")
    with r2[1]:
        st.metric("🔁 Last Volume", f"{sd['lastVolume']:,}")
    with r2[2]:
        st.metric("💼 Shares Outstanding", f"{sd['shares']:,}")
    with r2[3]:
        st.metric("💰 Market Cap", f"${sd['marketCap']:,}")
    with r2[4]:
        st.metric("📈 52W High", f"${sd['yearHigh']:.2f}")
    with r2[5]:
        st.metric("📉 52W Low", f"${sd['yearLow']:.2f}")
    with r2[6]:
        st.metric("⏳ Year Change", f"{sd['yearChange']:.2%}")

    # Technical indicators with enhanced chart
    td = pd.DataFrame(data["technical_data"])
    td["datetime"] = pd.to_datetime(td["datetime"])
    td.set_index("datetime", inplace=True)

    st.markdown('<div class="section-header">📊 Technical Analysis</div>', unsafe_allow_html=True)

    with st.expander("### 🔍 Technical Indicators Dashboard", expanded=True):
        all_inds = td.columns.tolist()
        
        col_filter, col_info = st.columns([3, 1])
        with col_filter:
            sel = st.multiselect(
                "Select indicators to display",
                options=all_inds,
                default=["ema", "sma", "rsi"],
                help="Choose technical indicators to visualize on the chart"
            )
        
        with col_info:
            st.markdown("""
            *📚 Indicators:*
            - *EMA*: Exponential Moving Average
            - *SMA*: Simple Moving Average  
            - *RSI*: Relative Strength Index
            """)
        
        if not sel:
            st.warning("⚠️ Please select at least one indicator to display the chart.")
        else:
            # Keep the original chart functionality
            st.line_chart(
                td[sel],
                use_container_width=True,
                height=400,
            )

    # News section with modern cards
    st.markdown('<div class="section-header">📰 Latest Market News</div>', unsafe_allow_html=True)
    
    for i, itm in enumerate(data["news_data"][:5]):
        dt = datetime.fromtimestamp(itm["datetime"]).strftime("%Y-%m-%d %H:%M")
        
        st.markdown(f"""
        <div class="news-card">
            <h4 style="margin: 0 0 0.5rem 0; color: #fbbf24;">
                <a href="{itm['url']}" target="_blank">{itm['headline']}</a>
            </h4>
            <p style="color: #94a3b8; font-size: 0.9rem; margin: 0 0 1rem 0;">
                📅 {dt} • 📰 {itm['source']}
            </p>
            <p style="margin: 0; line-height: 1.6;">
                {itm['summary']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Summary analysis with enhanced styling
    st.markdown('<div class="section-header">📋 AI-Powered Analysis</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(251,191,36,0.1) 0%, rgba(245,158,11,0.1) 100%); 
                border: 1px solid rgba(251,191,36,0.3); border-radius: 16px; padding: 2rem; 
                backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
        <div style="font-size: 1.1rem; line-height: 1.8; color: #e2e8f0;">
            {data["final_summary"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # — Full financials in collapsible section (now “Company Fundamental Data”)
    with st.expander("🔍 Company Fundamental Data", expanded=False):
        financials = data["company_data"]["financials"]
        for section_title, metrics in financials.items():
            # Section heading
            st.markdown(f"### {section_title}")
            
            # Convert the inner dict to a single-column DataFrame
            df = pd.DataFrame.from_dict(metrics, orient="index", columns=["Value"])
            df.index.name = None
            # Display as a table
            st.table(df)

else:
    # Welcome screen when no data is loaded
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <h1 style="font-size: 4rem; margin: 0; background: linear-gradient(45deg, #667eea, #764ba2, #fbbf24); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">
            📈 Stock Analyzer Pro
        </h1>
        <p style="color: #e2e8f0; font-size: 1.3rem; margin: 2rem 0; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.6;">
            Welcome to the most advanced stock analysis platform. Get real-time data, technical indicators, 
            and AI-powered insights for any publicly traded stock.
        </p>
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); 
                    border: 1px solid rgba(255,255,255,0.2); border-radius: 24px; padding: 3rem; 
                    margin: 3rem auto; max-width: 800px; backdrop-filter: blur(20px);">
            <h3 style="color: #fbbf24; margin-bottom: 2rem;">✨ Features</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; text-align: left;">
                <div>
                    <h4 style="color: #fbbf24; margin-bottom: 1rem;">📊 Real-time Data</h4>
                    <p style="color: #e2e8f0;">Live stock prices, volume, and market metrics updated in real-time.</p>
                </div>
                <div>
                    <h4 style="color: #fbbf24; margin-bottom: 1rem;">📈 Technical Analysis</h4>
                    <p style="color: #e2e8f0;">Advanced indicators including EMA, SMA, RSI and more.</p>
                </div>
                <div>
                    <h4 style="color: #fbbf24; margin-bottom: 1rem;">📰 Market News</h4>
                    <p style="color: #e2e8f0;">Latest news and updates affecting your stock picks.</p>
                </div>
                <div>
                    <h4 style="color: #fbbf24; margin-bottom: 1rem;">🤖 AI Insights</h4>
                    <p style="color: #e2e8f0;">AI-powered analysis and recommendations for informed decisions.</p>
                </div>
            </div>
        </div>
        <p style="color: #94a3b8; font-size: 1.1rem; margin-top: 3rem;">
            👈 Enter a stock ticker in the sidebar to get started
        </p>
    </div>
    """, unsafe_allow_html=True)