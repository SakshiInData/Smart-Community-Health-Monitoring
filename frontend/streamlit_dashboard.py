import streamlit as st
import pandas as pd

st.title("Smart Community Health Monitoring")

# Demo symptom reporting
st.header("Submit Symptom Report")
village = st.text_input("Village name")
cases = st.number_input("Diarrhea cases", 0, 100)

if st.button("Submit"):
    st.success(f"Report submitted for {village} ({cases} cases)")
