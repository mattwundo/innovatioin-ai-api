import streamlit as st
import requests
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import time
from fpdf import FPDF  # Install with: pip install fpdf

# Set up Streamlit page
st.set_page_config(page_title="AI R&D Predictor", page_icon="🚀", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    h1 {color: #2E86C1;}
    .stButton>button {background-color: #2E86C1; color: white; font-size: 18px;}
    </style>
""", unsafe_allow_html=True)

# Sidebar: Company Insights
st.sidebar.header("🔍 Company Insights")
company_ticker = st.sidebar.text_input("Enter Company Ticker (e.g., AAPL, TSLA)", value="AAPL")

if st.sidebar.button("📊 Get Financial Data"):
    stock = yf.Ticker(company_ticker)
    try:
        market_cap = stock.info.get("marketCap", "Not Available")
        revenue = stock.financials.loc["Total Revenue"].iloc[0]
        st.sidebar.write(f"**Market Cap:** ${market_cap:,}")
        st.sidebar.write(f"**Revenue:** ${revenue:,}")
    except:
        st.sidebar.warning("⚠️ Unable to fetch data. Check ticker symbol.")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["🔮 AI Prediction", "📊 Company Data", "📈 Innovation Tradeoff"])

# 🔮 AI Prediction Tab - Manual Input for Private Companies
with tab1:
    st.title("🚀 AI-Powered R&D Investment Predictor")

    # Private Company Data Table
    st.subheader("📊 Enter Private Company Data")
    
    revenue = st.number_input("Revenue ($)", min_value=0, step=1000000, key="revenue_input")
    r_and_d_spend = st.number_input("R&D Investment ($)", min_value=0, step=50000, key="rd_input")
    profit_margin = st.number_input("Operating Profit Margin (%)", min_value=0.0, max_value=100.0, step=0.1, key="profit_input")
    patents = st.number_input("Total Patents Filed (Last 3 Years)", min_value=0, step=1, key="patent_input")
    risk_tolerance = st.slider("R&D Risk Tolerance (1-10)", 1, 10, key="risk_input")
    rd_allocation = st.slider("Incremental vs. Radical R&D (%)", 0, 100, key="allocation_input")
    competitor_threat = st.slider("Competitor Threat Level (1-10)", 1, 10, key="threat_input")
    disruptive_impact = st.slider("Disruptive Event Impact (1-10)", 1, 10, key="disruptive_input")
    industry = st.selectbox("Select Industry", ["Tech", "Pharma", "Automotive", "Other"], key="industry_input")
    market_growth = st.number_input("Market Growth Rate (%)", min_value=-10.0, max_value=20.0, step=0.1, key="growth_input")

    # Convert Data into a Table
    data_dict = {
        "Revenue ($)": revenue,
        "R&D Investment ($)": r_and_d_spend,
        "Operating Profit Margin (%)": profit_margin,
        "Total Patents (3Y)": patents,
        "R&D Risk Tolerance": risk_tolerance,
        "Incremental vs. Radical R&D (%)": rd_allocation,
        "Competitor Threat Level": competitor_threat,
        "Disruptive Event Impact": disruptive_impact,
        "Industry": industry,
        "Market Growth Rate (%)": market_growth
    }

    df_private = pd.DataFrame([data_dict])
    st.write("📋 **Entered Data:**")
    st.dataframe(df_private)

    # API URL (Replace with actual Render API URL)
    API_URL = "https://your-app-name.onrender.com/predict"

    def generate_innovation_tradeoff_graph(revenue, r_and_d_spend, risk_tolerance, rd_allocation):
        """
        Generates a dynamic Innovation Tradeoff Graph based on user-entered private company data.
        """
        fig, ax = plt.subplots()

        # Time (Years)
        years = np.arange(0, 10, 1)

        # Incremental Innovation Decline (S1)
        s1 = r_and_d_spend * 0.002 * np.exp(-0.2 * (years - 5) ** 2)

        # Radical Innovation Max Impact (S2)
        s2 = np.where(years < 5, r_and_d_spend * 0.002, r_and_d_spend * 0.002 + (years - 5) * (rd_allocation / 40))

        # Creative Destruction Threshold
        threshold = np.full_like(years, revenue * 0.15 + (risk_tolerance * 0.01 * revenue))

        # Radical Innovation Shift
        radical_innovation = np.where(years < 5, revenue * 0.1, revenue * 0.1 + (years - 5) * (risk_tolerance * 0.01 * revenue))

        # Plot the tradeoff curves
        ax.plot(years, s1, label="S1: Incremental Decline", color="blue")
        ax.plot(years, s2, label="S2: Radical Max Impact", color="red")
        ax.plot(years, threshold, label="Creative Destruction Threshold", linestyle="dashed", color="red")
        ax.plot(years, radical_innovation, label="Radical Innovation", linestyle="dashed", color="purple")

        # Labels & Formatting
        ax.set_xlabel("Time (Years)")
        ax.set_ylabel("Innovation Value (Project Outcomes)")
        ax.set_title(f"Innovation Tradeoff Simulation\n(Revenue: ${revenue:,.0f}, R&D: ${r_and_d_spend:,.0f})")
        ax.legend()
        st.pyplot(fig)

    # Button to Generate Prediction
    if st.button("🔮 Generate AI-Powered Tradeoff Graph"):
        if revenue > 0 and r_and_d_spend > 0:
            generate_innovation_tradeoff_graph(revenue, r_and_d_spend, risk_tolerance, rd_allocation)
        else:
            st.warning("⚠️ Please enter valid revenue & R&D investment data.")

# 📥 Generate & Download PDF Report
def generate_pdf(revenue, r_and_d_spend):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, "AI-Powered R&D Investment Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, f"Revenue: ${revenue:,.2f}", ln=True)
    pdf.cell(200, 10, f"R&D Investment: ${r_and_d_spend:,.2f}", ln=True)
    
    pdf_file = "R&D_Report.pdf"
    pdf.output(pdf_file)
    return pdf_file

if st.button("📥 Download Report as PDF"):
    if revenue > 0 and r_and_d_spend > 0:
        pdf_file = generate_pdf(revenue, r_and_d_spend)
        with open(pdf_file, "rb") as f:
            st.download_button("Download Report", f, file_name="R&D_Report.pdf")
    else:
        st.warning("⚠️ Please enter valid revenue & R&D investment data.")
