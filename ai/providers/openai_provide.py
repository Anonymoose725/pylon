from openai import OpenAI
from ai.providers.base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = "gpt-5.5"):
        self.client = OpenAI()
        self.model = model
        
    def complete(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model = self.model,
            stream = False,
            message = [{"role": "user", "content": prompt}]
        )
        return response.choice[0].message.content # no autofill on structure. could be wrong