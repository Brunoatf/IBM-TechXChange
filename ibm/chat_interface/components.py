import streamlit as st
import pandas as pd

def import_products():
    file = st.file_uploader("Upload Excel file", type=["xlsx", "csv"])

    if file is not None:
        df = pd.read_excel(file)
        st.write(df)


def create_seller():
    st.title("Create your own sales agent in 5 minutes 🚀")

    seller_name = st.text_input("Seller Name")
    seller_description = st.text_area("Seller Description")

    seller = {
        "name": seller_name,
        "description": seller_description,
    }

    import_products()

    return seller