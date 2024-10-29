from enum import Enum
import os
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "")
API_USERS_URL = f"{API_BASE_URL}/users"


class Pages(str, Enum):
    login = "login",
    user_list = "user_list"


def show_login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        credentials = {"email": username, "password": password}

        response = requests.post(
            f"{API_USERS_URL}/login",
            json=credentials
        )

        response.raise_for_status()

        if response.status_code == 200:
            st.success("Login successful!")
            st.session_state.token = response.json().get("access_token")
            st.session_state.page = Pages.user_list
            st.session_state.reload = True
        else:
            st.error("Invalid username or password")


def show_users_list():
    st.title("Users")

    response = requests.get(
        f"{API_USERS_URL}/all",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )

    response.raise_for_status()

    users_data = response.json()

    df = pd.DataFrame(users_data)
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gridOptions = gb.build()

    AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)


if 'page' not in st.session_state:
    st.session_state.page = Pages.login

if 'reload' not in st.session_state:
    st.session_state.reload = False


if st.session_state.page == Pages.login:
    show_login_page()
elif st.session_state.page == Pages.user_list:
    show_users_list()
