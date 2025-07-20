import streamlit as st
import json, requests
from src.backend.agent_tool import tools
from langchain.prompts import PromptTemplate

# ------------------------------------- #
API_BASE_URL = "http://127.0.0.1:8000/"
# ------------------------------------- #

def get_current_model():
    response = requests.get(f"{API_BASE_URL}/current_model")
    if response.status_code==200:
        model = response.json()['current_model']
        return model
    else:
        st.error("[page_2|get_current_model] Model instance is not available")
        st.stop()

def get_llm_response(model, query):
    payload = {
        "user_model":model,
        "user_message":query
    }
    response = requests.post(f"{API_BASE_URL}/invoke",json=payload)
    return response

tool = tools()
model = get_current_model()
model_with_tool = model.bind_tools([tool])
prompt = PromptTemplate(template="""
                                    Your a agent tasked for solving users mathemtical question. Logically arrive at the solution and provide a detailed explanation
                                    and display it point wise for the question below
                                    Question:{question}
                                    Answer:                                
                                """,
                        input_variables=['question'])

get_llm_response(model=model_with_tool, query=prompt)
