import json
import os
import streamlit as st
import pandas as pd
from components import company_page

def load_cart():
    """Carrega o estado atual do carrinho de um arquivo JSON"""
    cart_file = "cart.json"
    
    if os.path.exists(cart_file):
        with open(cart_file, "r") as f:
            return json.load(f)
    else:
        return {}

def show_cart():
    """Exibe o estado atual do carrinho"""
    st.title("Current Cart Status")
    
    cart = load_cart()
    
    st.title("🛒 Your Shopping Cart")

    # Display each item in the cart
    for item in cart:
        # Create columns for layout (product image placeholder, name, quantity, price)
        col1, col2, col3, col4 = st.columns([2, 4, 2, 2])
        
        with col1:
            # Placeholder for product image (replace with actual image if available)
            st.image("https://picsum.photos/100/100", width=80)
            
        with col2:
            st.markdown(f"**{item['name']}**")
            st.write(f"${item['price_per_unit']:.2f} per unit")
        
        with col3:
            st.write(f"Quantity: {item['quantity']}")
            
        with col4:
            st.write(f"**Total: ${item['total_price']:.2f}**")

        st.markdown("---")
    # Display cart total
    total_amount = sum(item['total_price'] for item in cart)

    st.write(f"### Total Amount: **${total_amount:.2f}**")
    if st.button("Proceed to Checkout"):
        st.image("qr.png", caption="Scan to proceed with payment", use_column_width=True)

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

# if "chatbot" in st.session_state:
#     company = st.session_state["chatbot"].business
#     st.session_state["messages"].append(
#         {"role": "assistant", "content": "Hello, I'm Watsell, shopping assistant for {business}! How can I help you today?"}
#     )

# Tab 1: Configurations
with tab1:
    company_page()

# Tab 2: Chat tab (left unchanged)

def display():

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

with tab2:
    if user_message := st.chat_input("Type your message here..."):
        st.session_state["messages"].append({"role": "user", "content": user_message})


        response = st.session_state["chatbot"].get_response(user_message)
        response_dict = {"role": "assistant", "content": response}
        st.session_state["messages"].append(response_dict)
        
        display()


# Tab 3: Cart tab to show current cart status
with tab3:
    show_cart()
