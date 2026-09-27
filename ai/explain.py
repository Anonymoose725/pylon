# explain.py receives a response regardless of the LLM provider of choice
from ai.providers.base import LLMProvider

def explain_finding(finding, source_snippet: str, provider: LLMProvider) -> str:
    """Explain a finding using an LLM and return its response"""
    # provide finding in destructured form
    # provide source_snippet in python markdown
    prompt = f"..." # the prompt to ask for clarirication goes here. optimize heavily. TBD!
    return provider.complete(prompt)