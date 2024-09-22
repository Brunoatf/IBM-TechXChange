import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.bot import Chatbot
from components import create_seller

# Set page title
st.set_page_config(page_title="Watsell", page_icon="🛒", layout="wide")

# Hide default Streamlit footer and menu
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       .block-container {
           padding-left: 10 !important;
           padding-right: 10 !important;
           max-width: 100% !important;

       }
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Initialize session state for messages and conversation ID if not present
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chatbot" not in st.session_state:
    st.session_state["chatbot"] = Chatbot(
        business="Foo",
        business_description="A fictional convenience store",
        products=[
            {"name": "Apple", "price": 1.0},
            {"name": "Banana", "price": 0.5},
            {"name": "Orange", "price": 0.75},
        ],
    )


st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 3em; color: #2c5ad4;">Hello, I'm Watsell  💬</h1>
        <p style="font-size: 1.5em; color: #555;">The customizable sales agent for your business</p>
    </div>
    """, unsafe_allow_html=True)

st.write("Welcome to Watsell! Use the chat interface to interact with the virtual sales assistant.")

# Add tabs
tab1, tab2 = st.tabs(["Chat", "Configurations"])

# Chat tab
with tab1:

    def process_reset_button_click() -> None:
        """Resets the chatbot conversation."""
        st.session_state.pop("messages", None)

    def display_textual_message(message: dict) -> None:
        """Displays textual messages in the chat window."""
        role = message["role"]
        content = message["content"]
        st.chat_message(role).write(content)

    def display_messages(messages=st.session_state.get("messages", [])) -> None:
        """Displays messages in the chat window."""
        for msg in messages:
            if msg["role"] in ["assistant", "user"]:
                display_textual_message(msg)

    def process_message(user_message: str) -> None:
        """Receives user message and processes it."""
        with st.spinner("Please wait while your message is processed..."):
            response = st.session_state["chatbot"].get_response(user_message)
            response_dict = {"role": "assistant", "content": response}
            st.session_state["messages"].append(response_dict)

    display_messages()

    if user_message := st.chat_input(placeholder="Type your message here..."):
        st.session_state["messages"].append({"role": "user", "content": user_message})
        st.chat_message("user").write(user_message)
        process_message(user_message)

        # Rerun the app to display the messages and update the UI dynamically
        st.rerun()

# Other component tab (e.g., settings or information tab)
with tab2:
    st.header("Other Component")
    st.write("This tab can be used for other functionalities, like settings or information.")
    create_seller()
