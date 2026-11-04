from google import genai
from ai.providers.base import LLMProvider

class GoogleProvider(LLMProvider):
    def __init__(self, model: str = "gemini-3.8-flash"):
        self.client = genai.Client()
        self.model = model
    
    def complete(self, prompt: str) -> str:
        response = self.client.interactions.create(
            model=self.model,
            input=prompt
        )
        return response.output_text
