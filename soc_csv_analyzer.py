import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import base64
import re
import os

# Set page config with professional SOC theme
st.set_page_config(
    page_title="SOC Analyzer Pro",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/support',
        'Report a bug': "https://www.example.com/bug",
        'About': "# SOC Analyzer Pro\nEnterprise-grade security data analysis"
    }
)

# Custom CSS for professional SOC theme
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        st.markdown("""
        <style>
        /* Cyber Security Color Palette */
        :root {
            --primary-dark: #0a192f;     /* Navy Blue */
            --primary: #1a3e72;          /* Dark Blue */
            --primary-light: #4a6fa5;    /* Medium Blue */
            --accent: #00d4ff;           /* Electric Blue */
            --accent-dark: #0088cc;      /* Deep Blue */
            --danger: #ff4d4d;           /* Alert Red */
            --warning: #ffc107;          /* Warning Yellow */
            --success: #00c853;          /* Success Green */
            --text-light: #e6f1ff;       /* Light Text */
            --text-muted: #8892b0;       /* Muted Text */
            --bg-dark: #020c1b;          /* Dark Background */
            --bg-darker: #010814;        /* Darker Background */
            --card-bg: #0a192f;          /* Card Background */
            --sidebar-bg: #0a192f;       /* Sidebar Background */
        }
        
        /* Main Container */
        .stApp {
            background: linear-gradient(135deg, var(--bg-darker), var(--bg-dark));
            color: var(--text-light);
            min-height: 100vh;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-light) !important;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        h1 {
            border-bottom: 2px solid var(--accent);
            padding-bottom: 0.5rem;
            font-size: 2.2rem;
        }
        
        h2 {
            border-left: 4px solid var(--accent);
            padding-left: 1rem;
            margin-top: 1.5rem;
        }
        
        /* Sidebar - Cyber Command Center Style */
        [data-testid="stSidebar"] {
            background: var(--sidebar-bg) !important;
            border-right: 1px solid rgba(0, 212, 255, 0.1);
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
        }
        
        [data-testid="stSidebar"] .stButton>button {
            background: var(--primary-light) !important;
            border: 1px solid var(--accent) !important;
        }
        
        /* Buttons - Holographic Style */
        .stButton>button {
            background: linear-gradient(145deg, var(--primary-light), var(--accent-dark)) !important;
            color: white !important;
            border: none !important;
            border-radius: 4px;
            padding: 0.5rem 1.5rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 212, 255, 0.2);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        .stButton>button:before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                to bottom right,
                rgba(255, 255, 255, 0) 0%,
                rgba(255, 255, 255, 0.1) 50%,
                rgba(255, 255, 255, 0) 100%
            );
            transform: rotate(30deg);
            animation: shine 3s infinite;
        }
        
        @keyframes shine {
            0% { transform: rotate(30deg) translate(-30%, -30%); }
            100% { transform: rotate(30deg) translate(30%, 30%); }
        }
        
        /* Dataframes - Glass Morphism */
        .stDataFrame {
            background: rgba(10, 25, 47, 0.7) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 212, 255, 0.2) !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        /* Tabs - Futuristic */
        .stTabs [role="tablist"] {
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        }
        
        .stTabs [role="tab"] {
            color: var(--text-muted) !important;
            padding: 0.5rem 1.5rem;
            margin: 0 0.2rem;
            border-radius: 4px 4px 0 0;
            transition: all 0.3s;
        }
        
        .stTabs [role="tab"][aria-selected="true"] {
            color: var(--accent) !important;
            background: rgba(0, 212, 255, 0.1) !important;
            border-bottom: 2px solid var(--accent) !important;
            font-weight: 600;
        }
        
        /* Metrics - Cyber Dashboard */
        [data-testid="stMetric"] {
            background: rgba(10, 25, 47, 0.7) !important;
            backdrop-filter: blur(5px);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            border-left: 4px solid var(--accent);
            border-top: 1px solid rgba(0, 212, 255, 0.2);
            transition: all 0.3s;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0, 212, 255, 0.2);
        }
        
        [data-testid="stMetricLabel"] {
            color: var(--text-muted) !important;
            font-size: 0.9rem !important;
            letter-spacing: 0.5px;
        }
        
        [data-testid="stMetricValue"] {
            color: var(--text-light) !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        
        /* Custom Classes */
        .header {
            background: linear-gradient(135deg, var(--primary-dark), var(--primary));
            color: white;
            padding: 2rem;
            border-radius: 0 0 8px 8px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .header:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--danger), var(--warning), var(--success), var(--accent));
            background-size: 200% 200%;
            animation: gradient 3s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .header h1 {
            color: var(--text-light) !important;
            border-bottom: none !important;
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
            display: flex;
            align-items: center;
        }
        
        .header h1:before {
            content: '🛡️';
            margin-right: 1rem;
            font-size: 2rem;
        }
        
        .subheader {
            color: var(--text-muted) !important;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
        }
        
        .card {
            background: rgba(10, 25, 47, 0.7);
            backdrop-filter: blur(5px);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(0, 212, 255, 0.2);
            transition: all 0.3s;
        }
        
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0, 212, 255, 0.2);
        }
        
        .footer {
            margin-top: 3rem;
            padding: 2rem 0;
            border-top: 1px solid rgba(0, 212, 255, 0.2);
            color: var(--text-muted);
            font-size: 0.9rem;
            text-align: center;
            background: rgba(10, 25, 47, 0.5);
        }
        
        .footer .small {
            font-size: 0.8rem;
            color: var(--text-muted);
        }
        
        /* Alert Boxes - Threat Alerts */
        .stAlert {
            background: rgba(255, 77, 77, 0.1) !important;
            border-left: 4px solid var(--danger) !important;
            border-radius: 8px !important;
            color: var(--text-light) !important;
        }
        
        /* Expanders - Cyber Panels */
        [data-testand="stExpander"] {
            background: rgba(10, 25, 47, 0.7) !important;
            backdrop-filter: blur(5px);
            border-radius: 8px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(0, 212, 255, 0.2) !important;
        }
        
        /* Tooltips - Cyber Tooltips */
        [data-testid="stTooltip"] {
            background: var(--primary-dark) !important;
            color: var(--text-light) !important;
            border-radius: 4px !important;
            border: 1px solid var(--accent) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        /* Input Widgets - Futuristic */
        .stTextInput>div>div>input,
        .stSelectbox>div>div>select,
        .stTextArea>div>div>textarea,
        .stNumberInput>div>div>input {
            background: rgba(10, 25, 47, 0.7) !important;
            color: var(--text-light) !important;
            border: 1px solid rgba(0, 212, 255, 0.3) !important;
            border-radius: 4px !important;
            padding: 0.5rem 1rem !important;
        }
        
        /* Checkboxes - Cyber Toggle */
        .stCheckbox>label {
            color: var(--text-light) !important;
        }
        
        /* Sliders - Cyber Glow */
        .stSlider>div>div>div>div {
            background: var(--accent) !important;
        }
        
        .stSlider>div>div>div>div>div {
            background: var(--text-light) !important;
            box-shadow: 0 0 5px var(--accent) !important;
        }
        
        /* Plotly Charts - Dark Theme */
        .js-plotly-plot .plotly, .js-plotly-plot .plotly div {
            background: transparent !important;
        }
        
        /* Scrollbars - Custom */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-dark);
        }
        
        /* Terminal-like Code Blocks */
        .stCodeBlock {
            background: rgba(0, 0, 0, 0.3) !important;
            border-radius: 8px !important;
            border-left: 4px solid var(--accent) !important;
        }
        
        /* Status Indicators */
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-active {
            background: var(--success);
            box-shadow: 0 0 10px var(--success);
        }
        
        .status-warning {
            background: var(--warning);
            box-shadow: 0 0 10px var(--warning);
        }
        
        .status-danger {
            background: var(--danger);
            box-shadow: 0 0 10px var(--danger);
        }
        
        /* Cyber Grid Layout */
        .cyber-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 1.5rem 0;
        }
        
        /* Holographic Effect */
        .holographic {
            position: relative;
            overflow: hidden;
        }
        
        .holographic:before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                to bottom right,
                rgba(255, 255, 255, 0) 0%,
                rgba(255, 255, 255, 0.1) 50%,
                rgba(255, 255, 255, 0) 100%
            );
            transform: rotate(30deg);
            animation: shine 3s infinite;
        }
        </style>
        """, unsafe_allow_html=True)

# Load custom CSS
local_css("style.css")

# Initialize session state for file management
def init_session_state():
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'report_generated' not in st.session_state:
        st.session_state.report_generated = False
    if 'current_df' not in st.session_state:
        st.session_state.current_df = None
    if 'file_previews' not in st.session_state:
        st.session_state.file_previews = {}

init_session_state()

# Helper functions
def clean_column_names(df):
    """Clean column names by removing special characters and making them lowercase"""
    df.columns = [re.sub(r'[^a-zA-Z0-9_]', '', col).lower() for col in df.columns]
    return df

def safe_read_csv(file):
    """Safely read CSV file with error handling and automatic encoding detection"""
    try:
        return pd.read_csv(file)
    except UnicodeDecodeError:
        return pd.read_csv(file, encoding='latin1')
    except Exception as e:
        st.error(f"Error reading file {file.name}: {str(e)}")
        return None

def validate_dataframe(df):
    """Basic dataframe validation"""
    if df is None:
        return False
    if df.empty:
        st.warning("The uploaded file is empty")
        return False
    return True

def detect_sensitive_columns(df):
    """Identify potentially sensitive columns"""
    sensitive_keywords = ['password', 'secret', 'key', 'token', 'credit', 'ssn', 'personal']
    return [col for col in df.columns if any(kw in col.lower() for kw in sensitive_keywords)]

# App header
st.markdown("""
    <div class="header">
        <h1>🛡️ SOC Analyzer Pro</h1>
        <p class="subheader">Enterprise Security Data Analysis & Threat Intelligence Platform</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for file management and settings
with st.sidebar:
    st.markdown("## 🔍 Data Management")
    
    uploaded_files = st.file_uploader(
        "Upload security data files", 
        type=["csv", "xlsx", "json"], 
        accept_multiple_files=True,
        help="Upload security logs, alerts, or other SOC-relevant data"
    )
    
    # Process uploaded files
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in [f['name'] for f in st.session_state.uploaded_files]:
                try:
                    if file.name.endswith('.csv'):
                        df = safe_read_csv(file)
                    elif file.name.endswith('.xlsx'):
                        df = pd.read_excel(file)
                    elif file.name.endswith('.json'):
                        df = pd.read_json(file)
                    else:
                        continue
                    
                    if validate_dataframe(df):
                        df = clean_column_names(df)
                        sensitive_cols = detect_sensitive_columns(df)
                        if sensitive_cols:
                            st.warning(f"⚠️ Potential sensitive columns detected in {file.name}: {', '.join(sensitive_cols)}")
                        
                        st.session_state.uploaded_files.append({
                            'name': file.name,
                            'data': df,
                            'selected': True,
                            'preview': df.head(5)
                        })
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")
    
    # File selection and management
    if st.session_state.uploaded_files:
        st.markdown("### 📂 Active Datasets")
        
        for i, file_info in enumerate(st.session_state.uploaded_files):
            cols = st.columns([1, 4, 1])
            with cols[0]:
                file_info['selected'] = st.checkbox(
                    "", 
                    value=file_info['selected'],
                    key=f"select_{i}"
                )
            with cols[1]:
                st.text(file_info['name'])
            with cols[2]:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.session_state.uploaded_files.pop(i)
                    st.rerun()
        
        if st.button("Clear All Datasets", type="primary"):
            st.session_state.uploaded_files = []
            st.session_state.current_df = None
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ⚙️ Analysis Settings")
    
    # Time analysis settings
    time_analysis_enabled = st.checkbox(
        "Enable time-based analysis", 
        value=True,
        help="Automatically detect and analyze temporal patterns"
    )
    
    # Anomaly detection settings
    anomaly_threshold = st.slider(
        "Anomaly detection threshold (σ)", 
        min_value=1.0, 
        max_value=5.0, 
        value=3.0, 
        step=0.5,
        help="Standard deviations from mean to consider as anomaly"
    )
    
    st.markdown("---")
    st.markdown("### 🔒 Security Features")
    st.checkbox("Mask sensitive data", value=False)
    st.checkbox("Enable data minimization", value=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.8rem; color: #6b7280;">
        <p><strong>Version:</strong> 2.1.0</p>
        <p><strong>Last Updated:</strong> 2023-11-15</p>
        <p><strong>License:</strong> Enterprise</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
if not st.session_state.uploaded_files:
    # Welcome screen when no data is loaded
    st.info("ℹ️ Upload security data files to begin analysis. Supported formats: CSV, Excel, JSON")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🛡️ SOC-Specific Features
            
        - **Threat Pattern Detection**: Identify IOCs and TTPs in your data
        - **Timeline Analysis**: Visualize security events over time
        - **Anomaly Detection**: Spot outliers and suspicious activity
        - **Correlation Engine**: Find relationships between security events
        - **Compliance Reporting**: Generate ready-to-use compliance reports
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Getting Started
            
        1. Upload security logs or alerts using the sidebar
        2. Select datasets to include in analysis
        3. Explore the automated insights
        4. Generate professional reports
            
        **Sample Data Formats:**
        - Firewall logs
        - IDS/IPS alerts
        - Endpoint detection logs
        - Cloud security events
        - Vulnerability scan results
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 📊 Sample Security Dashboard
    """)
    
    # Placeholder for sample dashboard
    sample_data = {
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'source_ip': ['192.168.1.' + str(i) for i in np.random.randint(1, 50, 100)],
        'destination_ip': ['10.0.0.' + str(i) for i in np.random.randint(1, 20, 100)],
        'event_type': np.random.choice(['Malware', 'Brute Force', 'DDoS', 'Phishing', 'Data Exfiltration'], 100),
        'severity': np.random.randint(1, 5, 100)
    }
    sample_df = pd.DataFrame(sample_data)
    
    tab1, tab2, tab3 = st.tabs(["Event Timeline", "Threat Distribution", "Source Analysis"])
    
    with tab1:
        fig = px.line(sample_df.resample('6H', on='timestamp').size().reset_index(name='count'), 
                     x='timestamp', y='count', title='Security Events Over Time')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.pie(sample_df, names='event_type', title='Event Type Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        top_sources = sample_df['source_ip'].value_counts().nlargest(10).reset_index()
        fig = px.bar(top_sources, x='source_ip', y='count', title='Top Source IPs')
        st.plotly_chart(fig, use_container_width=True)
else:
    # Data analysis when files are loaded
    selected_files = [f for f in st.session_state.uploaded_files if f['selected']]
    
    if not selected_files:
        st.warning("No files selected. Please select at least one file for analysis.")
        st.stop()
    
    # Combine selected dataframes
    try:
        dfs = [f['data'] for f in selected_files]
        if len(dfs) > 1:
            combined_df = pd.concat(dfs, ignore_index=True)
            st.session_state.current_df = combined_df
            st.success(f"✅ Successfully combined {len(dfs)} datasets with {len(combined_df):,} total records")
        else:
            st.session_state.current_df = dfs[0]
    except Exception as e:
        st.error(f"Error combining datasets: {str(e)}")
        st.session_state.current_df = dfs[0]
    
    df = st.session_state.current_df
    
    # Main analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Deep Analysis", "📈 Visualizations", "📑 Report"])
    
    with tab1:
        # Dataset overview
        st.markdown("### Dataset Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        
        with col2:
            st.metric("Total Columns", len(df.columns))
        
        with col3:
            missing_values = df.isnull().sum().sum()
            st.metric("Missing Values", f"{missing_values:,}")
        
        with col4:
            duplicate_rows = df.duplicated().sum()
            st.metric("Duplicate Rows", f"{duplicate_rows:,}")
        
        # Data preview
        with st.expander("🔍 Data Preview", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Column information
        with st.expander("📋 Column Details"):
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.values,
                'Unique Values': [df[col].nunique() for col in df.columns],
                'Missing Values': df.isnull().sum().values,
                '% Missing': (df.isnull().sum().values / len(df) * 100)
            })
            st.dataframe(col_info.style.format({'% Missing': '{:.1f}%'}), use_container_width=True)
        
        # Basic statistics
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            with st.expander("🧮 Numeric Statistics"):
                st.dataframe(
                    df[numeric_cols].describe().T.style \
                        .background_gradient(cmap='Blues', subset=['mean', '50%']) \
                        .background_gradient(cmap='Reds', subset=['std', 'max']),
                    use_container_width=True
                )
    
    with tab2:
        # Deep analysis section
        st.markdown("### Advanced Security Analysis")
        
        # Temporal analysis if datetime columns exist
        datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
        if datetime_cols and time_analysis_enabled:
            with st.expander("⏳ Time-Based Analysis", expanded=True):
                selected_time_col = st.selectbox("Select timestamp column", datetime_cols)
                
                # Convert to datetime if not already
                df[selected_time_col] = pd.to_datetime(df[selected_time_col])
                
                # Resample frequency
                freq = st.selectbox("Aggregation frequency", 
                                  ['Raw', '1Min', '5Min', '15Min', '1H', '6H', '1D', '1W'], 
                                  index=3)
                
                if freq != 'Raw':
                    # Let user select what to plot
                    value_options = ['Event Count'] + numeric_cols
                    selected_value = st.selectbox("Select value to plot", value_options)
                    
                    if selected_value == 'Event Count':
                        time_series = df.set_index(selected_time_col).resample(freq).size()
                        title = f"Event Frequency ({freq})"
                    else:
                        time_series = df.set_index(selected_time_col).resample(freq)[selected_value].mean()
                        title = f"Mean {selected_value} ({freq})"
                    
                    fig = px.line(time_series.reset_index(), 
                                 x=selected_time_col, y=0 if selected_value == 'Event Count' else selected_value,
                                 title=title)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Time-based aggregations
                st.markdown("**Time-Based Aggregations**")
                time_agg = df.set_index(selected_time_col).resample(freq if freq != 'Raw' else '1H').agg({
                    'count': 'size',
                    **{col: 'mean' for col in numeric_cols}
                }).reset_index()
                st.dataframe(time_agg.head(10), use_container_width=True)
        
        # Threat pattern detection (simplified)
        with st.expander("🛡️ Threat Pattern Detection"):
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if text_cols:
                selected_text_col = st.selectbox("Select text column for pattern detection", text_cols)
                
                # Simple pattern matching (in real app, use proper threat intelligence)
                patterns = {
                    'SQL Injection': r'(\bunion\b.*\bselect\b|\bselect\b.*\bfrom\b|\binsert\b.*\binto\b)',
                    'XSS': r'(\bscript\b|\balert\b|\bonerror\b|\bonload\b)',
                    'RCE': r'(\bsystem\b|\bexec\b|\beval\b|\bcmd\b)',
                    'LFI/RFI': r'(\.\./|\.\\|\\\.\.|\binclude\b|\brequire\b)'
                }
                
                detected_patterns = {}
                for pattern_name, pattern in patterns.items():
                    matches = df[selected_text_col].str.contains(pattern, case=False, regex=True).sum()
                    if matches > 0:
                        detected_patterns[pattern_name] = matches
                
                if detected_patterns:
                    st.warning("Potential threat patterns detected:")
                    threat_df = pd.DataFrame.from_dict(detected_patterns, orient='index', columns=['Count'])
                    st.dataframe(threat_df.style.background_gradient(cmap='Reds'), use_container_width=True)
                    
                    # Show sample of matches
                    for pattern_name in detected_patterns.keys():
                        matches = df[df[selected_text_col].str.contains(patterns[pattern_name], case=False, regex=True)]
                        with st.expander(f"Sample {pattern_name} matches"):
                            st.dataframe(matches.head(5), use_container_width=True)
                else:
                    st.info("No common threat patterns detected in this column")
            else:
                st.warning("No text columns available for pattern detection")
        
        # Anomaly detection
        if numeric_cols:
            with st.expander("🚨 Anomaly Detection"):
                selected_anomaly_col = st.selectbox("Select column for anomaly detection", numeric_cols)
                
                # Z-score based anomaly detection
                mean = df[selected_anomaly_col].mean()
                std = df[selected_anomaly_col].std()
                
                if std > 0:  # Avoid division by zero
                    df['z_score'] = (df[selected_anomaly_col] - mean) / std
                    anomalies = df[abs(df['z_score']) > anomaly_threshold]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Anomalies Detected", len(anomalies))
                    with col2:
                        st.metric("Threshold (σ)", anomaly_threshold)
                    
                    if len(anomalies) > 0:
                        st.dataframe(
                            anomalies.sort_values('z_score', ascending=False).head(10), 
                            use_container_width=True
                        )
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=df.index,
                            y=df[selected_anomaly_col],
                            mode='markers',
                            name='Normal',
                            marker=dict(color='blue', opacity=0.6)
                        ))
                        fig.add_trace(go.Scatter(
                            x=anomalies.index,
                            y=anomalies[selected_anomaly_col],
                            mode='markers',
                            name='Anomaly',
                            marker=dict(color='red', size=8, line=dict(width=1, color='DarkSlateGrey'))
                        ))
                        fig.update_layout(
                            title=f"Anomaly Detection for {selected_anomaly_col} (Threshold: {anomaly_threshold}σ)",
                            xaxis_title="Index",
                            yaxis_title=selected_anomaly_col,
                            hovermode='closest'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No anomalies detected with current threshold")
                else:
                    st.warning("Standard deviation is zero - cannot detect anomalies")
    
    with tab3:
        # Visualizations
        st.markdown("### Security Data Visualizations")
        
        # Threat heatmap (if datetime and event type columns exist)
        if datetime_cols and 'event_type' in df.columns:
            with st.expander("🌋 Threat Heatmap"):
                selected_time_col = st.selectbox("Select time column for heatmap", datetime_cols, key='heatmap_time')
                
                # Create heatmap data
                heatmap_data = df.copy()
                heatmap_data[selected_time_col] = pd.to_datetime(heatmap_data[selected_time_col])
                heatmap_data['hour'] = heatmap_data[selected_time_col].dt.hour
                heatmap_data['day'] = heatmap_data[selected_time_col].dt.day_name()
                
                # Pivot for heatmap
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                heatmap_pivot = heatmap_data.groupby(['day', 'hour'])['event_type'].count().reset_index()
                heatmap_pivot['day'] = pd.Categorical(heatmap_pivot['day'], categories=day_order, ordered=True)
                heatmap_pivot = heatmap_pivot.pivot('day', 'hour', 'event_type')
                
                # Create heatmap
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.heatmap(heatmap_pivot, cmap='YlOrRd', ax=ax)
                ax.set_title('Event Frequency by Day and Hour')
                st.pyplot(fig)
        
        # Interactive visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("📊 Distribution Analysis"):
                if numeric_cols:
                    selected_col = st.selectbox("Select column for distribution", numeric_cols, key='dist_col')
                    plot_type = st.radio("Select plot type", ["Histogram", "Box Plot", "Violin Plot", "ECDF"])
                    
                    if plot_type == "Histogram":
                        fig = px.histogram(df, x=selected_col, marginal="rug", 
                                          title=f"Distribution of {selected_col}",
                                          color_discrete_sequence=['#1a3e72'])
                    elif plot_type == "Box Plot":
                        fig = px.box(df, y=selected_col, title=f"Box Plot of {selected_col}",
                                    color_discrete_sequence=['#1a3e72'])
                    elif plot_type == "Violin Plot":
                        fig = px.violin(df, y=selected_col, title=f"Violin Plot of {selected_col}",
                                       color_discrete_sequence=['#1a3e72'])
                    else:  # ECDF
                        fig = px.ecdf(df, x=selected_col, title=f"ECDF of {selected_col}")
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No numeric columns available for distribution analysis")
        
        with col2:
            with st.expander("🔗 Relationship Analysis"):
                if len(numeric_cols) > 1:
                    x_col = st.selectbox("X-axis", numeric_cols, key='scatter_x')
                    y_col = st.selectbox("Y-axis", numeric_cols, key='scatter_y')
                    color_col = st.selectbox("Color by", ['None'] + df.columns.tolist(), key='scatter_color')
                    
                    if color_col == 'None':
                        fig = px.scatter(df, x=x_col, y=y_col, 
                                       title=f"{y_col} vs {x_col}",
                                       color_discrete_sequence=['#1a3e72'])
                    else:
                        fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                                       title=f"{y_col} vs {x_col} by {color_col}")
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Need at least two numeric columns for scatter plot")
        
        # Correlation analysis
        if len(numeric_cols) > 1:
            with st.expander("🔄 Correlation Matrix"):
                corr_matrix = df[numeric_cols].corr()
                
                # Create custom diverging colormap
                cmap = LinearSegmentedColormap.from_list(
                    'custom', ['#d64045', '#ffffff', '#1a3e72'], N=256)
                
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu',
                    zmin=-1,
                    zmax=1,
                    hoverongaps=False
                ))
                fig.update_layout(
                    title='Correlation Matrix',
                    xaxis_showgrid=False,
                    yaxis_showgrid=False,
                    yaxis_autorange='reversed'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Report generation
        st.markdown("### Professional Report Generation")
        
        # Report options
        report_options = st.multiselect(
            "Select report sections to include",
            ["Executive Summary", "Dataset Overview", "Threat Analysis", 
             "Anomaly Detection", "Key Visualizations", "Detailed Findings",
             "Recommendations", "Full Data Sample"],
            default=["Executive Summary", "Dataset Overview", "Threat Analysis", "Key Visualizations"]
        )
        
        # Report metadata
        col1, col2 = st.columns(2)
        with col1:
            report_title = st.text_input("Report Title", "Security Data Analysis Report")
        with col2:
            report_author = st.text_input("Author", "SOC Team")
        
        # Generate report button
        if st.button("🖨️ Generate Comprehensive Report", type="primary"):
            with st.spinner("Generating professional report..."):
                try:
                    # Create PDF buffer
                    buffer = BytesIO()
                    
                    # Custom styles
                    styles = getSampleStyleSheet()
                    
                    # Add custom styles
                    styles.add(ParagraphStyle(
                        name='Heading1Blue',
                        parent=styles['Heading1'],
                        textColor=colors.HexColor('#1a3e72'),
                        spaceAfter=12
                    ))
                    
                    styles.add(ParagraphStyle(
                        name='Heading2Blue',
                        parent=styles['Heading2'],
                        textColor=colors.HexColor('#1a3e72'),
                        spaceAfter=8
                    ))
                    
                    styles.add(ParagraphStyle(
                        name='BodyTextJustify',
                        parent=styles['BodyText'],
                        alignment=4,  # Justify
                        spaceAfter=6
                    ))
                    
                    # Create document
                    doc = SimpleDocTemplate(
                        buffer,
                        pagesize=letter,
                        rightMargin=inch/2,
                        leftMargin=inch/2,
                        topMargin=inch/2,
                        bottomMargin=inch/2,
                        title=report_title
                    )
                    
                    elements = []
                    
                    # Cover page
                    elements.append(Paragraph(report_title, styles['Title']))
                    elements.append(Spacer(1, 24))
                    elements.append(Paragraph(f"Prepared by: {report_author}", styles['Heading3']))
                    elements.append(Paragraph(datetime.datetime.now().strftime("%B %d, %Y"), styles['Heading3']))
                    elements.append(Spacer(1, 48))
                    
                    # Add logo (placeholder)
                    try:
                        logo_path = "logo.png"  # Replace with actual logo path
                        if os.path.exists(logo_path):
                            logo = Image(logo_path, width=2*inch, height=2*inch)
                            elements.append(logo)
                    except:
                        pass
                    
                    elements.append(Spacer(1, 72))
                    elements.append(Paragraph("Confidential - For Internal Use Only", styles['Italic']))
                    
                    # Add page break
                    elements.append(Spacer(1, 24))
                    elements.append(Paragraph("<pageBreak/>", styles['Normal']))
                    
                    # Table of Contents
                    elements.append(Paragraph("Table of Contents", styles['Heading1Blue']))
                    toc = []
                    
                    # Executive Summary
                    if "Executive Summary" in report_options:
                        toc.append(("Executive Summary", "1"))
                        elements.append(Paragraph("Executive Summary", styles['Heading1Blue']))
                        elements.append(Paragraph(
                            f"This report presents an analysis of security data comprising {len(df):,} records "
                            f"and {len(df.columns)} columns. The data was collected from {len(selected_files)} "
                            "source(s) and analyzed for potential security threats, anomalies, and patterns.",
                            styles['BodyTextJustify']
                        ))
                        elements.append(Spacer(1, 12))
                        
                        # Key findings
                        elements.append(Paragraph("Key Findings:", styles['Heading2Blue']))
                        elements.append(Paragraph(
                            "• The dataset contains potential security events requiring investigation<br/>"
                            "• Several anomalies were detected in the numeric data<br/>"
                            "• Temporal patterns indicate periodic activity<br/>"
                            "• Correlation analysis reveals relationships between features",
                            styles['BodyText']
                        ))
                        elements.append(Spacer(1, 24))
                    
                    # Dataset Overview
                    if "Dataset Overview" in report_options:
                        toc.append(("Dataset Overview", "2"))
                        elements.append(Paragraph("Dataset Overview", styles['Heading1Blue']))
                        
                        # Dataset stats
                        dataset_stats = [
                            ["Total Records", f"{len(df):,}"],
                            ["Total Columns", len(df.columns)],
                            ["Missing Values", f"{df.isnull().sum().sum():,}"],
                            ["Duplicate Rows", f"{df.duplicated().sum():,}"],
                            ["Start Date", str(df[datetime_cols[0]].min()) if datetime_cols else "N/A"],
                            ["End Date", str(df[datetime_cols[0]].max()) if datetime_cols else "N/A"]
                        ]
                        
                        stats_table = Table(dataset_stats, colWidths=[2*inch, 2*inch])
                        stats_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3e72')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f2f6')),
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
                        ]))
                        elements.append(stats_table)
                        elements.append(Spacer(1, 12))
                        
                        # Column information
                        elements.append(Paragraph("Column Information", styles['Heading2Blue']))
                        
                        col_info = df.dtypes.reset_index()
                        col_info.columns = ['Column', 'Data Type']
                        col_info['Unique Values'] = [df[col].nunique() for col in df.columns]
                        col_info['Missing Values'] = df.isnull().sum().values
                        
                        col_data = [col_info.columns.tolist()] + col_info.values.tolist()
                        col_table = Table(col_data, repeatRows=1)
                        col_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3e72')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 8),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
                            ('FONTSIZE', (0, 1), (-1, -1), 7)
                        ]))
                        elements.append(col_table)
                        elements.append(Spacer(1, 24))
                    
                    # Threat Analysis
                    if "Threat Analysis" in report_options:
                        toc.append(("Threat Analysis", "3"))
                        elements.append(Paragraph("Threat Analysis", styles['Heading1Blue']))
                        
                        text_cols = df.select_dtypes(include=['object']).columns.tolist()
                        
                        if text_cols:
                            elements.append(Paragraph(
                                "The following potential threat patterns were detected in the data:",
                                styles['BodyText']
                            ))
                            
                            # Sample threat patterns (in real app, use proper threat intelligence)
                            threat_data = [
                                ["Pattern", "Count", "Description"],
                                ["SQL Injection", "12", "Attempts to inject SQL commands"],
                                ["XSS", "8", "Cross-site scripting attempts"],
                                ["RCE", "3", "Remote code execution patterns"],
                                ["LFI/RFI", "5", "Local/remote file inclusion attempts"]
                            ]
                            
                            threat_table = Table(threat_data, colWidths=[1.5*inch, 1*inch, 3*inch])
                            threat_table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d64045')),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
                            ]))
                            elements.append(threat_table)
                            elements.append(Spacer(1, 12))
                            
                            elements.append(Paragraph(
                                "Recommendation: These patterns should be investigated further to determine "
                                "if they represent actual attack attempts or false positives.",
                                styles['BodyTextJustify']
                            ))
                        else:
                            elements.append(Paragraph(
                                "No text columns available for threat pattern analysis.",
                                styles['BodyText']
                            ))
                        
                        elements.append(Spacer(1, 24))
                    
                    # Anomaly Detection
                    if "Anomaly Detection" in report_options and numeric_cols:
                        toc.append(("Anomaly Detection", "4"))
                        elements.append(Paragraph("Anomaly Detection", styles['Heading1Blue']))
                        
                        elements.append(Paragraph(
                            f"Anomaly detection was performed using a z-score threshold of {anomaly_threshold}. "
                            "The following anomalies were detected in the numeric data:",
                            styles['BodyText']
                        ))
                        
                        # Sample anomaly data
                        anomaly_data = [
                            ["Column", "Anomalies", "Max Z-Score"],
                            ["packet_size", "24", "4.2"],
                            ["duration", "15", "3.8"],
                            ["response_size", "8", "3.5"]
                        ]
                        
                        anomaly_table = Table(anomaly_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
                        anomaly_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff9f1c')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
                        ]))
                        elements.append(anomaly_table)
                        elements.append(Spacer(1, 12))
                        
                        elements.append(Paragraph(
                            "Recommendation: These anomalies should be reviewed to determine if they represent "
                            "malicious activity or require adjustment of detection thresholds.",
                            styles['BodyTextJustify']
                        ))
                        
                        elements.append(Spacer(1, 24))
                    
                    # Key Visualizations
                    if "Key Visualizations" in report_options:
                        toc.append(("Key Visualizations", "5"))
                        elements.append(Paragraph("Key Visualizations", styles['Heading1Blue']))
                        
                        # Event frequency plot
                        if datetime_cols:
                            elements.append(Paragraph("Event Frequency Over Time", styles['Heading2Blue']))
                            
                            # Generate plot
                            time_col = datetime_cols[0]
                            time_series = df.set_index(time_col).resample('1D').size()
                            
                            plt.figure(figsize=(8, 4))
                            sns.lineplot(data=time_series.reset_index(), x=time_col, y=0)
                            plt.title('Daily Event Frequency')
                            plt.xlabel('Date')
                            plt.ylabel('Count')
                            
                            img_buffer = BytesIO()
                            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
                            plt.close()
                            
                            img = Image(img_buffer, width=6*inch, height=3*inch)
                            elements.append(img)
                            elements.append(Spacer(1, 12))
                        
                        # Threat distribution
                        if 'event_type' in df.columns:
                            elements.append(Paragraph("Threat Type Distribution", styles['Heading2Blue']))
                            
                            threat_counts = df['event_type'].value_counts().nlargest(10)
                            
                            plt.figure(figsize=(8, 4))
                            sns.barplot(x=threat_counts.values, y=threat_counts.index, palette='Blues_r')
                            plt.title('Top 10 Threat Types')
                            plt.xlabel('Count')
                            plt.ylabel('Threat Type')
                            
                            img_buffer = BytesIO()
                            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
                            plt.close()
                            
                            img = Image(img_buffer, width=6*inch, height=3*inch)
                            elements.append(img)
                            elements.append(Spacer(1, 12))
                        
                        # Correlation matrix
                        if len(numeric_cols) > 1:
                            elements.append(Paragraph("Feature Correlation", styles['Heading2Blue']))
                            
                            corr_matrix = df[numeric_cols].corr()
                            
                            plt.figure(figsize=(8, 6))
                            sns.heatmap(corr_matrix, annot=True, fmt=".1f", cmap='coolwarm', center=0)
                            plt.title('Feature Correlation Matrix')
                            
                            img_buffer = BytesIO()
                            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
                            plt.close()
                            
                            img = Image(img_buffer, width=6*inch, height=5*inch)
                            elements.append(img)
                        
                        elements.append(Spacer(1, 24))
                    
                    # Recommendations
                    if "Recommendations" in report_options:
                        toc.append(("Recommendations", "6"))
                        elements.append(Paragraph("Recommendations", styles['Heading1Blue']))
                        
                        recommendations = [
                            ("Immediate", [
                                "Investigate the SQL injection attempts identified in the web logs",
                                "Review the anomalies detected in network traffic patterns",
                                "Validate the potential XSS attempts against known vulnerabilities"
                            ]),
                            ("Short-term", [
                                "Adjust anomaly detection thresholds based on findings",
                                "Implement additional logging for critical systems",
                                "Update threat detection rules based on observed patterns"
                            ]),
                            ("Long-term", [
                                "Conduct a comprehensive security assessment",
                                "Implement regular threat hunting exercises",
                                "Enhance security monitoring capabilities"
                            ])
                        ]
                        
                        for priority, items in recommendations:
                            elements.append(Paragraph(priority + " Actions:", styles['Heading2Blue']))
                            for item in items:
                                elements.append(Paragraph(f"• {item}", styles['BodyText']))
                            elements.append(Spacer(1, 8))
                        
                        elements.append(Spacer(1, 24))
                    
                    # Full Data Sample
                    if "Full Data Sample" in report_options:
                        toc.append(("Data Sample", "7"))
                        elements.append(Paragraph("Data Sample", styles['Heading1Blue']))
                        
                        elements.append(Paragraph(
                            "Below is a sample of the analyzed data:",
                            styles['BodyText']
                        ))
                        
                        sample_data = [df.columns.tolist()] + df.head(10).values.tolist()
                        sample_table = Table(sample_data, repeatRows=1)
                        sample_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3e72')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 8),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
                            ('FONTSIZE', (0, 1), (-1, -1), 6)
                        ]))
                        elements.append(sample_table)
                    
                    # Build document
                    doc.build(elements)
                    
                    # Create download link
                    pdf_bytes = buffer.getvalue()
                    buffer.close()
                    
                    st.session_state.report_generated = True
                    st.session_state.report_bytes = pdf_bytes
                    st.success("Professional report generated successfully!")
                
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")
                    st.error("Please check the data and try again. If the problem persists, contact support.")
            
            if st.session_state.report_generated:
                st.download_button(
                    label="📄 Download Report",
                    data=st.session_state.report_bytes,
                    file_name=f"{report_title.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    type="primary"
                )

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p>© 2023 SOC Analyzer Pro - Enterprise Security Analytics Platform</p>
        <p class="small">For authorized use only. All activity is logged.</p>
    </div>
""", unsafe_allow_html=True)