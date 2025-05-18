import streamlit as st
import os
from datetime import datetime


form_data = {
    "name": "",
    "height": 0,
    "gender": "",
    "dob": ""
}
min_dob = datetime(1900, 1, 1)
max_dob = datetime.today()

with st.form(key="form1"):
    st.subheader("Form Example")
    form_data["name"] = st.text_input("Enter your name:")
    form_data["height"] = st.number_input("Enter your height (cm):", min_value=0, max_value=300)
    form_data["gender"] = st.selectbox("Select your gender:", ["Male", "Female"])
    form_data["dob"] = st.date_input("Enter your date of birth:", min_value=min_dob, max_value=max_dob)
    submit_button = st.form_submit_button(label="Submit")
if submit_button:
    if not all(form_data.values()):
        st.error("Please fill in all fields.")
    else:
        st.success("Form submitted successfully!")
        st.balloons()
        st.write("Form Data:")
        st.write(f"Name: {form_data['name']}")
        st.write(f"Height: {form_data['height']} cm")
        st.write(f"Gender: {form_data['gender']}")
        st.write(f"Date of Birth: {form_data['dob']}")

st.title("Form Example")
st.write("This is a simple form example.")
with st.form(key="my_form"):
    st.subheader("Text Input")
    name = st.text_input("Enter your name:")
    st.subheader("Number Input")
    age = st.number_input("Enter your age:", min_value=0, max_value=120)
    st.subheader("Checkbox")
    agree = st.checkbox("I agree to the terms and conditions")
    st.subheader("Radio Button")
    gender = st.radio("Select your gender:", ["Male", "Female", "Other"])
    st.subheader("Submit Button")
    submit_button = st.form_submit_button(label="Submit")
    st.slider("Select a range", 0, 100, (25, 75))
if submit_button:
        st.write(f"Name: {name}")
        st.write(f"Age: {age}")
        st.write(f"City: {city}")
        st.write(f"Agree: {agree}")
        st.write(f"Gender: {gender}")

st.write("Hello, Streamlit!")
st.write("한글이 잘되어야함")
st.write("中文也可以")
st.write("日本語も大丈夫です")
st.write("This is a test for the Streamlit app.1")
dict1 = {
    "key1": "value1",
    "key2": "value2"
}
3 + 7
st.write(dict1)
pressed = st.button("Click me!")
if pressed:
    st.write("Button was pressed!")
st.divider()
st.title("This is a title")
st.header("This is a header")
st.subheader("This is a subheader")
st.markdown("This is a **markdown** __text__")
st.caption("This is a caption")
code_block = """
def hello_world():
    print("Hello, world!")
"""
st.code(code_block, language="python")
st.image(os.path.join(os.getcwd(), "static", "santiago.png"), caption="산티아고 지브리스타일")
st.title("Streamlit Elements")
st.subheader("DataFrame")
import pandas as pd
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
})
st.dataframe(df)
# 수정
st.subheader("DataFrame 수정")
editable_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

st.table(df)

# Metrics
st.subheader("Metrics")
st.metric(label="Temperature", value="20 °C", delta="1 °C")
st.metric(label="Humidity", value="50 %", delta="-5 %")
st.metric(label="Wind Speed", value="10 km/h", delta="2 km/h")

st.subheader("Json and Dictionary")
json_data = {
    "name": "Alice",
    "age": 25,
    "city": "New York",
    "skills": ["Python", "Data Science", "Machine Learning"]
}
st.json(json_data)

st.write("Dictionary:", json_data)
