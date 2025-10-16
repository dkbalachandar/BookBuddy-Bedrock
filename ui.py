#!/usr/bin/env python3
"""
BookBuddy Streamlit Web UI
A web interface for the BookBuddy AI reading companion with Amazon purchase links
"""

import streamlit as st
import time
from bookbuddy import BookBuddyAgent

# Configure Streamlit page
st.set_page_config(
    page_title="BookBuddy - AI Reading Companion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize BookBuddy agent (cached for performance)
@st.cache_resource
def initialize_bookbuddy():
    """Initialize BookBuddy agent (cached to avoid recreating)."""
    config = {
        "agent_name": "BookBuddy",
        "foundation_model": "anthropic.claude-3-haiku-20240307-v1:0",
        "alias_name": "BookBuddy",
        "region": "us-east-1"
    }
    
    bookbuddy = BookBuddyAgent(**config)
    
    with st.spinner("🚀 Initializing BookBuddy..."):
        if bookbuddy.initialize():
            return bookbuddy
        else:
            st.error("❌ Failed to initialize BookBuddy. Please check your AWS credentials.")
            return None

# Main UI
def main():
    # Header
    st.title("📚 BookBuddy - AI Reading Companion")
    st.markdown("*Get personalized book recommendations with direct Amazon purchase links!*")
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About BookBuddy")
        st.markdown("""
        BookBuddy is an AI-powered reading companion that provides:
        
        ✅ **Personalized recommendations**  
        ✅ **Specific book titles & authors**  
        ✅ **Direct Amazon purchase links**  
        ✅ **Genre-based suggestions**  
        ✅ **Mood-based recommendations**
        
        ### 💡 Try asking for:
        - "motivational books"
        - "sci-fi novels"
        - "self-help books"
        - "books about habits"
        - "mystery novels"
        - "books for entrepreneurs"
        """)
        
        st.header("🔧 Settings")
        session_id = st.text_input("Session ID", value=f"session-{int(time.time())}")
    
    # Initialize BookBuddy
    bookbuddy = initialize_bookbuddy()
    
    if bookbuddy is None:
        st.error("❌ BookBuddy is not available. Please check your configuration.")
        return
    
    # Main chat interface
    st.header("💬 Ask BookBuddy for Recommendations")
    
    # Input area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "What kind of books are you looking for?",
            placeholder="e.g., motivational books, sci-fi novels, books about productivity...",
            key="book_input"
        )
    
    with col2:
        get_recommendation = st.button("📚 Get Books", type="primary")
    
    # Quick suggestion buttons
    st.markdown("**Quick suggestions:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎯 Self Help"):
            user_input = "self help books"
            get_recommendation = True
    
    with col2:
        if st.button("🚀 Motivation"):
            user_input = "motivational books"
            get_recommendation = True
    
    with col3:
        if st.button("🧠 Psychology"):
            user_input = "psychology books"
            get_recommendation = True
    
    with col4:
        if st.button("💼 Business"):
            user_input = "business books"
            get_recommendation = True
    
    # Process recommendation request
    if get_recommendation and user_input:
        with st.spinner("🤔 BookBuddy is thinking..."):
            try:
                response = bookbuddy.chat(user_input, session_id)
                
                if response and not response.startswith("❌"):
                    st.success("📚 Here are BookBuddy's recommendations:")
                    
                    # Display response with proper formatting
                    st.markdown(response)
                    
                    # Add some helpful notes
                    st.info("💡 **Tip:** Click the Amazon links to purchase books directly!")
                    
                else:
                    st.error(f"❌ Error getting recommendations: {response}")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    
    elif get_recommendation and not user_input:
        st.warning("⚠️ Please enter what kind of books you're looking for!")
    
    # Chat history (optional enhancement)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if get_recommendation and user_input and 'response' in locals():
        st.session_state.chat_history.append({
            "user": user_input,
            "bookbuddy": response,
            "timestamp": time.time()
        })
    
    # Display chat history
    if st.session_state.chat_history:
        st.header("📝 Recent Recommendations")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history[-3:])):  # Show last 3
            with st.expander(f"💬 {chat['user'][:50]}..." if len(chat['user']) > 50 else f"💬 {chat['user']}"):
                st.markdown(f"**You:** {chat['user']}")
                st.markdown(f"**BookBuddy:** {chat['bookbuddy']}")
    
    # Footer
    st.markdown("---")
    st.markdown("*Powered by Amazon Bedrock & Claude 3 Haiku* 🤖")

if __name__ == "__main__":
    main()
