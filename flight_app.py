import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Configuration & Data ---
st.set_page_config(page_title="SkyHigh Flights", page_icon="✈️", layout="wide")

# Mock Data for Flights
def get_flights_hyd_to_goi():
    data = [
        {"Airline": "IndiGo", "Flight No": "6E-554", "Departure": "06:00", "Duration": "1h 15m", "Price": 3500},
        {"Airline": "SpiceJet", "Flight No": "SG-102", "Departure": "09:30", "Duration": "1h 20m", "Price": 3200},
        {"Airline": "Air India", "Flight No": "AI-889", "Departure": "13:45", "Duration": "1h 10m", "Price": 4100},
        {"Airline": "Vistara", "Flight No": "UK-876", "Departure": "17:00", "Duration": "1h 15m", "Price": 4500},
        {"Airline": "IndiGo", "Flight No": "6E-221", "Departure": "21:15", "Duration": "1h 10m", "Price": 3800},
    ]
    return pd.DataFrame(data)

def get_flights_goi_to_hyd():
    data = [
        {"Airline": "IndiGo", "Flight No": "6E-555", "Departure": "08:00", "Duration": "1h 15m", "Price": 3600},
        {"Airline": "SpiceJet", "Flight No": "SG-103", "Departure": "11:30", "Duration": "1h 20m", "Price": 3300},
        {"Airline": "Air India", "Flight No": "AI-890", "Departure": "15:45", "Duration": "1h 10m", "Price": 4200},
        {"Airline": "Vistara", "Flight No": "UK-877", "Departure": "19:00", "Duration": "1h 15m", "Price": 4600},
        {"Airline": "IndiGo", "Flight No": "6E-222", "Departure": "23:15", "Duration": "1h 10m", "Price": 3900},
    ]
    return pd.DataFrame(data)

# --- UI Layout ---

st.title("✈️ SkyHigh Flight Booking")
st.markdown("### Book your flights from **Hyderabad (HYD)** to **Goa (GOI)**")
st.markdown("---")

# Date Selection
col1, col2 = st.columns(2)
with col1:
    dep_date = st.date_input("Departure Date", min_value=datetime.today())
with col2:
    ret_date = st.date_input("Return Date", min_value=dep_date + timedelta(days=1))

st.markdown("---")

# Load Data
df_outbound = get_flights_hyd_to_goi()
df_inbound = get_flights_goi_to_hyd()

# Flight Selection
st.subheader("1. Select Outbound Flight (HYD → GOI)")

# Helper to format radio button options nicely
def format_flight_option(row):
    return f"{row['Airline']} ({row['Flight No']}) | 🕒 {row['Departure']} | ⏳ {row['Duration']} | ₹{row['Price']}"

# Outbound
outbound_options = df_outbound.apply(format_flight_option, axis=1).tolist()
selected_outbound_str = st.radio("Choose your outbound flight:", outbound_options, key="outbound")

# Find the selected row data
selected_outbound_idx = outbound_options.index(selected_outbound_str)
selected_outbound_flight = df_outbound.iloc[selected_outbound_idx]

st.markdown("---")

st.subheader("2. Select Return Flight (GOI → HYD)")

# Inbound
inbound_options = df_inbound.apply(format_flight_option, axis=1).tolist()
selected_inbound_str = st.radio("Choose your return flight:", inbound_options, key="inbound")

# Find the selected row data
selected_inbound_idx = inbound_options.index(selected_inbound_str)
selected_inbound_flight = df_inbound.iloc[selected_inbound_idx]

st.markdown("---")

# Booking Section
if st.button("Book Ticket", type="primary", use_container_width=True):
    # Calculate Total
    total_price = selected_outbound_flight['Price'] + selected_inbound_flight['Price']
    
    # Success Message
    st.success("🎉 Booking Confirmed! Have a safe trip.")
    
    # Summary Card
    with st.container():
        st.markdown("### 🧾 Booking Summary")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.info("**Outbound Flight**")
            st.write(f"**Date:** {dep_date.strftime('%d %b %Y')}")
            st.write(f"**Airline:** {selected_outbound_flight['Airline']}")
            st.write(f"**Flight:** {selected_outbound_flight['Flight No']}")
            st.write(f"**Time:** {selected_outbound_flight['Departure']}")
            st.write(f"**Price:** ₹{selected_outbound_flight['Price']}")
            
        with c2:
            st.info("**Return Flight**")
            st.write(f"**Date:** {ret_date.strftime('%d %b %Y')}")
            st.write(f"**Airline:** {selected_inbound_flight['Airline']}")
            st.write(f"**Flight:** {selected_inbound_flight['Flight No']}")
            st.write(f"**Time:** {selected_inbound_flight['Departure']}")
            st.write(f"**Price:** ₹{selected_inbound_flight['Price']}")
        
        st.markdown("---")
        st.metric(label="Total Amount Paid", value=f"₹{total_price}")

