import streamlit as st

file_path = "example.txt"

@st.cache_resource
def get_file_handler():
    file = open (file_path, "a+")
    return file

file_handler = get_file_handler()

if st.button("Write to file"):
    file_handler.write("Hello, Streamlit!\n")
    file_handler.flush()  # Ensure data is written to the file
    st.success("Data written to file.")

if st.button("Read from file"):
    file_handler.seek(0)  # Move the cursor to the beginning of the file
    content = file_handler.read()
    st.text(content)

if st.button("Close file"):
    file_handler.close()
    st.success("File closed.")