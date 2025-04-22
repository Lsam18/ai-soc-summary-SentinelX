import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import tempfile
import os
import base64
import io
import datetime
from io import BytesIO
import numpy as np
from pandas.api.types import is_numeric_dtype
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(
    page_title="SOC CSV Analyzer Pro",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
local_css("style.css")

# App header
st.markdown("""
    <div class="header">
        <h1>🛡️ SOC CSV Analyzer Pro - Sentinel-X</h1>
        <p class="subheader">Professional Security Data Analysis & Reporting Tool - Powered by Sentinel-X</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for multiple files
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

# Sidebar for file management
with st.sidebar:
    st.markdown("## 🔍 File Management")
    uploaded_files = st.file_uploader(
        "Upload CSV files", 
        type=["csv"], 
        accept_multiple_files=True,
        help="Upload one or more CSV files for analysis"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in [f['name'] for f in st.session_state.uploaded_files]:
                st.session_state.uploaded_files.append({
                    'name': file.name,
                    'data': pd.read_csv(file),
                    'selected': True
                })
    
    # Display file selection checkboxes
    if st.session_state.uploaded_files:
        st.markdown("### 📂 Selected Files")
        for i, file_info in enumerate(st.session_state.uploaded_files):
            file_info['selected'] = st.checkbox(
                file_info['name'], 
                value=file_info['selected'],
                key=f"file_{i}"
            )
        
        if st.button("Clear All"):
            st.session_state.uploaded_files = []

# Main content
if not st.session_state.uploaded_files:
    st.info("ℹ️ Please upload one or more CSV files to begin analysis.")
    st.markdown("""
    ### ☣︎ Features:
    - **Multiple CSV Analysis**: Combine and analyze multiple CSV files simultaneously
    - **Comprehensive Statistics**: Detailed statistical analysis of your data
    - **Advanced Visualizations**: Interactive charts for data exploration
    - **Professional Reporting**: Generate detailed PDF reports with one click
    - **SOC-Specific Tools**: Specialized analysis for security operations data
    """)
else:
    # Get selected dataframes
    selected_files = [f for f in st.session_state.uploaded_files if f['selected']]
    dfs = [f['data'] for f in selected_files]
    
    # Combine data if multiple files selected
    if len(dfs) > 1:
        try:
            combined_df = pd.concat(dfs, ignore_index=True)
            df = combined_df
            st.success(f"✅ Successfully combined {len(dfs)} files with {len(df)} total records")
        except Exception as e:
            st.error(f"Error combining files: {str(e)}")
            df = dfs[0]
    else:
        df = dfs[0]
    
    # Basic info section
    st.markdown("## 📊 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    
    with col2:
        st.metric("Total Columns", len(df.columns))
    
    with col3:
        missing_values = df.isnull().sum().sum()
        st.metric("Missing Values", missing_values)
    
    # Data preview
    with st.expander("🔍 Data Preview", expanded=True):
        st.dataframe(df.head(10))
    
    # Column information
    with st.expander("📋 Column Information"):
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.values,
            'Unique Values': [df[col].nunique() for col in df.columns],
            'Missing Values': df.isnull().sum().values
        })
        st.dataframe(col_info)
    
    # Statistics section
    st.markdown("## 📈 Statistical Analysis")
    
    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        with st.expander("🧮 Numeric Columns Statistics", expanded=True):
            st.dataframe(df[numeric_cols].describe().T.style.background_gradient(cmap='Blues'))
    else:
        st.warning("No numeric columns found for statistical analysis")
    
    # Categorical columns analysis
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if cat_cols:
        with st.expander("📊 Categorical Columns Analysis"):
            selected_cat_col = st.selectbox("Select categorical column", cat_cols)
            value_counts = df[selected_cat_col].value_counts().reset_index()
            value_counts.columns = ['Value', 'Count']
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(value_counts)
            with col2:
                fig = px.pie(value_counts, values='Count', names='Value', 
                            title=f'Distribution of {selected_cat_col}')
                st.plotly_chart(fig, use_container_width=True)
    
    # Correlation analysis
    if len(numeric_cols) > 1:
        with st.expander("🔄 Correlation Analysis"):
            corr_matrix = df[numeric_cols].corr()
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmin=-1,
                zmax=1
            ))
            fig.update_layout(title='Correlation Matrix')
            st.plotly_chart(fig, use_container_width=True)
    
    # Time series analysis (if datetime columns exist)
    datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    if datetime_cols:
        with st.expander("⏳ Time Series Analysis"):
            selected_time_col = st.selectbox("Select datetime column", datetime_cols)
            selected_value_col = st.selectbox("Select value column", numeric_cols)
            
            df[selected_time_col] = pd.to_datetime(df[selected_time_col])
            time_series_df = df.set_index(selected_time_col).resample('D')[selected_value_col].mean().reset_index()
            
            fig = px.line(time_series_df, x=selected_time_col, y=selected_value_col, 
                         title=f'{selected_value_col} Over Time')
            st.plotly_chart(fig, use_container_width=True)
    
    # Advanced Visualizations
    st.markdown("## 📊 Advanced Visualizations")
    
    if numeric_cols:
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("📉 Distribution Plots"):
                selected_col = st.selectbox("Select column for distribution", numeric_cols)
                plot_type = st.radio("Select plot type", ["Histogram", "Box Plot", "Violin Plot"])
                
                if plot_type == "Histogram":
                    fig = px.histogram(df, x=selected_col, marginal="rug", 
                                      title=f"Distribution of {selected_col}")
                elif plot_type == "Box Plot":
                    fig = px.box(df, y=selected_col, title=f"Box Plot of {selected_col}")
                else:
                    fig = px.violin(df, y=selected_col, title=f"Violin Plot of {selected_col}")
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            with st.expander("🔗 Scatter Plot"):
                x_col = st.selectbox("X-axis", numeric_cols, key='scatter_x')
                y_col = st.selectbox("Y-axis", numeric_cols, key='scatter_y')
                color_col = st.selectbox("Color by", ['None'] + cat_cols, key='scatter_color')
                
                if color_col == 'None':
                    fig = px.scatter(df, x=x_col, y=y_col, 
                                   title=f"{y_col} vs {x_col}")
                else:
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                                   title=f"{y_col} vs {x_col} by {color_col}")
                
                st.plotly_chart(fig, use_container_width=True)
    
    # Anomaly Detection (basic)
    if len(numeric_cols) >= 1:
        with st.expander("🚨 Anomaly Detection"):
            selected_anomaly_col = st.selectbox("Select column for anomaly detection", numeric_cols)
            
            # Simple z-score based anomaly detection
            mean = df[selected_anomaly_col].mean()
            std = df[selected_anomaly_col].std()
            threshold = st.slider("Anomaly threshold (z-score)", 1.0, 5.0, 3.0, 0.5)
            
            df['z_score'] = (df[selected_anomaly_col] - mean) / std
            anomalies = df[abs(df['z_score']) > threshold]
            
            st.metric("Total Anomalies Detected", len(anomalies))
            
            if len(anomalies) > 0:
                st.dataframe(anomalies.sort_values('z_score', ascending=False))
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[selected_anomaly_col],
                    mode='markers',
                    name='Normal',
                    marker=dict(color='blue')
                ))
                fig.add_trace(go.Scatter(
                    x=anomalies.index,
                    y=anomalies[selected_anomaly_col],
                    mode='markers',
                    name='Anomaly',
                    marker=dict(color='red', size=8)
                ))
                fig.update_layout(title=f"Anomaly Detection for {selected_anomaly_col}")
                st.plotly_chart(fig, use_container_width=True)
    
    # Report Generation
    st.markdown("## 📑 Generate Professional Report")
    
    report_options = st.multiselect(
        "Select report sections",
        ["Dataset Overview", "Statistical Analysis", "Visualizations", 
         "Correlation Analysis", "Anomaly Detection", "Full Data Sample"],
        default=["Dataset Overview", "Statistical Analysis", "Visualizations"]
    )
    
    report_title = st.text_input("Report Title", "SOC Data Analysis Report")
    
    if st.button("🖨️ Generate PDF Report"):
        with st.spinner("Generating report..."):
            try:
                # Create PDF
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                elements = []
                
                # Add title
                elements.append(Paragraph(report_title, styles['Title']))
                elements.append(Spacer(1, 12))
                
                # Add metadata
                metadata = [
                    f"Report generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    f"Total records: {len(df)}",
                    f"Total columns: {len(df.columns)}",
                    f"Source files: {', '.join([f['name'] for f in selected_files])}"
                ]
                
                for meta in metadata:
                    elements.append(Paragraph(meta, styles['Normal']))
                    elements.append(Spacer(1, 6))
                
                elements.append(Spacer(1, 24))
                
                # Dataset Overview
                if "Dataset Overview" in report_options:
                    elements.append(Paragraph("Dataset Overview", styles['Heading2']))
                    
                    # Column info table
                    col_info = pd.DataFrame({
                        'Column': df.columns,
                        'Type': df.dtypes.astype(str),
                        'Unique Values': [df[col].nunique() for col in df.columns],
                        'Missing Values': df.isnull().sum().values
                    })
                    
                    col_table_data = [col_info.columns.tolist()] + col_info.values.tolist()
                    col_table = Table(col_table_data)
                    col_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    elements.append(col_table)
                    elements.append(Spacer(1, 24))
                
                # Statistical Analysis
                if "Statistical Analysis" in report_options and numeric_cols:
                    elements.append(Paragraph("Statistical Analysis", styles['Heading2']))
                    
                    stats_df = df[numeric_cols].describe().T
                    stats_data = [stats_df.columns.tolist()] + stats_df.reset_index().values.tolist()
                    
                    stats_table = Table(stats_data)
                    stats_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    elements.append(stats_table)
                    elements.append(Spacer(1, 24))
                
                # Visualizations
                if "Visualizations" in report_options and numeric_cols:
                    elements.append(Paragraph("Key Visualizations", styles['Heading2']))
                    
                    # Histogram
                    selected_col = numeric_cols[0]
                    fig = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
                    img_bytes = fig.to_image(format="png")
                    img = Image(BytesIO(img_bytes), width=6*inch, height=4*inch)
                    elements.append(Paragraph(f"Distribution of {selected_col}", styles['Heading3']))
                    elements.append(img)
                    elements.append(Spacer(1, 12))
                    
                    # Box plot
                    fig = px.box(df, y=selected_col, title=f"Box Plot of {selected_col}")
                    img_bytes = fig.to_image(format="png")
                    img = Image(BytesIO(img_bytes), width=6*inch, height=4*inch)
                    elements.append(Paragraph(f"Box Plot of {selected_col}", styles['Heading3']))
                    elements.append(img)
                    elements.append(Spacer(1, 24))
                
                # Correlation Analysis
                if "Correlation Analysis" in report_options and len(numeric_cols) > 1:
                    elements.append(Paragraph("Correlation Analysis", styles['Heading2']))
                    
                    corr_matrix = df[numeric_cols].corr()
                    plt.figure(figsize=(10, 8))
                    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
                    plt.title('Correlation Matrix')
                    
                    img_buffer = BytesIO()
                    plt.savefig(img_buffer, format='png', bbox_inches='tight')
                    plt.close()
                    
                    img = Image(img_buffer, width=6*inch, height=6*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 24))
                
                # Anomaly Detection
                if "Anomaly Detection" in report_options and len(numeric_cols) >= 1:
                    elements.append(Paragraph("Anomaly Detection", styles['Heading2']))
                    
                    selected_col = numeric_cols[0]
                    mean = df[selected_col].mean()
                    std = df[selected_col].std()
                    threshold = 3.0
                    df['z_score'] = (df[selected_col] - mean) / std
                    anomalies = df[abs(df['z_score']) > threshold]
                    
                    elements.append(Paragraph(f"Anomalies in {selected_col} (z-score > {threshold})", styles['Heading3']))
                    elements.append(Paragraph(f"Total anomalies detected: {len(anomalies)}", styles['Normal']))
                    
                    if len(anomalies) > 0:
                        anomaly_data = [anomalies.columns.tolist()] + anomalies.head(10).values.tolist()
                        anomaly_table = Table(anomaly_data)
                        anomaly_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 8),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ]))
                        elements.append(anomaly_table)
                    elements.append(Spacer(1, 24))
                
                # Full Data Sample
                if "Full Data Sample" in report_options:
                    elements.append(Paragraph("Data Sample", styles['Heading2']))
                    
                    sample_data = [df.columns.tolist()] + df.head(20).values.tolist()
                    sample_table = Table(sample_data)
                    sample_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 6),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    elements.append(sample_table)
                
                # Build PDF
                doc.build(elements)
                
                # Create download link
                pdf_bytes = buffer.getvalue()
                buffer.close()
                
                st.success("Report generated successfully!")
                st.download_button(
                    label="📄 Download Report",
                    data=pdf_bytes,
                    file_name=f"{report_title.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p> → SOC CSV Analyzer Pro - Professional Security Data Analysis Tool</p>
        <p class="small">For SOC analysts and security professionals</p>
    </div>
""", unsafe_allow_html=True)