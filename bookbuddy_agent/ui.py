
#!/usr/bin/env python3
"""
BookBuddy Streamlit Web UI
A web interface for the BookBuddy AI reading companion with Amazon purchase links
"""

import streamlit as st
import sys
import os
import time

# Add parent directory to path to import bookbuddy module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bookbuddy import BookBuddyAgent

# Configure Streamlit page
st.set_page_config(
    page_title="BookBuddy - AI Reading Companion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.recommendation-box {
    background-color: #f8f9fa;
    border-left: 4px solid #007bff;
    border-radius: 8px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.book-item {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    position: relative;
}

.summary-section {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-left: 4px solid #6c757d;
    padding: 15px 18px;
    margin: 15px 0;
    border-radius: 6px;
    font-style: normal;
    line-height: 1.6;
    color: #495057;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.summary-section strong {
    color: #343a40;
    font-weight: 600;
    display: block;
    margin-bottom: 8px;
    font-size: 1.05em;
}



.book-title {
    color: #2c3e50;
    font-weight: bold;
    font-size: 1.2em;
    margin-bottom: 12px;
    line-height: 1.4;
}

.book-title strong {
    color: #1a365d;
    font-weight: 700;
}

.summary-section {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-left: 4px solid #6c757d;
    padding: 15px 18px;
    margin: 15px 0;
    border-radius: 6px;
    line-height: 1.6;
    color: #495057;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}


</style>
""", unsafe_allow_html=True)

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

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/books.png", width=80)
    st.title("📚 BookBuddy AI")
    st.markdown("*Find your next favorite book with AI recommendations and direct purchase links!*")
    
    st.header("💡 Try asking for:")
    st.markdown("""
    - "motivational books"
    - "sci-fi novels"
    - "self-help books"
    - "books about habits"
    - "mystery novels"
    - "business books"
    - "psychology books"
    """)

# Main content
st.title("📚 BookBuddy AI Agent")
st.markdown("*Get personalized book recommendations with direct Amazon purchase links!*")

# Initialize BookBuddy
bookbuddy = initialize_bookbuddy()

if bookbuddy is None:
    st.error("❌ BookBuddy is not available. Please check your configuration.")
    st.stop()

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "What kind of books are you looking for?", 
        placeholder="e.g., motivational books, sci-fi novels, books about productivity...",
        key="book_query"
    )
    
    # Add summary option
    include_summary = st.checkbox("📖 Include book summaries", help="Get a brief summary of each book's content")

with col2:
    st.image("https://img.icons8.com/color/96/000000/open-book--v2.png", width=80)

# Action button
get_rec = st.button("🔍 Get Recommendations", type="primary")

# Process recommendation
if get_rec and query:
    with st.spinner("🤔 BookBuddy is finding the perfect books for you..."):
        try:
            # Generate a unique session ID automatically
            session_id = f"session-{int(time.time())}"
            response = bookbuddy.chat(query, session_id, include_summary=include_summary)
            
            if response and not response.startswith("❌"):
                st.success("📚 Here are BookBuddy's recommendations:")
                
                # Display the response with enhanced formatting
                st.markdown("### 📚 Recommendations:")
                
                # Simple approach: treat entire response as one formatted block
                def convert_markdown_to_html(text):
                    """Convert markdown formatting to HTML."""
                    import re
                    # Convert **bold** to <strong>bold</strong>
                    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
                    return text
                
                def clean_amazon_urls(text):
                    """Clean up malformed Amazon URLs."""
                    import re
                    
                    # Find malformed URLs that contain too much text
                    def fix_url(match):
                        full_url = match.group(0)
                        # If URL is too long (more than 80 chars), it's probably malformed
                        if len(full_url) > 80:
                            # Try to extract book title and author from the surrounding text
                            # Look for pattern like "📚 **Title** by Author" before the URL
                            context = text[:match.start()]
                            
                            # Try multiple patterns to find book info
                            patterns = [
                                r'📚\s*\*\*(.*?)\*\*\s*by\s*(.*?)(?:\n|$)',  # Standard format
                                r'book\s+"([^"]+)"\s*by\s*([^\n]+)',         # "Book Title" by Author
                                r'The\s+Power\s+of\s+Habit.*?Charles\s+Duhigg',  # Specific fallback
                            ]
                            
                            for pattern in patterns:
                                book_match = re.search(pattern, context[-300:], re.IGNORECASE)
                                if book_match:
                                    if len(book_match.groups()) >= 2:
                                        title = book_match.group(1).strip()
                                        author = book_match.group(2).strip()
                                    else:
                                        # For specific patterns, use hardcoded values
                                        title = "The Power of Habit"
                                        author = "Charles Duhigg"
                                    
                                    # Clean title and author
                                    title = re.sub(r'[^\w\s]', '', title).replace(' ', '+')
                                    author = re.sub(r'[^\w\s]', '', author).replace(' ', '+')
                                    return f"https://amazon.com/s?k={title}+{author}"
                            
                            # If no pattern matches, try to extract from the URL itself
                            # Look for recognizable book titles in the URL
                            if "Power+of+Habit" in full_url or "Power+Habit" in full_url:
                                return "https://amazon.com/s?k=The+Power+of+Habit+Charles+Duhigg"
                        
                        return full_url
                    
                    # Fix malformed Amazon URLs
                    text = re.sub(r'https://amazon\.com/s\?k=[^\s\n]+', fix_url, text)
                    return text
                
                def format_summary_sections(text):
                    """Format summary sections with better styling."""
                    import re
                    
                    # Find and format summary sections
                    def format_summary(match):
                        summary_text = match.group(0)
                        # Add proper styling to summary sections
                        formatted = f'<div class="summary-section">{summary_text}</div>'
                        return formatted
                    
                    # Format lines that start with 📖
                    text = re.sub(r'📖[^\n]*(?:\n(?!📚|🛒)[^\n]*)*', format_summary, text, flags=re.MULTILINE)
                    return text
                
                def make_links_clickable(text):
                    """Convert Amazon URLs to clickable links."""
                    import re
                    
                    def create_link(match):
                        url = match.group(0)
                        return f'<a href="{url}" target="_blank" style="color: #007bff; text-decoration: underline;">{url}</a>'
                    
                    # Make Amazon URLs clickable
                    text = re.sub(r'https://amazon\.com/s\?k=[^\s\n]+', create_link, text)
                    return text
                
                # Clean up malformed Amazon URLs first, then format
                cleaned_response = clean_amazon_urls(response)
                summary_formatted = format_summary_sections(cleaned_response)
                clickable_links = make_links_clickable(summary_formatted)
                formatted_response = convert_markdown_to_html(clickable_links)
                
                # Create one container for the entire response
                with st.container():
                    st.markdown(f"""
                    <div class="book-item">
                        <div style="line-height: 1.6; white-space: pre-line;">{formatted_response}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Add helpful tip
                st.info("💡 **Tip:** Click the 🛒 Buy links to purchase books directly from Amazon!")
                
                # Store in session state for history
                if "recommendations" not in st.session_state:
                    st.session_state.recommendations = []
                
                st.session_state.recommendations.append({
                    "query": query,
                    "response": response,
                    "include_summary": include_summary,
                    "timestamp": time.time()
                })
                
            else:
                st.error(f"❌ Error getting recommendations: {response}")
                # Show more details for debugging
                with st.expander("🔍 Debug Details"):
                    st.code(f"Response: {response}")
                
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            # Show more details for debugging
            with st.expander("🔍 Debug Details"):
                st.code(f"Exception: {e}")
                st.code(f"Agent ID: {bookbuddy.agent_id if hasattr(bookbuddy, 'agent_id') else 'Not set'}")
                st.code(f"Alias ID: {bookbuddy.alias_id if hasattr(bookbuddy, 'alias_id') else 'Not set'}")

elif get_rec and not query:
    st.warning("⚠️ Please enter what kind of books you're looking for!")

# Show recent recommendations
if "recommendations" in st.session_state and st.session_state.recommendations:
    st.header("📝 Recent Recommendations")
    
    # Show last 3 recommendations
    for i, rec in enumerate(reversed(st.session_state.recommendations[-3:])):
        with st.expander(f"💬 {rec['query'][:50]}..." if len(rec['query']) > 50 else f"💬 {rec['query']}"):
            st.markdown(f"**You asked:** {rec['query']}")
            st.markdown(f"**BookBuddy recommended:**")
            st.markdown(rec["response"])

# Footer
st.markdown("---")
st.markdown("*Powered by Amazon Bedrock & Claude 3 Haiku* 🤖")

