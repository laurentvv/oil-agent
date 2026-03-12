"""
Fonctions utilitaires pour le module llama_cpp_wrapper.

Ce module fournit des fonctions utilitaires pour la gestion du serveur
llama-server, notamment la vérification des ports, l'attente de disponibilité
du serveur, et la validation des chemins de modèles.
"""

import subprocess
import sys
import time
import requests
import socket
from pathlib import Path
from typing import Optional

from .exceptions import ServerConnectionError, TimeoutError, ModelNotFoundError


def check_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """Vérifie si un port est disponible pour l'écoute.
    
    Cette fonction tente de lier un socket au port spécifié pour vérifier
    s'il est disponible. Si le port est déjà utilisé, la fonction retourne False.
    
    Args:
        port: Numéro de port à vérifier (1-65535)
        host: Adresse hôte (par défaut: 127.0.0.1)
        
    Returns:
        True si le port est disponible, False s'il est déjà utilisé
        
    Example:
        if check_port_available(8080):
            print("Le port 8080 est disponible")
        else:
            print("Le port 8080 est déjà utilisé")
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


def wait_for_server(
    api_base: str,
    timeout: int = 60,
    check_interval: float = 1.0
) -> bool:
    """Attend que le serveur soit prêt à accepter des requêtes.
    
    Cette fonction interroge régulièrement le point de terminaison /health
    du serveur jusqu'à ce qu'il réponde avec un code 200 ou que le timeout
    soit dépassé.
    
    Args:
        api_base: URL de base de l'API (ex: http://127.0.0.1:8080)
        timeout: Timeout maximum en secondes (par défaut: 60)
        check_interval: Intervalle entre les vérifications en secondes (par défaut: 1.0)
        
    Returns:
        True si le serveur est prêt
        
    Raises:
        TimeoutError: Si le timeout est dépassé avant que le serveur ne soit prêt
        
    Example:
        wait_for_server("http://127.0.0.1:8080", timeout=30)
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{api_base}/health", timeout=2)
            if response.status_code == 200:
                return True
            elif response.status_code == 503:
                # Modèle en cours de chargement
                time.sleep(check_interval)
                continue
        except requests.RequestException:
            pass
        
        time.sleep(check_interval)
    
    raise TimeoutError(f"Le serveur n'est pas prêt après {timeout} secondes")


def kill_process_on_port(port: int, host: str = "127.0.0.1") -> bool:
    """Tue le processus utilisant un port spécifique.
    
    Cette fonction identifie et termine le processus qui écoute sur le
    port spécifié. Elle est utile pour libérer un port avant de démarrer
    un nouveau serveur.
    
    Args:
        port: Numéro de port
        host: Adresse hôte (par défaut: 127.0.0.1)
        
    Returns:
        True si un processus a été tué, False sinon
        
    Note:
        Sur Windows, utilise netstat et taskkill.
        Sur Linux/Mac, utilise lsof et kill.
        
    Example:
        kill_process_on_port(8080)  # Tue le processus sur le port 8080
    """
    try:
        if sys.platform == "win32":
            # Windows
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if f"{host}:{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True)
                        return True
        else:
            # Linux/Mac
            result = subprocess.run(
                ["lsof", "-t", "-i", f":{port}"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                pid = result.stdout.strip()
                subprocess.run(["kill", "-9", pid], capture_output=True)
                return True
    except Exception:
        pass
    
    return False


def format_llama_command(
    executable: str,
    model_path: str,
    server_config: dict
) -> list:
    """Formate la commande llama-server de manière cohérente.
    
    Cette fonction construit la liste d'arguments pour lancer llama-server
    avec les paramètres de configuration spécifiés. Elle gère automatiquement
    l'extension .exe sur Windows.
    
    Args:
        executable: Nom de l'exécutable (ex: llama-server)
        model_path: Chemin vers le fichier du modèle
        server_config: Dictionnaire de configuration du serveur
        
    Returns:
        Liste des arguments pour subprocess
        
    Example:
        cmd = format_llama_command(
            "llama-server",
            "model.gguf",
            {"host": "127.0.0.1", "port": 8080}
        )
        subprocess.Popen(cmd)
    """
    # Ajouter l'extension .exe sur Windows si nécessaire
    if sys.platform == "win32" and not executable.endswith(".exe"):
        executable += ".exe"
    
    cmd = [
        executable,
        "-m", model_path,
        "--host", server_config.get("host", "127.0.0.1"),
        "--port", str(server_config.get("port", 8080)),
        "-ngl", str(server_config.get("n_gpu_layers", -1)),
        "-t", str(server_config.get("n_threads", 0)),
        "-c", str(server_config.get("ctx_size", 8192)),
        "-b", str(server_config.get("batch_size", 512)),
        "-ub", str(server_config.get("ubatch_size", 128)),
        "-ctk", server_config.get("cache_type_k", "f16"),
        "-ctv", server_config.get("cache_type_v", "f16"),
    ]
    
    return cmd


def validate_model_path(model_path: str) -> Path:
    """Valide et retourne le chemin du modèle.
    
    Cette fonction vérifie que le chemin spécifié pointe vers un fichier
    existant. Elle est utilisée avant de démarrer le serveur pour s'assurer
    que le modèle est disponible.
    
    Args:
        model_path: Chemin vers le fichier du modèle
        
    Returns:
        Chemin validé sous forme d'objet Path
        
    Raises:
        ModelNotFoundError: Si le modèle n'existe pas ou n'est pas un fichier
        
    Example:
        try:
            path = validate_model_path("model.gguf")
            print(f"Modèle valide: {path}")
        except ModelNotFoundError as e:
            print(f"Erreur: {e}")
    """
    path = Path(model_path)
    if not path.exists():
        raise ModelNotFoundError(f"Modèle introuvable : {model_path}")
    if not path.is_file():
        raise ModelNotFoundError(f"Le chemin n'est pas un fichier : {model_path}")
    return path
