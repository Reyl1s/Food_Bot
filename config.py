import os
from dotenv import load_dotenv, dotenv_values

config = None

def init_config():
    global config
    
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        config = dotenv_values(".env")

def get_config():
    return config
