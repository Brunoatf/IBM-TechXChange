import json
import os
import streamlit as st
import pandas as pd
from rich import print

def import_products():
    file = st.file_uploader("Upload your products here", type=["csv"])

    if file is not None:
        df = pd.read_csv(file)
        st.write(df)

        return df.to_dict(orient='records')
    return None

def create_seller():
    st.title("Create your own sales agent in 5 minutes 🚀")
    seller_name = st.text_input("Seller Name", value="", max_chars=100)
    seller_description = st.text_area("Seller Description", value="", max_chars=500)
    products = import_products()

    if st.button("Confirm"):
        if seller_name and seller_description and products:
            # Store seller in session state
            seller = {
                "name": seller_name,
                "description": seller_description,
                "products": products
            }
            st.session_state["seller"] = seller
            st.success("Seller created successfully!")
            show_seller(seller)
            return seller
        else:
            st.error("Please complete all fields and upload products.")

def show_products(products):
    st.title("Product List")

    for product in products:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 4, 2, 2])

            with col1:
                st.image("https://via.placeholder.com/100", width=80) 
                st.subheader(product['product'])
            
            with col2:
                st.write(product['description'])

            with col3:
                st.metric(label="Stock", value=product['stock'])

            with col4:
                st.metric(label="Price ($)", value=product['price'])

            # Add a horizontal divider
            st.divider()

def show_seller(seller):
    
    name = seller["name"]
    description = seller["description"]
    products = seller["products"]

    st.write(f"## {name}")
    st.write(description)

    show_products(products)

def save_seller(seller: dict):
    os.makedirs("ibm/chat_interface/collect_data", exist_ok=True)

    file_path = os.path.join("ibm/chat_interface/collect_data", "seller.json")

    with open(file_path, "w") as f:
        json.dump(seller, f, indent=4)

def company_page():
    st.write("## Create your seller.")

    if "seller" not in st.session_state:
        st.session_state["seller"] = None

    seller = create_seller()

    if seller:
        save_seller(seller)
        st.write("## Seller saved successfully.")



    