import streamlit as st
import json, requests

API_BASE_URL = "http://127.0.0.1:8000/"

# -----------
if not "selection" in st.session_state:
    st.session_state.selection = {}

if not "message_history" in st.session_state:
    st.session_state.message_history = []

if not "current_config" in st.session_state:
    st.session_state.current_config = {}
# ------------

# Get Model Providers
def model_provider():
    try:
        response = requests.get(f"{API_BASE_URL}/provider")
        if response.status_code==200:
            return response.json()["models providers"] # list of Models Provided
        else:
            st.error("Un-anble to fetch provider")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return []

# Get Models Provided by the Providers
def models_from_provider(provider):
    try:
        response = requests.get(f"{API_BASE_URL}/model/{provider}")
        if response.status_code==200:
            return response.json()["models"]
        else:
            st.error("Un-anble to fetch models")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return []

# Gettinig Model Instance Initialization
def configure_groq(api_key, model_name):
    try:
        payload = {
            "api_key":api_key,
            "model_name":model_name
        }
        response = requests.post(f"{API_BASE_URL}/groq/model", json=payload)
        if response.status_code==200:
            st.session_state.current_config = {"model_detail" : response.json()["config"]}
            return True
        else:
            st.error("Error Occured Unable to get Slected Model, from Provider")
            return False

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return []

def configure_ollama(model_name):
    try:
        payload = {
            "model_name":model_name
        }
        response = requests.post(f"{API_BASE_URL}/ollama/model", json=payload)
        if response.status_code == 200:
            st.session_state.current_config = {"model_detail" : response.json()["config"]}
            return True
        else:
            st.error("Error Occured Unable to get Slected Model, from Provider")
            return False
    except Exception as e:
        st.error(f"Connection error: {e}")
        return []
    
def get_model():
    "Current Config related to model"
    try:
        response = requests.get(f"{API_BASE_URL}/model_config")
        if response.status_code == 200:
            return response.json()
        else:
            return False
    except Exception as e:
        st.error(f"Connection error: {e}")
        return []


def sidebar():
    with st.sidebar:
        Provider_selected = st.selectbox(label="Choose a Model Provider: ", options=model_provider()) #GROQ, OLLAMA
        if Provider_selected:
            if Provider_selected == "GROQ":
                Model_selected = st.selectbox(label="Choose a Model: ", options=models_from_provider(Provider_selected)) #List of Models with each Provider
                if Model_selected:
                    api = st.text_input(label="API Key: ", type="password").strip()
                    if api and st.button('Save', key="Model from Provider Groq"):
                        if not configure_groq(api, Model_selected):
                            st.stop()
                    else:
                        st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                        st.stop()
                else:
                    st.warning("Select a Model to preceed further")
                    st.stop()

            elif Provider_selected == "OLLAMA":
                Model_selected = st.selectbox(label="Choose a Model: ", options=models_from_provider(Provider_selected))
                if Model_selected:
                    # Model call and test
                    if not configure_ollama(Model_selected):
                        st.stop()
            else:
                st.error("Error 400, Model Provider Selected in present")
        else:
            st.stop()
        
