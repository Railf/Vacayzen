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


def GetGuestDetails():
    col1, col2, col3, col4 = st.columns([2,1,1,1])
    location = col1.text_input("LOCATION")
    arrival = col2.date_input("ARRIVAL")
    departure  = col3.date_input("DEPARTURE")
    col4.write("")
    col4.write("")
    col4.button("START SHOPPING")

def UpdatePromotion(promotions):
    st.session_state['image'] = promotions[st.session_state['counter'] - 1]['image']
    st.session_state['title'] = promotions[st.session_state['counter'] - 1]['title']
    st.session_state['description'] = promotions[st.session_state['counter'] - 1]['description']
    


def DisplayPromotions():
    promotions = list(Vacayzen.Promotions.find())
    # st.session_state['image'] = promotions[0]['image']
    # st.session_state['title'] = promotions[0]['title']
    # st.session_state['description'] = promotions[0]['description']

    col1, col2, col3 = st.columns(3)
    col2.image(st.session_state['image'])
    col2.subheader(st.session_state['title'])
    col2.caption(st.session_state['description'])
    st.session_state['counter'] = col2.slider('promo',
    min_value=1,
    max_value=len(list(promotions)),
    label_visibility='hidden',
    on_change=UpdatePromotion(promotions))


def LandingPage(partner):
    if partner == "Vacayzen":
        st.title(partner)
    else:
        st.title(partner + " by Vacayzen")

    st.write("---")

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


GetGuestDetails()
DisplayPromotions()
# LandingPage(partner)
# DisplayAssets(partner)