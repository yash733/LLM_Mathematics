
import streamlit as st
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from backend.configuration.config import Config  # Extract UI Configuration
from backend.model import Model  # Initialize Model from groq or ollama

# from logger.logging import logging

# debug = logging.getLogger('Side-Bar')
# debug.setLevel(logging.DEBUG)

if 'user_selection' not in st.session_state:
    st.session_state.user_selection = {}
if 'config_saved' not in st.session_state:
    st.session_state.config_saved = False

def sidebar():
    with st.sidebar:
        if st.session_state.config_saved == False:
            provider = st.selectbox(label='Provider', options=Config().get_llm())
            if provider == 'GROQ':
                # -- provider -- api -- model -- # 
                st.session_state.user_selection.update({'model':'groq', 'api_key':st.text_input(label= 'Enter API key for Groq', type='password').strip(),
                                                        'model_name':st.selectbox(label='Groq Model', options=Config().get_groq_model())})

                if st.session_state.user_selection['api_key'] and st.session_state.user_selection['model_name'] and st.button(label='Proceed', key='Satge1 Groq'):
                    try :
                        if st.session_state.user_selection.get('llm_model'):
                            del st.session_state.user_selection['llm_model']
                        with st.spinner('Testing Connection'):
                            st.session_state.user_selection.update({'llm_model':Model.get_groq(st.session_state.user_selection['api_key'], st.session_state.user_selection['model_name'])})

                            model = st.session_state.user_selection.get('llm_model')
                            res = model.invoke('hello')
                            st.session_state.config_saved = True
                            # debug.info(f'Model working response - {res}')
                                            
                        # debug.info('GROQ - ',st.session_state.user_selection.get('llm_model')) # log
                    
                    except Exception as e:
                        # debug.error(f'Un-able establish connection with Groq - \n{e}')
                        st.error(f'Un-able establish connection with Groq - \n{e}')
                else:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")

                    # debug.error('Groq No API KEY')  # log

            elif provider == 'OLLAMA':
                # -- provider -- model -- #
                st.session_state.user_selection.update({'model':'ollama', 'model_name':st.selectbox(label='Ollama Model', options=Config().get_ollama_model())})

                if st.session_state.user_selection['model_name'] and st.button(label='Proceed', key='Stage1 Ollama'):
                    try:
                        if st.session_state.user_selection.get('llm_model'):
                            del st.session_state.user_selection['llm_model']
                        st.session_state.user_selection.update({'llm_model':Model.get_ollama(st.session_state.user_selection['model_name'])})

                        with st.spinner('Testing Connection'):
                            model = st.session_state.user_selection.get('llm_model')
                            res = model.invoke('hello')
                            st.session_state.config_saved = True
                        #     debug.info(f'Model working - {res}') # log
                        # debug.info(f"Ollama - {st.session_state.user_selection.get('llm_model')}") # log
                    except Exception as e:
                        # debug.info('Ollama Model empty, object not created')
                        st.error(('Ollama Model empty, object not created'))

                    # log 
                    # debug.info('Ollama - ',st.session_state.user_selection.get('model_name'), st.session_state.user_selection.get('llm_model'))
                    
                else:
                    st.warning("⚠️ Select a Model")

                    # debug.error('Ollama Unable to form connection')
            else:
                st.warning("⚠️ Select an Option to Start")

        # --- Show selected config
        elif st.session_state.config_saved:
            st.markdown("### Selected Configuration")
            st.write(f"**Model**: {st.session_state.user_config['model']}")
            st.write(f"**Model Type**: {st.session_state.user_config['llm_model']}")

            if st.button('Reset Config'):
                st.session_state.config_saved = False
                st.session_state.user_selection = {}
                st.rerun()