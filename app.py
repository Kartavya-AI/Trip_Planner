import streamlit as st
import pandas as pd
from graph import app
from datetime import date

st.set_page_config(page_title="🚗 Road Trip Planner", layout="wide")
st.title("🚗 Travel Planner")

if "state" not in st.session_state:
    st.session_state.state = {}

with st.form("trip_form"):
    st.subheader("Enter Trip Details")
    origin = st.text_input("Starting Location", value="")
    destination = st.text_input("Destination", value="")
    travel_date = st.date_input("Travel Date",min_value=date.today())
    days = st.number_input("Number of Days", min_value=1, max_value=15, value=1)

    st.subheader("Optional Preferences")
    interests = st.text_input("Your Interests", value="")
    accommodation_budget = st.text_input("Accommodation Budget", value="")
    dietary_preferences = st.text_input("Dietary Preferences", value="")
    food_budget = st.text_input("Food Budget", value="")

    submitted = st.form_submit_button("Generate Trip Plan")

if submitted:
    st.session_state.state = {
        "origin": origin,
        "destination": destination,
        "travel_date": str(travel_date),
        "days": days,
        "interests": interests,
        "accommodation_budget": accommodation_budget,
        "dietary_preferences": dietary_preferences,
        "food_budget": food_budget,
    }

    st.session_state.state = app.invoke(st.session_state.state)

    st.success("✅ Trip Plan Generated!")

    if "finder_results" in st.session_state.state:
        st.subheader("🔎 Suggested Stops & Food Options")
        st.markdown(st.session_state.state["finder_results"])

    if "itinerary" in st.session_state.state:
        st.subheader("📅 Detailed Itinerary")
        itinerary_text = st.session_state.state["itinerary"]

        # Just render the Markdown table directly
        st.markdown(itinerary_text, unsafe_allow_html=True)


