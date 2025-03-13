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
tab1, tab2, tab3 = st.tabs(["🔮 AI Prediction", "📊 Company Data", "📈 R&D Trends"])

# 🔮 AI Prediction Tab
with tab1:
    st.title("🚀 AI-Powered R&D Investment Predictor")
    revenue = st.number_input("Enter Company Revenue ($)", min_value=0, step=1000000, key="revenue_input")

    # API URL (Replace with actual Render API URL)
    API_URL = "https://your-app-name.onrender.com/predict"

    def get_prediction():
        if revenue > 0:
            with st.spinner("🔄 Fetching AI prediction..."):
                time.sleep(2)  # Simulate loading time
                data = {"Revenue": revenue}
                response = requests.post(API_URL, json=data)

                if response.status_code == 200:
                    prediction = response.json()
                    predicted_r_and_d = prediction["Predicted R&D Spend"]
                    st.success(f"💡 Predicted R&D Investment: **${predicted_r_and_d:,.2f}**")

                    # Generate R&D vs Revenue Chart
                    revenue_values = np.linspace(1, revenue, 10)
                    predicted_values = [predicted_r_and_d * (r / revenue) for r in revenue_values]

                    fig, ax = plt.subplots()
                    ax.plot(revenue_values, predicted_values, marker='o', color="blue", label="Predicted R&D")
                    ax.set_xlabel("Revenue ($)")
                    ax.set_ylabel("Predicted R&D Spend ($)")
                    ax.legend()
                    st.pyplot(fig)

                    return predicted_r_and_d
                else:
                    st.error("⚠️ Error: Could not fetch prediction from API.")
        else:
            st.warning("⚠️ Please enter a revenue amount greater than 0.")
        return None

    st.button("🔮 Predict R&D Spend", on_click=get_prediction)

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

        # Generate a bar chart
        st.bar_chart(df.set_index("Company")[["Revenue", "R&D Spend"]])

# 📈 R&D Trends Tab (Compare with Industry Benchmarks)
with tab3:
    st.title("📈 R&D Spending Trends")
    
    industry_averages = {
        "Tech": 0.15,  # Tech companies spend ~15% of revenue on R&D
        "Pharma": 0.20,  # Pharma companies ~20%
        "Automotive": 0.05  # Automotive ~5%
    }

    st.subheader("📊 Compare to Industry Benchmarks")
    industry = st.selectbox("Select Industry", list(industry_averages.keys()))

    if revenue > 0:
        benchmark_r_and_d = revenue * industry_averages[industry]
        st.write(f"📌 Industry-standard R&D investment for {industry}: **${benchmark_r_and_d:,.2f}**")

# 📥 Generate & Download PDF Report
def generate_pdf(revenue, predicted_r_and_d, benchmark_r_and_d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, "AI-Powered R&D Investment Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, f"Revenue: ${revenue:,.2f}", ln=True)
    pdf.cell(200, 10, f"Predicted R&D Spend: ${predicted_r_and_d:,.2f}", ln=True)
    pdf.cell(200, 10, f"Industry Benchmark R&D Spend: ${benchmark_r_and_d:,.2f}", ln=True)
    
    pdf_file = "R&D_Report.pdf"
    pdf.output(pdf_file)
    return pdf_file

if st.button("📥 Download Report as PDF"):
    if revenue > 0:
        predicted_r_and_d = get_prediction()
        if predicted_r_and_d:
            benchmark_r_and_d = revenue * industry_averages[industry]
            pdf_file = generate_pdf(revenue, predicted_r_and_d, benchmark_r_and_d)
            with open(pdf_file, "rb") as f:
                st.download_button("Download Report", f, file_name="R&D_Report.pdf")
    else:
        st.warning("⚠️ Please enter a revenue amount first.")
