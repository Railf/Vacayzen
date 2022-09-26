from pymongo import MongoClient

import streamlit as st

import certifi

connect  = "mongodb+srv://" + st.secrets["username"] + ":" + st.secrets["password"] + "@vacadb.dfmrc.mongodb.net/?retryWrites=true&w=majority"

client   = MongoClient(connect, tlsCAFile=certifi.where())

Vacayzen = client["Vacayzen"]

st.set_page_config(
    page_title="Vacayzen",
    page_icon="V",
    layout="wide"
)

params = st.experimental_get_query_params()

st.title(params["affiliate"])