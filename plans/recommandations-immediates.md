# Recommandations Immédiatement Applicables
## Guide d'Action Prioritaire pour Résoudre le Bloat Contextuel

**Date**: 2026-03-13  
**Problème**: 74,052 tokens en entrée à l'étape 10 → Échec de finalisation  
**Objectif**: Réduire à <20,000 tokens pour garantir l'exécution complète

---

## 🚨 ACTIONS PRIORITAIRES (AUJOURD'HUI)

### Action 1: Optimiser le Prompt Principal
**Temps estimé**: 5 minutes  
**Difficulté**: Très facile  
**Impact**: -1,100 tokens par étape

#### Instructions:
1. Ouvrir [`oil_agent.py`](oil_agent.py)
2. Aller à la ligne 1146 (fonction `get_master_prompt`)
3. Remplacer tout le contenu de la fonction par:

```python
def get_master_prompt() -> str:
    """Génère le prompt principal optimisé de collecte d'informations."""
    from datetime import datetime
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""Date: {current_date} {current_datetime}
Task: Monitor oil market for price-impacting events.

TOOLS (use systematically):
- search_iran_conflict: Iran/Hormuz tensions
- search_refinery_damage: Refinery attacks/fires
- search_opec_supply: OPEC+ production decisions
- search_gas_disruption: Gas pipeline/LNG issues
- search_shipping_disruption: Red Sea/Suez disruptions
- search_geopolitical_escalation: Broad escalations
- get_oil_price: Current Brent/WTI prices
- get_vix_index: Market volatility
- search_recent_news: Breaking news (24h)
- read_rss_feeds: Real-time feeds

OUTPUT FORMAT (per event):
[CAT] Title | Impact: X/10 | Source: X | Date: X
Details: [2-3 sentences]
Price Impact: [specific mechanism]

Prioritize events with impact ≥6. Deduplicate sources."""
    return prompt
```

4. Sauvegarder le fichier

---

### Action 2: Condenser les Descriptions de Tools
**Temps estimé**: 15 minutes  
**Difficulté**: Facile  
**Impact**: -4,620 tokens par étape

#### Instructions:
1. Ouvrir [`oil_agent.py`](oil_agent.py)
2. Modifier les descriptions des 11 tools suivantes:

#### Tool 1: IranConflictTool (ligne 540)
```python
description = (
    "Search Iran/Hormuz conflicts, IRGC actions, Israel escalation, "
    "sanctions disrupting oil supply. Returns structured summary."
)
```

#### Tool 2: RefineryDamageTool (ligne 590)
```python
description = (
    "Search refinery damage, fires, explosions, drone attacks worldwide. "
    "Returns structured results affecting global oil supply."
)
```

#### Tool 3: OPECSupplyTool (ligne 652)
```python
description = (
    "Search OPEC+ production cuts, quota decisions, emergency meetings, "
    "supply policy changes. Covers Saudi, Russia, UAE unilateral cuts."
)
```

#### Tool 4: NaturalGasDisruptionTool (ligne 702)
```python
description = (
    "Search gas pipeline sabotage, LNG terminal damage, Russia gas cuts. "
    "Returns disruptions affecting oil price correlation."
)
```

#### Tool 5: ShippingDisruptionTool (ligne 751)
```python
description = (
    "Search Houthi attacks, Red Sea tensions, Suez blockage, tanker seizures. "
    "Returns disruptions impacting Brent crude prices."
)
```

#### Tool 6: GeopoliticalEscalationTool (ligne 793)
```python
description = (
    "Search Russia-Ukraine attacks, Libya civil war, Venezuela sanctions, "
    "Nigeria pipeline attacks. Returns escalations spiking oil prices."
)
```

#### Tool 7: OilPriceTool (ligne 834)
```python
description = (
    "Fetch current Brent crude and WTI oil prices, recent movements, "
    "analyst forecasts. Returns price data and trends."
)
```

#### Tool 8: RecentNewsTool (ligne 874)
```python
description = (
    "Search recent oil news from Reuters, Bloomberg, AP, BBC, FT, WSJ. "
    "Filters by date (24h, 48h, 7d). Returns breaking stories."
)
```

#### Tool 9: RSSFeedTool (ligne 951)
```python
description = (
    "Read RSS feeds from Reuters, Bloomberg, AP, BBC for real-time news. "
    "Filters entries by publication date. Returns recent headlines."
)
```

#### Tool 10: VIXTool (ligne 1046)
```python
description = (
    "Fetch current VIX (CBOE Volatility Index), recent movements, "
    "volatility trends. Returns market fear indicator data."
)
```

#### Tool 11: VisitWebpageTool (built-in, non modifiable)
- Pas de modification nécessaire

3. Sauvegarder le fichier

---

### Action 3: Simplifier la Signature DSPy
**Temps estimé**: 3 minutes  
**Difficulté**: Très facile  
**Impact**: -700 tokens

#### Instructions:
1. Ouvrir [`oil_agent.py`](oil_agent.py)
2. Aller à la ligne 60 (classe `OilEventSignature`)
3. Remplacer par:

```python
class OilEventSignature(dspy.Signature):
    """Extract structured oil events from intelligence. ALL fields required per event."""
    
    current_date: str = dspy.InputField(desc="Date (YYYY-MM-DD)")
    current_datetime: str = dspy.InputField(desc="Timestamp")
    alert_threshold: int = dspy.InputField(desc="Alert threshold (0-10)")
    news_sources: list[str] = dspy.InputField(desc="Priority news sources")
    raw_intelligence: str = dspy.InputField(desc="Collected intelligence data")
    
    events: List[OilEvent] = dspy.OutputField(desc="Oil events with all required fields")
    confidence_score: float = dspy.OutputField(desc="Global confidence (0.0-1.0)")
```

4. Sauvegarder le fichier

---

### Action 4: Ajouter une Fonction d'Estimation de Tokens
**Temps estimé**: 2 minutes  
**Difficulté**: Très facile  
**Impact**: Monitoring

#### Instructions:
1. Ouvrir [`oil_agent.py`](oil_agent.py)
2. Aller à la ligne 417 (avant `logging.basicConfig`)
3. Ajouter:

```python
def estimate_tokens(text: str) -> int:
    """
    Estime le nombre de tokens dans un texte.
    Approximation: 4 caractères ≈ 1 token pour l'anglais.
    """
    return len(text) // 4
```

4. Sauvegarder le fichier

---

## 📊 TESTER LES MODIFICATIONS

### Test 1: Vérifier la Taille des Prompts
**Temps estimé**: 2 minutes

```bash
# Dans un terminal Python
from oil_agent import get_master_prompt, estimate_tokens

prompt = get_master_prompt()
tokens = estimate_tokens(prompt)

print(f"Prompt principal: {tokens:,} tokens")
print(f"Objectif: < 500 tokens")
print(f"Résultat: {'✅ PASS' if tokens < 500 else '❌ FAIL'}")
```

**Attendu**: < 500 tokens (actuellement ~1,500)

---

### Test 2: Exécuter l'Agent
**Temps estimé**: 5 minutes

```bash
# Exécuter l'agent
python oil_agent.py
```

**Attendu**: 
- L'agent démarre normalement
- Les prompts sont plus courts
- Pas d'erreurs de parsing

---

### Test 3: Surveiller l'Utilisation des Tokens
**Temps estimé**: 10 minutes

Ajouter du logging dans [`run_monitoring_cycle()`](oil_agent.py:1212):

```python
# Avant d'appeler agent.run()
log.info(f"📊 Prompt size: {estimate_tokens(prompt):,} tokens")

# Après agent.run()
log.info(f"📊 Output size: {estimate_tokens(raw_intelligence):,} tokens")
log.info(f"📊 Ratio: {estimate_tokens(raw_intelligence) / estimate_tokens(prompt):.2%}")
```

**Attendu**: 
- Input: < 10,000 tokens par étape
- Ratio output/input: > 5%

---

## 📈 RÉSULTATS ATTENDUS

### Après Actions Prioritaires (Aujourd'hui)

| Métrique | Avant | Après | Amélioration |
|---------|--------|-------|-------------|
| Prompt principal | 1,500 tokens | 400 tokens | -73% |
| Descriptions tools | 5,500 tokens | 880 tokens | -84% |
| Signature DSPy | 1,000 tokens | 300 tokens | -70% |
| **Total Phase 1** | **8,000 tokens** | **1,580 tokens** | **-80%** |

### Projection à l'Étape 10

| Scénario | Tokens Entrée | Statut |
|----------|--------------|---------|
| Actuel | 74,052 tokens | ❌ Échec |
| Phase 1 uniquement | ~67,000 tokens | ❌ Toujours trop élevé |
| Phase 1 + 2 | ~24,000 tokens | ✅ Succès |
| Phase 1 + 2 + 3 | ~18,600 tokens | ✅ Succès optimal |

---

## 🔄 PROCHAINES ÉTAPES (Cette Semaine)

### Étape 1: Créer le Module de Gestion du Contexte
**Fichier**: `context_management.py`  
**Contenu**: Voir [`plans/modifications-code-existant.md`](modifications-code-existant.md#32-crer-le-fichier-context_managementpy)

**Commande**:
```bash
# Créer le fichier
cat > context_management.py << 'EOF'
# Copier le contenu depuis modifications-code-existant.md
EOF
```

---

### Étape 2: Intégrer la Gestion du Contexte
**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Modifications**:
1. Ajouter les imports (ligne 34)
2. Modifier [`build_agent()`](oil_agent.py:1090)
3. Modifier [`run_monitoring_cycle()`](oil_agent.py:1212)

**Voir**: [`plans/modifications-code-existant.md`](modifications-code-existant.md#22-modifier-la-fonction-build_agent)

---

### Étape 3: Tester et Valider
**Commande**:
```bash
# Créer le fichier de test
cat > test_optimization.py << 'EOF'
# Copier le contenu depuis modifications-code-existant.md
EOF

# Exécuter les tests
python test_optimization.py
```

---

## ⚠️ POINTS D'ATTENTION

### 1. Qualité des Résultats
- **Risque**: La compression pourrait affecter la qualité des événements détectés
- **Surveillance**: Comparer les résultats avant/après sur les mêmes données
- **Action**: Si la qualité diminue, ajuster les paramètres de compression

### 2. Compatibilité
- **Risque**: Les modifications pourraient casser des fonctionnalités existantes
- **Surveillance**: Tester tous les tools et workflows
- **Action**: Garder une sauvegarde du fichier original

### 3. Performance
- **Risque**: La gestion du contexte pourrait ralentir l'exécution
- **Surveillance**: Mesurer le temps d'exécution avant/après
- **Action**: Optimiser si nécessaire

---

## 📝 CHECKLIST DE VALIDATION

### Avant de Commencer
- [ ] Sauvegarder [`oil_agent.py`](oil_agent.py)
- [ ] Sauvegarder [`config.json`](config.json)
- [ ] Noter les métriques actuelles (tokens par étape)

### Pendant les Modifications
- [ ] Modifier [`get_master_prompt()`](oil_agent.py:1146)
- [ ] Modifier les 11 descriptions de tools
- [ ] Modifier [`OilEventSignature`](oil_agent.py:60)
- [ ] Ajouter `estimate_tokens()`
- [ ] Sauvegarder les modifications

### Après les Modifications
- [ ] Tester la taille des prompts
- [ ] Exécuter l'agent
- [ ] Surveiller l'utilisation des tokens
- [ ] Comparer les résultats avant/après
- [ ] Documenter les observations

### Si Problèmes
- [ ] Restaurer la sauvegarde
- [ ] Identifier la modification causant le problème
- [ ] Ajuster ou supprimer la modification
- [ ] Re-tester

---

## 🎯 OBJECTIFS DE PERFORMANCE

### Objectifs Minimaux (Phase 1)
- ✅ Prompt principal < 500 tokens
- ✅ Descriptions tools < 1,000 tokens
- ✅ Signature DSPy < 400 tokens
- ✅ Total prompts système < 2,000 tokens

### Objectifs Intermédiaires (Phase 2)
- ✅ Historique compressé < 5,000 tokens
- ✅ Fenêtre glissante activée
- ✅ Gestion du contexte fonctionnelle
- ✅ Étape 10 exécutable

### Objectifs Optimaux (Phase 3)
- ✅ Cache de tools activé
- ✅ Déduplication efficace
- ✅ Étape 10 < 20,000 tokens
- ✅ Ratio output/input > 5%

---

## 📞 SUPPORT ET DÉPANNAGE

### Problèmes Courants

#### Problème: "ModuleNotFoundError: No module named 'context_management'"
**Solution**: Créer le fichier `context_management.py` avec le contenu fourni

#### Problème: "AttributeError: 'CodeAgent' object has no attribute 'state'"
**Solution**: Modifier [`build_agent()`](oil_agent.py:1090) pour initialiser l'état

#### Problème: "Token count still too high"
**Solution**: 
- Vérifier que toutes les modifications ont été appliquées
- Augmenter le ratio de compression dans la configuration
- Réduire la taille de la fenêtre glissante

#### Problème: "Quality of events decreased"
**Solution**:
- Réduire l'agressivité de la compression
- Augmenter le nombre d'étapes conservées dans la fenêtre
- Ajuster les seuils de déduplication

---

## 📚 RÉFÉRENCES

### Documentation
- [`plans/optimisation-contextuelle-smolagents.md`](optimisation-contextuelle-smolagents.md) - Stratégie complète
- [`plans/modifications-code-existant.md`](modifications-code-existant.md) - Modifications détaillées
- [`docs/OPTIMIZATION.md`](docs/OPTIMIZATION.md) - Documentation DSPy existante

### Code Source
- [`oil_agent.py`](oil_agent.py) - Agent principal
- [`optimize_agent.py`](optimize_agent.py) - Script d'optimisation DSPy
- [`config.json`](config.json) - Configuration

### Outils
- smolagents: Framework d'agents
- DSPy: Framework d'optimisation de prompts
- llama.cpp: Serveur LLM

---

## ✅ RÉSUMÉ EXÉCUTIF

### Actions Immédiates (Aujourd'hui - 25 minutes)
1. ✅ Optimiser [`get_master_prompt()`](oil_agent.py:1146) (-1,100 tokens)
2. ✅ Condenser descriptions de tools (-4,620 tokens)
3. ✅ Simplifier [`OilEventSignature`](oil_agent.py:60) (-700 tokens)
4. ✅ Ajouter `estimate_tokens()` (monitoring)

### Résultats Attendus
- **Phase 1**: -6,420 tokens par étape
- **Phase 2**: -50,000 tokens à l'étape 10
- **Phase 3**: -6,000 tokens supplémentaires
- **Total**: 74,000 → 18,600 tokens (**-75%**)

### Prochaines Étapes
- Cette semaine: Implémenter la gestion du contexte
- Ce mois: Optimisations avancées et surveillance
- Continu: Ajustements basés sur les métriques

---

**Note**: Ce document fournit un guide pas-à-pas pour résoudre immédiatement le problème de bloat contextuel. Commencez par les actions prioritaires aujourd'hui, puis progressez vers les phases suivantes selon les résultats observés.
