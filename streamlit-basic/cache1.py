import streamlit as st
import time

@st.cache_data(ttl=60, show_spinner=True)
def fetch_data():
    time.sleep(3)  # Simulate a long computation
    return {"data": "This is some data"}

st.title("Caching Example")
data = fetch_data()
st.write(data)
st.write("This is a simple example of caching in Streamlit.")