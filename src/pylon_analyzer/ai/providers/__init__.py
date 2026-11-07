from pylon_analyzer.ai.providers.base import LLMProvider
import importlib
# from pylon_analyzer.ai.providers.anthropic_provider import AnthropicProvider
# from pylon_analyzer.ai.providers.ollama_provider import OllamaProvider
# from pylon_analyzer.ai.providers.openai_provider import OpenAIProvider
# from pylon_analyzer.ai.providers.google_provider import GoogleProvider

# converstion from explicit calls to a dict string-matching
_ALL_PROVIDERS = {
    "ollama": ("ollama_provider", "OllamaProvider", "ollama"),
    "anthropic": ("anthropic_provider", "AnthropicProvider", "anthropic"),
    "openai": ("openai_provider", "OpenAIProvider", "openai"),
    "google": ("google_provider", "GoogleProvider", "google-genai")
}

def get_provider(name: str) -> LLMProvider:
    
    if name not in _ALL_PROVIDERS:
        raise ValueError(f"Unknown LLM provider: {name}. Choose from: {list(_ALL_PROVIDERS)}")
    
    module_name, class_name, extra = _ALL_PROVIDERS[name]
    try:
        module = importlib.import_module(f"pylon_analyzer.ai.providers.{module_name}")
    except ImportError as e:
        raise ImportError(
            f"The '{name}' provider requires installation of an optional dependency. Do you need to install it? "
            f'Install with: pip install "pylon-analyzer[{extra}]"'
        ) from e
    
    return getattr(module, class_name)() # callable