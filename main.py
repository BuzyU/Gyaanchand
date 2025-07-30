    # Gyaanchand - Streamlit Web Interface
import streamlit as st
st.title('🤖 Gyaanchand: Universal AI Assistant')
st.write('Ask me to code, simulate, or generate tests!')
from agent_core import handle_query

st.set_page_config(page_title="Gyaanchand", layout="wide")

# Chat input (for user prompt)
user_input = st.chat_input("Type your question here...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        response = handle_query(user_input)
        st.write(response)
