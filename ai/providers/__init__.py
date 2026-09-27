from ai.providers.base import LLMProvider
from ai.providers.anthropic_provide import AnthropicProvider
from ai.providers.ollama_provide import OllamaProvider
from ai.providers.openai_provide import OpenAIProvider

def get_provider(name: str) -> LLMProvider:
    all_providers = {
        "ollama": OllamaProvider,
        "anthropic": AnthropicProvider,
        "openai": OpenAIProvider
    }
    
    if name not in all_providers:
        raise ValueError(f"Unknown LLM provider: {name}. Choose from: {list(all_providers.keys())}")
    return all_providers[name]() 
    # note that () calls it as a function i.e. it returns the respective provider function