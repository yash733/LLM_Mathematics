from pydantic import BaseModel, Field
from typing import Annotated, Optional, TypedDict, Dict, Any

class State(TypedDict):
    model : str
    user_input : str
    responsce : str
    provider : str
    provider_model : str

class GroqConfigRequest(BaseModel):
    api_key: str = Field(..., description="Groq API key to access GROQ")
    model_name: str = Field(..., description="Model selected which is hosted on GROQ")

class OllamaConfigRequest(BaseModel):
    model_name: str = Field(..., description="Model selected which is hosted by Ollama")

class ModelStatusCheck(BaseModel):
    success: bool
    message : str
    output : str

class User_Message(BaseModel):
    message : str

class Model_Answer(BaseModel):
    response : str
    success : bool
    error_message : Optional[str] = None