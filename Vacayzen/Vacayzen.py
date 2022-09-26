from pymongo import MongoClient
import streamlit as st
import certifi

connect  = "mongodb+srv://" + st.secrets["username"] + ":" + st.secrets["password"] + "@vacadb.dfmrc.mongodb.net/?retryWrites=true&w=majority"
client   = MongoClient(connect, tlsCAFile=certifi.where())
Vacayzen = client["Vacayzen"]

st.set_page_config( page_title="Vacayzen", page_icon=":bike:", layout="wide" )

params = st.experimental_get_query_params()

partners = ["Vacayzen", "360 Blue", "Royal Destinations"]

partner = ""

if "partner" in params.keys():
    partner = params["partner"][0]
else:
    partner = "Vacayzen"

if partner not in partners: partner = "Vacayzen"


def LandingPage(partner):
    if partner == "Vacayzen":
        st.title(partner)
    else:
        st.title(partner + " by Vacayzen")

    st.write("---")

def GetDates():
    col1, col2 = st.columns(2)

    col1.date_input("ARRIVAL")
    col2.date_input("DEPARTURE")

def DisplayAssets(partner):
    cart = []
    column = 1
    col1, col2, col3 = st.columns(3)
    for asset in Vacayzen.Assets.find({"sites": {"$in": [partner]}}):
        if column == 1:
            col1.header(asset["title"])
            col1.write(asset["price"])
            col1.image(asset["image"], width=300)
            col1.button("ADD TO CART", key=asset["_id"])
            
            column = 2

        elif column == 2:
            col2.header(asset["title"])
            col2.write(asset["price"])
            col2.image(asset["image"], width=300)
            col2.button("ADD TO CART", key=asset["_id"])

            column = 3

        else:
            col3.header(asset["title"])
            col3.write(asset["price"])
            col3.image(asset["image"], width=300)
            col3.button("ADD TO CART",key=asset["_id"])
            column = 1


LandingPage(partner)
GetDates()
DisplayAssets(partner)

st.sidebar.title("SHOPPING CART")
st.sidebar.button("CHECK OUT")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.write("###")
st.sidebar.title("DISCOUNT PROGRESS")
st.sidebar.write("(5% OFF) Order Contains 4 Categories")
st.sidebar.progress(10)
st.sidebar.write("(5% OFF) Order is over $400")
st.sidebar.progress(10)