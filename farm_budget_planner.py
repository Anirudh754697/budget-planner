import streamlit as st
import time
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="Farm Budget Planner", page_icon="🌾")
    st.title("🌾 Farm Budget Planner Chatbot")

    st.markdown("Welcome to your personalized Farm Budget Planner! Let's go step by step.")

    # Sidebar for user to select crop type
    st.sidebar.header("Farm Budget Planner - Chatbot")
    crop = st.sidebar.selectbox("Select your crop:", ["Rice", "Wheat", "Maize", "Vegetables", "Others"])
    
    st.write(f"**You selected:** {crop}")

    # Question 1: Input land area
    land_area = st.number_input("How much land area (in hectares) do you have?", min_value=0.1, step=0.1)
    if land_area > 0:
        st.write(f"**Land area:** {land_area} hectares")
    else:
        st.write("Please provide a valid land area.")

    # Expenses Section
    st.subheader("Enter your Estimated Costs (in ₹):")
    seed_cost = st.number_input("How much do you plan to spend on seeds?", min_value=0.0, step=100.0)
    fertilizer_cost = st.number_input("How much do you plan to spend on fertilizers?", min_value=0.0, step=100.0)
    labor_cost = st.number_input("How much do you plan to spend on labor?", min_value=0.0, step=100.0)
    machinery_cost = st.number_input("How much do you plan to spend on machinery?", min_value=0.0, step=100.0)
    misc_cost = st.number_input("Any miscellaneous costs (e.g., transportation)?", min_value=0.0, step=100.0)

    # Question 2: Input yield and price
    st.subheader("Expected Yield & Market Price")
    yield_per_hectare = st.number_input("What is the expected yield per hectare (in kg)?", min_value=0.0, step=100.0)
    market_price = st.number_input("What is the market price per kg (₹)?", min_value=0.0, step=1.0)

    # **Step 4: Add a Progress Bar or Spinner**
    # Create a button to calculate
    if st.button("Calculate My Farm Budget"):
        with st.spinner('Calculating your budget...'):
            time.sleep(2)  # Simulating a delay for calculations

            # **Step 2: Make it Conversational (Chatbot Flow)**
            total_expense = seed_cost + fertilizer_cost + labor_cost + machinery_cost + misc_cost
            total_yield = yield_per_hectare * land_area
            total_income = total_yield * market_price
            profit = total_income - total_expense
            reserve = 0.1 * profit if profit > 0 else 0

            # **Step 3: Personalized Feedback**
            st.success("✅ Budget Summary")
            st.write(f"**Crop Selected:** {crop}")
            st.write(f"**Land Area:** {land_area} hectares")
            st.write(f"**Total Expense:** ₹{total_expense:,.2f}")
            st.write(f"**Estimated Income:** ₹{total_income:,.2f}")
            st.write(f"**Estimated Profit:** ₹{profit:,.2f}")
            st.info(f"💡 Tip: Save ₹{reserve:,.2f} for unexpected costs.")
            
            # **Step 6: Add Graphs & Visualizations (Pie Chart)**
            labels = ['Seeds', 'Fertilizers', 'Labor', 'Machinery', 'Miscellaneous']
            sizes = [seed_cost, fertilizer_cost, labor_cost, machinery_cost, misc_cost]

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

            st.pyplot(fig)

            # **Step 5: Add Dynamic Chatbot-like Interaction**
            # Show a balloon effect when the calculation is done.
            st.balloons()

if __name__ == "__main__":
    main()
