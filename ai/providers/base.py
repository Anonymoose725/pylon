# ABC = abstract base class, much like a java interface
# subclasses must implement complete(), much like subclasses of interfaces abstract methods
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
            """Send a prompt and return the model's response"""