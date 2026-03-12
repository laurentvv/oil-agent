"""
Modèles Pydantic pour la validation des configurations et réponses.

Ce module définit les modèles de données utilisés dans le module
llama_cpp_wrapper pour la validation des configurations et des réponses
du serveur llama-server.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from pathlib import Path


class ServerConfig(BaseModel):
    """Configuration du serveur llama-server.
    
    Ce modèle définit tous les paramètres de configuration possibles
    pour le serveur llama-server. Les valeurs par défaut sont optimisées
    pour une utilisation standard.
    
    Attributes:
        executable: Nom de l'exécutable du serveur (doit être dans le PATH)
        host: Adresse d'écoute du serveur
        port: Port d'écoute du serveur (1-65535)
        n_gpu_layers: Nombre de couches GPU (-1 pour toutes, 0 pour CPU uniquement)
        n_threads: Nombre de threads CPU (0 pour auto-détection)
        ctx_size: Taille du contexte en tokens
        batch_size: Taille du batch de traitement
        ubatch_size: Taille du micro-batch
        cache_type_k: Type de cache pour les clés (f16, q8_0, etc.)
        cache_type_v: Type de cache pour les valeurs
    
    Example:
        config = ServerConfig(
            executable="llama-server",
            host="127.0.0.1",
            port=8080,
            n_gpu_layers=-1
        )
    """
    executable: str = Field(
        default="llama-server",
        description="Exécutable du serveur"
    )
    host: str = Field(
        default="127.0.0.1",
        description="Adresse d'écoute"
    )
    port: int = Field(
        default=8080,
        ge=1,
        le=65535,
        description="Port d'écoute"
    )
    n_gpu_layers: int = Field(
        default=-1,
        ge=-1,
        description="Nombre de couches GPU (-1 pour toutes)"
    )
    n_threads: int = Field(
        default=0,
        ge=-1,
        description="Nombre de threads CPU (0 pour auto)"
    )
    ctx_size: int = Field(
        default=8192,
        gt=0,
        description="Taille du contexte"
    )
    batch_size: int = Field(
        default=512,
        gt=0,
        description="Taille du batch"
    )
    ubatch_size: int = Field(
        default=128,
        gt=0,
        description="Taille du micro-batch"
    )
    cache_type_k: str = Field(
        default="f16",
        description="Type de cache K"
    )
    cache_type_v: str = Field(
        default="f16",
        description="Type de cache V"
    )
    
    @field_validator('executable')
    @classmethod
    def validate_executable(cls, v):
        """Valide que l'exécutable existe dans le PATH.
        
        Args:
            v: Nom de l'exécutable
            
        Returns:
            Le nom de l'exécutable s'il est valide
            
        Raises:
            ValueError: Si l'exécutable n'est pas trouvé
        """
        import shutil
        if not shutil.which(v):
            raise ValueError(f"Exécutable introuvable : {v}")
        return v


class ModelConfig(BaseModel):
    """Configuration du modèle LLM.
    
    Ce modèle définit les paramètres de configuration pour le modèle
    de langage utilisé par le serveur llama-server.
    
    Attributes:
        name: Nom du modèle (utilisé dans les requêtes API)
        path: Chemin vers le fichier du modèle (.gguf)
        api_base: URL de base de l'API (dérivée de server_config si None)
        num_ctx: Taille du contexte en tokens
    
    Example:
        config = ModelConfig(
            name="qwen3.5-9b",
            path="C:/Modeles/Qwen3.5-9B-Q4_K_S.gguf",
            num_ctx=8192
        )
    """
    name: str = Field(
        ...,
        description="Nom du modèle"
    )
    path: str = Field(
        ...,
        description="Chemin vers le fichier du modèle"
    )
    api_base: Optional[str] = Field(
        None,
        description="URL de base de l'API (dérivée si None)"
    )
    num_ctx: int = Field(
        default=8192,
        gt=0,
        description="Taille du contexte"
    )
    
    @field_validator('path')
    @classmethod
    def path_exists(cls, v):
        """Vérifie que le fichier du modèle existe.
        
        Args:
            v: Chemin vers le fichier du modèle
            
        Returns:
            Le chemin validé
            
        Raises:
            ValueError: Si le fichier n'existe pas ou n'est pas un fichier
        """
        path = Path(v)
        if not path.exists():
            raise ValueError(f"Modèle introuvable : {v}")
        if not path.is_file():
            raise ValueError(f"Le chemin n'est pas un fichier : {v}")
        return v


class GenerationParams(BaseModel):
    """Paramètres de génération de texte.
    
    Ce modèle définit tous les paramètres de génération possibles
    pour contrôler le comportement du modèle lors de la génération
    de texte.
    
    Attributes:
        max_tokens: Nombre maximum de tokens à générer
        temperature: Température de génération (0.0 = déterministe, 2.0 = très créatif)
        top_p: Top-p sampling (nucleus sampling)
        top_k: Top-k sampling
        repeat_penalty: Pénalité de répétition (1.0 = pas de pénalité)
        presence_penalty: Pénalité de présence (-2.0 à 2.0)
        frequency_penalty: Pénalité de fréquence (-2.0 à 2.0)
        stop: Séquences d'arrêt pour stopper la génération
    
    Example:
        params = GenerationParams(
            max_tokens=512,
            temperature=0.7,
            top_p=0.9
        )
    """
    max_tokens: int = Field(
        default=512,
        ge=1,
        description="Nombre maximum de tokens"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Température"
    )
    top_p: float = Field(
        default=0.9,
        ge=0.0,
        le=1.0,
        description="Top-p sampling"
    )
    top_k: int = Field(
        default=40,
        ge=0,
        description="Top-k sampling"
    )
    repeat_penalty: float = Field(
        default=1.0,
        ge=0.0,
        description="Pénalité de répétition"
    )
    presence_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Pénalité de présence"
    )
    frequency_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Pénalité de fréquence"
    )
    stop: Optional[List[str]] = Field(
        None,
        description="Séquences d'arrêt"
    )


class Message(BaseModel):
    """Message de chat.
    
    Ce modèle représente un message dans une conversation de chat.
    Il est utilisé pour les requêtes de type chat/completions.
    
    Attributes:
        role: Rôle du message ('user', 'assistant', 'system')
        content: Contenu du message
    
    Example:
        msg = Message(
            role="user",
            content="Bonjour, comment allez-vous ?"
        )
    """
    role: str = Field(
        ...,
        description="Rôle : 'user', 'assistant', 'system'"
    )
    content: str = Field(
        ...,
        description="Contenu du message"
    )


class GenerationResponse(BaseModel):
    """Réponse de génération.
    
    Ce modèle représente la réponse retournée par le serveur
    llama-server après une génération de texte.
    
    Attributes:
        content: Texte généré par le modèle
        model: Nom du modèle utilisé
        tokens_used: Nombre total de tokens utilisés (prompt + génération)
        finish_reason: Raison de fin de génération (stop, length, etc.)
    
    Example:
        response = GenerationResponse(
            content="Bonjour ! Je vais bien, merci.",
            model="qwen3.5-9b",
            tokens_used=42,
            finish_reason="stop"
        )
    """
    content: str = Field(
        ...,
        description="Texte généré"
    )
    model: str = Field(
        ...,
        description="Nom du modèle utilisé"
    )
    tokens_used: int = Field(
        default=0,
        description="Nombre de tokens utilisés"
    )
    finish_reason: Optional[str] = Field(
        None,
        description="Raison de fin"
    )
