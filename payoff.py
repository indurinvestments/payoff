import streamlit as st
import opstrat as op
import matplotlib.pyplot as plt

# Initialize session state variables
if 'strategy_added' not in st.session_state:
    st.session_state.strategy_added = False
if 'num_legs' not in st.session_state:
    st.session_state.num_legs = 0
if 'legs' not in st.session_state:
    st.session_state.legs = []

# Function to reset legs and strategy state
def reset_strategy():
    st.session_state.strategy_added = False
    st.session_state.num_legs = 0
    st.session_state.legs = []

# Main App Logic
def main_app():
    # Add Strategy Button
    if not st.session_state.strategy_added:
        if st.button("Add Strategy"):
            st.session_state.strategy_added = True

    # Number of Legs Input
    if st.session_state.strategy_added and not st.session_state.num_legs:
        num_legs = st.number_input("Enter Number of Legs", min_value=1, max_value=10, value=2, step=1)
        if st.button("Confirm Number of Legs"):
            st.session_state.num_legs = num_legs

    # Input Fields for Each Leg
    if st.session_state.num_legs > 0:
        st.write("Configure Each Leg")
        for i in range(st.session_state.num_legs):
            if len(st.session_state.legs) < st.session_state.num_legs:
                # Initialize leg details in session state with quantity
                st.session_state.legs.append({"op_type": "c", "strike": 100, "tr_type": "b", "op_pr": 5, "quantity": 10})
            
            # Display input fields for each leg dynamically in a row
            with st.expander(f"Leg {i+1}"):
                col1, col2, col3, col4, col5 = st.columns(5)
                op_type = col1.selectbox(f"Option Type", options=["Call", "Put"], key=f"op_type_{i}")
                strike = col2.number_input(f"Strike Price", value=st.session_state.legs[i].get("strike", 100), step=1, key=f"strike_{i}")
                tr_type = col3.selectbox(f"Transaction Type", options=["Buy", "Sell"], key=f"tr_type_{i}")
                op_pr = col4.number_input(f"Option Premium", value=st.session_state.legs[i].get("op_pr", 5), step=1, key=f"op_pr_{i}")
                quantity = col5.number_input(f"Quantity", value=st.session_state.legs[i].get("quantity", 10), step=1, key=f"quantity_{i}")

                # Update session state with new values
                st.session_state.legs[i] = {"op_type": op_type.lower()[0], "strike": strike, "tr_type": tr_type.lower()[0], "op_pr": op_pr, "quantity": quantity}

        # Save and Plot Button
        if st.button("Save & Plot Strategy"):
            if len(st.session_state.legs) == st.session_state.num_legs:
                # Generate the payoff plot using Opstrat
                spot = 100  # Example spot price; this can be made dynamic as well.
                spot_range = 20  # Example spot range; this can also be dynamic.
                
                # Create a figure to display the plot
                fig, ax = plt.subplots()
                op.multi_plotter(spot=spot, spot_range=spot_range, op_list=st.session_state.legs)
                plt.savefig('payoff_plot.png', bbox_inches='tight')
                st.image('payoff_plot.png')  # Display the plot in Streamlit
                
                # Show Edit Button after plotting
                if st.button("Edit Strategy"):
                    reset_strategy()

# Run the main app
main_app()
