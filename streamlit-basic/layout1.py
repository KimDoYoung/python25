import streamlit as st
# sidebar
st.sidebar.title("Sidebar")
st.sidebar.write("This is a sidebar.")
sidebar_input = st.sidebar.text_input("Enter something:")

tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.write("This is Tab 1.")
    st.write(f"Sidebar input: {sidebar_input}")
    st.button("Button in Tab 1")
with tab2:
    st.write("This is Tab 2.")
    st.button("Button in Tab 2")
with tab3:
    st.write("This is Tab 3.")
    st.button("Button in Tab 3")

with st.container(border=True):
    st.write("This is a container.")
    st.button("Button in Container")

placeholder = st.empty()
with placeholder.container():
    st.write("This is a placeholder.")
    st.button("Button in Placeholder")
    st.text_input("Enter something in Placeholder:")

with st.expander("Expander", expanded=True):
    st.write("This is an expander.")
    st.button("Button in Expander")
    st.text_input("Enter something in Expander:")