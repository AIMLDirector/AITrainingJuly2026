import streamlit as st
from ollama import chat, list as list_ollama

# Set up page configurations
st.set_page_config(page_title="Ollama Multi-Chat", page_icon="🤖", layout="wide")

# --- 1. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("Settings & Chats")
    
    # Dynamically fetch available models from Ollama, fallback to custom model if offline
    try:
        ollama_models = [m['model'] for m in list_ollama()['models']]
        default_index = ollama_models.index("qwenmodel_Development:latest") if "qwenmodel_Development:latest" in ollama_models else 0
    except Exception:
        ollama_models = ["qwenmodel_Development:latest", "llama3:latest", "mistral:latest"]
        default_index = 0

    # Model Dropdown Selector
    selected_model = st.selectbox("Select AI Model", options=ollama_models, index=default_index)
    
    st.divider()
    
    # Button to create a new chat tab
    if st.button("➕ New Chat", use_container_width=True):
        # Generate a unique key using the current count
        new_id = len(st.session_state.get("chats", {})) + 1
        tab_key = f"Chat {new_id}"
        
        # Initialize the new chat in session state
        st.session_state.chats[tab_key] = []
        st.session_state.active_chat = tab_key
        st.rerun()

    st.write("**Your Conversations:**")
    
    # Initialize global state containers if they don't exist
    if "chats" not in st.session_state:
        st.session_state.chats = {"Chat 1": []}
    if "active_chat" not in st.session_state:
        st.session_state.active_chat = "Chat 1"

    # Display active chat tabs as clickable buttons in the sidebar
    for chat_title in list(st.session_state.chats.keys()):
        # Highlight the currently active chat
        is_active = (chat_title == st.session_state.active_chat)
        type_style = "primary" if is_active else "secondary"
        
        if st.button(chat_title, key=f"btn_{chat_title}", type=type_style, use_container_width=True):
            st.session_state.active_chat = chat_title
            st.rerun()

# --- 2. MAIN CHAT INTERFACE ---
active_tab = st.session_state.active_chat
st.title(f"💬 {active_tab}")
st.caption(f"Running via model: `{selected_model}`")

# Fetch history for the active chat tab
chat_history = st.session_state.chats[active_tab]

# Render historic messages for this specific tab
for message in chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user messaging
if user_input := st.chat_input("Message your local Ollama model..."):
    
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Save user entry to the active tab's history
    chat_history.append({"role": "user", "content": user_input})

    # Query Ollama server with full context of the active tab
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat(
                    model=selected_model,
                    messages=chat_history
                )
                ai_response = response["message"]["content"]
                st.markdown(ai_response)
                
                # Save assistant entry to the active tab's history
                chat_history.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"Error communicating with local server: {e}")
