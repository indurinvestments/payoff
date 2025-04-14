import streamlit as st
import opstrat as op

# Streamlit App Title
st.title("Multi-Leg Option Strategy Visualizer")

# Sidebar for Inputs
st.sidebar.header("Configure Your Option Strategy")

# Spot Price Input
spot = st.sidebar.number_input("Current Market Price (Spot)", value=100, step=1)

# Spot Range Input
spot_range = st.sidebar.number_input("Spot Range (%)", value=20, step=1)

# Dynamic Leg Configuration
st.sidebar.subheader("Option Legs")
legs = st.sidebar.number_input("Number of Legs", min_value=1, max_value=10, value=2, step=1)

# Initialize an empty list for option legs
option_legs = []

# Collect leg details dynamically based on the number of legs
for i in range(legs):
    st.sidebar.subheader(f"Leg {i+1}")
    op_type = st.sidebar.selectbox(f"Option Type (Leg {i+1})", options=["Call", "Put"], key=f"op_type_{i}")
    strike = st.sidebar.number_input(f"Strike Price (Leg {i+1})", value=100 + i * 10, step=1, key=f"strike_{i}")
    tr_type = st.sidebar.selectbox(f"Transaction Type (Leg {i+1})", options=["Buy", "Sell"], key=f"tr_type_{i}")
    op_pr = st.sidebar.number_input(f"Option Premium (Leg {i+1})", value=5 + i * 2, step=1, key=f"op_pr_{i}")

    # Append leg details to the list
    option_legs.append({"op_type": op_type.lower()[0], "strike": strike, "tr_type": tr_type.lower()[0], "op_pr": op_pr})

# Button to Save and Plot
if st.button("Save & Plot Strategy"):
    # Generate the payoff plot using Opstrat
    st.subheader("Payoff Diagram")
    op.multi_plotter(spot=spot, spot_range=spot_range, op_list=option_legs)

# Footer
st.write("Use the sidebar to configure your strategy. Click 'Save & Plot Strategy' to visualize the payoff.")
