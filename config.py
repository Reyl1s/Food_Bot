import os
from dotenv import load_dotenv, dotenv_values

class Config:
    data = []

    def __init__(self):
        self.data = self.get_config()

    def get_config(_):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            config = dotenv_values(".env")

            return config
        return None

    
