# llama_cpp_wrapper

Module Python autonome et réutilisable qui encapsule llama.cpp pour remplacer Ollama dans vos projets.

## 📋 Table des matières

- [Installation](#installation)
- [Prérequis](#prérequis)
- [Usage rapide](#usage-rapide)
- [Documentation](#documentation)
- [Exemples](#exemples)
- [Intégration](#intégration)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Gestion des erreurs](#gestion-des-erreurs)

## 🚀 Installation

### Prérequis

1. **llama-server** doit être installé et disponible dans le PATH
   - Téléchargez llama-server depuis [GitHub](https://github.com/ggerganov/llama.cpp)
   - Placez l'exécutable dans un répertoire inclus dans votre PATH

2. **Python 3.8+** est requis

3. **Dépendances Python** :
   ```bash
   pip install requests pydantic pyyaml
   ```

### Installation du module

Copiez simplement le répertoire `llama_cpp_wrapper/` dans votre projet ou installez-le comme package :

```bash
cd llama_cpp_wrapper
pip install -e .
```

## ⚡ Usage rapide

### Génération simple

```python
from llama_cpp_wrapper import LlamaServer

# Créer et démarrer le serveur
server = LlamaServer(
    model_path="path/to/model.gguf",
    model_name="my-model"
)

# Générer du texte
response = server.generate("Hello, world!")
print(response.content)

# Arrêter le serveur
server.stop()
```

### Avec gestionnaire de contexte

```python
from llama_cpp_wrapper import LlamaServer

with LlamaServer(model_path="path/to/model.gguf", model_name="my-model") as server:
    response = server.generate("Hello, world!")
    print(response.content)
# Le serveur s'arrête automatiquement
```

### Fonctions utilitaires

```python
from llama_cpp_wrapper import quick_generate, quick_chat

# Génération rapide
result = quick_generate(
    "path/to/model.gguf",
    "Dis-moi une blague.",
    model_name="my-model"
)
print(result)

# Chat rapide
messages = [{"role": "user", "content": "Qui es-tu ?"}]
response = quick_chat(
    "path/to/model.gguf",
    messages,
    model_name="my-model"
)
print(response)
```

## 📚 Documentation

### Classes principales

#### LlamaServer

Classe principale pour gérer llama-server.

```python
from llama_cpp_wrapper import LlamaServer, ServerConfig, ModelConfig

# Configuration par paramètres
server = LlamaServer(
    model_path="path/to/model.gguf",
    model_name="my-model",
    server_config=ServerConfig(port=8080),
    model_config=ModelConfig(num_ctx=8192),
    auto_start=True,
    auto_stop=True
)

# Configuration par fichier
server = LlamaServer(config_path=Path("config.json"))
```

**Propriétés** :
- `server_config` : Configuration du serveur (lecture seule)
- `model_config` : Configuration du modèle (lecture seule)
- `api_base` : URL de base de l'API (lecture seule)
- `is_running` : État du serveur (lecture seule)

**Méthodes** :
- `start(timeout=60)` : Démarre le serveur
- `stop(force=False)` : Arrête le serveur
- `restart(timeout=60)` : Redémarre le serveur
- `generate(prompt, params=None, timeout=120)` : Génère du texte
- `chat(messages, params=None, timeout=120)` : Chat avec historique

#### ConfigManager

Gestionnaire de configuration.

```python
from llama_cpp_wrapper import ConfigManager, ServerConfig, ModelConfig

# Créer un gestionnaire
config = ConfigManager()

# Définir la configuration
config.set_server_config(ServerConfig(port=8080))
config.set_model_config(ModelConfig(name="model", path="model.gguf"))

# Sauvegarder
config.save_to_file(Path("config.json"))

# Charger depuis un fichier
config = ConfigManager(config_path=Path("config.json"))
```

#### Modèles Pydantic

**ServerConfig** : Configuration du serveur
```python
from llama_cpp_wrapper import ServerConfig

config = ServerConfig(
    executable="llama-server",
    host="127.0.0.1",
    port=8080,
    n_gpu_layers=-1,
    n_threads=0,
    ctx_size=8192,
    batch_size=512,
    ubatch_size=128
)
```

**ModelConfig** : Configuration du modèle
```python
from llama_cpp_wrapper import ModelConfig

config = ModelConfig(
    name="my-model",
    path="path/to/model.gguf",
    num_ctx=8192
)
```

**GenerationParams** : Paramètres de génération
```python
from llama_cpp_wrapper import GenerationParams

params = GenerationParams(
    max_tokens=512,
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    repeat_penalty=1.0,
    presence_penalty=0.0,
    frequency_penalty=0.0,
    stop=["\n", "###"]
)
```

**Message** : Message de chat
```python
from llama_cpp_wrapper import Message

msg = Message(
    role="user",
    content="Hello, world!"
)
```

**GenerationResponse** : Réponse de génération
```python
# Retourné par generate() et chat()
response.content  # Texte généré
response.model  # Nom du modèle
response.tokens_used  # Tokens utilisés
response.finish_reason  # Raison de fin
```

## 📖 Exemples

### Exemple basique

```python
from llama_cpp_wrapper import LlamaServer, GenerationParams

server = LlamaServer(
    model_path="path/to/model.gguf",
    model_name="my-model"
)

response = server.generate(
    "Expliquez ce qu'est l'intelligence artificielle.",
    params=GenerationParams(max_tokens=200, temperature=0.7)
)

print(response.content)
print(f"Tokens utilisés: {response.tokens_used}")
```

### Chat avec historique

```python
from llama_cpp_wrapper import LlamaServer, Message, GenerationParams

with LlamaServer(model_path="path/to/model.gguf", model_name="my-model") as server:
    messages = [
        Message(role="system", content="Vous êtes un assistant utile."),
        Message(role="user", content="Quel est le sens de la vie ?"),
    ]
    
    response = server.chat(messages, GenerationParams(max_tokens=150))
    print(f"Assistant: {response.content}")
    
    # Continuer la conversation
    messages.append(Message(role="assistant", content=response.content))
    messages.append(Message(role="user", content="Peux-tu développer ?"))
    
    response = server.chat(messages, GenerationParams(max_tokens=150))
    print(f"Assistant: {response.content}")
```

### Gestion des erreurs

```python
from llama_cpp_wrapper import (
    LlamaServer,
    ServerStartupError,
    ServerConnectionError,
    ModelNotFoundError,
    GenerationError
)

try:
    server = LlamaServer(
        model_path="path/to/model.gguf",
        model_name="my-model"
    )
    
    response = server.generate("Hello, world!")
    print(response.content)
    
except ModelNotFoundError as e:
    print(f"❌ Modèle introuvable : {e}")
except ServerStartupError as e:
    print(f"❌ Erreur de démarrage : {e}")
except ServerConnectionError as e:
    print(f"❌ Erreur de connexion : {e}")
except GenerationError as e:
    print(f"❌ Erreur de génération : {e}")
finally:
    server.stop()
```

## 🔗 Intégration

### DSPy

```python
import dspy
from llama_cpp_wrapper import LlamaServer

server = LlamaServer(
    model_path="path/to/model.gguf",
    model_name="my-model"
)

lm = dspy.LM(
    model=f"openai/{server.model_config.name}",
    api_base=server.api_base,
    api_key="dummy",
    model_type="chat"
)
dspy.configure(lm=lm)

result = lm("Réponds par 'OK DSPy'.")
print(result)

server.stop()
```

### smolagents

```python
from smolagents import LiteLLMModel
from llama_cpp_wrapper import LlamaServer

server = LlamaServer(
    model_path="path/to/model.gguf",
    model_name="my-model"
)

model = LiteLLMModel(
    model_id=f"openai/{server.model_config.name}",
    api_base=server.api_base,
    api_key="dummy",
    num_ctx=8192,
)

response = model("Réponds par 'OK smolagents'.")
print(response)

server.stop()
```

### LangChain

```python
from langchain_openai import ChatOpenAI
from llama_cpp_wrapper import LlamaServer

server = LlamaServer(
    model_path="path/to/model.gguf",
    model_name="my-model"
)

llm = ChatOpenAI(
    model=server.model_config.name,
    base_url=server.api_base,
    api_key="dummy",
    temperature=0.7
)

response = llm.invoke("Réponds par 'OK LangChain'.")
print(response.content)

server.stop()
```

### LiteLLM

```python
from litellm import completion
from llama_cpp_wrapper import LlamaServer

server = LlamaServer(
    model_path="path/to/model.gguf",
    model_name="my-model"
)

response = completion(
    model=f"openai/{server.model_config.name}",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base=server.api_base,
    api_key="dummy"
)

print(response.choices[0].message.content)

server.stop()
```

## ⚙️ Configuration

### Fichier JSON

```json
{
  "server": {
    "executable": "llama-server",
    "host": "127.0.0.1",
    "port": 8080,
    "n_gpu_layers": -1,
    "n_threads": 0,
    "ctx_size": 8192,
    "batch_size": 512,
    "ubatch_size": 128,
    "cache_type_k": "f16",
    "cache_type_v": "f16"
  },
  "model": {
    "name": "my-model",
    "path": "path/to/model.gguf",
    "num_ctx": 8192
  }
}
```

### Fichier YAML

```yaml
server:
  executable: llama-server
  host: 127.0.0.1
  port: 8080
  n_gpu_layers: -1
  n_threads: 0
  ctx_size: 8192
  batch_size: 512
  ubatch_size: 128
  cache_type_k: f16
  cache_type_v: f16

model:
  name: my-model
  path: path/to/model.gguf
  num_ctx: 8192
```

## 📋 API Reference

### Exceptions

- `LlamaCppError` : Exception de base
- `ServerStartupError` : Erreur lors du démarrage du serveur
- `ServerConnectionError` : Erreur lors de la connexion au serveur
- `ModelNotFoundError` : Modèle introuvable
- `GenerationError` : Erreur lors de la génération
- `ConfigurationError` : Erreur de configuration
- `TimeoutError` : Timeout lors d'une opération

### Fonctions utilitaires

- `quick_generate(model_path, prompt, model_name, **kwargs)` : Génération rapide
- `quick_chat(model_path, messages, model_name, **kwargs)` : Chat rapide

## 🛠️ Gestion des erreurs

Le module fournit une hiérarchie d'exceptions pour gérer les erreurs de manière précise :

```python
from llama_cpp_wrapper import (
    LlamaCppError,
    ServerStartupError,
    ServerConnectionError,
    ModelNotFoundError,
    GenerationError,
    ConfigurationError,
    TimeoutError
)

try:
    # Code utilisant llama_cpp_wrapper
    pass
except ModelNotFoundError as e:
    # Gérer les erreurs de modèle introuvable
    pass
except ServerStartupError as e:
    # Gérer les erreurs de démarrage
    pass
except ServerConnectionError as e:
    # Gérer les erreurs de connexion
    pass
except GenerationError as e:
    # Gérer les erreurs de génération
    pass
except ConfigurationError as e:
    # Gérer les erreurs de configuration
    pass
except TimeoutError as e:
    # Gérer les timeouts
    pass
except LlamaCppError as e:
    # Gérer toutes les erreurs llama.cpp
    pass
```

## 📦 Structure du module

```
llama_cpp_wrapper/
├── __init__.py                 # Point d'entrée principal
├── core.py                     # Classe principale LlamaServer
├── config.py                   # Gestion de configuration
├── exceptions.py               # Exceptions personnalisées
├── utils.py                    # Fonctions utilitaires
├── models.py                   # Modèles Pydantic
├── examples/
│   ├── basic_usage.py          # Exemple d'utilisation basique
│   ├── advanced_usage.py       # Exemple d'utilisation avancée
│   └── integration_example.py  # Exemple d'intégration
└── README.md                   # Documentation
```

## ✨ Avantages

1. **Interface simple** : API intuitive et facile à utiliser
2. **Robustesse** : Gestion complète des erreurs et des ressources
3. **Flexibilité** : Configuration via code ou fichier
4. **Compatibilité** : Fonctionne avec DSPy, smolagents, LiteLLM, LangChain
5. **Gestionnaire de contexte** : Nettoyage automatique des ressources
6. **Fonctions utilitaires** : Pour une utilisation rapide
7. **Documentation complète** : Exemples et guides d'utilisation
8. **Isolation** : Module autonome, facile à intégrer

## 📄 Licence

Ce module est fourni tel quel pour une utilisation dans vos projets.

## 🤝 Contribution

Pour contribuer à ce module, veuillez soumettre des issues ou des pull requests sur le dépôt du projet principal.

## 📞 Support

Pour toute question ou problème, veuillez consulter la documentation ou ouvrir une issue sur le dépôt du projet.
