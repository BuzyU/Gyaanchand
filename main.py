# main.py
# Gyaanchand - Streamlit Web Interface

import streamlit as st
from agent_core import handle_query

# Page configuration
st.set_page_config(page_title="Gyaanchand", layout="wide")

# Title and description
st.title("🤖 Gyaanchand: Universal AI Assistant")
st.write("Ask me to code, simulate, generate tests, and more!")

# Initialize session state for conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append(("user", user_input))

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Handle and display assistant response
    with st.chat_message("assistant"):
        response = handle_query(user_input)
        st.markdown(response)
        st.session_state.chat_history.append(("assistant", response))

# Optional: Show chat history (in case of refresh)
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)
