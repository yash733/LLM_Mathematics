import streamlit as st

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