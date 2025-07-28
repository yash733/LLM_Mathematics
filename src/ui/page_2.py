import streamlit as st
import json, requests
# from langchain.callbacks import StreamlitCallbackHandler
from datetime import datetime

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

def get_llm_response(query, config):
    payload = {
        # "user_model":model,
        "user_input":str(query),
        "config":config
    }
    response = requests.post(f"{API_BASE_URL}/invoke",json=payload)
    if response.status_code==200:
        return response.json()
    else:
        st.error(f"[page_2|get_llm_response] Could not generate response for your Query {response}")
        st.stop()

def page_2_ui():
    get_current_model()

    if st.session_state.message_history == []:
        st.session_state.message_history = [{"role":"assistant","content":"Hi, I'm a Math's chatbot who can answer all your maths related questions"}]

    for msg in st.session_state.message_history:
        st.chat_message(msg['role']).write(msg['content'])

    query = st.text_area(label='Enter your query: ', value='I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?')
    if st.button(label="Next") and query:
        with st.spinner("Generating Response"):
            st.chat_message('human').write(query) # Display human message 
            
            # st_callback = StreamlitCallbackHandler(st.container())
            if st.session_state.config == '':
                st.session_state.config = {'configurable': {'thread_id': f'{datetime.now()}'}}
            # Get LLM Response
            print('model: ',st.session_state.model, '\nquery: ',query, '\nconfig: ',st.session_state.config, '\n -----------------------------')
            result = get_llm_response(query=query, config = st.session_state.config)
            
            st.chat_message('ai').write(result.get('content'))
            st.session_state.message_history.extend([{'role':'human', 'content':query},
                                            {'role':'ai','content':result['response']}])
            st.rerun()
            
    else:
        st.error("Please add a question into to proceed further.")
