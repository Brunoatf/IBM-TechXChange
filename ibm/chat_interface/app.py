import json
import os
import streamlit as st
import pandas as pd
from components import company_page

def load_cart():
    """Carrega o estado atual do carrinho de um arquivo JSON"""
    cart_file = "ibm/chat_interface/cart.json"
    
    if os.path.exists(cart_file):
        with open(cart_file, "r") as f:
            return json.load(f)
    else:
        return {}

def show_cart():
    """Exibe o estado atual do carrinho"""
    st.title("Current Cart Status")
    
    cart = load_cart()
    
    if cart:
        total_items = sum(item['quantity'] for item in cart.values())
        total_price = sum(item["total_price"] for item in cart.values())

        st.write(f"Total Items: {total_items}")
        st.write(f"Total Price: ${total_price:.2f}")

        st.write("### Cart Details")
        for product_name, details in cart.items():
            st.write(f"**{product_name}**")
            st.write(f"Price: ${details['price']} - Quantity: {details['quantity']}")
            st.divider()

    else:
        st.write("Your cart is currently empty.")

# Set page title
st.set_page_config(page_title="Watsell", page_icon="🛒", layout="wide")

# Hide default Streamlit footer and menu
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       .block-container {
           padding-left: 10px !important;
           padding-right: 10px !important;
           max-width: 95% !important;
       }
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 3em; color: #2c5ad4;">Hello, I'm Watsell! 💬</h1>
        <p style="font-size: 1.5em; color: #555;">The customizable sales agent for your business</p>
    </div>
    """, unsafe_allow_html=True)

# Add tabs for Configurations, Chat, and Cart
tab1, tab2, tab3 = st.tabs(["Configurations", "Chat", "Cart"])

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chatbot" in st.session_state:
    company = st.session_state["chatbot"].business
    st.session_state["messages"].append(
        {"role": "assistant", "content": "Hello, I'm Watsell, shopping assistant for {business}! How can I help you today?"}
    )

# Tab 1: Configurations
with tab1:
    company_page()

# Tab 2: Chat tab (left unchanged)
with tab2:

    def display_textual_message(message: dict) -> None:
        """Displays textual messages in the chat window."""
        role = message["role"]
        content = message["content"]
        content = content.replace("$", "\\$")
        st.chat_message(role).write(content)

    def display_messages(messages=st.session_state.get("messages", [])) -> None:
        """Displays messages in the chat window."""
        st.session_state["messages"] = messages
        for msg in messages:
            if msg["role"] in ["assistant", "user"]:
                display_textual_message(msg)

    def process_message(user_message: str) -> None:
        """Receives user message and processes it."""
        with st.spinner("Please wait while your message is processed..."):
            response = st.session_state["chatbot"].get_response(user_message)
            response_dict = {"role": "assistant", "content": response}
            st.session_state["messages"].append(response_dict)

    # Chat input at the bottom
    user_message = st.chat_input(placeholder="Type your message here...")

    display_messages()

    if user_message:
        # Append user message and display it immediately
        st.session_state["messages"].append({"role": "user", "content": user_message})
        st.chat_message("user").write(user_message)

        # Process the message and get the chatbot's response
        process_message(user_message)
        st.rerun()

# Tab 3: Cart tab to show current cart status
with tab3:
    show_cart()
