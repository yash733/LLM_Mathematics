import streamlit as st
import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

def home_page():
    st.set_page_config(page_title="Maths Problem Solver", page_icon="🧮", layout="centered")
  
    st.markdown(
        """
        Welcome to **Maths Problem Solver**!  
        This app lets you solve mathematical problems using advanced Large Language Models (LLMs) and symbolic computation tools.

        ---
        ### 🚀 Features
        - Natural language math problem solving
        - Symbolic computation (SymPy)
        - Wikipedia search integration
        - Multiple LLM providers (Groq, Ollama, etc.)
        - Step-by-step explanations

        ---
        ### 🛠️ Quick Start

        1. **Install Dependencies**
            ```sh
            pip install uv
            python -m venv .myvenv
            .myvenv/Scripts/activate
            uv pip install -r requirements.txt
            ```

        2. **Run the Backend**
            ```sh
            uvicorn src.ui.fastapi:app --reload
            ```

        3. **Launch the Frontend**
            ```sh
            streamlit run src/ui/app.py
            ```

        ---
        ### 📚 How to Use

        - Select your preferred LLM provider and model.
        - Enter your math question in natural language.
        - View detailed, step-by-step solutions and explanations.

        ---
        ### 💡 About

        This project combines the power of LLMs and symbolic math engines to help you solve and understand mathematical problems interactively.

        ---
        """
    )
    st.info("Get started by selecting a provider and entering your first math question!")
