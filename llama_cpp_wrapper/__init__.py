"""
Module llama_cpp_wrapper - Encapsulation autonome de llama.cpp.

Ce module fournit une interface Python simple et robuste pour utiliser
llama.cpp (llama-server) comme alternative à Ollama dans vos projets.

Usage basique:
    >>> from llama_cpp_wrapper import LlamaServer, quick_generate
    >>>
    >>> # Avec la classe
    >>> server = LlamaServer(model_path="path/to/model.gguf")
    >>> response = server.generate("Hello, world!")
    >>> print(response.content)
    >>> server.stop()
    >>>
    >>> # Avec la fonction utilitaire
    >>> result = quick_generate("path/to/model.gguf", "Hello, world!")
    >>> print(result)

Usage avec gestionnaire de contexte:
    >>> from llama_cpp_wrapper import LlamaServer
    >>>
    >>> with LlamaServer(model_path="path/to/model.gguf") as server:
    >>>     response = server.generate("Hello, world!")
    >>>     print(response.content)
    >>> # Le serveur s'arrête automatiquement à la sortie du bloc with

Usage avec configuration:
    >>> from llama_cpp_wrapper import LlamaServer
    >>> from pathlib import Path
    >>>
    >>> with LlamaServer(config_path=Path("config.json")) as server:
    >>>     response = server.generate("Hello, world!")
    >>>     print(response.content)

Intégration avec DSPy:
    >>> import dspy
    >>> from llama_cpp_wrapper import LlamaServer
    >>>
    >>> server = LlamaServer(model_path="model.gguf", model_name="model")
    >>> lm = dspy.LM(
    >>>     model=f"openai/{server.model_config.name}",
    >>>     api_base=server.api_base,
    >>>     api_key="dummy",
    >>>     model_type="chat"
    >>> )
    >>> dspy.configure(lm=lm)
"""

from .core import LlamaServer, quick_generate, quick_chat
from .models import (
    ServerConfig, ModelConfig, GenerationParams, 
    Message, GenerationResponse
)
from .config import ConfigManager
from .exceptions import (
    LlamaCppError,
    ServerStartupError,
    ServerConnectionError,
    ModelNotFoundError,
    GenerationError,
    ConfigurationError,
    TimeoutError
)

__version__ = "1.0.0"
__all__ = [
    # Classes principales
    "LlamaServer",
    "ConfigManager",
    
    # Modèles
    "ServerConfig",
    "ModelConfig",
    "GenerationParams",
    "Message",
    "GenerationResponse",
    
    # Exceptions
    "LlamaCppError",
    "ServerStartupError",
    "ServerConnectionError",
    "ModelNotFoundError",
    "GenerationError",
    "ConfigurationError",
    "TimeoutError",
    
    # Fonctions utilitaires
    "quick_generate",
    "quick_chat",
]
