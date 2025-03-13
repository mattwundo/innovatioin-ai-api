import streamlit as st
import requests

# Set up Streamlit page with sidebar
st.set_page_config(page_title="AI R&D Predictor", page_icon="🚀", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    h1 {color: #2E86C1;}
    .stButton>button {background-color: #2E86C1; color: white; font-size: 18px;}
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔍 Navigation")
st.sidebar.info("Use this app to predict R&D investment based on company revenue!")

# Main title
st.title("🚀 AI-Powered R&D Investment Predictor")

# User input section
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
        else:
            st.error("⚠️ Error: Could not fetch prediction from API.")
    else:
        st.warning("⚠️ Please enter a revenue amount greater than 0.")

# Predict button
st.button("🔮 Predict R&D Spend", on_click=get_prediction)
