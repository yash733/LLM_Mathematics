import streamlit as st
import json, requests
from langchain.prompts import PromptTemplate
from langchain_core.prompts import AIMessagePromptTemplate
from schema import State
from langchain.callbacks import StreamlitCallbackHandler

import os ,sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

# ------------------------------------- #
API_BASE_URL = "http://127.0.0.1:8000/"
# ------------------------------------- #

def get_current_model():
    response = requests.get(f"{API_BASE_URL}/current_model")
    if response.status_code==200:
        model = response.json()['current_model']
        
        # Not Binding in if model in st.session_state
        # As If at point user decides to switch to another model he can ! 
        st.session_state.model = model
        return
    else:
        st.error("[page_2|get_current_model] Model instance is not available")
        st.stop()

def get_llm_response(model, query):
    payload = {
        "user_model":model,
        "user_message":query
    }
    response = requests.post(f"{API_BASE_URL}/invoke",json=payload)
    if response.status_code==200:
        return response.json()
    else:
        st.error("[page_2|get_llm_response] Could not generate response for your Query")
        st.stop()

def page_2_ui():
    get_current_model()

    st.session_state.message_history = [{"role":"assistant","content":"Hi, I'm a MAth chatbot who can answer all your maths questions"}]

    for msg in st.session_state.message_history:
        st.chat_message(msg['role']).write(msg['content'])

    query = st.text_area(label='Enter your query: ')
    if st.button(label="Next") and query:
        with st.spinner("Generating Response"):
            st.chat_message('human').write(query) # Display human message 
            
            # Get LLM Response
            result = get_llm_response(model=st.session_state.model, query=query)

            st.chat_message('ai').write(result.get('content'))
            st.session_state.message_history.extend([{'role':'human', 'content':query},
                                            {'role':'ai','content':result['response']}])
            
            StreamlitCallbackHandler(st.container())
            
    else:
        st.error("Please add a question into to proceed further.")
