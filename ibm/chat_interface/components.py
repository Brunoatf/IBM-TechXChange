import json
import os
import streamlit as st
import pandas as pd

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.bot import Chatbot

def import_products():
    """Função para importar catálogo de produtos"""
    file = st.file_uploader("Upload your product catalog here", type=["csv"])

    if file is not None:
        df = pd.read_csv(file)
        st.write(df)
        return df.to_dict(orient='records')
    return None

def create_seller():
    """Criação do assistente de vendas"""
    st.title("Let's begin!")
    st.write("Create your own sales agent in 5 minutes with the help of IBM Watsonx 🚀")
    
    # Nome da empresa
    seller_name = st.text_input("Company Name", value="", max_chars=100)
    
    # Descrição da empresa
    seller_description = st.text_area("Company Description", value="", max_chars=500)
    
    # Importar produtos
    products = import_products()

    # Dropdown para selecionar modelo de IA
    model_choices = ["mistralai/mistral-large", "llama-3-405b-instruct"]
    selected_model = st.selectbox("Select your AI model", model_choices)

    # Campos de senha para IBM API Key e IBM Project ID
    ibm_api_key = st.text_input("IBM API Key", type="password", help="Enter your IBM API Key")
    ibm_project_id = st.text_input("IBM Project ID", type="password", help="Enter your IBM Project ID")

    # Confirmação
    if st.button("Confirm"):
        if seller_name and seller_description and products and ibm_api_key and ibm_project_id:
            # Armazenar informações do vendedor no estado da sessão
            seller = {
                "name": seller_name,
                "description": seller_description,
                "products": products,
                "ai_model": selected_model,
                "ibm_api_key": ibm_api_key,
                "ibm_project_id": ibm_project_id
            }
            st.session_state["seller"] = seller
            st.success("Seller created successfully!")
            show_seller(seller)
            return seller
        else:
            st.error("Please complete all fields, including the API Key and Project ID.")

def show_products(products):
    """Exibição de produtos"""
    st.title("Product List")

    for product in products:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 4, 2, 2])

            with col1:
                st.image("https://via.placeholder.com/100", width=80)  # Placeholder para imagens dos produtos
                st.subheader(product['product'])
            
            with col2:
                st.write(product['description'])

            with col3:
                st.metric(label="Stock", value=product['stock'])

            with col4:
                st.metric(label="Price ($)", value=product['price'])

            # Divisor horizontal
            st.divider()

def show_seller(seller):
    """Mostra as informações do vendedor"""
    name = seller["name"]
    description = seller["description"]
    products = seller["products"]
    ai_model = seller["ai_model"]

    st.write(f"## {name}")
    st.write(f"**Description**: {description}")
    st.write(f"**Selected AI Model**: {ai_model}")

    # Mostrar lista de produtos
    show_products(products)

def save_seller(seller: dict):
    """Salva informações do vendedor em um arquivo JSON"""
    os.makedirs("ibm/chat_interface/collect_data", exist_ok=True)

    file_path = os.path.join("ibm/chat_interface/collect_data", "seller.json")

    with open(file_path, "w") as f:
        json.dump(seller, f, indent=4)

def company_page():
    """Página da empresa"""
    if "seller" not in st.session_state:
        st.session_state["seller"] = None

    seller = create_seller()

    if seller:
        save_seller(seller)
        st.write("## Seller saved successfully.")

        st.session_state["chatbot"] = Chatbot(
            business=seller["name"],
            business_description=seller["description"],
            products=seller["products"],
            ibm_api_key=seller["ibm_api_key"],
            ibm_project_id=seller["ibm_project_id"],
            model_id=seller["ai_model"]
        )