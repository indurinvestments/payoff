import streamlit as st
import opstrat as op

# Initialize session state variables
if 'strategy_added' not in st.session_state:
    st.session_state.strategy_added = False
if 'editing' not in st.session_state:
    st.session_state.editing = False

# Main App Logic
def main_app():
    # Add Strategy Button
    if st.button("Add Strategy"):
        st.session_state.strategy_added = True
        st.experimental_rerun()

    if st.session_state.strategy_added:
        # Number of Legs Input
        col1, col2 = st.columns([3, 1])
        num_legs = col1.number_input("Number of Legs", min_value=1, max_value=10, value=2, step=1)
        if col2.button("Add"):
            # Initialize list for legs
            if 'legs' not in st.session_state:
                st.session_state.legs = []
            
            # Clear previous legs if editing
            if st.session_state.editing:
                st.session_state.legs = []
                st.session_state.editing = False
            
            # Generate input fields for each leg
            st.session_state.legs = []
            for i in range(num_legs):
                with st.expander(f"Leg {i+1}"):
                    op_type = st.selectbox(f"Option Type (Leg {i+1})", options=["Call", "Put"])
                    strike = st.number_input(f"Strike Price (Leg {i+1})", value=100 + i * 10, step=1)
                    tr_type = st.selectbox(f"Transaction Type (Leg {i+1})", options=["Buy", "Sell"])
                    op_pr = st.number_input(f"Option Premium (Leg {i+1})", value=5 + i * 2, step=1)
                    
                    # Append leg details to the list
                    st.session_state.legs.append({"op_type": op_type.lower()[0], "strike": strike, "tr_type": tr_type.lower()[0], "op_pr": op_pr})
            
            # Save and Plot Button
            if st.button("Save & Plot Strategy"):
                # Generate the payoff plot using Opstrat
                st.subheader("Payoff Diagram")
                op.multi_plotter(spot=100, spot_range=20, op_list=st.session_state.legs)
                
                # Edit Button
                if st.button("Edit Strategy"):
                    st.session_state.editing = True
                    st.rerun()

# Run the main app
main_app()
