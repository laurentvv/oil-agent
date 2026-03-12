"""
Exceptions personnalisées pour le module llama_cpp_wrapper.

Ce module définit une hiérarchie d'exceptions pour gérer les erreurs
spécifiques à l'utilisation de llama.cpp et du serveur llama-server.
"""


class LlamaCppError(Exception):
    """Exception de base pour toutes les erreurs llama.cpp.
    
    Cette exception sert de classe parente pour toutes les exceptions
    spécifiques du module. Elle permet de capturer toutes les erreurs
    liées à llama.cpp avec un seul bloc except.
    
    Exemple:
        try:
            # Code utilisant llama_cpp_wrapper
            pass
        except LlamaCppError as e:
            print(f"Erreur llama.cpp: {e}")
    """
    pass


class ServerStartupError(LlamaCppError):
    """Erreur lors du démarrage du serveur llama-server.
    
    Cette exception est levée lorsque le serveur llama-server ne peut
    pas être démarré correctement. Cela peut être dû à:
    - L'exécutable introuvable
    - Le port déjà utilisé
    - Le modèle introuvable
    - Des permissions insuffisantes
    
    Exemple:
        try:
            server = LlamaServer(model_path="model.gguf")
        except ServerStartupError as e:
            print(f"Impossible de démarrer le serveur: {e}")
    """
    pass


class ServerConnectionError(LlamaCppError):
    """Erreur lors de la connexion au serveur.
    
    Cette exception est levée lorsque le client ne peut pas communiquer
    avec le serveur llama-server. Cela peut être dû à:
    - Le serveur n'est pas démarré
    - L'adresse ou le port incorrect
    - Problèmes de réseau
    
    Exemple:
        try:
            response = server.generate("Hello")
        except ServerConnectionError as e:
            print(f"Impossible de contacter le serveur: {e}")
    """
    pass


class ModelNotFoundError(LlamaCppError):
    """Erreur : fichier modèle introuvable.
    
    Cette exception est levée lorsque le fichier du modèle spécifié
    n'existe pas ou n'est pas accessible. Elle est utilisée lors
    de la validation du chemin du modèle avant le démarrage du serveur.
    
    Exemple:
        try:
            server = LlamaServer(model_path="path/to/model.gguf")
        except ModelNotFoundError as e:
            print(f"Modèle introuvable: {e}")
    """
    pass


class GenerationError(LlamaCppError):
    """Erreur lors de la génération de texte.
    
    Cette exception est levée lorsqu'une requête de génération échoue.
    Cela peut être dû à:
    - Erreur HTTP du serveur
    - Timeout de la requête
    - Format de réponse invalide
    - Paramètres de génération invalides
    
    Exemple:
        try:
            response = server.generate("Hello")
        except GenerationError as e:
            print(f"Erreur de génération: {e}")
    """
    pass


class ConfigurationError(LlamaCppError):
    """Erreur de configuration invalide.
    
    Cette exception est levée lorsque la configuration fournie est
    invalide ou incomplète. Cela peut être dû à:
    - Fichier de configuration inexistant
    - Format de fichier invalide
    - Paramètres de configuration invalides
    - Configuration du modèle manquante
    
    Exemple:
        try:
            config_manager = ConfigManager(config_path="config.json")
        except ConfigurationError as e:
            print(f"Erreur de configuration: {e}")
    """
    pass


class TimeoutError(LlamaCppError):
    """Erreur : timeout lors d'une opération.
    
    Cette exception est levée lorsqu'une opération prend plus de temps
    que le timeout spécifié. Cela peut concerner:
    - Le démarrage du serveur
    - Une requête de génération
    - L'attente de disponibilité du serveur
    
    Exemple:
        try:
            server.start(timeout=30)
        except TimeoutError as e:
            print(f"Timeout: {e}")
    """
    pass
