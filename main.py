import streamlit as st
from pipeline import run_analysis_pipeline
import pandas as pd
import time

# Set page config
st.set_page_config(
    page_title="Data Analysis Chatbot",
    page_icon="📊",
    layout="wide"
)

# Custom CSS with dark theme
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    
    /* Input field styling */
    .stTextInput input {
        font-size: 1.1rem;
        padding: 0.75rem;
        margin-bottom: 1.5rem;
        border: 2px solid #363636;
        border-radius: 8px;
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: flex-start;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* User message styling */
    .user-message {
        background-color: #2C5282;
        color: #FFFFFF;
        margin-left: 2rem;
    }
    
    /* Bot message styling */
    .bot-message {
        background-color: #2D3748;
        color: #FFFFFF;
        border: 1px solid #4A5568;
        margin-right: 2rem;
    }
    
    /* Message icon styling */
    .message-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        min-width: 35px;
        color: #FFFFFF;
    }
    
    /* Title styling */
    h1 {
        color: #FFFFFF !important;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        margin-bottom: 2rem !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #252526;
        padding: 2rem 1rem;
        color: #FFFFFF;
    }
    
    /* Example queries styling */
    .streamlit-expanderHeader {
        background-color: #2D3748;
        border-radius: 8px;
        padding: 1rem;
        font-weight: 600;
        color: #FFFFFF;
    }
    
    /* Warning message styling */
    .stAlert {
        background-color: #2D3748;
        color: #FBD38D;
        border-color: #744210;
        padding: 1rem;
        border-radius: 8px;
    }

    /* Global text color */
    .stMarkdown {
        color: #FFFFFF;
    }

    /* Sidebar text color */
    .css-1d391kg .stMarkdown {
        color: #FFFFFF;
    }

    /* File uploader styling */
    .stUploader {
        background-color: #2D3748;
        border: 1px dashed #4A5568;
        border-radius: 8px;
    }

    /* Slider styling */
    .stSlider {
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False

def display_chat_message(message, is_user=False):
    message_type = "user-message" if is_user else "bot-message"
    icon = "👤" if is_user else "🤖"
    st.markdown(f"""
        <div class="chat-message {message_type}">
            <div class="message-icon">{icon}</div>
            <div style="flex: 1;">{message}</div>
        </div>
    """, unsafe_allow_html=True)

def main():
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("📊 Settings")
        uploaded_file = st.file_uploader("Upload your dataset", type=['csv', 'xlsx'])
        max_attempts = st.slider("Max retry attempts", 1, 5, 3)
        
        if uploaded_file:
            file_details = {
                "FileName": uploaded_file.name,
                "FileType": uploaded_file.type,
                "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
            }
            st.write("File Details:")
            for key, value in file_details.items():
                st.write(f"- {key}: {value}")
            
            # Save uploaded file
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.file_uploaded = True
            st.session_state.file_name = uploaded_file.name

    # Main chat interface
    st.title("💬 Data Analysis Assistant")
    
    if not st.session_state.file_uploaded:
        st.warning("Please upload a dataset first!")
        return

    # Chat input handling with form
    with st.form(key="query_form", clear_on_submit=True):
        user_query = st.text_input("Ask me anything about your data:", key="user_input")
        submit_button = st.form_submit_button("Send")
        
        if submit_button and user_query:
            # Add user message to chat
            st.session_state.messages.append({"text": user_query, "is_user": True})
            
            # Show typing indicator
            with st.spinner("Analyzing..."):
                try:
                    result = run_analysis_pipeline(
                        user_query, 
                        st.session_state.file_name, 
                        max_attempts
                    )
                    # Add bot response to chat
                    st.session_state.messages.append({"text": result, "is_user": False})
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            st.rerun()

    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(message['text'], message['is_user'])

    # Reset last_query when the current query is empty
    if not user_query:
        if 'last_query' in st.session_state:
            del st.session_state.last_query

    # Add some helpful examples
    with st.expander("📝 Example queries"):
        st.markdown("""
        Try these example queries:
        - Show me the highest revenue by product
        - What is the total sales amount?
        - How many unique customers do we have?
        - Show sales trend over time
        """)

if __name__ == "__main__":
    main()