import streamlit as st

def main():
    st.set_page_config(page_title="Farm Budget Planner", page_icon="🌾")
    st.title("🌾 Farm Budget Planner Chatbot")

    st.markdown("Plan your farm expenses, estimate income, and calculate profit easily!")

    # Crop selection
    crop = st.selectbox("Select a crop type:", ["Rice", "Wheat", "Maize", "Vegetables", "Others"])

    # Land area input
    land_area = st.number_input("Enter land area (in hectares):", min_value=0.1, step=0.1)

    # Expenses
    st.subheader("Enter Estimated Costs (in ₹):")
    seed_cost = st.number_input("Seeds:", min_value=0.0, step=100.0)
    fertilizer_cost = st.number_input("Fertilizer:", min_value=0.0, step=100.0)
    labor_cost = st.number_input("Labor:", min_value=0.0, step=100.0)
    machinery_cost = st.number_input("Machinery:", min_value=0.0, step=100.0)
    misc_cost = st.number_input("Miscellaneous:", min_value=0.0, step=100.0)

    # Yield & price
    st.subheader("Expected Yield & Market Price")
    yield_per_hectare = st.number_input("Yield per hectare (kg):", min_value=0.0, step=100.0)
    market_price = st.number_input("Market price per kg (₹):", min_value=0.0, step=1.0)

    if st.button("Calculate Budget"):
        total_expense = seed_cost + fertilizer_cost + labor_cost + machinery_cost + misc_cost
        total_yield = yield_per_hectare * land_area
        total_income = total_yield * market_price
        profit = total_income - total_expense
        reserve = 0.1 * profit if profit > 0 else 0

        st.success("✅ Budget Summary")
        st.write(f"**Crop:** {crop}")
        st.write(f"**Land Area:** {land_area} hectares")
        st.write(f"**Total Expense:** ₹{total_expense:,.2f}")
        st.write(f"**Estimated Income:** ₹{total_income:,.2f}")
        st.write(f"**Estimated Profit:** ₹{profit:,.2f}")
        st.info(f"💡 Tip: Save ₹{reserve:,.2f} for unexpected costs.")

        st.balloons()

if __name__ == "__main__":
    main()
