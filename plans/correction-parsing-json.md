# Plan de Correction : Parsing JSON - Amélioration du Prompt

## Problème Identifié

**Symptôme**: L'agent retourne du texte brut au lieu d'un JSON structuré, causant l'erreur "Impossible de parser le JSON — pas d'alerte envoyée".

**Cause**: Le modèle `qwen3.5:9b` ne suit pas correctement les instructions de formatage JSON du prompt.

**Localisation**: [`oil_agent.py`](oil_agent.py:830-908) - fonction `get_master_prompt()`

---

## Solution Choisie

**Option 1**: Amélioration du prompt avec des instructions JSON plus explicites et des exemples.

---

## Plan de Mise en Œuvre

### Étape 1: Analyser le Prompt Actuel

Le prompt actuel (`get_master_prompt()`) contient:
- Instructions claires pour utiliser tous les outils
- Description des critères d'évaluation (impact score 1-10)
- Structure JSON attendue
- Exemple de format JSON

**Problèmes identifiés**:
1. Le format JSON est présenté tardivement dans le prompt
2. Pas de marqueurs de début/fin explicites pour le JSON
3. Pas d'exemples concrets de réponses complètes
4. L'instruction "Return your final answer as a JSON list" n'est pas assez impérative

### Étape 2: Conception du Prompt Amélioré

#### Nouvelle Structure du Prompt:

```
1. INSTRUCTIONS DE FORMATAGE (tout en haut, très visibles)
   - Marqueurs de début/fin explicites: ```json ... ```
   - Instruction impérative: "VOUS DEVEZ retourner SEULEMENT du JSON valide"
   - Avertissement: "Tout texte en dehors du JSON sera ignoré"

2. EXEMPLES CONCRETS
   - Exemple de réponse JSON complète avec événements
   - Exemple de réponse vide []
   - Exemple de réponse avec plusieurs événements

3. CONTEXTE ET MISSION
   - Rôle de l'analyste
   - Date actuelle
   - Outils disponibles

4. CRITÈRES D'ÉVALUATION
   - Impact score 1-10
   - Seuil d'alerte (>= 6)
   - Catégories d'événements

5. FORMAT JSON DÉTAILLÉ
   - Structure complète avec tous les champs
   - Types de données attendus
   - Contraintes de validation

6. INSTRUCTIONS FINALES
   - Rappel: SEULEMENT du JSON
   - Marqueurs de fin
```

#### Éléments Clés à Ajouter:

1. **Marqueurs de bloc JSON**:
   ```json
   {
     "events": [...]
   }
   ```

2. **Exemples de réponses**:
   - Exemple avec événement de haute priorité
   - Exemple avec événements multiples
   - Exemple sans événement

3. **Instructions impératives**:
   - "MUST return ONLY valid JSON"
   - "NO additional text, explanations, or formatting"
   - "The entire response must be a single JSON object"

4. **Validation explicite**:
   - "Ensure the JSON is valid and parseable"
   - "All required fields must be present"
   - "Arrays must be properly formatted"

### Étape 3: Modifications à Apporter

#### Fichier: [`oil_agent.py`](oil_agent.py:830-908)

**Section à modifier**: Fonction `get_master_prompt()` (lignes 830-908)

**Changements proposés**:

1. Ajouter une section "FORMAT OBLIGATOIRE" au début du prompt
2. Ajouter des exemples de réponses JSON complètes
3. Renforcer les instructions de formatage
4. Ajouter des marqueurs de début/fin pour le JSON
5. Simplifier et clarifier la structure attendue

### Étape 4: Prompt Amélioré (Proposition)

```python
def get_master_prompt() -> str:
    """Génère le prompt principal avec la date du jour dynamique."""
    from datetime import datetime
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    threshold = CONFIG["alert_threshold"]
    
    prompt = f"""
═══════════════════════════════════════════════════════════════════════════════
⚠️  FORMAT DE RÉPONSE OBLIGATOIRE - À LIRE ATTENTIVEMENT
═══════════════════════════════════════════════════════════════════════════════

VOUS DEVEZ RETOURNER SEULEMENT DU JSON VALIDE. AUCUN AUTRE TEXTE N'EST ACCEPTÉ.

Votre réponse doit être EXACTEMENT dans ce format:

```json
{{
  "events": [
    {{
      "id": "unique_event_id",
      "category": "Iran|Refinery|OPEC|Gas|Shipping|Geopolitical",
      "title": "Court titre descriptif",
      "impact_score": 8,
      "urgency": "Breaking|Recent|Developing|Background",
      "summary": "Analyse détaillée de l'événement et son impact sur les prix du pétrole",
      "price_impact": "+$3-5/barrel attendu",
      "source_hint": "Brève description de la source",
      "publication_date": "{current_date}"
    }}
  ]
}}
```

RÈGLES STRICTES:
- ✓ Retourner SEULEMENT le bloc JSON entre ```json et ```
- ✓ AUCUN texte avant ou après le JSON
- ✓ AUCUNE explication, commentaire ou formatage supplémentaire
- ✓ Le JSON doit être valide et parseable
- ✓ Si aucun événement n'est trouvé, retourner: {{"events": []}}

═══════════════════════════════════════════════════════════════════════════════
EXEMPLES DE RÉPONSES
═══════════════════════════════════════════════════════════════════════════════

EXEMPLE 1 - Avec événement de haute priorité:
```json
{{
  "events": [
    {{
      "id": "iran_hormuz_blockade_20260311",
      "category": "Iran",
      "title": "Iran bloque le détroit d'Ormuz - menace majeure sur l'approvisionnement",
      "impact_score": 9,
      "urgency": "Breaking",
      "summary": "L'Iran a annoncé le blocage du détroit d'Ormuz, qui transporte 20% du pétrole mondial. Cette action sans précédent menace gravement l'approvisionnement mondial et pourrait entraîner une hausse immédiate des prix du Brent de $5-10/barrel.",
      "price_impact": "+$5-10/barrel attendu",
      "source_hint": "Reuters Breaking News",
      "publication_date": "{current_date}"
    }}
  ]
}}
```

EXEMPLE 2 - Avec plusieurs événements:
```json
{{
  "events": [
    {{
      "id": "saudi_refinery_attack_20260311",
      "category": "Refinery",
      "title": "Attaque drone sur raffinerie Aramco en Arabie Saoudite",
      "impact_score": 7,
      "urgency": "Breaking",
      "summary": "Une attaque de drone a touché la raffinerie Aramco à Ras Tanura, causant des dégâts importants et réduisant la production de 500k barils/jour. Les forces de sécurité ont intercepté l'attaque mais les opérations sont suspendues.",
      "price_impact": "+$2-4/barrel attendu",
      "source_hint": "Bloomberg Energy",
      "publication_date": "{current_date}"
    }},
    {{
      "id": "opec_emergency_meeting_20260311",
      "category": "OPEC",
      "title": "OPEC convoque réunion d'urgence sur les coupes de production",
      "impact_score": 6,
      "urgency": "Recent",
      "summary": "L'OPEC a annoncé une réunion d'urgence pour discuter de coupes de production supplémentaires en réponse à la baisse des prix. Les analystes anticipent une réduction de 1M barils/jour.",
      "price_impact": "+$1-3/barrel attendu",
      "source_hint": "Reuters Energy",
      "publication_date": "{current_date}"
    }}
  ]
}}
```

EXEMPLE 3 - Sans événement:
```json
{{
  "events": []
}}
```

═══════════════════════════════════════════════════════════════════════════════
VOTRE MISSION
═══════════════════════════════════════════════════════════════════════════════

Vous êtes un expert analyste du marché pétrolier surveillant les événements géopolitiques 
et industriels qui pourraient faire rebondir le cours du pétrole (Brent, WTI).

DATE ACTUELLE: {current_date}
DATE ET HEURE: {current_datetime}

1. Utilisez TOUS les outils spécialisés disponibles:
   - search_iran_conflict: Tensions militaires Iran, IRGC, détroit d'Ormuz
   - search_refinery_damage: Attaques de raffineries, incendies, explosions
   - search_opec_supply: Coupes de production OPEC+, décisions de quotas
   - search_gas_disruption: Perturbations gaz naturel, pipelines, LNG
   - search_shipping_disruption: Attaques Houthis, saisies de tankers
   - search_geopolitical_escalation: Russie/Ukraine, Libye, Venezuela, Nigeria
   - get_oil_price: Prix actuels Brent/WTI et contexte
   - search_recent_news: Actualités très récentes (24h/48h/7j)
   - read_rss_feeds: Flux RSS en temps réel (Reuters, Bloomberg, AP, BBC)
   - get_vix_index: Indice VIX actuel (indicateur de peur du marché)

2. IMPORTANT: Pour une exécution plus rapide, appelez les outils directement:
   - Pour vérifications rapides: search_recent_news(topic="all", timeframe="24h")
   - Pour mises à jour en temps réel: read_rss_feeds(feed="all", hours_back=12)
   - Pour évaluation volatilité: get_vix_index()
   - Pour vérifications prix: get_oil_price()

3. PRIORITÉ: Événements d'AUJOURD'HUI ({current_date}) et dernières 24-48 heures.
   Utilisez des requêtes spécifiques avec "today", "breaking", "just in".

4. Pour chaque événement trouvé, évaluez:
   - CATÉGORIE: (Iran/Refinery/OPEC/Gas/Shipping/Geopolitical/Other)
   - SCORE D'IMPACT: 1-10 (10 = hausse majeure immédiate des prix très probable)
   - URGENCE: (Breaking/Recent/Developing/Background)
   - RÉSUMÉ: 2-3 phrases expliquant l'événement et son mécanisme d'impact
   - TITRE_SOURCE: Titre bref de l'actualité
   - DATE_PUBLICATION: Date de l'actualité (si disponible)

5. FILTRAGE: Gardez SEULEMENT les événements avec Impact Score >= {threshold}

6. RETOURNEZ VOTRE RÉPONSE AU FORMAT JSON SPÉCIFIÉ CI-DESSUS.

═══════════════════════════════════════════════════════════════════════════════
RAPPEL FINAL
═══════════════════════════════════════════════════════════════════════════════

⚠️  RAPPEL: Retournez SEULEMENT du JSON valide entre ```json et ```
⚠️  AUCUN texte avant ou après le JSON
⚠️  AUCUNE explication ou commentaire

```json
{{
  "events": [...]
}}
```
"""
    return prompt
```

### Étape 5: Améliorations Complémentaires du Parsing

Bien que l'option 1 se concentre sur l'amélioration du prompt, il est recommandé d'améliorer légèrement le parsing pour plus de robustesse:

**Fichier**: [`oil_agent.py`](oil_agent.py:935-948)

**Modifications proposées**:

```python
# Parse JSON - Version améliorée
events = []
if isinstance(raw_result, list):
    events = raw_result
elif isinstance(raw_result, str):
    # Extraction du JSON depuis la réponse texte
    import re
    
    # Pattern 1: Bloc JSON avec marqueurs ```json ... ```
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', raw_result, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            events = data.get("events", [])
        except json.JSONDecodeError as e:
            log.warning(f"Erreur parsing JSON (pattern 1): {e}")
    
    # Pattern 2: Tableau JSON direct [...]
    if not events:
        match = re.search(r'\[.*\]', raw_result, re.DOTALL)
        if match:
            try:
                events = json.loads(match.group())
            except json.JSONDecodeError as e:
                log.warning(f"Erreur parsing JSON (pattern 2): {e}")
    
    # Pattern 3: Objet JSON avec clé "events"
    if not events:
        match = re.search(r'\{.*"events".*?\}', raw_result, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
                events = data.get("events", [])
            except json.JSONDecodeError as e:
                log.warning(f"Erreur parsing JSON (pattern 3): {e}")
    
    if not events:
        log.warning("Impossible de parser le JSON — pas d'alerte envoyée")
        events = []
```

### Étape 6: Tests et Validation

1. **Test avec événements**:
   - Vérifier que le JSON est correctement parsé
   - Confirmer que les événements sont bien extraits
   - Valider l'envoi des alertes

2. **Test sans événements**:
   - Vérifier que `{"events": []}` est correctement parsé
   - Confirmer qu'aucune alerte n'est envoyée

3. **Test avec événements multiples**:
   - Vérifier que tous les événements sont extraits
   - Confirmer que les IDs sont uniques

4. **Test de robustesse**:
   - Tester avec des réponses partiellement formatées
   - Vérifier le comportement avec du texte supplémentaire

### Étape 7: Documentation

Mettre à jour le README.md avec:
- Description du problème et de la solution
- Exemples de format JSON attendu
- Instructions pour le debugging

---

## Avantages de cette Approche

1. **Simple et ciblée**: Modifie uniquement le prompt, pas la logique de parsing complexe
2. **Rapide à implémenter**: Changements localisés dans une seule fonction
3. **Facile à tester**: Peut être validé rapidement avec le modèle actuel
4. **Non invasive**: Ne modifie pas l'architecture existante
5. **Réversible**: Facile à revenir à l'ancien prompt si nécessaire

---

## Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Le modèle ne suit toujours pas les instructions | Moyenne | Élevé | Ajouter parsing robuste en complément |
| Le prompt devient trop long | Faible | Moyen | Simplifier les exemples si nécessaire |
| Performances réduites du modèle | Faible | Faible | Tester et ajuster si nécessaire |

---

## Critères de Succès

- [ ] Le modèle retourne systématiquement du JSON valide
- [ ] Le JSON est correctement parsé sans erreur
- [ ] Les événements sont correctement extraits et envoyés
- [ ] Le parsing fonctionne avec et sans événements
- [ ] Les logs montrent des résultats cohérents

---

## Prochaines Étapes

Une fois ce plan validé:
1. Implémenter les modifications du prompt
2. Améliorer légèrement le parsing (complément)
3. Tester avec le modèle actuel
4. Valider le fonctionnement complet
5. Documenter les changements
