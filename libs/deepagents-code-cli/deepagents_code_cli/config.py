import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.codebase_path = os.getenv("CODEBASE_PATH")
        self.reference_codebase_path = os.getenv("REFERENCE_CODEBASE_PATH")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gpt-4o")

    def validate(self):
        if not self.codebase_path:
            raise ValueError("CODEBASE_PATH environment variable is not set")
        if not self.reference_codebase_path:
            raise ValueError("REFERENCE_CODEBASE_PATH environment variable is not set")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

config = Config()
