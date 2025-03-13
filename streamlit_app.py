import streamlit as st
import requests

# Set up Streamlit page
st.set_page_config(page_title="AI R&D Predictor", page_icon="🚀")

# Title
st.title("🚀 AI-Powered R&D Investment Predictor")

# User input section
st.subheader("📊 Enter Company Financial Data")

# ✅ Correct placement for the revenue input field
revenue = st.number_input("Enter Company Revenue ($)", min_value=0, step=1000000, key="revenue_input")

# API URL (Replace with actual URL)
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

# ✅ Correct placement for the "Predict" button
st.button("🔮 Predict R&D Spend", on_click=get_prediction)
