import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq 
import streamlit as st

class Model:
    """Testing Proper if connection is istablished with Model and Provider Correctly"""
    def get_groq(api_key, model):
        try:
            model_instance = ChatGroq(model=model,api_key=api_key)
            test_responce = model_instance.invoke('Testing Connection')
            return model_instance, test_responce
        except Exception as e:
            st.warning('⚠️ Enter Correct API Key to Proceed')
            st.error(f"Authentication Error: {str(e)}")
            st.stop()
            
    def get_ollama(model):
        try:
            model_instance = ChatOllama(model=model)
            test_responce = model_instance.invoke('Testing Connection')
            return model_instance, test_responce
        except Exception as e:
            st.warning('⚠️ Un able to stance connection with Ollama')
            st.error(f"Error: {str(e)}")
            st.stop()