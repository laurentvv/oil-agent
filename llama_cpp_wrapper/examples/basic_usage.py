"""
Exemple d'utilisation basique du module llama_cpp_wrapper.

Cet exemple montre comment utiliser le module llama_cpp_wrapper de manière
simple pour démarrer un serveur llama-server et générer du texte.
"""

from llama_cpp_wrapper import LlamaServer, GenerationParams


def main():
    """Fonction principale de l'exemple."""
    
    # Créer et démarrer le serveur
    # Remplacez le chemin par le chemin vers votre modèle
    server = LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b",
        auto_start=True,
        auto_stop=True
    )
    
    # Vérifier que le serveur est en cours d'exécution
    print(f"📊 Serveur en cours d'exécution : {server.is_running}")
    print(f"🌐 API de base : {server.api_base}")
    print()
    
    # Exemple 1 : Génération simple
    print("=" * 60)
    print("Exemple 1 : Génération simple")
    print("=" * 60)
    
    response = server.generate(
        "Expliquez en quelques phrases ce qu'est l'intelligence artificielle.",
        params=GenerationParams(
            max_tokens=200,
            temperature=0.7
        )
    )
    
    print(f"📝 Réponse : {response.content}")
    print(f"📊 Tokens utilisés : {response.tokens_used}")
    print(f"🏁 Raison de fin : {response.finish_reason}")
    print()
    
    # Exemple 2 : Génération avec paramètres personnalisés
    print("=" * 60)
    print("Exemple 2 : Génération avec paramètres personnalisés")
    print("=" * 60)
    
    response = server.generate(
        "Quels sont les avantages de llama.cpp par rapport à Ollama ?",
        params=GenerationParams(
            max_tokens=300,
            temperature=0.5,
            top_p=0.9,
            top_k=40
        )
    )
    
    print(f"📝 Réponse : {response.content}")
    print(f"📊 Tokens utilisés : {response.tokens_used}")
    print()
    
    # Exemple 3 : Chat simple
    print("=" * 60)
    print("Exemple 3 : Chat simple")
    print("=" * 60)
    
    from llama_cpp_wrapper import Message
    
    messages = [
        Message(role="system", content="Vous êtes un assistant utile et concis."),
        Message(role="user", content="Quel est le sens de la vie ?"),
    ]
    
    response = server.chat(
        messages,
        params=GenerationParams(max_tokens=150)
    )
    
    print(f"📝 Réponse : {response.content}")
    print(f"📊 Tokens utilisés : {response.tokens_used}")
    print()
    
    # Le serveur s'arrête automatiquement grâce à auto_stop=True


if __name__ == "__main__":
    main()
