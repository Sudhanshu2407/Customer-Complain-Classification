import streamlit as st
import pandas as pd
import numpy as np
import pyttsx3
import pickle

# Load the model and vectorizer
model = pickle.load(open(r"C:\sudhanshu_projects\project-task-training-course\Customer_complain_classification\customer_complain_classification.pkl", "rb"))
vectorizer = pickle.load(open(r"C:\sudhanshu_projects\project-task-training-course\Customer_complain_classification\vectorizer.pkl", "rb"))

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function for prediction
def predict_complaint(description):
    description_transformed = vectorizer.transform([description])
    prediction = model.predict(description_transformed)[0]
    return prediction

# SOP Guidelines
def get_guidelines(category):
    guidelines = {
        0: "Follow SOP for handling Credit Card Problems.",
        1: "Follow SOP for handling Retail Banking issues.",
        2: "Follow SOP for handling Credit Reporting issues.",
        3: "Follow SOP for handling Mortgages and Loans.",
        4: "Follow SOP for handling Debt Collection issues."
    }
    return guidelines.get(category, "No SOP available for this category.")

# Pages
def signup_page():
    st.title("Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Signup"):
        # Add signup logic
        st.session_state['username'] = username
        st.success("Signup successful. Please login.")

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        # Add login logic
        st.session_state['username'] = username
        st.success("Login successful.")
        st.session_state['logged_in'] = True

def main_page():
    st.title("ComplainEase")
    description = st.text_area("Enter the complaint description:")
    if st.button("Predict"):
        if description.strip():  # Check if the description is not empty
            prediction = predict_complaint(description)
            categories = ["Credit Card Problem", "Retail Banking", "Credit Reporting", "Mortgages and Loans", "Debt Collection"]
            result = categories[prediction]
            st.write(f"Prediction: {result}")
            guidelines = get_guidelines(prediction)
            st.write(guidelines)
            engine.say(f"The predicted category is {result}. {guidelines}")
            engine.runAndWait()
        else:
            st.warning("Please enter a description.")

# Logo
st.image(r"C:\sudhanshu_projects\project-task-training-course\Customer_complain_classification\logo.png", use_column_width=True)

# App flow
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Select a page", ["Signup", "Login", "Main page"])
    if menu == "Signup":
        signup_page()
    elif menu == "Login":
        login_page()
else:
    main_page()
