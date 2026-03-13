# Modifications Concrètes du Code Existant
## Implémentation de l'Optimisation Contextuelle

**Date**: 2026-03-13  
**Objectif**: Fournir les modifications concrètes à appliquer à [`oil_agent.py`](oil_agent.py)

---

## 1. MODIFICATIONS PRIORITAIRES (Phase 1)

### 1.1 Optimiser le Prompt Principal

**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Lignes**: 1146-1182  
**Action**: Remplacer [`get_master_prompt()`](oil_agent.py:1146) par la version optimisée

```python
# === ANCIEN CODE (Lignes 1146-1182) ===
def get_master_prompt() -> str:
    """Génère le prompt principal de collecte d'informations."""
    from datetime import datetime
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""
You are an expert oil market analyst monitoring geopolitical and industrial events
that could cause oil prices (Brent crude, WTI) to spike or rebound.

CURRENT DATE: {current_date}
CURRENT DATETIME: {current_datetime}

YOUR MISSION:
1. Use ALL available specialized tools to gather current intelligence from TODAY ({current_date}) and the last 24-48 hours.
2. Focus on:
   - Iran tensions & Strait of Hormuz (search_iran_conflict)
   - Refinery attacks or damage (search_refinery_damage)
   - OPEC+ production decisions (search_opec_supply)
   - Gas disruptions (search_gas_disruption)
   - Shipping/Red Sea tensions (search_shipping_disruption)
   - Broad geopolitical escalations (search_geopolitical_escalation)
   - Current oil prices & volatility (get_oil_price, get_vix_index)
   - Breaking news from Reuters, Bloomberg, AP, BBC, FT, WSJ (search_recent_news, read_rss_feeds)

3. OUTPUT: Provide a COMPREHENSIVE report of your findings. For EACH significant event or news item, you MUST include:
   - EXACT DATE and TIME (if available).
   - SOURCE (Website, tool, or news agency).
   - CATEGORY (Iran, Refinery, OPEC, Gas, Shipping, Geopolitical).
   - DETAILED EXPLANATION of the event.
   - PRICE IMPACT: How exactly this influences oil supply or market sentiment.

Be extremely thorough. Do NOT provide a high-level summary. I need the raw, detailed intelligence to perform a structured synthesis later.
If you find multiple sources for the same event, list them all to increase certainty.
"""
    return prompt

# === NOUVEAU CODE (Remplacement) ===
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

**Gain estimé**: ~1,100 tokens économisés par étape (**-73%**)

---

### 1.2 Condenser les Descriptions de Tools

**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Action**: Réécrire toutes les descriptions de tools (11 tools)

#### Exemple 1: IranConflictTool (Lignes 540-543)

```python
# === ANCIEN CODE ===
class IranConflictTool(Tool):
    """Tool : conflits Iran / Détroit d'Ormuz / IRGC"""
    name = "search_iran_conflict"
    description = (
        "Searches for recent news about Iran military conflicts, IRGC actions, "
        "Strait of Hormuz tensions, Iran-Israel escalation, or Iran sanctions "
        "that could disrupt oil supply. Returns a structured summary."
    )

# === NOUVEAU CODE ===
class IranConflictTool(Tool):
    """Tool : conflits Iran / Détroit d'Ormuz / IRGC"""
    name = "search_iran_conflict"
    description = (
        "Search Iran/Hormuz conflicts, IRGC actions, Israel escalation, "
        "sanctions disrupting oil supply. Returns structured summary."
    )
```

#### Exemple 2: RefineryDamageTool (Lignes 590-595)

```python
# === ANCIEN CODE ===
class RefineryDamageTool(Tool):
    """Tool : dommages raffineries (attaques, accidents, incendies)"""
    name = "search_refinery_damage"
    description = (
        "Searches for news about oil refinery damage, fires, explosions, drone attacks "
        "on refineries worldwide (Saudi Arabia, Russia, Iraq, UAE, Kazakhstan). "
        "Returns structured results that can affect global oil supply."
    )

# === NOUVEAU CODE ===
class RefineryDamageTool(Tool):
    """Tool : dommages raffineries (attaques, accidents, incendies)"""
    name = "search_refinery_damage"
    description = (
        "Search refinery damage, fires, explosions, drone attacks worldwide. "
        "Returns structured results affecting global oil supply."
    )
```

#### Exemple 3: OPECSupplyTool (Lignes 652-658)

```python
# === ANCIEN CODE ===
class OPECSupplyTool(Tool):
    """Tool : décisions OPEC+, coupes de production, quotas"""
    name = "search_opec_supply"
    description = (
        "Searches for OPEC+ production cuts, quota decisions, emergency meetings, "
        "and supply policy changes that could drive oil prices higher. "
        "Also covers Saudi Arabia, Russia, UAE unilateral cuts."
    )

# === NOUVEAU CODE ===
class OPECSupplyTool(Tool):
    """Tool : décisions OPEC+, coupes de production, quotas"""
    name = "search_opec_supply"
    description = (
        "Search OPEC+ production cuts, quota decisions, emergency meetings, "
        "supply policy changes. Covers Saudi, Russia, UAE unilateral cuts."
    )
```

**Gain estimé**: ~4,620 tokens économisés par étape (**-84%**)

---

### 1.3 Optimiser la Signature DSPy

**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Lignes**: 60-76  
**Action**: Simplifier [`OilEventSignature`](oil_agent.py:60)

```python
# === ANCIEN CODE (Lignes 60-76) ===
class OilEventSignature(dspy.Signature):
    """Analyse les événements du marché pétrolier, évalue leur impact et extrait des données structurées.
    
    IMPORTANT: Pour chaque événement, vous DEVEZ inclure TOUS les champs: id, category, title, impact_score, 
    certainty_score, urgency, summary, price_impact, source_hint, publication_date.
    Ne sautez JAMAIS le champ 'title'.
    """
    
    current_date: str = dspy.InputField(desc="Date actuelle (YYYY-MM-DD)")
    current_datetime: str = dspy.InputField(desc="Horodatage complet actuel")
    alert_threshold: int = dspy.InputField(desc="Seuil d'alerte (0-10)")
    news_sources: list[str] = dspy.InputField(desc="Domaines de sources d'actualités prioritaires")
    raw_intelligence: str = dspy.InputField(desc="Données brutes collectées par les outils de surveillance")
    
    events: List[OilEvent] = dspy.OutputField(desc="Liste d'objets OilEvent. CHAQUE objet doit avoir TOUS les champs requis.")
    confidence_score: float = dspy.OutputField(desc="Score de confiance global dans l'analyse (0.0-1.0)")

# === NOUVEAU CODE (Remplacement) ===
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

**Gain estimé**: ~700 tokens économisés (**-70%**)

---

## 2. MODIFICATIONS D'ARCHITECTURE (Phase 2)

### 2.1 Ajouter les Imports pour la Gestion du Contexte

**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Ligne**: 34 (après les imports existants)

```python
# === AJOUTER APRÈS LA LIGNE 34 ===
from context_management import (
    HistoryCompressor,
    SlidingWindowManager,
    MemoryCleaner,
    AgentState,
    build_optimized_prompt_context,
)
```

### 2.2 Modifier la Fonction build_agent()

**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Lignes**: 1090-1139  
**Action**: Intégrer la gestion du contexte dans [`build_agent()`](oil_agent.py:1090)

```python
# === ANCIEN CODE (Lignes 1090-1139) ===
def build_agent() -> CodeAgent:
    """Initialise le modèle llama-server et l'agent avec tous les tools."""
    from smolagents.local_python_executor import LocalPythonExecutor
    
    model = LiteLLMModel(
        model_id=f"openai/{CONFIG.model.name}",
        api_base=CONFIG.model.api_base,
        api_key="dummy",
        num_ctx=CONFIG.model.num_ctx,
    )

    # Tools built-in réutilisés dans les tools custom
    ddg = DuckDuckGoSearchTool(max_results=5)
    visit = VisitWebpageTool(max_output_length=4000)

    tools = [
        ddg,
        visit,
        IranConflictTool(ddg),
        RefineryDamageTool(ddg, visit),
        OPECSupplyTool(ddg),
        NaturalGasDisruptionTool(ddg),
        ShippingDisruptionTool(ddg),
        GeopoliticalEscalationTool(ddg),
        OilPriceTool(ddg),
        RecentNewsTool(ddg),
        RSSFeedTool(),
        VIXTool(ddg),
    ]

    # Créer un executor personnalisé avec un timeout augmenté à 60 secondes
    custom_executor = LocalPythonExecutor(
        additional_authorized_imports=["json", "datetime", "hashlib", "feedparser"],
        timeout_seconds=60,
    )

    # Créer l'agent avec le format markdown pour les balises de code
    agent = CodeAgent(
        tools=tools,
        model=model,
        max_steps=10,
        additional_authorized_imports=["json", "datetime", "hashlib", "feedparser"],
        executor=custom_executor,
        code_block_tags="markdown",
    )
    
    log.info(f"🔧 CodeAgent code_block_tags: {agent.code_block_tags}")
    log.info(f"🔧 CodeAgent attend le format: {agent.code_block_tags[0]}...{agent.code_block_tags[1]}")
    
    return agent

# === NOUVEAU CODE (Remplacement) ===
def build_agent() -> CodeAgent:
    """Initialise le modèle llama-server et l'agent avec tous les tools et gestion de contexte."""
    from smolagents.local_python_executor import LocalPythonExecutor
    
    model = LiteLLMModel(
        model_id=f"openai/{CONFIG.model.name}",
        api_base=CONFIG.model.api_base,
        api_key="dummy",
        num_ctx=CONFIG.model.num_ctx,
    )

    # Tools built-in réutilisés dans les tools custom
    ddg = DuckDuckGoSearchTool(max_results=5)
    visit = VisitWebpageTool(max_output_length=4000)

    tools = [
        ddg,
        visit,
        IranConflictTool(ddg),
        RefineryDamageTool(ddg, visit),
        OPECSupplyTool(ddg),
        NaturalGasDisruptionTool(ddg),
        ShippingDisruptionTool(ddg),
        GeopoliticalEscalationTool(ddg),
        OilPriceTool(ddg),
        RecentNewsTool(ddg),
        RSSFeedTool(),
        VIXTool(ddg),
    ]

    # Créer un executor personnalisé avec un timeout augmenté à 60 secondes
    custom_executor = LocalPythonExecutor(
        additional_authorized_imports=["json", "datetime", "hashlib", "feedparser"],
        timeout_seconds=60,
    )

    # Créer l'agent avec le format markdown pour les balises de code
    agent = CodeAgent(
        tools=tools,
        model=model,
        max_steps=10,
        additional_authorized_imports=["json", "datetime", "hashlib", "feedparser"],
        executor=custom_executor,
        code_block_tags="markdown",
    )
    
    # Initialiser la gestion du contexte
    agent.state = AgentState(max_steps=10)
    agent.window_manager = SlidingWindowManager(window_size=3, max_tokens=8000)
    agent.memory_cleaner = MemoryCleaner()
    
    log.info(f"🔧 CodeAgent code_block_tags: {agent.code_block_tags}")
    log.info(f"🔧 CodeAgent attend le format: {agent.code_block_tags[0]}...{agent.code_block_tags[1]}")
    log.info(f"📦 Context management initialized with window_size=3, max_tokens=8000")
    
    return agent
```

### 2.3 Modifier la Fonction run_monitoring_cycle()

**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Lignes**: 1212-1323  
**Action**: Intégrer la gestion du contexte dans [`run_monitoring_cycle()`](oil_agent.py:1212)

```python
# === ANCIEN CODE (Lignes 1212-1237) ===
def run_monitoring_cycle():
    """Lance un cycle de surveillance avec DSPy pour la synthèse finale."""
    log.info("=" * 60)
    log.info("🛢️  Démarrage cycle de surveillance pétrole (DSPy Mode)")
    log.info("=" * 60)

    # 0. Démarrer automatiquement llama-server si nécessaire
    if not start_llama_server():
        log.error("❌ Impossible de démarrer llama-server. Abandon.")
        return

    # 1. Configuration DSPy
    configure_dspy()
    
    seen_events = load_seen_events()
    agent = build_agent()

    # 2. Collecte d'intelligence via smolagents
    try:
        prompt = get_master_prompt()
        raw_intelligence = agent.run(prompt)
        log.info(f"🔍 Intelligence récoltée ({len(raw_intelligence)} caractères)")
    except Exception as e:
        log.error(f"Agent error: {e}")
        return

# === NOUVEAU CODE (Remplacement) ===
def run_monitoring_cycle():
    """Lance un cycle de surveillance avec DSPy et gestion de contexte optimisée."""
    log.info("=" * 60)
    log.info("🛢️  Démarrage cycle de surveillance pétrole (DSPy + Context Optimization)")
    log.info("=" * 60)

    # 0. Démarrer automatiquement llama-server si nécessaire
    if not start_llama_server():
        log.error("❌ Impossible de démarrer llama-server. Abandon.")
        return

    # 1. Configuration DSPy
    configure_dspy()
    
    seen_events = load_seen_events()
    agent = build_agent()

    # 2. Collecte d'intelligence via smolagents avec contexte optimisé
    try:
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Construire le prompt avec contexte optimisé
        prompt = build_optimized_prompt_context(
            agent.state,
            agent.window_manager,
            current_date,
            current_datetime
        )
        
        # Ajouter les instructions de la tâche
        prompt += "\n\n" + get_master_prompt()
        
        raw_intelligence = agent.run(prompt)
        log.info(f"🔍 Intelligence récoltée ({len(raw_intelligence)} caractères)")
        
        # Mettre à jour les statistiques de l'agent
        agent.state.total_tokens_input += estimate_tokens(prompt)
        agent.state.total_tokens_output += estimate_tokens(raw_intelligence)
        
        log.info(f"📊 Token usage: {agent.state.total_tokens_input:,} in → {agent.state.total_tokens_output:,} out")
    except Exception as e:
        log.error(f"Agent error: {e}")
        return
```

### 2.4 Ajouter une Fonction d'Estimation de Tokens

**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Ligne**: 417 (avant la configuration du logging)

```python
# === AJOUTER AVANT LA LIGNE 417 ===
def estimate_tokens(text: str) -> int:
    """
    Estime le nombre de tokens dans un texte.
    Approximation: 4 caractères ≈ 1 token pour l'anglais.
    """
    return len(text) // 4
```

---

## 3. MODIFICATIONS AVANCÉES (Phase 3)

### 3.1 Créer le Fichier context_management.py

**Fichier**: `context_management.py` (nouveau fichier)  
**Contenu**: Voir le document complet dans [`plans/context_management.py`](plans/context_management.py)

**Note**: Ce fichier contient toutes les classes de gestion du contexte:
- [`HistoryCompressor`](context_management.py:18)
- [`SlidingWindowManager`](context_management.py:208)
- [`MemoryCleaner`](context_management.py:257)
- [`AgentState`](context_management.py:318)
- [`build_optimized_prompt_context()`](context_management.py:437)

### 3.2 Optimiser les Résultats de Tools

**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Action**: Modifier chaque tool pour retourner des résultats condensés

#### Exemple: IranConflictTool.forward() (Lignes 559-585)

```python
# === ANCIEN CODE (Lignes 559-585) ===
def forward(self, days_back: int = 1) -> str:
    from datetime import datetime, timedelta
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_start = datetime.now() - timedelta(days=days_back)
    date_str = date_start.strftime("%Y-%m-%d")
    
    queries = [
        f"Iran military attack oil infrastructure {current_date} today breaking",
        f"Strait of Hormuz blockade tanker {current_date} just in",
        f"Iran IRGC oil tanker seized {current_date} recent",
        f"Iran Israel strike retaliation oil {current_date} breaking news",
        f"Iran US sanctions oil export disruption {current_date}",
    ]
    results = []
    for q in queries:
        try:
            r = self._search(q)
            if r and len(r) > 50:
                results.append(f"[Query: {q}]\n{r[:600]}")
        except Exception as e:
            results.append(f"[Query: {q}] Error: {e}")
    
    header = "=== IRAN CONFLICT SEARCH ===\n"
    header += f"Current Date: {current_date} | Searching since: {date_str}\n\n"
    
    return header + "\n\n---\n\n".join(results) if results else "No relevant results found."

# === NOUVEAU CODE (Remplacement) ===
def forward(self, days_back: int = 1) -> str:
    from datetime import datetime, timedelta
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_start = datetime.now() - timedelta(days=days_back)
    date_str = date_start.strftime("%Y-%m-%d")
    
    queries = [
        f"Iran military attack oil infrastructure {current_date} today breaking",
        f"Strait of Hormuz blockade tanker {current_date} just in",
        f"Iran IRGC oil tanker seized {current_date} recent",
        f"Iran Israel strike retaliation oil {current_date} breaking news",
        f"Iran US sanctions oil export disruption {current_date}",
    ]
    
    results = []
    events_found = []
    
    for q in queries:
        try:
            r = self._search(q)
            if r and len(r) > 50:
                # Extraire uniquement les événements pertinents
                event_snippets = self._extract_events(r)
                events_found.extend(event_snippets)
                results.append(f"[Query: {q}]\n{r[:300]}")  # Réduit de 600 à 300
        except Exception as e:
            results.append(f"[Query: {q}] Error: {e}")
    
    header = "=== IRAN CONFLICT SEARCH ===\n"
    header += f"Date: {current_date} | Events found: {len(events_found)}\n\n"
    
    # Ajouter un résumé des événements trouvés
    if events_found:
        header += "Key Events:\n"
        for event in events_found[:5]:  # Max 5 événements
            header += f"  - {event}\n"
        header += "\n"
    
    return header + "\n\n---\n\n".join(results) if results else "No relevant results found."

def _extract_events(self, text: str) -> List[str]:
    """Extrait les événements pertinents d'un texte."""
    import re
    events = []
    
    # Chercher des patterns d'événements
    patterns = [
        r'(?:Iran|IRGC|Hormuz).{0,100}(?:attack|tension|seizure|blockade)',
        r'(?:tanker|ship).{0,100}(?:seized|attacked|blocked)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches[:3]:  # Max 3 matches par pattern
            if len(match) > 20 and match not in events:
                events.append(match[:100])  # Tronquer à 100 caractères
    
    return events[:5]  # Max 5 événements au total
```

---

## 4. CONFIGURATION ADDITIONNELLE

### 4.1 Ajouter des Paramètres de Configuration

**Fichier**: [`config.json`](config.json)  
**Action**: Ajouter une section `context_optimization`

```json
{
  "model": {
    "name": "qwen3.5-9b",
    "path": "C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
    "api_base": "http://127.0.0.1:8080",
    "num_ctx": 65536,
    "provider": "llama.cpp"
  },
  "llama_server": {
    "executable": "llama-server",
    "n_gpu_layers": -1,
    "n_threads": 0,
    "ctx_size": 65536,
    "batch_size": 512,
    "ubatch_size": 128,
    "cache_type_k": "f16",
    "cache_type_v": "f16",
    "host": "0.0.0.0",
    "port": 8080
  },
  "email": {
    "smtp_host": "localhost",
    "smtp_port": 25,
    "email_from": "oil-monitor@localhost",
    "email_to": "admin@example.com",
    "email_subject_prefix": "[OIL-ALERT]",
    "send_emails": false
  },
  "persistence": {
    "history_file": "logs/email_history.json",
    "events_db": "logs/events_seen.json",
    "dataset_file": "data/oil_intelligence_dataset.jsonl"
  },
  "monitoring": {
    "alert_threshold": 6,
    "news_sources": [
      "reuters.com",
      "bloomberg.com",
      "apnews.com",
      "bbc.com",
      "ft.com",
      "wsj.com"
    ],
    "timezone": "Europe/Paris",
    "recent_news_hours": 24
  },
  "context_optimization": {
    "enabled": true,
    "window_size": 3,
    "max_history_tokens": 8000,
    "compression_ratio": 0.15,
    "enable_tool_caching": true,
    "enable_deduplication": true,
    "log_token_usage": true
  }
}
```

### 4.2 Charger la Configuration d'Optimisation

**Fichier**: [`oil_agent.py`](oil_agent.py)  
**Action**: Ajouter une classe de configuration pour l'optimisation

```python
# === AJOUTER APRÈS LA LIGNE 229 (après MonitoringConfig) ===
class ContextOptimizationConfig(BaseModel):
    """Configuration de l'optimisation contextuelle."""
    enabled: bool = Field(default=True, description="Activer l'optimisation contextuelle")
    window_size: int = Field(default=3, ge=1, le=10, description="Taille de la fenêtre glissante")
    max_history_tokens: int = Field(default=8000, gt=0, description="Tokens max pour l'historique compressé")
    compression_ratio: float = Field(default=0.15, ge=0.1, le=0.5, description="Ratio de compression cible")
    enable_tool_caching: bool = Field(default=True, description="Activer le cache des tools")
    enable_deduplication: bool = Field(default=True, description="Activer la déduplication")
    log_token_usage: bool = Field(default=True, description="Logger l'utilisation des tokens")

# === MODIFIER LA CLASSE Config (Ligne 223) ===
class Config(BaseModel):
    """Configuration principale."""
    model: ModelConfig
    llama_server: LlamaServerConfig
    email: EmailConfig
    persistence: PersistenceConfig
    monitoring: MonitoringConfig
    context_optimization: ContextOptimizationConfig = Field(default_factory=ContextOptimizationConfig)
```

---

## 5. TESTING ET VALIDATION

### 5.1 Script de Test

**Fichier**: `test_optimization.py` (nouveau fichier)

```python
"""
Script de test pour valider les optimisations contextuelles.
"""

import logging
from datetime import datetime
from oil_agent import build_agent, get_master_prompt, estimate_tokens

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def test_prompt_optimization():
    """Teste l'optimisation des prompts."""
    log.info("=" * 60)
    log.info("TEST 1: Optimisation des Prompts")
    log.info("=" * 60)
    
    # Test du prompt principal
    prompt = get_master_prompt()
    prompt_tokens = estimate_tokens(prompt)
    
    log.info(f"Prompt principal: {prompt_tokens:,} tokens")
    log.info(f"Objectif: < 500 tokens")
    log.info(f"Résultat: {'✅ PASS' if prompt_tokens < 500 else '❌ FAIL'}")
    
    return prompt_tokens < 500

def test_context_management():
    """Teste la gestion du contexte."""
    log.info("=" * 60)
    log.info("TEST 2: Gestion du Contexte")
    log.info("=" * 60)
    
    try:
        agent = build_agent()
        
        # Vérifier que l'agent a les attributs de gestion de contexte
        has_state = hasattr(agent, 'state')
        has_window_manager = hasattr(agent, 'window_manager')
        has_memory_cleaner = hasattr(agent, 'memory_cleaner')
        
        log.info(f"Agent state: {'✅' if has_state else '❌'}")
        log.info(f"Window manager: {'✅' if has_window_manager else '❌'}")
        log.info(f"Memory cleaner: {'✅' if has_memory_cleaner else '❌'}")
        
        return has_state and has_window_manager and has_memory_cleaner
    except Exception as e:
        log.error(f"Erreur lors du test: {e}")
        return False

def test_token_estimation():
    """Teste l'estimation des tokens."""
    log.info("=" * 60)
    log.info("TEST 3: Estimation des Tokens")
    log.info("=" * 60)
    
    test_texts = [
        "Short text.",
        "This is a longer text that should contain approximately 50 tokens when tokenized by a modern language model.",
        "A" * 1000,  # 1000 characters
    ]
    
    for text in test_texts:
        tokens = estimate_tokens(text)
        log.info(f"Text length: {len(text)} chars → Estimated tokens: {tokens:,}")
    
    return True

def main():
    """Exécute tous les tests."""
    log.info("🧪 Démarrage des tests d'optimisation")
    
    tests = [
        ("Optimisation des Prompts", test_prompt_optimization),
        ("Gestion du Contexte", test_context_management),
        ("Estimation des Tokens", test_token_estimation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            log.error(f"Erreur dans le test '{name}': {e}")
            results.append((name, False))
    
    # Résumé
    log.info("=" * 60)
    log.info("RÉSUMÉ DES TESTS")
    log.info("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        log.info(f"{name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    log.info(f"\nTotal: {passed}/{total} tests passés")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
```

---

## 6. RÉSUMÉ DES MODIFICATIONS

### Modifications par Fichier

| Fichier | Modifications | Lignes | Priorité |
|---------|--------------|---------|----------|
| [`oil_agent.py`](oil_agent.py) | Optimiser `get_master_prompt()` | 1146-1182 | Haute |
| [`oil_agent.py`](oil_agent.py) | Condenser descriptions de tools (11 tools) | 540, 590, 652, etc. | Haute |
| [`oil_agent.py`](oil_agent.py) | Simplifier `OilEventSignature` | 60-76 | Haute |
| [`oil_agent.py`](oil_agent.py) | Ajouter imports gestion contexte | 34 | Haute |
| [`oil_agent.py`](oil_agent.py) | Modifier `build_agent()` | 1090-1139 | Moyenne |
| [`oil_agent.py`](oil_agent.py) | Modifier `run_monitoring_cycle()` | 1212-1237 | Moyenne |
| [`oil_agent.py`](oil_agent.py) | Ajouter `estimate_tokens()` | 417 | Moyenne |
| [`context_management.py`](context_management.py) | Nouveau fichier complet | - | Moyenne |
| [`config.json`](config.json) | Ajouter `context_optimization` | - | Basse |
| `test_optimization.py` | Nouveau fichier de test | - | Basse |

### Gains Estimés

| Phase | Modifications | Gain par étape | Gain à l'étape 10 |
|-------|--------------|----------------|-------------------|
| 1 | Prompts optimisés | ~6,420 tokens | ~6,420 tokens |
| 2 | Gestion historique | ~30,000 tokens | ~50,000 tokens |
| 3 | Optimisations avancées | ~6,000 tokens | ~6,000 tokens |
| **TOTAL** | **Toutes phases** | **~42,420 tokens** | **~62,420 tokens** |

---

## 7. ORDRE D'IMPLÉMENTATION RECOMMANDÉ

### Jour 1 (Immédiat)
1. ✅ Optimiser [`get_master_prompt()`](oil_agent.py:1146)
2. ✅ Condenser descriptions de tools (11 tools)
3. ✅ Simplifier [`OilEventSignature`](oil_agent.py:60)
4. ✅ Ajouter `estimate_tokens()`

### Semaine 1 (Court terme)
5. ✅ Créer [`context_management.py`](context_management.py)
6. ✅ Ajouter imports dans [`oil_agent.py`](oil_agent.py)
7. ✅ Modifier [`build_agent()`](oil_agent.py:1090)
8. ✅ Modifier [`run_monitoring_cycle()`](oil_agent.py:1212)
9. ✅ Créer [`test_optimization.py`](test_optimization.py)
10. ✅ Exécuter les tests

### Mois 1 (Moyen terme)
11. ✅ Ajouter configuration `context_optimization` dans [`config.json`](config.json)
12. ✅ Optimiser les résultats de tools
13. ✅ Implémenter le cache de tools
14. ✅ Surveiller les métriques de tokens
15. ✅ Ajuster les paramètres selon les résultats

---

## 8. NOTES IMPORTANTES

### Risques et Atténuations

1. **Risque**: Perte de qualité due à la compression
   - **Atténuation**: Tests approfondis et surveillance continue

2. **Risque**: Complexité accrue du code
   - **Atténuation**: Documentation complète et tests unitaires

3. **Risque**: Dépendances supplémentaires
   - **Atténuation**: Utiliser uniquement les bibliothèques existantes

### Surveillance Continue

Après implémentation, surveiller:
- Nombre de tokens par étape
- Ratio output/input
- Qualité des événements détectés
- Taux de compression
- Performance globale

### Rollback

Si nécessaire, rollback possible en:
- Désactivant l'optimisation dans [`config.json`](config.json)
- Restaurant les anciennes versions des fonctions
- Utilisant le système sans gestion de contexte
