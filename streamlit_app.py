import streamlit as st
import requests

# Set the title of the dashboard
st.title("AI-Powered R&D Investment Predictor 🚀")

# User input: Revenue amount
revenue = st.number_input("Enter Company Revenue ($)", min_value=0, step=1000000)

# API URL (Replace with your actual Render API URL)
API_URL = "https://your-app-name.onrender.com/predict"

# Predict button
if st.button("Predict R&D Spend"):
    if revenue > 0:
        # Send a request to the API
        data = {"Revenue": revenue}
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"💡 Predicted R&D Investment: ${prediction['Predicted R&D Spend']:.2f}")
        else:
            st.error("⚠️ Error: Could not fetch prediction from API.")
    else:
        st.warning("⚠️ Please enter a revenue amount greater than 0.")
