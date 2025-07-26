from pydantic import BaseModel, Field
from typing import Annotated, Optional, TypedDict, Dict, Any
from operator import add
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

class State(TypedDict):
    model : str
    user_input : str
    response : str
    provider : str
    provider_model : str
    message_history : Annotated[Any,add]

class GroqConfigRequest(BaseModel):
    api_key: str = Field(..., description="Groq API key to access GROQ")
    model_name: str = Field(..., description="Model selected which is hosted on GROQ")

class OllamaConfigRequest(BaseModel):
    model_name: str = Field(..., description="Model selected which is hosted by Ollama")

class ModelStatusCheck(BaseModel):
    success: bool
    message : str
    output : str
    config : Dict[str, Any]

class User_Message(BaseModel):
    user_message : str
    user_model : Any

class Model_Answer(BaseModel):
    response : str
    success : bool
    error_message : Optional[str] = None