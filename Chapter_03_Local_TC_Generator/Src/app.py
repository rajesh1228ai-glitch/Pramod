import streamlit as st

st.set_page_config(page_title="Jira Test Case Generator", layout="wide")

page = st.sidebar.selectbox("Select page", ["Chat", "Settings"])

if page == "Chat":
    from pages.chat import render
    render()
else:
    from pages.settings import render
    render()
