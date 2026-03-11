# Plan de Correction : Parsing JSON - Solutions Alternatives

## Problème Identifié

**Symptôme**: L'agent retourne du texte brut au lieu d'un JSON structuré, causant l'erreur "Impossible de parser le JSON — pas d'alerte envoyée".

**Exemple de réponse incorrecte**:
```
The VIX index value on March 11, 2026 is approximately 24.93 (representing elevated market volatility amid geopolitical tensions and energy supply concerns).
```

**Cause**: Le modèle `qwen3.5:9b` ne suit pas correctement les instructions de formatage JSON du prompt, même avec des instructions explicites.

**Localisation**: [`oil-agent.py`](oil-agent.py:837-1008) - fonction `get_master_prompt()`

---

## Solutions Possibles

### Solution 1: Amélioration du Prompt (Approche Actuelle)

**Description**: Renforcer les instructions de formatage JSON dans le prompt avec des exemples plus explicites et des avertissements.

**Avantages**:
- Simple à implémenter
- Ne nécessite pas de changement d'architecture
- Réversible

**Inconvénients**:
- Dépend de la capacité du modèle à suivre les instructions
- Le modèle `qwen3.5:9b` a déjà du mal avec le prompt actuel
- Peut ne pas suffire

**Probabilité de succès**: 40-50%

---

### Solution 2: Parsing Robuste avec Extraction Intelligente ⭐ RECOMMANDÉE

**Description**: Améliorer significativement le parsing pour extraire du JSON même s'il est mal formaté, et ajouter une logique de fallback pour interpréter le texte brut.

**Avantages**:
- Fonctionne même si le modèle ne suit pas parfaitement les instructions
- Plus robuste face aux variations de format
- Peut extraire des informations même du texte brut
- Ne dépend pas du modèle

**Inconvénients**:
- Plus complexe à implémenter
- Nécessite des tests approfondis

**Probabilité de succès**: 80-90%

---

### Solution 3: Changement de Modèle

**Description**: Remplacer `qwen3.5:9b` par un modèle avec un meilleur respect des instructions (ex: `llama3.1:8b`, `mistral-nemo:12b`).

**Avantages**:
- Résout le problème à la source
- Meilleure qualité des réponses
- Plus fiable

**Inconvénients**:
- Nécessite de télécharger un nouveau modèle
- Coût de calcul potentiellement plus élevé
- Peut avoir des performances différentes

**Probabilité de succès**: 70-80%

---

### Solution 4: Utilisation d'un Parser JSON Spécialisé

**Description**: Utiliser une bibliothèque spécialisée pour extraire et valider du JSON depuis du texte brut (ex: `json5`, `hjson`).

**Avantages**:
- Plus tolérant aux erreurs de formatage
- Peut parser du JSON mal formé
- Simple à intégrer

**Inconvénients**:
- Ne résout pas le problème du modèle qui ne génère pas de JSON
- Ajoute une dépendance

**Probabilité de succès**: 50-60%

---

### Solution 5: Post-Processing avec LLM Secondaire

**Description**: Utiliser un second appel au modèle pour convertir la réponse texte brute en JSON structuré.

**Avantages**:
- Garantit le format JSON final
- Peut corriger les erreurs de formatage
- Flexible

**Inconvénients**:
- Double le coût de calcul
- Plus lent
- Complexité accrue

**Probabilité de succès**: 90-95%

---

## Solution Recommandée : Solution 2 (Parsing Robuste)

### Pourquoi cette solution ?

1. **Haute probabilité de succès** (80-90%)
2. **Ne dépend pas du modèle** - fonctionne avec n'importe quel modèle
3. **Robuste** - gère les variations de format
4. **Réversible** - peut être amélioré ou remplacé si nécessaire
5. **Coût minimal** - pas de changement d'infrastructure

### Implémentation Proposée

#### Étape 1: Amélioration du Prompt (Complémentaire)

Même si le parsing est robuste, un meilleur prompt améliore la qualité des réponses.

#### Étape 2: Parsing Multi-Patterns Avancé

Ajouter des patterns de parsing supplémentaires et une logique d'extraction intelligente.

#### Étape 3: Fallback vers Extraction de Texte Brut

Si aucun JSON n'est trouvé, extraire les informations du texte brut en utilisant des patterns regex.

#### Étape 4: Validation et Reconstruction

Valider les données extraites et reconstruire un JSON valide.

---

## Plan de Mise en Œuvre

### Phase 1: Analyse et Conception

1. Analyser les différents formats de réponse possibles
2. Identifier les patterns d'extraction pour chaque format
3. Concevoir la logique de fallback

### Phase 2: Implémentation

1. Modifier la fonction `run_monitoring_cycle()` dans [`oil-agent.py`](oil-agent.py:1015-1129)
2. Ajouter une nouvelle fonction `extract_events_from_response()`
3. Implémenter les patterns de parsing
4. Ajouter la logique de fallback

### Phase 3: Tests

1. Tester avec des réponses JSON valides
2. Tester avec des réponses texte brut
3. Tester avec des réponses partiellement formatées
4. Tester avec des réponses vides

### Phase 4: Documentation

1. Documenter les patterns de parsing
2. Ajouter des exemples dans le README
3. Créer un guide de debugging

---

## Spécifications Techniques

### Fonction `extract_events_from_response()`

```python
def extract_events_from_response(raw_result, current_date):
    """
    Extrait les événements depuis la réponse de l'agent.
    
    Gère plusieurs formats:
    1. JSON valide avec marqueurs ```json ... ```
    2. JSON valide sans marqueurs
    3. Tableau JSON [...]
    4. Objet JSON avec clé "events"
    5. Texte brut avec patterns identifiables
    6. Réponse vide ou sans événements
    
    Args:
        raw_result: Résultat brut de l'agent (str, list, dict)
        current_date: Date actuelle pour les événements sans date
    
    Returns:
        list: Liste d'événements extraits
    """
    events = []
    
    # Pattern 1: JSON avec marqueurs ```json ... ```
    # Pattern 2: JSON sans marqueurs
    # Pattern 3: Tableau JSON direct
    # Pattern 4: Objet JSON avec clé "events"
    # Pattern 5: Extraction depuis texte brut (NOUVEAU)
    # Pattern 6: Fallback vers événement vide
    
    return events
```

### Patterns d'Extraction depuis Texte Brut

Si le modèle retourne du texte brut, extraire les informations en utilisant des patterns:

```python
# Pattern pour détecter un événement dans le texte
event_patterns = [
    r"(?:Iran|Refinery|OPEC|Gas|Shipping|Geopolitical).{10,200}",
    r"(?:attack|blockade|disruption|cut|escalation).{10,200}",
    r"(?:oil|crude|Brent|WTI).{10,200}",
]
```

### Reconstruction d'Événement

Si des informations sont extraites du texte brut, reconstruire un événement valide:

```python
def reconstruct_event_from_text(text, current_date):
    """
    Reconstruit un événement depuis du texte brut.
    
    Args:
        text: Texte brut contenant des informations
        current_date: Date actuelle
    
    Returns:
        dict: Événement reconstruit
    """
    return {
        "id": f"extracted_{hashlib.md5(text.encode()).hexdigest()[:8]}",
        "category": "Other",
        "title": text[:100],
        "impact_score": 5,  # Score par défaut
        "urgency": "Recent",
        "summary": text[:500],
        "price_impact": "Impact inconnu",
        "source_hint": "Extraction automatique",
        "publication_date": current_date,
    }
```

---

## Critères de Succès

- [ ] Le parsing fonctionne avec du JSON valide
- [ ] Le parsing fonctionne avec du texte brut
- [ ] Les événements sont correctement extraits dans tous les cas
- [ ] Aucune alerte n'est envoyée si aucun événement n'est trouvé
- [ ] Les logs montrent des résultats cohérents
- [ ] Le système est robuste face aux variations de format

---

## Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| L'extraction depuis texte brut est imprécise | Moyenne | Moyen | Utiliser des patterns conservateurs et valider les résultats |
| Le parsing devient trop complexe | Faible | Moyen | Documenter clairement la logique et ajouter des tests |
| Faux positifs lors de l'extraction | Moyenne | Faible | Ajouter un seuil de confiance minimum |
| Performance réduite | Faible | Faible | Optimiser les patterns et utiliser du caching |

---

## Prochaines Étapes

Une fois ce plan validé:
1. Implémenter la fonction `extract_events_from_response()`
2. Modifier `run_monitoring_cycle()` pour utiliser cette fonction
3. Ajouter les patterns d'extraction depuis texte brut
4. Tester avec différents formats de réponse
5. Valider le fonctionnement complet
6. Documenter les changements
