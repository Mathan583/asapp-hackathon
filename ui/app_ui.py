import streamlit as st
import requests
import json
from datetime import datetime

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom CSS for better chat interface
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.bot {
        background-color: #475063;
        color: white;
    }
    .chat-message .avatar {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        margin-right: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("✈️ Airline Smart Bot")
st.markdown("Chat with our AI assistant for flight bookings, cancellations, and status updates!")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    try:
        response = requests.post("http://127.0.0.1:8000/chat", data={"message": prompt})
        bot_response = response.json()["response"]
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(bot_response)
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the backend server. Make sure it's running on http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Sidebar with options
with st.sidebar:
    st.header("Chat Options")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Quick Actions")
    
    if st.button("📋 Check Flight Status"):
        st.session_state.messages.append({"role": "user", "content": "Check my flight status"})
        st.rerun()
    
    if st.button("✈️ Book Flight"):
        st.session_state.messages.append({"role": "user", "content": "I want to book a flight"})
        st.rerun()
    
    if st.button("❌ Cancel Flight"):
        st.session_state.messages.append({"role": "user", "content": "I want to cancel my flight"})
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Chat Info")
    st.info(f"💬 Messages: {len(st.session_state.messages)}")
    
    if st.session_state.messages:
        st.markdown("**Last message:**")
        st.text(st.session_state.messages[-1]["content"][:50] + "...")
