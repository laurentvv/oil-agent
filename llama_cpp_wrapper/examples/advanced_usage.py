"""
Exemple d'utilisation avancée du module llama_cpp_wrapper.

Cet exemple montre des fonctionnalités avancées telles que :
- Utilisation du gestionnaire de contexte
- Chat avec historique de messages
- Gestion des erreurs
- Configuration personnalisée
"""

from llama_cpp_wrapper import (
    LlamaServer, Message, GenerationParams, ServerConfig, ModelConfig,
    ServerStartupError, ServerConnectionError, ModelNotFoundError, GenerationError
)


def example_context_manager():
    """Exemple d'utilisation avec gestionnaire de contexte."""
    print("=" * 60)
    print("Exemple 1 : Gestionnaire de contexte")
    print("=" * 60)
    
    with LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b"
    ) as server:
        # Le serveur démarre automatiquement
        
        response = server.generate(
            "Quels sont les avantages de llama.cpp par rapport à Ollama ?",
            params=GenerationParams(max_tokens=300, temperature=0.5)
        )
        
        print(f"📝 Réponse : {response.content}")
        print()
    
    # Le serveur s'arrête automatiquement à la sortie du bloc with


def example_chat_with_history():
    """Exemple de chat avec historique de messages."""
    print("=" * 60)
    print("Exemple 2 : Chat avec historique")
    print("=" * 60)
    
    with LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b"
    ) as server:
        # Historique de conversation
        messages = [
            Message(role="system", content="Vous êtes un assistant utile et concis."),
            Message(role="user", content="Quel est le sens de la vie ?"),
        ]
        
        # Premier échange
        response = server.chat(messages, GenerationParams(max_tokens=150))
        print(f"👤 Utilisateur : Quel est le sens de la vie ?")
        print(f"🤖 Assistant : {response.content}")
        print()
        
        # Ajouter la réponse à l'historique
        messages.append(Message(role="assistant", content=response.content))
        messages.append(Message(role="user", content="Peux-tu développer ?"))
        
        # Deuxième échange
        response = server.chat(messages, GenerationParams(max_tokens=150))
        print(f"👤 Utilisateur : Peux-tu développer ?")
        print(f"🤖 Assistant : {response.content}")
        print()


def example_custom_configuration():
    """Exemple avec configuration personnalisée."""
    print("=" * 60)
    print("Exemple 3 : Configuration personnalisée")
    print("=" * 60)
    
    # Configuration du serveur
    server_config = ServerConfig(
        executable="llama-server",
        host="127.0.0.1",
        port=8081,  # Port personnalisé
        n_gpu_layers=-1,  # Utiliser toutes les couches GPU
        n_threads=0,  # Auto-détection
        ctx_size=8192,
        batch_size=512
    )
    
    # Configuration du modèle
    model_config = ModelConfig(
        name="qwen3.5-9b",
        path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        num_ctx=8192
    )
    
    with LlamaServer(
        server_config=server_config,
        model_config=model_config
    ) as server:
        print(f"🌐 API de base : {server.api_base}")
        print(f"🎮 GPU Layers : {server.server_config.n_gpu_layers}")
        print(f"🧵 Threads : {server.server_config.n_threads}")
        print()
        
        response = server.generate(
            "Explique-moi ce qu'est llama.cpp en une phrase.",
            params=GenerationParams(max_tokens=100)
        )
        
        print(f"📝 Réponse : {response.content}")
        print()


def example_error_handling():
    """Exemple de gestion des erreurs."""
    print("=" * 60)
    print("Exemple 4 : Gestion des erreurs")
    print("=" * 60)
    
    # Exemple 1 : Modèle introuvable
    try:
        server = LlamaServer(
            model_path="chemin/inexistant/model.gguf",
            model_name="model",
            auto_start=True
        )
    except ModelNotFoundError as e:
        print(f"❌ Modèle introuvable : {e}")
    print()
    
    # Exemple 2 : Erreur de démarrage
    try:
        server = LlamaServer(
            model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
            model_name="qwen3.5-9b",
            server_config=ServerConfig(executable="executable_inexistant"),
            auto_start=True
        )
    except ServerStartupError as e:
        print(f"❌ Erreur de démarrage : {e}")
    print()
    
    # Exemple 3 : Utilisation correcte avec gestion des erreurs
    try:
        server = LlamaServer(
            model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
            model_name="qwen3.5-9b"
        )
        
        response = server.generate("Hello, world!")
        print(f"✅ Succès : {response.content}")
        
    except ModelNotFoundError as e:
        print(f"❌ Modèle introuvable : {e}")
    except ServerStartupError as e:
        print(f"❌ Erreur de démarrage : {e}")
    except ServerConnectionError as e:
        print(f"❌ Erreur de connexion : {e}")
    except GenerationError as e:
        print(f"❌ Erreur de génération : {e}")
    finally:
        try:
            server.stop()
        except:
            pass


def example_restart():
    """Exemple de redémarrage du serveur."""
    print("=" * 60)
    print("Exemple 5 : Redémarrage du serveur")
    print("=" * 60)
    
    server = LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b",
        auto_start=True
    )
    
    # Première génération
    response = server.generate("Dis-moi une blague.")
    print(f"📝 Blague 1 : {response.content}")
    print()
    
    # Redémarrer le serveur
    print("🔄 Redémarrage du serveur...")
    server.restart()
    print("✅ Serveur redémarré")
    print()
    
    # Deuxième génération
    response = server.generate("Dis-moi une autre blague.")
    print(f"📝 Blague 2 : {response.content}")
    print()
    
    server.stop()


def example_properties():
    """Exemple d'utilisation des propriétés."""
    print("=" * 60)
    print("Exemple 6 : Propriétés du serveur")
    print("=" * 60)
    
    server = LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b"
    )
    
    print(f"📊 Serveur en cours d'exécution : {server.is_running}")
    print(f"🌐 API de base : {server.api_base}")
    print(f"🎮 GPU Layers : {server.server_config.n_gpu_layers}")
    print(f"🧵 Threads : {server.server_config.n_threads}")
    print(f"📏 Taille du contexte : {server.server_config.ctx_size}")
    print(f"📦 Taille du batch : {server.server_config.batch_size}")
    print(f"📝 Nom du modèle : {server.model_config.name}")
    print(f"📂 Chemin du modèle : {server.model_config.path}")
    print()
    
    server.stop()


def main():
    """Fonction principale de l'exemple."""
    
    # Exemple 1 : Gestionnaire de contexte
    example_context_manager()
    
    # Exemple 2 : Chat avec historique
    example_chat_with_history()
    
    # Exemple 3 : Configuration personnalisée
    example_custom_configuration()
    
    # Exemple 4 : Gestion des erreurs
    example_error_handling()
    
    # Exemple 5 : Redémarrage du serveur
    example_restart()
    
    # Exemple 6 : Propriétés du serveur
    example_properties()


if __name__ == "__main__":
    main()
