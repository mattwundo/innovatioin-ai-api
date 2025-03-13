import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np

st.title("📊 AI-Powered R&D Predictor")

revenue = st.number_input("Enter Company Revenue ($)", min_value=0, step=1000000)

API_URL = "https://your-app-name.onrender.com/predict"

if st.button("🔮 Predict R&D Spend"):
    if revenue > 0:
        data = {"Revenue": revenue}
        response = requests.post(API_URL, json=data)
        
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"💡 Predicted R&D Investment: **${prediction['Predicted R&D Spend']:.2f}**")

            # Create a chart
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
