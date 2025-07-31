import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import streamlit as st

from sidebar import sidebar_
# from page_1 import readme_
from page_2 import page_2_ui
from page_1 import home_page

# if not "selection" in st.session_state:
#     st.session_state.selection = {}

if not "current_config" in st.session_state:
    st.session_state.current_config = {}

if "config" not in st.session_state:
    st.session_state.config = ''

if not "message_history" in st.session_state:
    st.session_state.message_history = []

if not 'config_saved' in st.session_state:
    st.session_state.config_saved = False
# ------------------------------------------- #

st.set_page_config(page_title="Mathemacis Assistant",
                   page_icon='✖️',
                   layout='wide')

st.title("🧮 Maths Problem Solver")
sidebar_()

if 'page' not in st.session_state:
    st.session_state.page = 'page1'

# Define navigation function
def navigate_to(page_name):
    st.session_state.page = page_name

# Navigation buttons
st.sidebar.button("Home", on_click=navigate_to, args=('page1',))
st.sidebar.button("Chat Bot", on_click=navigate_to, args=('page2',))

# Render pages based on session state
if st.session_state.page == 'page1':
    home_page()

elif st.session_state.page == 'page2':
    page_2_ui()
 
