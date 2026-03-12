"""
Classe principale pour la gestion de llama-server.

Ce module contient la classe LlamaServer qui encapsule toutes les fonctionnalités
nécessaires pour démarrer, gérer et utiliser llama-server de manière transparente.
"""

import subprocess
import sys
import time
import requests
import atexit
import logging
from typing import Optional, List, Dict, Any, Union
from contextlib import contextmanager
from pathlib import Path

from .models import (
    ServerConfig, ModelConfig, GenerationParams, 
    Message, GenerationResponse
)
from .config import ConfigManager
from .exceptions import (
    ServerStartupError, ServerConnectionError, 
    ModelNotFoundError, GenerationError, TimeoutError
)
from .utils import (
    check_port_available, wait_for_server, kill_process_on_port,
    format_llama_command, validate_model_path
)


class LlamaServer:
    """Classe principale pour gérer llama-server.
    
    Cette classe encapsule toutes les fonctionnalités nécessaires pour
    démarrer, gérer et utiliser llama-server de manière transparente.
    Elle supporte le gestionnaire de contexte pour un nettoyage automatique
    des ressources.
    
    Attributes:
        server_config: Configuration du serveur (lecture seule)
        model_config: Configuration du modèle (lecture seule)
        api_base: URL de base de l'API (lecture seule)
        is_running: État du serveur (lecture seule)
    
    Example:
        # Utilisation basique
        server = LlamaServer(model_path="model.gguf", model_name="model")
        response = server.generate("Hello, world!")
        print(response.content)
        server.stop()
        
        # Avec gestionnaire de contexte
        with LlamaServer(model_path="model.gguf", model_name="model") as server:
            response = server.generate("Hello, world!")
            print(response.content)
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        model_name: Optional[str] = None,
        server_config: Optional[ServerConfig] = None,
        model_config: Optional[ModelConfig] = None,
        config_path: Optional[Path] = None,
        auto_start: bool = True,
        auto_stop: bool = True
    ):
        """Initialise le gestionnaire llama-server.
        
        Args:
            model_path: Chemin vers le fichier modèle (prioritaire sur config)
            model_name: Nom du modèle (prioritaire sur config)
            server_config: Configuration du serveur
            model_config: Configuration du modèle
            config_path: Chemin vers un fichier de configuration
            auto_start: Démarrer automatiquement le serveur (par défaut: True)
            auto_stop: Arrêter automatiquement le serveur à la destruction (par défaut: True)
        
        Example:
            # Configuration par paramètres
            server = LlamaServer(
                model_path="model.gguf",
                model_name="my-model",
                server_config=ServerConfig(port=8080),
                auto_start=True,
                auto_stop=True
            )
            
            # Configuration par fichier
            server = LlamaServer(config_path=Path("config.json"))
        """
        self._process: Optional[subprocess.Popen] = None
        self._auto_stop = auto_stop
        self._started = False
        
        # Configuration
        self._config_manager = ConfigManager(config_path)
        
        # Appliquer les configurations prioritaires
        if server_config:
            self._config_manager.set_server_config(server_config)
        if model_config:
            self._config_manager.set_model_config(model_config)
        
        # Appliquer les paramètres directs
        if model_path:
            self._config_manager.model_config.path = model_path
        if model_name:
            self._config_manager.model_config.name = model_name
        
        # Logger
        self._logger = logging.getLogger(__name__)
        
        # Démarrage automatique
        if auto_start:
            self.start()
    
    @property
    def server_config(self) -> ServerConfig:
        """Retourne la configuration du serveur.
        
        Returns:
            Configuration du serveur (ServerConfig)
        """
        return self._config_manager.server_config
    
    @property
    def model_config(self) -> ModelConfig:
        """Retourne la configuration du modèle.
        
        Returns:
            Configuration du modèle (ModelConfig)
        """
        return self._config_manager.model_config
    
    @property
    def api_base(self) -> str:
        """Retourne l'URL de base de l'API.
        
        Si api_base est défini dans model_config, il est utilisé.
        Sinon, il est construit à partir de host et port.
        
        Returns:
            URL de base de l'API (ex: http://127.0.0.1:8080)
        """
        if self.model_config.api_base:
            return self.model_config.api_base
        return f"http://{self.server_config.host}:{self.server_config.port}"
    
    @property
    def is_running(self) -> bool:
        """Vérifie si le serveur est en cours d'exécution.
        
        Returns:
            True si le serveur est en cours d'exécution, False sinon
        """
        try:
            response = requests.get(f"{self.api_base}/health", timeout=2)
            return response.status_code == 200
        except Exception:
            return False
    
    def start(self, timeout: int = 60) -> bool:
        """Démarre le serveur llama-server.
        
        Cette méthode démarre le serveur llama-server avec la configuration
        actuelle. Elle vérifie la disponibilité du port, valide le modèle,
        et attend que le serveur soit prêt.
        
        Args:
            timeout: Timeout en secondes pour l'attente du serveur (par défaut: 60)
            
        Returns:
            True si le démarrage a réussi
            
        Raises:
            ServerStartupError: Si le démarrage échoue
            ModelNotFoundError: Si le modèle n'existe pas
            TimeoutError: Si le serveur ne devient pas prêt dans le délai imparti
        
        Example:
            server = LlamaServer(model_path="model.gguf", model_name="model", auto_start=False)
            server.start(timeout=30)
        """
        if self.is_running:
            self._logger.info("✅ llama-server est déjà en cours d'exécution")
            self._started = True
            return True
        
        # Valider le modèle
        validate_model_path(self.model_config.path)
        
        # Vérifier le port
        if not check_port_available(self.server_config.port, self.server_config.host):
            self._logger.warning(
                f"⚠️ Port {self.server_config.port} déjà utilisé, "
                "tentative de libération..."
            )
            kill_process_on_port(self.server_config.port, self.server_config.host)
        
        # Construire la commande
        cmd = format_llama_command(
            self.server_config.executable,
            self.model_config.path,
            self.server_config.model_dump()
        )
        
        self._logger.info("🚀 Démarrage de llama-server...")
        self._logger.info(f"   Modèle: {self.model_config.path}")
        self._logger.info(f"   Port: {self.server_config.port}")
        self._logger.info(f"   GPU Layers: {self.server_config.n_gpu_layers}")
        self._logger.info(f"   API: {self.api_base}")
        
        try:
            # Démarrer le processus
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            # Attendre que le serveur soit prêt
            wait_for_server(self.api_base, timeout)
            
            self._logger.info(
                f"✅ llama-server démarré avec succès (PID: {self._process.pid})"
            )
            self._started = True
            
            # Enregistrer l'arrêt automatique si demandé
            if self._auto_stop:
                atexit.register(self.stop)
            
            return True
            
        except TimeoutError as e:
            self._cleanup_process()
            raise ServerStartupError(f"Timeout lors du démarrage : {e}")
        except Exception as e:
            self._cleanup_process()
            raise ServerStartupError(f"Erreur lors du démarrage : {e}")
    
    def stop(self, force: bool = False) -> bool:
        """Arrête le serveur llama-server.
        
        Cette méthode arrête le serveur llama-server de manière propre.
        Si force=True, le processus est tué immédiatement.
        
        Args:
            force: Forcer l'arrêt (SIGKILL) (par défaut: False)
            
        Returns:
            True si l'arrêt a réussi, False sinon
        
        Example:
            server.stop()  # Arrêt propre
            server.stop(force=True)  # Arrêt forcé
        """
        if self._process is None:
            return True
        
        try:
            self._logger.info(
                f"🛑 Arrêt de llama-server (PID: {self._process.pid})..."
            )
            
            if force:
                self._process.kill()
            else:
                self._process.terminate()
            
            try:
                self._process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._logger.warning("⚠️ Timeout, envoi de SIGKILL...")
                self._process.kill()
                self._process.wait()
            
            self._logger.info("✅ llama-server arrêté proprement")
            return True
            
        except Exception as e:
            self._logger.error(f"❌ Erreur lors de l'arrêt : {e}")
            return False
        finally:
            self._cleanup_process()
    
    def _cleanup_process(self) -> None:
        """Nettoie le processus.
        
        Cette méthode ferme les flux stdout et stderr du processus
        et réinitialise les variables internes.
        """
        if self._process:
            try:
                self._process.stdout.close()
                self._process.stderr.close()
            except Exception:
                pass
            self._process = None
            self._started = False
    
    def restart(self, timeout: int = 60) -> bool:
        """Redémarre le serveur.
        
        Cette méthode arrête puis redémarre le serveur.
        
        Args:
            timeout: Timeout en secondes pour le démarrage (par défaut: 60)
            
        Returns:
            True si le redémarrage a réussi
            
        Example:
            server.restart(timeout=30)
        """
        self.stop()
        return self.start(timeout)
    
    def generate(
        self,
        prompt: str,
        params: Optional[GenerationParams] = None,
        timeout: int = 120
    ) -> GenerationResponse:
        """Génère du texte à partir d'un prompt.
        
        Cette méthode envoie une requête de génération au serveur
        llama-server et retourne la réponse.
        
        Args:
            prompt: Prompt de génération
            params: Paramètres de génération (optionnel)
            timeout: Timeout en secondes pour la requête (par défaut: 120)
            
        Returns:
            Réponse de génération (GenerationResponse)
            
        Raises:
            ServerConnectionError: Si le serveur n'est pas accessible
            GenerationError: Si la génération échoue
        
        Example:
            response = server.generate(
                "Expliquez ce qu'est l'intelligence artificielle.",
                params=GenerationParams(max_tokens=200, temperature=0.7)
            )
            print(response.content)
        """
        if not self.is_running:
            raise ServerConnectionError("Le serveur n'est pas en cours d'exécution")
        
        params = params or GenerationParams()
        
        payload = {
            "model": self.model_config.name,
            "prompt": prompt,
            "max_tokens": params.max_tokens,
            "temperature": params.temperature,
            "top_p": params.top_p,
            "top_k": params.top_k,
            "repeat_penalty": params.repeat_penalty,
            "presence_penalty": params.presence_penalty,
            "frequency_penalty": params.frequency_penalty,
        }
        
        if params.stop:
            payload["stop"] = params.stop
        
        try:
            response = requests.post(
                f"{self.api_base}/v1/completions",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            return GenerationResponse(
                content=data["choices"][0]["text"],
                model=data["model"],
                tokens_used=data.get("usage", {}).get("total_tokens", 0),
                finish_reason=data["choices"][0].get("finish_reason")
            )
            
        except requests.RequestException as e:
            raise GenerationError(f"Erreur lors de la génération : {e}")
    
    def chat(
        self,
        messages: List[Message],
        params: Optional[GenerationParams] = None,
        timeout: int = 120
    ) -> GenerationResponse:
        """Génère une réponse de chat.
        
        Cette méthode envoie une requête de chat au serveur
        llama-server et retourne la réponse.
        
        Args:
            messages: Liste des messages de conversation
            params: Paramètres de génération (optionnel)
            timeout: Timeout en secondes pour la requête (par défaut: 120)
            
        Returns:
            Réponse de génération (GenerationResponse)
            
        Raises:
            ServerConnectionError: Si le serveur n'est pas accessible
            GenerationError: Si la génération échoue
        
        Example:
            messages = [
                Message(role="system", content="Vous êtes un assistant utile."),
                Message(role="user", content="Bonjour !")
            ]
            response = server.chat(messages)
            print(response.content)
        """
        if not self.is_running:
            raise ServerConnectionError("Le serveur n'est pas en cours d'exécution")
        
        params = params or GenerationParams()
        
        payload = {
            "model": self.model_config.name,
            "messages": [m.model_dump() for m in messages],
            "max_tokens": params.max_tokens,
            "temperature": params.temperature,
            "top_p": params.top_p,
            "top_k": params.top_k,
            "repeat_penalty": params.repeat_penalty,
            "presence_penalty": params.presence_penalty,
            "frequency_penalty": params.frequency_penalty,
        }
        
        if params.stop:
            payload["stop"] = params.stop
        
        try:
            response = requests.post(
                f"{self.api_base}/v1/chat/completions",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            return GenerationResponse(
                content=data["choices"][0]["message"]["content"],
                model=data["model"],
                tokens_used=data.get("usage", {}).get("total_tokens", 0),
                finish_reason=data["choices"][0].get("finish_reason")
            )
            
        except requests.RequestException as e:
            raise GenerationError(f"Erreur lors de la génération : {e}")
    
    def __enter__(self):
        """Support du gestionnaire de contexte.
        
        Cette méthode est appelée lors de l'entrée dans un bloc 'with'.
        Elle démarre le serveur s'il n'est pas déjà démarré.
        
        Returns:
            L'instance de LlamaServer
        
        Example:
            with LlamaServer(model_path="model.gguf", model_name="model") as server:
                response = server.generate("Hello")
        """
        if not self._started:
            self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support du gestionnaire de contexte.
        
        Cette méthode est appelée lors de la sortie d'un bloc 'with'.
        Elle arrête le serveur proprement.
        
        Args:
            exc_type: Type de l'exception (si une exception s'est produite)
            exc_val: Valeur de l'exception
            exc_tb: Traceback de l'exception
            
        Returns:
            False (ne pas supprimer l'exception)
        """
        self.stop()
        return False
    
    def __del__(self):
        """Destructeur.
        
        Cette méthode est appelée lors de la destruction de l'objet.
        Elle arrête le serveur si auto_stop est activé.
        """
        if self._auto_stop:
            self.stop()


# Fonctions utilitaires pour une utilisation simplifiée


def quick_generate(
    model_path: str,
    prompt: str,
    model_name: str = "llama-model",
    **kwargs
) -> str:
    """Fonction utilitaire pour une génération rapide.
    
    Cette fonction simplifie l'utilisation du module en créant
    automatiquement un serveur, générant du texte, et arrêtant le serveur.
    
    Args:
        model_path: Chemin vers le fichier du modèle
        prompt: Prompt de génération
        model_name: Nom du modèle (par défaut: "llama-model")
        **kwargs: Paramètres supplémentaires pour GenerationParams
        
    Returns:
        Texte généré
        
    Example:
        result = quick_generate(
            "model.gguf",
            "Dis-moi une blague.",
            max_tokens=100,
            temperature=0.8
        )
        print(result)
    """
    server = LlamaServer(
        model_path=model_path,
        model_name=model_name,
        auto_start=True,
        auto_stop=True
    )
    response = server.generate(prompt, **kwargs)
    return response.content


def quick_chat(
    model_path: str,
    messages: List[Union[Message, Dict[str, str]]],
    model_name: str = "llama-model",
    **kwargs
) -> str:
    """Fonction utilitaire pour un chat rapide.
    
    Cette fonction simplifie l'utilisation du module en créant
    automatiquement un serveur, effectuant un chat, et arrêtant le serveur.
    
    Args:
        model_path: Chemin vers le fichier du modèle
        messages: Liste des messages (objets Message ou dictionnaires)
        model_name: Nom du modèle (par défaut: "llama-model")
        **kwargs: Paramètres supplémentaires pour GenerationParams
        
    Returns:
        Réponse générée
        
    Example:
        messages = [
            {"role": "user", "content": "Qui es-tu ?"}
        ]
        response = quick_chat(
            "model.gguf",
            messages,
            max_tokens=50
        )
        print(response)
    """
    # Convertir les dictionnaires en objets Message si nécessaire
    msg_objects = []
    for m in messages:
        if isinstance(m, dict):
            msg_objects.append(Message(**m))
        else:
            msg_objects.append(m)
    
    server = LlamaServer(
        model_path=model_path,
        model_name=model_name,
        auto_start=True,
        auto_stop=True
    )
    response = server.chat(msg_objects, **kwargs)
    return response.content
