import anthropic
from ai.providers.base import LLMProvider

class AnthropicProvider(LLMProvider):
    def __init__(self, model: str = "claude-sonnet-5"): # maybe opus is better?
        self.client = anthropic.Anthropic()
        self.model = model
    
    def complete(self, prompt: str) -> str:
        response = self.client.messages.create(
            model = self.model,
            max_tokens = 500, # limit size since claude drones on
            messages = [{"role": "user", "content": prompt}]
        )
        return response.content[0].text