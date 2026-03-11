# 📚 Plan d'Apprentissage DSPy

**Objectif** : Maîtriser DSPy pour améliorer l'agent de surveillance du marché pétrolier

**Durée estimée** : 2-3 semaines (à raison de 1-2h/jour)

**Prérequis** :
- Python 3.13+
- Ollama installé avec un modèle (qwen3.5:9b)
- Connaissance de base des LLMs

---

## 📋 Sommaire

1. [Semaine 1 : Fondamentaux DSPy](#semaine-1--fondamentaux-dspy)
2. [Semaine 2 : Modules Avancés](#semaine-2--modules-avancés)
3. [Semaine 3 : Optimisation et Production](#semaine-3--optimisation-et-production)
4. [Exercices Pratiques](#exercices-pratiques)
5. [Ressources](#ressources)

---

## Semaine 1 : Fondamentaux DSPy

### Jour 1-2 : Introduction à DSPy

**Objectifs** :
- Comprendre la philosophie de DSPy
- Installer et configurer DSPy avec Ollama
- Exécuter le premier programme DSPy

**Concepts clés** :
```
DSPy = Declarative + Stochastic + Programming + Yielding

Contrairement au prompt engineering manuel, DSPy :
- Déclare ce que vous voulez (Signatures)
- Compile en prompts optimisés automatiquement
- Sépare la logique du prompting
```

**À lire** :
- [Documentation officielle - Introduction](https://dspy-docs.vercel.app/)
- [DSPy GitHub](https://github.com/stanfordnlp/dspy)

**Pratique** :
```python
# test_dspy_basic.py
import dspy

# Configuration avec Ollama
ollama = dspy.LM(
    model="ollama_chat/qwen3.5:9b",
    api_base="http://127.0.0.1:11434",
    api_key="ollama"
)
dspy.configure(lm=ollama)

# Premier programme : Question → Réponse
qa = dspy.Predict("question -> answer")
result = qa(question="Quelle est la capitale de la France ?")
print(result.answer)
```

**Validation** :
- [ ] Le script s'exécute sans erreur
- [ ] Comprendre la différence entre `dspy.Predict` et `dspy.ChainOfThought`

---

### Jour 3-4 : Les Signatures DSPy

**Objectifs** :
- Maîtriser la définition de Signatures
- Comprendre InputField et OutputField
- Créer des signatures personnalisées

**Concepts clés** :
```python
class MaSignature(dspy.Signature):
    """Description claire de la tâche."""
    input1 = dspy.InputField(desc="Description de l'entrée")
    input2 = dspy.InputField(desc="Description d'une autre entrée")
    output = dspy.OutputField(desc="Description de la sortie attendue")
```

**À lire** :
- [DSPy Signatures Documentation](https://dspy-docs.vercel.app/docs/building-blocks/signatures)

**Pratique** :
```python
# test_signatures.py
import dspy

# Signature simple
class Summarize(dspy.Signature):
    """Résume un texte en 2-3 phrases."""
    text = dspy.InputField(desc="Texte à résumer")
    summary = dspy.OutputField(desc="Résumé concis")

# Utilisation
summarizer = dspy.Predict(Summarize)
result = summarizer(text="Le pétrole est une ressource...")
print(result.summary)

# Signature complexe (comme OilAnalysisSignature)
class OilAnalysisSignature(dspy.Signature):
    """Analyse des données sur le marché pétrolier."""
    raw_intelligence = dspy.InputField(
        desc="Données brutes collectées des outils et sources d'actualités"
    )
    current_date = dspy.InputField(desc="La date actuelle")
    
    report = dspy.OutputField(
        desc="Rapport JSON structuré avec: category, title, impact_score (1-10), "
             "urgency, summary, price_impact, source_hint, publication_date"
    )
```

**Validation** :
- [ ] Créer 3 signatures différentes
- [ ] Comprendre l'importance des descriptions (`desc`)

---

### Jour 5-7 : Modules DSPy

**Objectifs** :
- Maîtriser `dspy.Predict` et `dspy.ChainOfThought`
- Créer des modules personnalisés
- Comprendre le pattern `forward()`

**Concepts clés** :
```
dspy.Predict : Prompting direct
dspy.ChainOfThought : Ajoute un raisonnement étape par étape
dspy.Module : Classe de base pour créer des modules personnalisés
```

**Pratique** :
```python
# test_modules.py
import dspy

# 1. Predict simple
predict = dspy.Predict("question -> answer")
print(predict(question="2 + 2 = ?").answer)

# 2. ChainOfThought (raisonnement explicite)
cot = dspy.ChainOfThought("question -> answer")
result = cot(question="Si 3 chats attrapent 3 souris en 3 minutes, "
                      "combien de temps pour 100 chats attraper 100 souris ?")
print(f"Réponse: {result.answer}")
# Note: result contient aussi le raisonnement intermédiaire

# 3. Module personnalisé (comme OilAnalyst)
class OilAnalyst(dspy.Module):
    def __init__(self, num_trials=5):
        super().__init__()
        self.analyze = dspy.ChainOfThought(OilAnalysisSignature)
        self.num_trials = num_trials
    
    def forward(self, raw_intelligence, current_date):
        # Exécute l'analyse plusieurs fois
        reports = []
        for i in range(self.num_trials):
            prediction = self.analyze(
                raw_intelligence=raw_intelligence,
                current_date=current_date
            )
            reports.append(prediction.report)
        
        # Retourne le meilleur rapport ou consolide
        return self.consolidate(reports)
    
    def consolidate(self, reports):
        # Logique de consolidation
        class ConsolidatorSignature(dspy.Signature):
            reports = dspy.InputField(desc="Liste de rapports candidats")
            final_report = dspy.OutputField(desc="Rapport final consolidé")
        
        consolidator = dspy.Predict(ConsolidatorSignature)
        return consolidator(reports=str(reports)).final_report
```

**Validation** :
- [ ] Exécuter les 3 types de modules
- [ ] Comparer les sorties de Predict vs ChainOfThought
- [ ] Analyser le code de `dspy_oil_module.py`

---

## Semaine 2 : Modules Avancés

### Jour 8-10 : Configuration du Language Model

**Objectifs** :
- Configurer DSPy avec Ollama
- Comprendre les adaptateurs (ChatAdapter)
- Gérer les paramètres du modèle (température, max_tokens)

**Concepts clés** :
```python
# Configuration globale
dspy.configure(
    lm=dspy.LM(
        model="ollama_chat/qwen2.5:7b",
        api_base="http://127.0.0.1:11434",
        api_key="ollama",
        temperature=0.7,
        max_tokens=2000
    )
)

# Ou configuration locale
lm = dspy.LM("ollama_chat/qwen2.5:7b", ...)
module = dspy.ChainOfThought("q -> a")
module(lm=lm, question="...")  # Override global
```

**Pratique** :
```python
# test_lm_config.py
import dspy

# Configuration avec différents modèles
models = [
    "ollama_chat/qwen2.5:7b",
    "ollama_chat/llama3.1:8b",
    "ollama_chat/mistral:7b",
]

for model in models:
    print(f"\n=== Test avec {model} ===")
    dspy.configure(lm=dspy.LM(model, api_base="http://127.0.0.1:11434"))
    
    qa = dspy.ChainOfThought("question -> answer")
    result = qa(question="Explique brièvement ce qu'est DSPy")
    print(result.answer[:200])
```

**Validation** :
- [ ] Tester 3 modèles différents
- [ ] Comprendre l'impact de `temperature` sur les sorties
- [ ] Analyser `setup_dspy()` dans `dspy_oil_module.py`

---

### Jour 11-12 : Multi-Trial et Consolidation

**Objectifs** :
- Comprendre l'approche multi-trial
- Implémenter la consolidation de rapports
- Optimiser la qualité des sorties

**Concepts clés** :
```
Multi-Trial = Exécuter plusieurs fois + Sélectionner/Consolider le meilleur

Avantages :
- Réduit la variance des sorties
- Améliore la qualité moyenne
- Permet la validation croisée
```

**Pratique** :
```python
# test_multi_trial.py
import dspy
import json

dspy.configure(lm=dspy.LM("ollama_chat/qwen2.5:7b", api_base="http://127.0.0.1:11434"))

class MultiTrialAnalyzer(dspy.Module):
    def __init__(self, num_trials=5):
        super().__init__()
        self.analyze = dspy.ChainOfThought("data -> analysis")
        self.num_trials = num_trials
    
    def forward(self, data):
        # Collecte plusieurs analyses
        analyses = []
        for i in range(self.num_trials):
            result = self.analyze(data=data)
            analyses.append(result.analysis)
            print(f"Trial {i+1}: {len(result.analysis)} caractères")
        
        # Consolidation
        return self.consolidate(analyses)
    
    def consolidate(self, analyses):
        class ConsolidateSignature(dspy.Signature):
            """Consolide plusieurs analyses en une seule."""
            analyses = dspy.InputField(desc="Liste des analyses candidates")
            best_analysis = dspy.OutputField(desc="Meilleure analyse consolidée")
        
        consolidator = dspy.Predict(ConsolidateSignature)
        return consolidator(analyses=str(analyses)).best_analysis

# Test
analyzer = MultiTrialAnalyzer(num_trials=3)
result = analyzer(data="Le prix du pétrole a augmenté de 5% aujourd'hui")
print(f"\nRésultat consolidé:\n{result}")
```

**Validation** :
- [ ] Implémenter un module multi-trial
- [ ] Comparer qualité single-trial vs multi-trial
- [ ] Analyser la consolidation dans `OilAnalyst.consolidate()`

---

### Jour 13-14 : Intégration avec smolagents

**Objectifs** :
- Comprendre l'architecture oil-agent
- Intégrer DSPy dans un agent smolagents
- Optimiser le flux de travail

**À étudier** :
```python
# Dans oil-agent.py
from dspy_oil_module import OilAnalyst, setup_dspy

def run_monitoring_cycle():
    # 1. Collecte via smolagents
    raw_intelligence = agent.run(collector_prompt)
    
    # 2. Analyse via DSPy
    setup_dspy(CONFIG["ollama_model"], CONFIG["ollama_api_base"])
    analyst = OilAnalyst(num_trials=5)
    raw_result = analyst.forward(
        raw_intelligence=str(raw_intelligence),
        current_date=current_date
    )
    
    # 3. Parsing JSON et alertes
    events = parse_json_result(raw_result)
```

**Pratique** :
```python
# test_integration.py
"""Test d'intégration DSPy + smolagents"""
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool
from dspy_oil_module import OilAnalyst, setup_dspy

# Configuration
model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5:7b",
    api_base="http://127.0.0.1:11434",
)

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(max_results=3)],
    model=model,
    max_steps=5,
)

# Collecte
intelligence = agent.run("Recherche les dernières nouvelles sur le pétrole")
print(f"Intelligence collectée: {len(str(intelligence))} caractères")

# Analyse DSPy
setup_dspy("ollama_chat/qwen2.5:7b", "http://127.0.0.1:11434")
analyst = OilAnalyst(num_trials=3)
result = analyst.forward(
    raw_intelligence=str(intelligence),
    current_date="2025-03-11"
)
print(f"\nAnalyse DSPy:\n{result}")
```

**Validation** :
- [ ] Exécuter un cycle complet de collecte + analyse
- [ ] Mesurer le temps d'exécution
- [ ] Identifier les goulots d'étranglement

---

## Semaine 3 : Optimisation et Production

### Jour 15-17 : Optimisation DSPy (Optionnel)

**Objectifs** :
- Découvrir l'optimisation automatique de DSPy
- Comprendre le fine-tuning des prompts
- Explorer BootstrapFewShot

**Concepts clés** :
```
DSPy Optimizers :
- BootstrapFewShot : Génère des exemples automatiquement
- COPRO : Optimise les descriptions de signatures
- MIPRO : Optimisation avancée avec contraintes
```

**Pratique** :
```python
# test_optimization.py
import dspy
from dspy.evaluate import Evaluate
from dspy.teleprompt import BootstrapFewShot

# 1. Définir un jeu de données d'entraînement
trainset = [
    dspy.Example(
        raw_intelligence="Prix du pétrole en hausse...",
        current_date="2025-03-10"
    ).with_outputs(
        '[{"category": "OPEC", "impact_score": 7, "title": "..."}]'
    ),
    # Ajouter plus d'exemples...
]

# 2. Définir une métrique de validation
def validate_analysis(example, pred, trace=None):
    # Vérifier que la sortie est un JSON valide
    try:
        import json
        json.loads(pred.report)
        return True
    except:
        return False

# 3. Configurer l'optimizer
teleprompter = BootstrapFewShot(
    metric=validate_analysis,
    max_bootstrapped_demos=4,
    max_labeled_demos=8,
)

# 4. Compiler le module
analyst = OilAnalyst(num_trials=3)
compiled_analyst = teleprompter.compile(analyst, trainset=trainset)

# 5. Utiliser le modèle compilé
result = compiled_analyst(
    raw_intelligence="Nouvelle donnée...",
    current_date="2025-03-11"
)
```

**Validation** :
- [ ] Comprendre le principe de l'optimisation
- [ ] Tester BootstrapFewShot (si temps)
- [ ] Documenter les gains de performance

---

### Jour 18-19 : Debugging et Logging

**Objectifs** :
- Activer le logging DSPy
- Inspecter les prompts générés
- Debugger les erreurs courantes

**Pratique** :
```python
# test_debug.py
import dspy
import logging

# Activer le logging
logging.basicConfig(level=logging.DEBUG)

# Configuration
dspy.configure(lm=dspy.LM("ollama_chat/qwen2.5:7b", api_base="http://127.0.0.1:11434"))

# Inspecter les prompts
class DebugSignature(dspy.Signature):
    """Test signature."""
    input = dspy.InputField()
    output = dspy.OutputField()

debug_module = dspy.ChainOfThought(DebugSignature)

# Exécuter et inspecter
result = debug_module(input="Test input")

# Voir l'historique des appels
print("\n=== Historique des appels LM ===")
for i, call in enumerate(dspy.settings.lm.history):
    print(f"\nAppel {i+1}:")
    print(f"Prompt: {call['prompt'][:500]}...")
    print(f"Response: {call['response'][:200]}...")
```

**Validation** :
- [ ] Activer et lire les logs DSPy
- [ ] Inspecter les prompts générés
- [ ] Identifier les problèmes de format JSON

---

### Jour 20-21 : Projet Final

**Objectifs** :
- Créer un module DSPy personnalisé
- Intégrer dans oil-agent
- Documenter les améliorations

**Idées d'amélioration** :
```python
# 1. Signature améliorée avec validation
class ValidatedOilAnalysis(dspy.Signature):
    """Analyse validée du marché pétrolier."""
    raw_intelligence = dspy.InputField()
    current_date = dspy.InputField()
    
    report = dspy.OutputField(
        desc="JSON list with exact schema: "
             "[{'id': str, 'category': str, 'title': str, "
             "'impact_score': int (1-10), 'urgency': str, "
             "'summary': str, 'price_impact': str, "
             "'source_hint': str, 'publication_date': str}]"
    )

# 2. Module avec validation intégrée
class ValidatedOilAnalyst(dspy.Module):
    def __init__(self, num_trials=5):
        super().__init__()
        self.analyze = dspy.ChainOfThought(ValidatedOilAnalysis)
        self.num_trials = num_trials
    
    def forward(self, raw_intelligence, current_date):
        for trial in range(self.num_trials):
            result = self.analyze(
                raw_intelligence=raw_intelligence,
                current_date=current_date
            )
            
            # Validation JSON
            if self.is_valid_json(result.report):
                return result.report
        
        # Fallback après échecs
        return self.create_fallback_report()
    
    def is_valid_json(self, text):
        try:
            import json
            data = json.loads(text)
            return isinstance(data, list) and len(data) > 0
        except:
            return False
    
    def create_fallback_report(self):
        return "[]"  # Rapport vide par défaut

# 3. Utiliser dans oil-agent.py
def run_monitoring_cycle():
    # ...
    analyst = ValidatedOilAnalyst(num_trials=5)
    raw_result = analyst.forward(...)
    # ...
```

**Validation** :
- [ ] Implémenter une amélioration
- [ ] Tester en production
- [ ] Mesurer l'impact sur la qualité des alertes

---

## Exercices Pratiques

### Exercice 1 : Signature Simple
```python
# Créez une signature pour classifier l'urgence d'une nouvelle
class UrgencyClassifier(dspy.Signature):
    """Classifie l'urgence d'une nouvelle pétrolière."""
    news_title = dspy.InputField(desc="Titre de la nouvelle")
    news_content = dspy.InputField(desc="Contenu de la nouvelle")
    urgency_level = dspy.OutputField(desc="Niveau: Breaking/Recent/Background")
    impact_score = dspy.OutputField(desc="Score 1-10")

# Testez avec 5 nouvelles réelles
```

### Exercice 2 : Module Multi-Trial
```python
# Créez un module qui exécute 3 analyses et retourne la moyenne des scores
class AverageImpactAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.analyze = dspy.ChainOfThought("news -> impact_score")
    
    def forward(self, news):
        scores = []
        for _ in range(3):
            result = self.analyze(news=news)
            # Extraire le score
            scores.append(extract_score(result.impact_score))
        
        return {"average_score": sum(scores) / len(scores)}
```

### Exercice 3 : Intégration Complète
```python
# Modifiez oil-agent.py pour :
# 1. Ajouter un nouveau tool DSPy-powered
# 2. Utiliser l'optimisation multi-trial
# 3. Valider le JSON en sortie
# 4. Logger les prompts pour debugging
```

---

## Ressources

### Documentation Officielle
- [DSPy Docs](https://dspy-docs.vercel.app/)
- [GitHub Repository](https://github.com/stanfordnlp/dspy)
- [DSPy Paper](https://arxiv.org/abs/2310.03714)

### Tutoriels
- [DSPy Crash Course (YouTube)](https://www.youtube.com/results?search_query=dspy+tutorial)
- [DSPy Examples](https://github.com/stanfordnlp/dspy/tree/main/examples)

### Communauté
- [Discord DSPy](https://discord.gg/dspy)
- [Twitter @stanfordnlp](https://twitter.com/stanfordnlp)

### Lectures Avancées
- "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"
- "Optimizing Language Model Pipelines with DSPy"

---

## Suivi de Progression

| Semaine | Objectif | Status | Notes |
|---------|----------|--------|-------|
| 1 | Fondamentaux | ⬜ Pending | |
| 2 | Modules Avancés | ⬜ Pending | |
| 3 | Optimisation | ⬜ Pending | |

### Checklist Quotidienne

- [ ] Jour 1: Installation et premier programme
- [ ] Jour 2: Configuration Ollama
- [ ] Jour 3: Signatures simples
- [ ] Jour 4: Signatures complexes
- [ ] Jour 5: Modules Predict
- [ ] Jour 6: Modules ChainOfThought
- [ ] Jour 7: Module personnalisé OilAnalyst
- [ ] Jour 8: Configuration LM avancée
- [ ] Jour 9: Adaptateurs
- [ ] Jour 10: Paramètres de génération
- [ ] Jour 11: Multi-trial
- [ ] Jour 12: Consolidation
- [ ] Jour 13: Intégration smolagents
- [ ] Jour 14: Testing complet
- [ ] Jour 15: Optimisation (optionnel)
- [ ] Jour 16: BootstrapFewShot
- [ ] Jour 17: Évaluation
- [ ] Jour 18: Debugging
- [ ] Jour 19: Logging
- [ ] Jour 20: Projet final
- [ ] Jour 21: Documentation

---

## Prochaines Étapes

1. **Commencer Jour 1** : Installer DSPy et exécuter le premier exemple
2. **Utiliser le runner** : `python dspy_exercises/run_all.py`
3. **Rejoindre la communauté** : Discord DSPy pour poser des questions
4. **Contribuer** : Améliorer `dspy_oil_module.py` avec les nouvelles connaissances

---

## 📁 Fichiers d'exercices créés

Tous les exercices pratiques sont disponibles dans le dossier `dspy_exercises/` :

```
dspy_exercises/
├── run_all.py                  # Runner principal
├── README.md                   # Guide complet
├── jour_01_02/
│   └── test_dspy_basic.py      # Predict, ChainOfThought
├── jour_03_04/
│   └── test_signatures.py      # Signatures personnalisées
├── jour_05_07/
│   └── test_modules.py         # Modules DSPy
├── jour_08_10/
│   └── test_lm_config.py       # Configuration Ollama
├── jour_11_12/
│   └── test_multi_trial.py     # Multi-trial, consolidation
├── jour_13_14/
│   └── test_integration.py     # Intégration smolagents
├── jour_18_19/
│   └── test_debug.py           # Debugging, logging
└── jour_20_21/
    └── test_projet_final.py    # ValidatedOilAnalyst
```

### Utilisation rapide

```bash
# Exécuter tous les exercices
python dspy_exercises/run_all.py

# Exercice spécifique
python dspy_exercises/run_all.py --jour 1

# Lister les exercices
python dspy_exercises/run_all.py --liste
```

Voir [`dspy_exercises/README.md`](../dspy_exercises/README.md) pour plus de détails.

---

**Note** : Ce plan est basé sur l'architecture existante de oil-agent. Adaptez le rythme selon votre disponibilité et vos objectifs spécifiques.
