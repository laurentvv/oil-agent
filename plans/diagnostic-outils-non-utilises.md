# Diagnostic : Problème d'Utilisation des Outils - Oil Agent

**Date** : 2026-03-14  
**Statut** : Critique - Fonctionnement dégradé  
**Impact** : Événements hallucinés, aucune donnée réelle collectée

---

## 📋 Résumé Exécutif

L'agent oil-agent génère des alertes basées sur des événements **hallucinés** car **aucun outil de recherche n'est exécuté** (0/10). Bien que le système détecte et signale ce problème, il continue d'envoyer des alertes basées sur des données fictives.

### Problème Principal
```python
# Ligne 1580 dans oil_agent.py
raw_intelligence = agent.run(prompt)  # ❌ L'agent n'utilise PAS les outils
```

### Conséquences
- **0 outil utilisé sur 10** disponibles
- **9 événements hallucinés** détectés (Iran, Aramco, Houthis, etc.)
- **Alertes envoyées** pour des événements fictifs
- **Perte de confiance** dans le système

---

## 🔍 Analyse Détaillée

### 1. Problème : Fonction Non Utilisée

La fonction [`execute_all_tools_sequentially()`](oil_agent.py:1386) existe mais **n'est jamais appelée** :

```python
# Ligne 1386-1532 : Fonction complète et fonctionnelle
def execute_all_tools_sequentially(agent: CodeAgent) -> str:
    """Exécute tous les outils de recherche séquentiellement..."""
    # Exécute les 10 outils dans l'ordre
    # 1. search_iran_conflict
    # 2. search_refinery_damage
    # ...
    # 10. read_rss_feeds
    return combined_intelligence
```

**Problème** : Cette fonction n'est **JAMAIS** appelée dans [`run_monitoring_cycle()`](oil_agent.py:1539) !

### 2. Problème : Dépendance à l'Agent smolagents

Le code actuel (ligne1580) :

```python
raw_intelligence = agent.run(prompt)
```

S'attend à ce que l'agent smolagents utilise automatiquement les outils basés sur le prompt. Cependant :
- L'agent smolagents **ne suit pas** les instructions du prompt
- Le modèle LLM (Qwen3.5-9B) ne comprend pas le format attendu
- Aucun mécanisme de forçage d'exécution des outils

### 3. Problème : Validation Inefficace

La fonction [`validate_tool_usage()`](oil_agent.py:1248) détecte le problème mais ne le corrige pas :

```python
# Ligne 1596-1604
validation_passed, used_tools, missing_tools = validate_tool_usage(raw_intelligence, expected_tools)
log_tool_usage_summary(used_tools, missing_tools)

if not validation_passed:
    log.warning(f"⚠️ ATTENTION: {len(missing_tools)} outil(s) n'ont pas été utilisés!")
    log.warning("⚠️ Les événements détectés pourraient être basés sur des informations hallucinées.")
    # ❌ Mais le code CONTINUE quand même !
```

**Problème** : Le système détecte l'erreur mais **continue d'envoyer des alertes** !

### 4. Problème : Vérification de Véracité Défaillante

La fonction [`verify_event_truthfulness()`](oil_agent.py:1315) essaie de vérifier les événements mais échoue :

```python
# Ligne 1696
verified_events, unverified_events = verify_event_truthfulness(events, raw_intelligence)
```

**Problème** : Si `raw_intelligence` est vide (aucun outil utilisé), la fonction peut **valider par erreur** des événements hallucinés car :
- Elle cherche des mots-clés dans une intelligence vide
- Elle accepte les événements si `source_found` est True (par défaut)
- Les indicateurs de recherche (`===`, `---`) peuvent être absents

---

## 💡 Solutions Proposées

### Solution 1 : Utiliser `execute_all_tools_sequentially()` (RECOMMANDÉ)

**Avantages** :
- ✅ Garantit l'exécution de TOUS les outils
- ✅ Collecte des données réelles
- ✅ Élimine les hallucinations
- ✅ Code déjà écrit et testé

**Implémentation** :

```python
# Dans run_monitoring_cycle() (ligne 1580)
# REMPLACER :
raw_intelligence = agent.run(prompt)

# PAR :
raw_intelligence = execute_all_tools_sequentially(agent)
```

**Impact** :
- Modification minimale (1 ligne)
- Résultat immédiat
- Compatible avec le reste du code

### Solution 2 : Améliorer le Prompt smolagents

**Avantages** :
- ✅ Utilise l'agent smolagents comme prévu
- ✅ Plus flexible

**Inconvénients** :
- ❌ Ne garantit PAS l'exécution des outils
- ❌ Dépend du comportement du LLM
- ❌ Nécessite beaucoup de tests

**Implémentation** :

```python
# Améliorer get_master_prompt() pour être plus explicite
def get_master_prompt() -> str:
    prompt = f"""
    CRITICAL: You MUST call tools using this EXACT format:
    
    ```python
    result = search_iran_conflict(days_back=1)
    print(result)
    ```
    
    Do NOT write explanations. Only execute tools.
    """
    return prompt
```

### Solution 3 : Arrêter l'Exécution si Outils Non Utilisés

**Avantages** :
- ✅ Empêche l'envoi d'alertes basées sur des données fictives
- ✅ Sécurise le système

**Implémentation** :

```python
# Dans run_monitoring_cycle() (ligne 1602)
if not validation_passed:
    log.error(f"❌ ERREUR CRITIQUE: {len(missing_tools)} outil(s) n'ont pas été utilisés!")
    log.error("❌ Arrêt du cycle pour éviter les hallucinations.")
    return  # ❌ Arrêter l'exécution
```

### Solution 4 : Combiner Solutions 1 et 3 (OPTIMAL)

```python
# Dans run_monitoring_cycle()

# 1. Exécuter tous les outils séquentiellement
raw_intelligence = execute_all_tools_sequentially(agent)

# 2. Valider l'utilisation des outils
validation_passed, used_tools, missing_tools = validate_tool_usage(raw_intelligence, expected_tools)
log_tool_usage_summary(used_tools, missing_tools)

# 3. Arrêter si problème
if not validation_passed:
    log.error(f"❌ ERREUR CRITIQUE: {len(missing_tools)} outil(s) n'ont pas été utilisés!")
    log.error("❌ Arrêt du cycle pour éviter les hallucinations.")
    return

# 4. Continuer avec DSPy...
```

---

## 🎯 Recommandations

### Immédiat (Critique)

1. **Appliquer Solution 4** : Utiliser `execute_all_tools_sequentially()` + arrêt si erreur
2. **Tester** : Vérifier que les 10 outils sont exécutés
3. **Valider** : S'assurer que les événements sont basés sur des données réelles

### Court Terre (Améliorations)

1. **Améliorer le logging** : Ajouter plus de détails sur l'exécution des outils
2. **Ajouter des métriques** : Temps d'exécution par outil, nombre de résultats
3. **Améliorer DSPy** : Rendre la vérification de véracité plus stricte

### Long Terre (Architecture)

1. **Refactoriser** : Séparer la collecte d'outils de l'analyse DSPy
2. **Ajouter des tests** : Tests unitaires pour chaque outil
3. **Monitoring** : Dashboard pour surveiller l'exécution des outils en temps réel

---

## 📊 Impact des Solutions

| Solution | Complexité | Fiabilité | Effort | Recommandé |
|----------|-----------|-----------|---------|------------|
| Solution 1 | Faible | Élevée | 1 ligne | ✅ |
| Solution 2 | Moyenne | Faible | 2-3h | ❌ |
| Solution 3 | Faible | Élevée | 5 lignes | ✅ |
| Solution 4 | Faible | Très élevée | 10 lignes | ✅✅ |

---

## 🔧 Code de Correction (Solution 4)

```python
# Dans run_monitoring_cycle() (ligne 1579)

# REMPLACER les lignes 1580-1604 PAR :

# Exécuter tous les outils séquentiellement (garantit la collecte de données réelles)
raw_intelligence = execute_all_tools_sequentially(agent)
log.info(f"🔍 Intelligence récoltée ({len(raw_intelligence)} caractères)")

# Valider l'utilisation des outils
expected_tools = {
    "search_iran_conflict",
    "search_refinery_damage",
    "search_opec_supply",
    "search_gas_disruption",
    "search_shipping_disruption",
    "search_geopolitical_escalation",
    "get_oil_price",
    "get_vix_index",
    "search_recent_news",
    "read_rss_feeds"
}
validation_passed, used_tools, missing_tools = validate_tool_usage(raw_intelligence, expected_tools)

# Afficher le résumé de l'utilisation des outils
log_tool_usage_summary(used_tools, missing_tools)

# CRITIQUE: Arrêter l'exécution si des outils n'ont pas été utilisés
if not validation_passed:
    log.error(f"❌ ERREUR CRITIQUE: {len(missing_tools)} outil(s) n'ont pas été utilisés!")
    log.error("❌ Arrêt du cycle pour éviter les hallucinations.")
    log.error("❌ Veuillez vérifier la configuration et réessayer.")
    return  # Arrêter immédiatement - ne PAS envoyer d'alertes
```

---

## ✅ Checklist de Validation

Après application de la correction :

- [ ] Les 10 outils sont exécutés (vérifier dans les logs)
- [ ] L'intelligence brute contient des données réelles (pas vide)
- [ ] Les événements sont basés sur les résultats de recherche
- [ ] Aucun événement halluciné n'est détecté
- [ ] Les alertes ne sont envoyées que pour des événements vérifiés
- [ ] Le système s'arrête si les outils ne sont pas utilisés

---

## 📝 Notes Supplémentaires

### Pourquoi `execute_all_tools_sequentially()` n'est-elle pas utilisée ?

Hypothèses :
1. **Code hérité** : La fonction a été ajoutée mais jamais intégrée
2. **Test en cours** : Développement abandonné en cours de route
3. **Mauvaise compréhension** : Le développeur pensait que smolagents utiliserait automatiquement les outils

### Pourquoi l'agent smolagents n'utilise-t-il pas les outils ?

Hypothèses :
1. **Format de prompt incorrect** : Le prompt n'est pas dans le format attendu par smolagents
2. **Modèle LLM inadéquat** : Qwen3.5-9B ne comprend pas bien les instructions d'outils
3. **Configuration manquante** : Un paramètre de configuration smolagents est manquant

### Pourquoi la validation ne fonctionne-t-elle pas ?

Le problème est dans [`validate_tool_usage()`](oil_agent.py:1248) :

```python
# Ligne 1286-1289
for tool_name in required_tools:
    if tool_name in result_str:
        used_tools.add(tool_name)
```

Cette méthode cherche simplement le nom de l'outil dans la chaîne de caractères. Si l'agent mentionne "search_iran_conflict" dans son texte (sans l'exécuter), la validation considère l'outil comme utilisé !

---

## 🚀 Prochaines Étapes

1. **Appliquer la correction** (Solution 4)
2. **Tester** l'agent avec la correction
3. **Valider** les résultats
4. **Documenter** les changements
5. **Déployer** en production

---

**Document créé par** : Architect Mode  
**Date** : 2026-03-14  
**Version** : 1.0
