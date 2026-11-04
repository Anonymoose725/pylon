from google import genai
from ai.providers.base import LLMProvider

class GoogleProvider(LLMProvider):
    def __init__(self, model: str = "gemini-3.6-flash"):
        self.client = genai.Client()
        self.model = model
    
    def complete(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
