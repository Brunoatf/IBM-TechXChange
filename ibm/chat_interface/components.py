import streamlit as st

def create_seller():
    st.title("Create Seller")

    seller_name = st.text_input("Seller Name")
    seller_description = st.text_area("Seller Description")

    seller = {
        "name": seller_name,
        "description": seller_description,
    }
    return seller