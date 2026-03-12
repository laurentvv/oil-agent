"""
Exemple d'intégration du module llama_cpp_wrapper avec DSPy et smolagents.

Cet exemple montre comment utiliser llama_cpp_wrapper comme backend
pour des frameworks comme DSPy et smolagents.
"""

from llama_cpp_wrapper import LlamaServer, ServerConfig, ModelConfig


def example_dspy_integration():
    """Exemple d'intégration avec DSPy."""
    print("=" * 60)
    print("Exemple 1 : Intégration avec DSPy")
    print("=" * 60)
    
    try:
        import dspy
    except ImportError:
        print("❌ DSPy n'est pas installé. Installez-le avec : pip install dspy-ai")
        return
    
    # Configurer le serveur
    server = LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b",
        server_config=ServerConfig(port=8080),
        auto_start=True
    )
    
    print(f"🌐 API de base : {server.api_base}")
    print(f"📝 Nom du modèle : {server.model_config.name}")
    print()
    
    # Configurer DSPy
    lm = dspy.LM(
        model=f"openai/{server.model_config.name}",
        api_base=server.api_base,
        api_key="dummy",  # Non utilisé par llama-server
        model_type="chat"
    )
    dspy.configure(lm=lm)
    
    # Utiliser DSPy normalement
    print("📝 Envoi d'une requête via DSPy...")
    result = lm("Réponds par 'OK DSPy'.")
    print(f"📝 Réponse DSPy : {result}")
    print()
    
    # Arrêter le serveur
    server.stop()
    print("✅ Serveur arrêté")


def example_smolagents_integration():
    """Exemple d'intégration avec smolagents."""
    print("=" * 60)
    print("Exemple 2 : Intégration avec smolagents")
    print("=" * 60)
    
    try:
        from smolagents import LiteLLMModel
    except ImportError:
        print("❌ smolagents n'est pas installé. Installez-le avec : pip install smolagents")
        return
    
    # Configurer le serveur
    server = LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b",
        auto_start=True
    )
    
    print(f"🌐 API de base : {server.api_base}")
    print(f"📝 Nom du modèle : {server.model_config.name}")
    print()
    
    # Créer le modèle smolagents
    model = LiteLLMModel(
        model_id=f"openai/{server.model_config.name}",
        api_base=server.api_base,
        api_key="dummy",  # Non utilisé par llama-server
        num_ctx=8192,
    )
    
    # Utiliser le modèle
    print("📝 Envoi d'une requête via smolagents...")
    response = model("Réponds par 'OK smolagents'.")
    print(f"📝 Réponse smolagents : {response}")
    print()
    
    # Arrêter le serveur
    server.stop()
    print("✅ Serveur arrêté")


def example_litellm_integration():
    """Exemple d'intégration avec LiteLLM."""
    print("=" * 60)
    print("Exemple 3 : Intégration avec LiteLLM")
    print("=" * 60)
    
    try:
        from litellm import completion
    except ImportError:
        print("❌ LiteLLM n'est pas installé. Installez-le avec : pip install litellm")
        return
    
    # Configurer le serveur
    server = LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b",
        auto_start=True
    )
    
    print(f"🌐 API de base : {server.api_base}")
    print(f"📝 Nom du modèle : {server.model_config.name}")
    print()
    
    # Utiliser LiteLLM
    print("📝 Envoi d'une requête via LiteLLM...")
    response = completion(
        model=f"openai/{server.model_config.name}",
        messages=[{"role": "user", "content": "Réponds par 'OK LiteLLM'."}],
        api_base=server.api_base,
        api_key="dummy"  # Non utilisé par llama-server
    )
    
    print(f"📝 Réponse LiteLLM : {response.choices[0].message.content}")
    print()
    
    # Arrêter le serveur
    server.stop()
    print("✅ Serveur arrêté")


def example_langchain_integration():
    """Exemple d'intégration avec LangChain."""
    print("=" * 60)
    print("Exemple 4 : Intégration avec LangChain")
    print("=" * 60)
    
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        print("❌ LangChain n'est pas installé. Installez-le avec : pip install langchain-openai")
        return
    
    # Configurer le serveur
    server = LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b",
        auto_start=True
    )
    
    print(f"🌐 API de base : {server.api_base}")
    print(f"📝 Nom du modèle : {server.model_config.name}")
    print()
    
    # Créer le modèle LangChain
    llm = ChatOpenAI(
        model=server.model_config.name,
        base_url=server.api_base,
        api_key="dummy",  # Non utilisé par llama-server
        temperature=0.7
    )
    
    # Utiliser le modèle
    print("📝 Envoi d'une requête via LangChain...")
    response = llm.invoke("Réponds par 'OK LangChain'.")
    print(f"📝 Réponse LangChain : {response.content}")
    print()
    
    # Arrêter le serveur
    server.stop()
    print("✅ Serveur arrêté")


def example_custom_framework():
    """Exemple d'intégration avec un framework personnalisé."""
    print("=" * 60)
    print("Exemple 5 : Intégration avec un framework personnalisé")
    print("=" * 60)
    
    # Configurer le serveur
    server = LlamaServer(
        model_path="C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
        model_name="qwen3.5-9b",
        auto_start=True
    )
    
    print(f"🌐 API de base : {server.api_base}")
    print(f"📝 Nom du modèle : {server.model_config.name}")
    print()
    
    # Exemple de wrapper personnalisé
    class CustomLLM:
        """Wrapper personnalisé pour un framework LLM."""
        
        def __init__(self, server):
            self.server = server
        
        def __call__(self, prompt, **kwargs):
            """Appel du modèle."""
            from llama_cpp_wrapper import GenerationParams
            
            params = GenerationParams(
                max_tokens=kwargs.get("max_tokens", 512),
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 0.9),
                top_k=kwargs.get("top_k", 40)
            )
            
            response = self.server.generate(prompt, params=params)
            return response.content
        
        def chat(self, messages, **kwargs):
            """Chat avec le modèle."""
            from llama_cpp_wrapper import GenerationParams, Message
            
            # Convertir les messages
            msg_objects = []
            for m in messages:
                if isinstance(m, dict):
                    msg_objects.append(Message(**m))
                else:
                    msg_objects.append(m)
            
            params = GenerationParams(
                max_tokens=kwargs.get("max_tokens", 512),
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 0.9),
                top_k=kwargs.get("top_k", 40)
            )
            
            response = self.server.chat(msg_objects, params=params)
            return response.content
    
    # Utiliser le wrapper personnalisé
    llm = CustomLLM(server)
    
    print("📝 Envoi d'une requête via le wrapper personnalisé...")
    response = llm("Réponds par 'OK Custom Framework'.")
    print(f"📝 Réponse : {response}")
    print()
    
    # Arrêter le serveur
    server.stop()
    print("✅ Serveur arrêté")


def main():
    """Fonction principale de l'exemple."""
    
    # Exemple 1 : Intégration avec DSPy
    example_dspy_integration()
    print()
    
    # Exemple 2 : Intégration avec smolagents
    example_smolagents_integration()
    print()
    
    # Exemple 3 : Intégration avec LiteLLM
    example_litellm_integration()
    print()
    
    # Exemple 4 : Intégration avec LangChain
    example_langchain_integration()
    print()
    
    # Exemple 5 : Intégration avec un framework personnalisé
    example_custom_framework()


if __name__ == "__main__":
    main()
