import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import streamlit as st

from sidebar import sidebar_
# from page_1 import readme_
from page_2 import page_2_ui
# ------------------------------------------- #
if not "selection" in st.session_state:
    st.session_state.selection = {}

if not "message_history" in st.session_state:
    st.session_state.message_history = []

if not "current_config" in st.session_state:
    st.session_state.current_config = {}

if not 'config_saved' in st.session_state:
    st.session_state.config_saved = False
# ------------------------------------------- #

st.set_page_config(page_title="Mathemacis Assistant",
                   page_icon='✖️➗➕➖',
                   layout='wide')

st.title('Matematics problem solver')
sidebar_()

page_2_ui()