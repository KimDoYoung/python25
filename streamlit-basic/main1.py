import streamlit as st

st.title("session_state example")
count = 0

st.write(f"Counter value: {count}")

if st.button("Increment"):
    count += 1
    st.write(f"Counter value: {count}")
else:
    st.write("Counter not incremented.")

if "counter1" not in st.session_state:
    st.session_state.counter1 = 0

st.write(f"Counter value: {st.session_state.counter1}")

if st.button("Increment1"):
    st.session_state.counter1 += 1
    st.write(f"Counter value: {st.session_state.counter1}")
else:
    st.write("Counter not incremented.")

if st.button("Reset"):
    st.session_state.counter1 = 0
    st.write(f"Counter value: {st.session_state.counter1}")