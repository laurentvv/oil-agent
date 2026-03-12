"""
Gestion de configuration pour le module llama_cpp_wrapper.

Ce module fournit la classe ConfigManager pour gérer la configuration
du serveur et du modèle, avec support pour les fichiers JSON et YAML.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import json
import yaml

from .models import ServerConfig, ModelConfig
from .exceptions import ConfigurationError


class ConfigManager:
    """Gestionnaire de configuration pour llama_cpp_wrapper.
    
    Cette classe permet de gérer la configuration du serveur llama-server
    et du modèle LLM. Elle supporte le chargement depuis des fichiers
    JSON ou YAML, ainsi que depuis des dictionnaires.
    
    Attributes:
        config_path: Chemin vers le fichier de configuration (optionnel)
        _server_config: Configuration du serveur (ServerConfig)
        _model_config: Configuration du modèle (ModelConfig)
    
    Example:
        # Chargement depuis un fichier
        config = ConfigManager(config_path="config.json")
        
        # Configuration par programme
        config = ConfigManager()
        config.set_server_config(ServerConfig(port=8080))
        config.set_model_config(ModelConfig(name="model", path="model.gguf"))
        
        # Sauvegarde
        config.save_to_file("new_config.json")
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialise le gestionnaire de configuration.
        
        Args:
            config_path: Chemin vers le fichier de configuration (JSON ou YAML).
                        Si fourni et existe, la configuration est chargée automatiquement.
        
        Example:
            # Sans fichier de configuration
            config = ConfigManager()
            
            # Avec chargement automatique
            config = ConfigManager(config_path=Path("config.json"))
        """
        self.config_path = config_path
        self._server_config: Optional[ServerConfig] = None
        self._model_config: Optional[ModelConfig] = None
        
        if config_path and config_path.exists():
            self.load_from_file(config_path)
    
    def load_from_file(self, config_path: Path) -> None:
        """Charge la configuration depuis un fichier.
        
        Cette méthode charge la configuration depuis un fichier JSON ou YAML.
        Le fichier doit contenir deux sections : 'server' et 'model'.
        
        Args:
            config_path: Chemin vers le fichier de configuration
            
        Raises:
            ConfigurationError: Si le fichier est invalide ou ne peut pas être lu
        
        Example:
            config = ConfigManager()
            config.load_from_file(Path("config.json"))
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix in ['.yml', '.yaml']:
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
            
            self._server_config = ServerConfig(**data.get('server', {}))
            self._model_config = ModelConfig(**data.get('model', {}))
            
        except Exception as e:
            raise ConfigurationError(f"Erreur lors du chargement de la configuration : {e}")
    
    def load_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Charge la configuration depuis un dictionnaire.
        
        Cette méthode permet de charger la configuration depuis un dictionnaire
        Python, ce qui est utile pour la configuration par programme.
        
        Args:
            config_dict: Dictionnaire de configuration avec les clés 'server' et 'model'
        
        Example:
            config = ConfigManager()
            config.load_from_dict({
                "server": {"port": 8080, "host": "127.0.0.1"},
                "model": {"name": "model", "path": "model.gguf"}
            })
        """
        self._server_config = ServerConfig(**config_dict.get('server', {}))
        self._model_config = ModelConfig(**config_dict.get('model', {}))
    
    @property
    def server_config(self) -> ServerConfig:
        """Retourne la configuration du serveur.
        
        Si aucune configuration n'a été définie, retourne une configuration
        par défaut.
        
        Returns:
            Configuration du serveur (ServerConfig)
        
        Example:
            config = ConfigManager()
            server_config = config.server_config
            print(f"Port: {server_config.port}")
        """
        if self._server_config is None:
            self._server_config = ServerConfig()
        return self._server_config
    
    @property
    def model_config(self) -> ModelConfig:
        """Retourne la configuration du modèle.
        
        Raises:
            ConfigurationError: Si la configuration du modèle n'a pas été définie
        
        Returns:
            Configuration du modèle (ModelConfig)
        
        Example:
            config = ConfigManager()
            config.load_from_dict({"model": {"name": "model", "path": "model.gguf"}})
            model_config = config.model_config
            print(f"Nom: {model_config.name}")
        """
        if self._model_config is None:
            raise ConfigurationError("Configuration du modèle non définie")
        return self._model_config
    
    def set_server_config(self, config: ServerConfig) -> None:
        """Définit la configuration du serveur.
        
        Args:
            config: Configuration du serveur (ServerConfig)
        
        Example:
            config = ConfigManager()
            server_config = ServerConfig(port=8080, host="127.0.0.1")
            config.set_server_config(server_config)
        """
        self._server_config = config
    
    def set_model_config(self, config: ModelConfig) -> None:
        """Définit la configuration du modèle.
        
        Args:
            config: Configuration du modèle (ModelConfig)
        
        Example:
            config = ConfigManager()
            model_config = ModelConfig(name="model", path="model.gguf")
            config.set_model_config(model_config)
        """
        self._model_config = config
    
    def save_to_file(self, config_path: Path) -> None:
        """Sauvegarde la configuration dans un fichier.
        
        Cette méthode sauvegarde la configuration actuelle dans un fichier
        JSON ou YAML, selon l'extension du fichier.
        
        Args:
            config_path: Chemin vers le fichier de sauvegarde
        
        Example:
            config = ConfigManager()
            config.set_model_config(ModelConfig(name="model", path="model.gguf"))
            config.save_to_file(Path("config.json"))
        """
        data = {
            'server': self.server_config.model_dump(),
            'model': self.model_config.model_dump()
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            if config_path.suffix in ['.yml', '.yaml']:
                yaml.dump(data, f, default_flow_style=False)
            else:
                json.dump(data, f, indent=2)
