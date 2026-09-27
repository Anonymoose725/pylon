# explain.py receives a response regardless of the LLM provider of choice
from ai.providers.base import LLMProvider

def explain(finding, source_snippet: str, provider: LLMProvider) -> str:
    prompt = f"..." # the prompt to ask for clarirication goes here. optimize heavily.
    return provider.complete(prompt)