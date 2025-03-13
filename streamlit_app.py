import streamlit as st
import requests
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Set up Streamlit page
st.set_page_config(page_title="AI R&D Predictor", page_icon="🚀", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    h1 {color: #2E86C1;}
    .stButton>button {background-color: #2E86C1; color: white; font-size: 18px;}
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation & company data
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

# Main Title
st.title("🚀 AI-Powered R&D Investment Predictor")

# User Input Section
st.subheader("📊 Enter Company Financial Data")
revenue = st.number_input("Enter Company Revenue ($)", min_value=0, step=1000000, key="revenue_input")

# API URL (Replace with actual Render API URL)
API_URL = "https://your-app-name.onrender.com/predict"

# Function to make API request
def get_prediction():
    if revenue > 0:
        data = {"Revenue": revenue}
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            prediction = response.json()
            st.success(f"💡 Predicted R&D Investment: **${prediction['Predicted R&D Spend']:.2f}**")

            # Generate R&D vs Revenue Chart
            revenue_values = np.linspace(1, revenue, 10)
            predicted_values = [prediction["Predicted R&D Spend"] * (r / revenue) for r in revenue_values]

            fig, ax = plt.subplots()
            ax.plot(revenue_values, predicted_values, marker='o', color="blue", label="Predicted R&D")
            ax.set_xlabel("Revenue ($)")
            ax.set_ylabel("Predicted R&D Spend ($)")
            ax.legend()
            st.pyplot(fig)

        else:
            st.error("⚠️ Error: Could not fetch prediction from API.")
    else:
        st.warning("⚠️ Please enter a revenue amount greater than 0.")

# Predict Button
st.button("🔮 Predict R&D Spend", on_click=get_prediction)
