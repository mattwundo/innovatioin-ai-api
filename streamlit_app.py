import streamlit as st
import requests

# Set the page layout
st.set_page_config(page_title="AI R&D Predictor", page_icon="🚀", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    h1 {color: #2E86C1;}
    .stButton>button {background-color: #2E86C1; color: white; font-size: 18px;}
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🚀 AI-Powered R&D Investment Predictor")

# User Input
st.subheader("📊 Enter Company Financial Data")
revenue = st.number_input("Enter Company Revenue ($)", min_value=0, step=1000000)

# API URL (Replace with your actual Render API URL)
API_URL = "https://your-app-name.onrender.com/predict"

# Predict Button
if st.button("🔮 Predict R&D Spend"):
    if revenue > 0:
        # Send request to API
        data = {"Revenue": revenue}
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"💡 Predicted R&D Investment: **${prediction['Predicted R&D Spend']:.2f}**")
        else:
            st.error("⚠️ Error: Could not fetch prediction from API.")
    else:
        st.warning("⚠️ Please enter a revenue amount greater than 0.")
