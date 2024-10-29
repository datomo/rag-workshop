"""
RAG Application User Interface

Author: Anastasiia Popova
Email: anastasiia.popova@stud.unibas.ch

This module implements a UI for the RAG application using Streamlit.

Usage:
1. Install Streamlit in a separate virtual environment:
   pip install streamlit

2. Run the application:
   streamlit run rag_chat_ui.py

Note:
Perplexity AI assisted in code writing, editing, and more effective information searches. The generated output underwent critical evaluation. The author is solely responsible for the content.
"""

import streamlit as st
import time 

# Streamlit app
def main():

    # Set page configuration
    st.set_page_config(
        page_title="RAG Chat Assistant",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state = "collapsed"
    )
    
    # Custom CSS to change background colors
    st.markdown("""
        <style>
        .stApp {
            background-color: #a5d7d2;
        }
        .stTextInput > div > div > input {
            background-color: #2d373c;
        }
        .stTextArea > div > div > textarea {
            background-color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)

   
    
    # Add logo
    logo = "unibas_logo.png"
    st.image(logo, width=250)
    
    # Title
    st.title("RAG Chat Assistant")
    st.markdown('It is an **experimental version** of the application for the *"Hackathon on RAGs"* course.')
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Here you would typically process the user's input using your RAG system
        # For this example, we'll just echo the user's input
        response = f"You asked: {prompt}"
        
        # Display assistant response
        with st.chat_message("assistant"):
            #st.markdown(response)

        # Simulate bot response with typing effect

            message_placeholder = st.empty()
            full_response = ""
            assistant_response = "This is a simulated response from the RAG system. In a real application, this would be generated based on the user's input and relevant retrieved information."
            
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        
        # Add assistant response to chat history
        # st.session_state.messages.append({"role": "assistant", "content": response})

        st.session_state.messages.append({"role": "assistant", "content": full_response.strip()})


        # Sidebar for additional options
    with st.sidebar:
        st.header("Options")
        st.checkbox("Enable advanced features")
        st.slider("Response length", 1, 100, 50)
    
    # Sidebar for additional options
    # with st.sidebar:
    #     st.header("Options")
    #     if st.button("Clear Chat History"):
    #         st.session_state.messages = []
    #         st.experimental_rerun()


if __name__ == "__main__":
    main()
