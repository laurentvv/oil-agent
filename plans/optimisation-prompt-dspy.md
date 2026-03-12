# Optimisation du Prompt avec DSPy - Oil Market Monitoring Agent

## 📋 Analyse du Prompt Actuel

### Points d'amélioration identifiés

Le prompt actuel dans [`oil_agent.py`](oil_agent.py:837-1006) présente plusieurs limitations :

1. **Structure impérative** : Le prompt utilise des instructions impératives ("VOUS DEVEZ", "RÈGLES STRICTES") plutôt qu'une approche déclarative.
2. **Pas de signatures explicites** : Les entrées/sorties ne sont pas définies formellement comme des signatures DSPy.
3. **Instructions de raisonnement limitées** : Pas de guidage explicite pour le Chain of Thought (CoT).
4. **Redondance** : Les règles de formatage JSON sont répétées plusieurs fois.
5. **Manque de modularité** : Tout est dans un seul prompt géant sans séparation claire des responsabilités.

---

## 🎯 Principes DSPy Appliqués

### 1. Signatures Déclaratives
Les signatures DSPy définissent **ce que** le module doit faire, pas **comment** le faire. Nous enrichissons la signature avec des descriptions précises pour chaque champ.

```python
class OilEventSignature(dspy.Signature):
    """Analyse les événements du marché pétrolier, évalue leur impact et extrait des données structurées."""
    
    current_date: str = dspy.InputField(desc="Date actuelle (YYYY-MM-DD)")
    current_datetime: str = dspy.InputField(desc="Horodatage complet actuel")
    alert_threshold: int = dspy.InputField(desc="Seuil d'alerte (0-10)")
    news_sources: list[str] = dspy.InputField(desc="Domaines de sources d'actualités prioritaires")
    raw_intelligence: str = dspy.InputField(desc="Données brutes collectées par les outils")
    
    events: list[dict] = dspy.OutputField(desc="Événements validés avec impact >= alert_threshold")
    confidence_score: float = dspy.OutputField(desc="Score de confiance global dans l'analyse (0.0-1.0)")
```

### 2. Chain of Thought (CoT) avec Étapes Avancées
Le CoT guide le modèle à travers un raisonnement structuré, incluant une étape de contre-analyse.

**Étapes de raisonnement suggérées :**
1. **Extraction** : Identifier tous les événements potentiels dans `raw_intelligence`.
2. **Datation** : Vérifier si l'événement date d'aujourd'hui ({current_date}) ou des dernières 48h.
3. **Évaluation d'impact** : Estimer le mouvement de prix ($/baril) selon le mécanisme offre/demande.
4. **Contre-analyse** : Chercher des raisons pour lesquelles l'impact pourrait être moindre (ex: stocks élevés, démentis).
5. **Validation** : Filtrer selon `alert_threshold` et formater en JSON.

### 3. Programmation vs Prompting
Au lieu de simplement "écrire un meilleur prompt", DSPy permet de **programmer** le comportement.

---

## 📝 Implémentation DSPy Améliorée

### Modèles Pydantic Robustes

```python
from pydantic import BaseModel, Field, validator
from typing import List, Literal

class OilEvent(BaseModel):
    id: str = Field(..., description="ID unique (ex: iran_hormuz_20240311)")
    category: Literal["Iran", "Refinery", "OPEC", "Gas", "Shipping", "Geopolitical"]
    title: str
    impact_score: int = Field(..., ge=0, le=10)
    certainty_score: float = Field(..., ge=0.0, le=1.0, description="Niveau de certitude de l'information")
    urgency: Literal["Breaking", "Recent", "Developing", "Background"]
    summary: str
    price_impact: str = Field(..., description="Ex: +$2-4/barrel")
    source_hint: str
    publication_date: str

    @validator('impact_score')
    def check_threshold(cls, v, values, **kwargs):
        # On peut injecter une logique de validation ici si besoin
        return v
```

### Module avec Assertions DSPy

```python
class OilEventAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.analyze = dspy.ChainOfThought(OilEventSignature)

    def forward(self, **kwargs):
        result = self.analyze(**kwargs)
        
        # Assertion : On s'assure que les événements ne sont pas "vieux"
        for event in result.events:
            dspy.Suggest(
                event['publication_date'] >= kwargs['current_date'],
                f"L'événement {event['title']} semble daté. Merci de privilégier les news du jour."
            )
            
        return result
```

---

## 📚 Exemples Few-Shot (Apprentissage par l'exemple)

Il est crucial d'inclure des exemples de "Faux Positifs" pour affiner le filtrage.

**Exemple 4 - Fausse Alerte (Bruit de marché) :**
*Entrée* : "Rumeur sur Twitter d'une explosion en Libye, non confirmée par Reuters."
*Raisonnement* : L'information n'est pas corroborée par les `news_sources` prioritaires. L'impact est spéculatif.
*Sortie* : `{"events": []}` (Car `impact_score` < `alert_threshold` ou manque de fiabilité).

---

## 🚀 Plan d'Intégration dans `oil_agent.py`

1. **Installation** : `uv add dspy` : Déjà installé et mis dans pyproject.toml
2. **Initialisation du modèle** :
   ```python
   lm = dspy.LM("ollama_chat/qwen3.5:9b", api_base=CONFIG["ollama_api_base"])
   dspy.configure(lm=lm, adapter=dspy.JSONAdapter())
   ```
3. **Remplacement de la synthèse finale** :
   Au lieu de passer le `MASTER_PROMPT` brut à `CodeAgent`, utiliser le module `OilEventAnalyzer` pour transformer les résultats des outils en JSON final.

---

## 📊 Comparaison des Approches

| Aspect | Prompt Actuel (Manuel) | Approche DSPy (Programmée) |
|--------|------------------------|----------------------------|
| **Fiabilité JSON** | Aléatoire (dépend du modèle) | Garantie par `JSONAdapter` |
| **Logique d'impact** | Intuitive | Basée sur un CoT structuré |
| **Filtrage date** | Instruction textuelle | Assertion `dspy.Suggest` |
| **Optimisation** | Manuelle (Trial & Error) | Automatique via `BootstrapFewShot` |
| **Maintenance** | Modification d'un bloc de 200 lignes | Mise à jour de la Signature Python |

---

## 📝 Prochaines Étapes Recommandées

1. **Extraction de la Signature** : Isoler `OilEventSignature` dans un fichier `signatures.py`.
2. **Collecte de données** : Sauvegarder quelques exécutions réelles pour créer un `trainset` (entrées outils -> sorties attendues).
3. **Optimisation automatique** : Utiliser `dspy.teleprompt.MIPROv2` pour laisser DSPy trouver les meilleures instructions de raisonnement pour `qwen3.5`.
4. **Validation par assertions** : Ajouter des contraintes sur le format des prix et la cohérence des catégories.
