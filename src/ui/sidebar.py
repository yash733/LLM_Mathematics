import streamlit as st
import requests
from log.logger import logging
import os ,sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

# ---- Log ---- #
log = logging.getLogger('sidebar')
log.setLevel(logging.DEBUG)

# ------------------------------------ #
API_BASE_URL = "http://127.0.0.1:8000/"
# ------------------------------------ #

# Get Model Providers
def model_provider():
    try:
        response = requests.get(f"{API_BASE_URL}/provider")
        if response.status_code==200:
            log.info(f'[model_provider] list of Models Provided')  #log
            return response.json()["models providers"] # list of Models Provided
        else:
            log.error("[model_provider] Un-anble to fetch provider")  #log
            st.error("Un-anble to fetch provider")
    except requests.exceptions.RequestException as e:
        log.error(f'[model_provider] Error: {e}')  #log
        st.error(f"Connection error --> /provider?: {e}")
        return []

# Get Models Provided by the Providers
def models_from_provider(provider):
    try:
        response = requests.get(f"{API_BASE_URL}/model/{provider}")
        if response.status_code==200:
            log.info(f'[models_from_provider] {response}')  #log
            return response.json()["models"]
        else:
            log.error(f'[models_from_provider] Un-anble to fetch models')
            st.error("Un-anble to fetch models")
    except requests.exceptions.RequestException as e:
        log.error(f'[models_from_provider] Error: {e}')  #log
        st.error(f"Connection error --> /model/provider?: {e}")
        return []

# Gettinig Model Instance Initialization
def configure_groq(api_key, model_name):
    try:
        payload = {
            "api_key":api_key,
            "model_name":model_name
        }
        response = requests.post(f"{API_BASE_URL}/groq/model", json=payload)  
        log.info(f'[configure_groq] payload: {payload} \nResponse: {response}')  #log
        if response.status_code==200:
            st.session_state.current_config = {"model_detail" : response.json()["config"]}
            return True
        else:
            log.error(f'[configure_groq] Error Occured Unable to get Selected Model, from Provider: {response}')  #log
            st.error(f"Error Occured Unable to get Selected Model, from Provider {response}")
            return False

    except requests.exceptions.RequestException as e:
        log.erro(f'[configure_groq] Error: {e}')  #log
        st.error(f"Connection error --> /groq/model?: {e}")
        return []

def configure_ollama(model_name):
    try:
        payload = {
            "model_name":model_name
        }
        response = requests.post(f"{API_BASE_URL}/ollama/model", json=payload)
        # log.info(f'[configure_ollama] payload: {payload} \nResponse: {response}')
        if response.status_code == 200:
            st.session_state.current_config = {"model_detail" : response.json()}
            return True
        else:
            log.error('[configure_ollama] Error Occured Unable to get Slected Model, from Provider')  #log
            st.error("Error Occured Unable to get Slected Model, from Provider")
            return False
    except Exception as e:
        log.error(f'[configure_ollama] Error: {e}')  #log
        st.error(f"Connection error --> /ollama/model?: {e}")
        return []
    
def get_model():
    "Current Config related to model"
    try:
        response = requests.get(f"{API_BASE_URL}/model_config")
        log.info(f'[get_model] Response: {response}')  #log
        if response.status_code == 200:
            return response.json()
        else:
            return False
    except Exception as e:
        log.error(f'[get_model] Error: {e}') #log
        st.error(f"Connection error --> /model_config?: {e}") 
        return []


def sidebar_():
    with st.sidebar:
        if st.session_state.config_saved:
            st.markdown("## Selected Configuration: ")
            st.write(f"**Model**: {st.session_state.current_config['model_detail']['config']['provider']}")
            st.write(f"**Model Type**: {st.session_state.current_config['model_detail']['config']['model_name']}")
            
            if st.button('Reset Config'):
                log.info('[sidebar_] Reset Config')  #log
                response = requests.delete(f"{API_BASE_URL}/config_reset")
                st.success(response.json()['message'])
                st.session_state.selection = {}
                st.session_state.message_history = []
                st.session_state.config = ''
                st.session_state.current_config = {}
                st.session_state.config_saved = False
                st.rerun()

            with st.expander(label="Meta Data"):
                st.write("current_config: ",st.session_state.current_config)
                # st.write("selection: ",st.session_state.selection)
                st.write("message_history: ",st.session_state.message_history)
                st.write('config: ',st.session_state.config)

        elif st.session_state.config_saved == False:
            Provider_selected = st.selectbox(label="Choose a Model Provider: ", options=model_provider()) #GROQ, OLLAMA
            if Provider_selected == "GROQ":
                Model_selected = st.selectbox(label="Choose a Model: ", options=models_from_provider(Provider_selected)) #List of Models with each Provider
                if Model_selected:
                    api = st.text_input(label="API Key: ", type="password").strip()
                    if api and st.button('Save', key="Model from Provider Groq"):
                        with st.spinner("Model Connection Testing"):
                            if configure_groq(api, Model_selected):
                                st.session_state.config_saved = True
                                log.info('[sidebar_] connected with groq') #log
                                st.rerun() 
                            else:
                                log.error(f'[sidebar_] not connected groq')  #log
                                st.stop()
                    else:
                        st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                        st.stop()
                else:
                    st.warning("Select a Model to preceed further")
                    st.stop()

            elif Provider_selected == "OLLAMA":
                Model_selected = str(st.selectbox(label="Choose a Model: ", options=models_from_provider(Provider_selected))) #List of Models with each Provider
                if Model_selected and st.button("Setup Connection", key = "Ollama model connection"):
                    # Model call and test
                    with st.spinner("Model Connection Testing"):
                        if configure_ollama(Model_selected):
                            st.session_state.config_saved = True
                            log.info(f'[sidebar_] connected with Ollama') #log
                            st.rerun()
                        else:
                            log.error(f'[sidebar_] not connected ollama') #log
                            st.stop()
                else:
                    st.stop()

        