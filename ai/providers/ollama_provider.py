import requests
from ai.providers.base import LLMProvider

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "qwen2.5-coder:7b"):
        self.model = model
    
    def complete(self, prompt):
        response = requests.post(
            "http://localhost:11434/api/generate", # post api endpoint
            json={"model": self.model, "prompt": prompt, "stream": False} # dont stream since we want it to return one chunk
        )
        response.raise_for_status() # raises http error if one occurred
        return response.json()["response"]