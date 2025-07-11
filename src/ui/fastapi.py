from fastapi import FastAPI, HTTPException
import uvicorn
import streamlit as st
import os,sys

# ---------- #
from src.backend.configuration.config import Config
from src.schema import GroqConfigRequest, OllamaConfigRequest, ModelStatusCheck, User_Message, Model_Answer
from src.backend.model import Model

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

app = FastAPI(title="LLM for Mathematics", version="0.0.1")

current_config = {}
current_model = None

@app.get("/")
async def root():
    return {'message':'LLM application is running'}

@app.get("/provider")
async def get_model_provider():
    try:
        models = Config.get_llm()
        if models:
            return {"models providers":models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No provider found in the server: {str(e)}")

@app.get("/model/{provider}")
async def get_model(provider: str):
    # Models within each Providers
    try:
        if provider == 'GROQ':
            return {'models' : Config.get_groq_model()} # if no details found in config then except will handel it
        
        elif provider == 'OLLAMA':
            return {'models' : Config.get_ollama_model()}
        
        else:
            raise HTTPException(status_code=400, detail='Model Provider does not exists')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model selcted was not found: {str(e)}")
    
@app.post("/groq/model", response_model=ModelStatusCheck)
async def groq_model_test(request: GroqConfigRequest):
    # Check model Connected? Save model call instace.
    try:
        global current_model, current_config
        model = Model.get_groq(request.api_key, request.model_name)
        test_responce = model.invoke('Testing Connection')

        # model works so storing it 
        current_model = model
        current_config = {
            "provider": "groq",
            "model_name": request.model_name,
            "key": "..."+request.api_key[-6:]
        }

        return {
            "success" : True,
            "message" : "Groq is Connecetd",
            "output" : str(test_responce.content),
            "config" : current_config
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to establish connection with GROQ: {str(e)}")
    
@app.post("/ollama/model", response_model=ModelStatusCheck)
async def ollama_model_test(request: OllamaConfigRequest):
    try:
        global current_config, current_model
        model = Model.get_ollama(request.model_name)
        test_responce = model.invoke('Testing Connection')

        # model save
        current_model = model
        current_config = {
            "provider": "ollama",
            "model_name": request.model_name
        }

        return{
            "success" : True,
            "message" : "Ollama is Connected",
            "output" : str(test_responce.content),
            "config" : current_config
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to establish connection with Ollama: {str(e)}")

@app.get("/model_config")
async def get_current_model_config():
    try:
        global current_config, current_model

        if not current_model:
            raise HTTPException(status_code=400, detail="No model configured")
        
        return {"config": current_config, "model_ready": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error occured at server side")

@app.delete("/config_reset")
async def reset_config():
    """Reset the current configuration"""
    global current_model, current_config
    
    current_model = None
    current_config = {}
    
    return {"message": "Configuration reset successfully"}

@app.post("/invoke", response_model=Model_Answer)
async def chat(request:User_Message):
    global current_model
    
    if not current_model:
        raise HTTPException(status_code=400, detail="No model configured. Please configure a model first.")
    
    try:
        response = current_model.invoke(request.message)
        return {
            "response" : response,
            "success" : True
        }
    except Exception as e:
        return {
            "response" : "",
            "success" : False,
            "error_message" : f"Error generating response: {str(e)}"
        }