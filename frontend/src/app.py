import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "")
API_USERS_URL = f"{API_BASE_URL}/users"

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    credentials = {"email": username, "password": password}
    st.write(credentials)

    response = requests.post(
        f"{API_USERS_URL}/login",
        json=credentials
    )

    response.raise_for_status()

    if response.status_code == 200:
        st.success("Login successful!")
        st.session_state.page = "table"
    else:
        st.error("Invalid username or password")
