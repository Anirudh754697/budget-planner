import streamlit as st

# ✅ Set config at the very top
st.set_page_config(page_title="Farm Budget Planner", page_icon="🌾", layout="centered")

import time
import matplotlib.pyplot as plt
import requests
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if WEATHER_API_KEY:
    st.sidebar.text("🔑 API Key Loaded Successfully ✅")
else:
    st.sidebar.error("❌ API Key not found!")

# 🌤️ Weather Fetch Function
def get_weather_info(city):
    if not WEATHER_API_KEY:
        return {"error": "Missing WEATHER_API_KEY"}
    
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return {
                "location": data["location"]["name"],
                "temp": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "humidity": data["current"]["humidity"]
            }
        return {"error": f"Weather API error: {res.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# 🚜 Main App
def main():
    st.markdown("""
    <h1 style='text-align: center; color: #2E8B57;'>🌾 Farm Budget Planner Chatbot</h1>
    <h4 style='text-align: center; color: #444;'>Your Smart Assistant for Farm Budgeting</h4>
    <hr style='border: 1px solid #ccc;'>
    """, unsafe_allow_html=True)

    st.markdown("""
    This chatbot helps you:
    - 📈 Estimate income from crops/livestock  
    - 💸 Track expenses  
    - ✅ Calculate profit/loss  
    - 🧠 Get financial tips  
    - 🗓️ Generate seasonal summaries
    """)

    # Sidebar Controls
    st.sidebar.title("🚀 Let's Begin")

    farm_type = st.sidebar.radio("What kind of farm do you run?", ["Crops", "Livestock", "Mixed"])

    # 🌤️ Weather Lookup
    st.sidebar.subheader("Weather Info")
    city = st.sidebar.text_input("Enter city name")
    if st.sidebar.button("Check Weather"):
        if not city:
            st.sidebar.error("Please enter a city name to check the weather.")
        else:
            weather = get_weather_info(city)
            if "error" not in weather:
                st.sidebar.success(f"{weather['location']}: {weather['temp']}°C, {weather['condition']} (Humidity: {weather['humidity']}%)")
            else:
                st.sidebar.error(weather['error'])

    st.header("📝 Tell Us About Your Farm")

    # Input Section: Crops & Livestock
    if farm_type == "Mixed":
        st.subheader("🌾 Crop Details")
        crop_type = st.selectbox("Select crop:", ["Rice", "Wheat", "Maize"])
        crop_area = st.number_input("Land area (hectares):", min_value=0.1, step=0.1)
        crop_yield = st.number_input("Yield per hectare (kg/liters):", min_value=0.0, step=10.0)

        st.subheader("🐄 Livestock Details")
        livestock_type = st.selectbox("Select livestock:", ["Dairy", "Poultry"])
        livestock_count = st.number_input("Number of animals:", min_value=1)
        livestock_yield = st.number_input("Yield per animal (kg/liters):", min_value=0.0, step=10.0)

        st.subheader("🌱 Costs")
        seed_cost = st.number_input("Seed cost (₹):", min_value=0.0, step=100.0)
        feed_cost = st.number_input("Feed cost (₹):", min_value=0.0, step=100.0)
    else:
        if farm_type == "Crops":
            st.subheader("🌾 Crop Details")
            crop_type = st.selectbox("Select crop:", ["Rice", "Wheat", "Maize"])
            crop_area = st.number_input("Land area (hectares):", min_value=0.1)
            crop_yield = st.number_input("Yield per hectare (kg/liters):", min_value=0.0, step=10.0)
            livestock_count = livestock_yield = feed_cost = 0
            seed_cost = st.number_input("Seed cost (₹):", min_value=0.0, step=100.0)
        else:
            st.subheader("🐄 Livestock Details")
            livestock_type = st.selectbox("Select livestock:", ["Dairy", "Poultry"])
            livestock_count = st.number_input("Number of animals:", min_value=1)
            livestock_yield = st.number_input("Yield per animal (kg/liters):", min_value=0.0, step=10.0)
            crop_area = crop_yield = seed_cost = 0
            feed_cost = st.number_input("Feed cost (₹):", min_value=0.0, step=100.0)

    price_per_unit = st.number_input("Market price per unit (₹):", min_value=0.0)

    # Costs Section
    st.subheader("🏗️ Fixed Costs")
    equipment = st.number_input("Equipment (₹):", min_value=0.0, step=100.0)
    rent = st.number_input("Land/facility rent (₹):", min_value=0.0, step=100.0)
    salaries = st.number_input("Labor/Salaries (₹):", min_value=0.0, step=100.0)

    st.subheader("🧪 Variable Costs")
    fertilizers = st.number_input("Fertilizers/Water (₹):", min_value=0.0, step=100.0)
    misc = st.number_input("Miscellaneous (₹):", min_value=0.0, step=100.0)

    # 💰 Budget Calculation
    if st.button("📊 Calculate Budget"):
        with st.spinner("Calculating..."):
            time.sleep(1.5)

            if farm_type == "Mixed":
                crop_income = crop_area * crop_yield * price_per_unit
                livestock_income = livestock_count * livestock_yield * price_per_unit
                total_income = crop_income + livestock_income
                total_variable = seed_cost + feed_cost + fertilizers + misc
            elif farm_type == "Crops":
                total_income = crop_area * crop_yield * price_per_unit
                total_variable = seed_cost + fertilizers + misc
            else:
                total_income = livestock_count * livestock_yield * price_per_unit
                total_variable = feed_cost + fertilizers + misc

            total_expense = equipment + rent + salaries + total_variable
            net_profit = total_income - total_expense
            suggested_reserve = 0.1 * net_profit if net_profit > 0 else 0

            # 📋 Results
            st.success("📈 Budget Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Income", f"₹{total_income:,.2f}")
            col2.metric("Expenses", f"₹{total_expense:,.2f}")
            col3.metric("Net Profit" if net_profit >= 0 else "Loss", f"₹{net_profit:,.2f}", delta_color="inverse")

            st.info(f"💡 Tip: Save ₹{suggested_reserve:,.2f} for emergencies or future investment.")

            # 📊 Pie Chart
            labels = ['Equipment', 'Rent', 'Salaries', 'Seeds/Feed', 'Fertilizers/Water', 'Misc']
            values = [equipment, rent, salaries, seed_cost if farm_type != "Livestock" else feed_cost, fertilizers, misc]

            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis("equal")
            st.pyplot(fig)

            st.balloons()

# 🏁 Run the app
if __name__ == "__main__":
    main()
