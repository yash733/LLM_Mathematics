import streamlit as st
import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

def readme_():

    st.markdown("""
                ### Install Dependencies
                    - `pip install uv`
                    - `python -m venv .myvenv`
                    - `.myvenv/Scripts/activate`
                    - `uv pip install -r requirements.txt`
                
                ### Execute
                    - `uvicorn .src.ui.fastapi:app --reload`
                    - `streamlit run src\ui\app.py`
                """)