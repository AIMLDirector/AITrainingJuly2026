import streamlit as st
from ollama import chat

# Set up the web page title
st.set_page_config(page_title="Ollama Chatbot", page_icon="🤖")
st.title("Ollama AI Assistant")

# Define your custom Ollama model
MODEL_NAME = "qwenmodel_Development:latest"

# Initialize chat history in session state so it persists across reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages from the history on the UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input using Streamlit's chat input bar
if user_input := st.chat_input("Type your message here..."):
    
    # 1. Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # 2. Add user message to the session state history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 3. Fetch response from the Ollama local server
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat(
                    model=MODEL_NAME,
                    messages=st.session_state.messages # Passes full context to the model
                )
                ai_response = response["message"]["content"]
                st.markdown(ai_response)
                
                # 4. Add AI response to the session state history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"Failed to connect to Ollama: {e}")
