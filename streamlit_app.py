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

# 🔮 AI Prediction Tab
with tab1:
    st.title("🚀 AI-Powered R&D Investment Predictor")
    revenue = st.number_input("Enter Company Revenue ($)", min_value=0, step=1000000, key="revenue_input")

    # API URL (Replace with actual Render API URL)
    API_URL = "https://your-app-name.onrender.com/predict"

    def generate_innovation_tradeoff_graph(revenue, predicted_r_and_d):
        """
        Generates a dynamic Innovation Tradeoff Graph for each inquiry.
        """
        fig, ax = plt.subplots()

        # Time (Years)
        years = np.arange(0, 10, 1)

        # Incremental Innovation Decline (S1) - Peaks then declines
        s1 = 40 + 10 * np.exp(-0.2 * (years - 5) ** 2)

        # Radical Innovation Max Impact (S2) - Jumps at the threshold
        s2 = np.where(years < 5, 70, 70 + (years - 5) * 2.5)

        # Creative Destruction Threshold - A constant threshold where radical innovation dominates
        threshold = np.full_like(years, 80)

        # Radical Innovation Shift - Sharp increase after year 5
        radical_innovation = np.where(years < 5, 65, 65 + (years - 5) * 1.5)

        # Plot the tradeoff curves
        ax.plot(years, s1, label="S1: Incremental Decline", color="blue")
        ax.plot(years, s2, label="S2: Radical Max Impact", color="red")
        ax.plot(years, threshold, label="Creative Destruction Threshold", linestyle="dashed", color="red")
        ax.plot(years, radical_innovation, label="Radical Innovation", linestyle="dashed", color="purple")

        # Labels & Formatting
        ax.set_xlabel("Time (Years)")
        ax.set_ylabel("Innovation Value (Project Outcomes)")
        ax.set_title("Manufacturing Investment Innovation Tradeoff Simulation")
        ax.legend()

        # Annotate critical points
        ax.axvline(x=5, color="black", linestyle="dashed")
        ax.text(5.2, 85, "Incremental Innovation", fontsize=10, color="black")
        ax.text(8.2, 85, "Radical Innovation", fontsize=10, color="black")

        st.pyplot(fig)

    def get_prediction():
        """
        Fetches AI-powered R&D prediction and generates a dynamic Innovation Tradeoff Graph.
        """
        if revenue > 0:
            with st.spinner("🔄 Running Innovation Model..."):
                time.sleep(2)  # Simulate processing time
                data = {"Revenue": revenue}
                response = requests.post(API_URL, json=data)

                if response.status_code == 200:
                    prediction = response.json()
                    predicted_r_and_d = prediction["Predicted R&D Spend"]
                    st.success(f"💡 Predicted R&D Investment: **${predicted_r_and_d:,.2f}**")

                    # Generate the Innovation Tradeoff Graph
                    generate_innovation_tradeoff_graph(revenue, predicted_r_and_d)

                else:
                    st.error("⚠️ Error: Could not fetch prediction from API.")
        else:
            st.warning("⚠️ Please enter a revenue amount greater than 0.")

    st.button("🔮 Predict & Generate Graph", on_click=get_prediction)

# 📊 Company Data Tab (Compare Multiple Companies)
with tab2:
    st.title("📊 Compare Company Financials")

    tickers = st.text_input("Enter company tickers (comma-separated):", "AAPL, TSLA, MSFT")
    tickers = [ticker.strip() for ticker in tickers.split(",")]

    compare_data = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        try:
            revenue = stock.financials.loc["Total Revenue"].iloc[0]
            r_and_d = stock.financials.loc["Research Development"].iloc[0] if "Research Development" in stock.financials.index else revenue * 0.05
            compare_data.append({"Company": ticker, "Revenue": revenue, "R&D Spend": r_and_d})
        except:
            pass

    if compare_data:
        df = pd.DataFrame(compare_data)
        st.write(df)
        st.bar_chart(df.set_index("Company")[["Revenue", "R&D Spend"]])

# 📥 Generate & Download PDF Report
def generate_pdf(revenue, predicted_r_and_d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, "AI-Powered R&D Investment Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, f"Revenue: ${revenue:,.2f}", ln=True)
    pdf.cell(200, 10, f"Predicted R&D Spend: ${predicted_r_and_d:,.2f}", ln=True)
    
    pdf_file = "R&D_Report.pdf"
    pdf.output(pdf_file)
    return pdf_file

if st.button("📥 Download Report as PDF"):
    if revenue > 0:
        predicted_r_and_d = get_prediction()
        if predicted_r_and_d:
            pdf_file = generate_pdf(revenue, predicted_r_and_d)
            with open(pdf_file, "rb") as f:
                st.download_button("Download Report", f, file_name="R&D_Report.pdf")
    else:
        st.warning("⚠️ Please enter a revenue amount first.")
