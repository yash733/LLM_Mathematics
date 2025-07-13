from configparser import ConfigParser
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

class Config:
    config_info = ConfigParser()
    config_path = f'{os.getcwd()}\\src\\backend\\configuration\\config.ini'
    with open(config_path, encoding='utf-8') as f:
        config_info.read_file(f)

    @staticmethod
    def get_llm():
        return Config.config_info['DEFAULT'].get('LLM').split(', ')
    
    @staticmethod
    def get_groq_model():
        return Config.config_info['DEFAULT'].get('LLM_GROQ').split(', ')
    
    @staticmethod
    def get_ollama_model():
        return Config.config_info['DEFAULT'].get('LLM_OLLAMA').split(', ')
    
    @staticmethod
    def get_options():
        return Config.config_info['DEFAULT'].get('OPTIONS').split(', ')