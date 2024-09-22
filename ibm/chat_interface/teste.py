import streamlit as st

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    name = "edffdsfds"
    st.session_state["messages"].append(
        {"role": "assistant", "content": f"Hello, I'm Watsell, shopping assistant for {name}! How can I help you today?"}
    )

    with st.chat_message("assistant"):
        st.write(f"Hello, I'm Watsell, shopping assistant for {name}! How can I help you today?")

if user_message := st.chat_input("Type your message here..."):
    st.session_state["messages"].append({"role": "user", "content": user_message})

    st.session_state["messages"].append({"role": "assistant", "content": "I'm sorry"})

    # Display all messages from the session state
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
