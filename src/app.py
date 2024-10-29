import requests
import streamlit as st

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

API_BASE_URL = "http://0.0.0.0:8000/api/v1"
API_USERS_URL = f"{API_BASE_URL}/users"

if st.button("Login"):
    response = requests.post(
        f"{API_USERS_URL}/login", json={"username": username, "password": password}
    )
    response.raise_for_status()  # Levanta un error para códigos de estado HTTP 4xx/5xx

    if response.status_code == 200:
        st.success("Login successful!")
        # Navegar a la página de tabla
        st.session_state.page = "table"  # Cambia el estado de la página
    else:
        st.error("Invalid username or password")
