# 🚀 Skill : Utilisation directe des Tools Python pour accélération

## 📋 Description

Ce skill explique comment utiliser les outils Python du projet **oil-agent** directement, sans passer par l'agent complet smolagents. Cela permet d'accélérer considérablement l'exécution en évitant les étapes intermédiaires de l'agent.

---

## 🎯 Pourquoi utiliser les outils directement ?

### Avantages :
- **⚡ Plus rapide** : Pas d'analyse par l'agent, exécution directe
- **💰 Moins coûteux** : Moins d'appels au LLM (llama-server)
- **🎯 Plus précis** : Contrôle total sur les paramètres
- **🔧 Plus flexible** : Peut être intégré dans d'autres scripts
- **📊 Plus flexible** : Peut être intégré dans d'autres scripts d'automatisation
- **🎨 Compatible avec llama-server** : Fonctionne avec l'infrastructure de migration

---

## 🛠️ Initialisation des outils

### Prérequis
```python
# Assurez-vous que les dépendances sont installées
# uv sync (voir README.md)
```

### Code d'initialisation
```python
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from oil_agent import (
    IranConflictTool,
    RefineryDamageTool,
    OPECSupplyTool,
    NaturalGasDisruptionTool,
    ShippingDisruptionTool,
    GeopoliticalEscalationTool,
    OilPriceTool,
    RecentNewsTool,
    RSSFeedTool,
    VIXTool,
)

# Initialisation des outils de base
ddg = DuckDuckGoSearchTool(max_results=5)
visit = VisitWebpageTool(max_output_length=4000)

# Initialisation des outils personnalisés
iran_tool = IranConflictTool(ddg)
refinery_tool = RefineryDamageTool(ddg, visit)
opec_tool = OPECSupplyTool(ddg)
gas_tool = NaturalGasDisruptionTool(ddg)
shipping_tool = ShippingDisruptionTool(ddg)
geo_tool = GeopoliticalEscalationTool(ddg)
price_tool = OilPriceTool(ddg)
news_tool = RecentNewsTool(ddg)
rss_tool = RSSFeedTool()
vix_tool = VIXTool(ddg)
```

---

## 📚 Utilisation des outils

### 1. IranConflictTool - Conflits Iran / Ormuz

**Description** : Recherche les actualités sur les conflits militaires iraniens, les tensions dans le détroit d'Ormuz, les actions du IRGC.

```python
# Recherche des conflits des dernières 24 heures
result = iran_tool.forward(days_back=1)
print(result)

# Recherche des 3 derniers jours
result = iran_tool.forward(days_back=3)
print(result)
```

**Paramètres** :
- `days_back` (int, optionnel) : Nombre de jours à rechercher (défaut: 1)

---

### 2. RefineryDamageTool - Dommages aux raffineries

**Description** : Recherche les actualités sur les dommages aux raffineries, incendies, explosions, attaques de drones.

```python
# Recherche globale
result = refinery_tool.forward(region="global")
print(result)

# Recherche au Moyen-Orient
result = refinery_tool.forward(region="middle_east")
print(result)

# Recherche en Russie
result = refinery_tool.forward(region="russia")
print(result)

# Recherche en Irak
result = refinery_tool.forward(region="iraq")
print(result)
```

**Paramètres** :
- `region` (str, optionnel) : 'global', 'middle_east', 'russia', 'iraq' (défaut: 'global')

---

### 3. OPECSupplyTool - Décisions OPEC+

**Description** : Recherche les décisions de production OPEC+, coupes de production, réunions d'urgence.

```python
# Recherche toutes les actualités OPEC+
result = opec_tool.forward(focus="all")
print(result)

# Recherche des réunions OPEC
result = opec_tool.forward(focus="opec_meeting")
print(result)

# Recherche des coupes de production
result = opec_tool.forward(focus="production_cut")
print(result)
```

**Paramètres** :
- `focus` (str, optionnel) : 'opec_meeting', 'production_cut', 'all' (défaut: 'all')

---

### 4. NaturalGasDisruptionTool - Perturbations gaz naturel

**Description** : Recherche les perturbations de l'approvisionnement en gaz naturel, sabotages de pipelines, terminaux LNG.

```python
# Recherche toutes les perturbations
result = gas_tool.forward(topic="all")
print(result)

# Recherche des pipelines
result = gas_tool.forward(topic="pipeline")
print(result)

# Recherche des terminaux LNG
result = gas_tool.forward(topic="lng")
print(result)

# Recherche des coupures russes
result = gas_tool.forward(topic="russia_gas")
print(result)
```

**Paramètres** :
- `topic` (str, optionnel) : 'pipeline', 'lng', 'russia_gas', 'all' (défaut: 'all')

---

### 5. ShippingDisruptionTool - Perturbations maritimes

**Description** : Recherche les perturbations maritimes : attaques Houthis, tensions Bab-el-Mandeb, blocage canal de Suez.

```python
# Recherche des perturbations maritimes
result = shipping_tool.forward()
print(result)
```

**Paramètres** :
- Aucun

---

### 6. GeopoliticalEscalationTool - Escalades géopolitiques

**Description** : Recherche les escalades géopolitiques pouvant faire augmenter les prix du pétrole.

```python
# Recherche des escalades géopolitiques
result = geo_tool.forward()
print(result)
```

**Paramètres** :
- Aucun

---

### 7. OilPriceTool - Prix actuels Brent / WTI

**Description** : Récupère les prix actuels du pétrole Brent et WTI, les mouvements récents et les prévisions des analystes.

```python
# Récupération des prix actuels
result = price_tool.forward()
print(result)
```

**Paramètres** :
- Aucun

---

### 8. RecentNewsTool - Actualités très récentes ⚡

**Description** : Recherche les actualités très récentes sur le pétrole depuis les sources majeures (Reuters, Bloomberg, AP, BBC, FT, WSJ). Filtre les résultats par date (dernières 24h, 48h, ou 7 jours) et priorise les breaking news et developing stories.

```python
# Recherche des actualités des dernières 24h
result = news_tool.forward(topic="all", timeframe="24h")
print(result)

# Recherche des actualités sur l'Iran des 48 dernières heures
result = news_tool.forward(topic="iran", timeframe="48h")
print(result)

# Recherche des actualités sur les raffineries des 7 derniers jours
result = news_tool.forward(topic="refinery", timeframe="7d")
print(result)
```

**Paramètres** :
- `topic` (str, optionnel) : 'iran', 'refinery', 'opec', 'gas', 'shipping', 'geopolitical', 'all' (défaut: 'all')
- `timeframe` (str, optionnel) : '24h', '48h', '7d' (défaut: '24h')

**Topics disponibles** :
- `iran` : Conflits Iran, Ormuz, IRGC
- `refinery` : Raffineries, incendies, attaques
- `opec` : OPEC+, coupes de production
- `gas` : Gaz naturel, pipelines, LNG
- `shipping` : Perturbations maritimes, Houthis
- `geopolitical` : Escalades géopolitiques
- `all` : Toutes les actualités pétrolières

---

### 9. RSSFeedTool - Flux RSS en temps réel ⚡

**Description** : Lit les flux RSS des sources d'actualités majeures pour obtenir des informations en temps réel.

```python
# Lecture de tous les flux RSS des dernières 24h
result = rss_tool.forward(feed="all", hours_back=24)
print(result)

# Lecture du flux Reuters Energy des 12 dernières heures
result = rss_tool.forward(feed="reuters_energy", hours_back=12)
print(result)

# Lecture du flux Bloomberg Energy des 6 dernières heures
result = rss_tool.forward(feed="bloomberg_energy", hours_back=6)
print(result)

# Lecture du flux AP Business des 3 dernières heures
result = rss_tool.forward(feed="ap_business", hours_back=3)
print(result)

# Lecture du flux BBC Business des dernières 48h
result = rss_tool.forward(feed="bbc_business", hours_back=48)
print(result)
```

**Paramètres** :
- `feed` (str, optionnel) : 'reuters_energy', 'bloomberg_energy', 'ap_business', 'bbc_business', 'all' (défaut: 'all')
- `hours_back` (int, optionnel) : Nombre d'heures en arrière pour filtrer (défaut: 24)

**Flux disponibles** :
- `reuters_energy` : Reuters Business News
- `bloomberg_energy` : Bloomberg Markets News
- `ap_business` : AP Business News
- `bbc_business` : BBC Business News

---

### 10. VIXTool - Indice de volatilité VIX ⚡

**Description** : Récupère l'indice VIX (CBOE Volatility Index), un indicateur clé de la peur du marché.

```python
# Récupération de la valeur actuelle du VIX
result = vix_tool.forward()
print(result)
```

**Paramètres** :
- Aucun

---

## 🔄 Exemple d'utilisation complète

### Script de surveillance rapide
```python
#!/usr/bin/env python3
"""
Script de surveillance rapide utilisant les outils directement.
Plus rapide que l'agent complet pour des recherches ciblées.
"""

from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from oil_agent import (
    RecentNewsTool,
    RSSFeedTool,
    VIXTool,
    OilPriceTool,
)
from datetime import datetime
import json

# Initialisation des outils
ddg = DuckDuckGoSearchTool(max_results=5)
news_tool = RecentNewsTool(ddg)
rss_tool = RSSFeedTool()
vix_tool = VIXTool(ddg)
price_tool = OilPriceTool(ddg)

def quick_monitoring():
    """Surveillance rapide des événements à fort impact."""
    print(f"\n{'='*60}")
    print(f"🛢️ SURVEILLANCE RAPIDE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 1. Actualités très récentes (24h)
    print("📰 ACTUALITÉS RÉCENTES (24h)")
    print("-" * 60)
    recent_news = news_tool.forward(topic="all", timeframe="24h")
    print(recent_news)
    print()
    
    # 2. Flux RSS en temps réel
    print("📡 FLUX RSS (12h)")
    print("-" * 60)
    rss_feeds = rss_tool.forward(feed="all", hours_back=12)
    print(rss_feeds)
    print()
    
    # 3. Indice VIX
    print("📊 INDICE VIX (Volatilité)")
    print("-" * 60)
    vix = vix_tool.forward()
    print(vix)
    print()
    
    # 4. Prix du pétrole
    print("💰 PRIX DU PÉTROLE")
    print("-" * 60)
    prices = price_tool.forward()
    print(prices)
    print()
    
    print(f"{'='*60}")
    print("✅ Surveillance terminée")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    quick_monitoring()
```

### Script de surveillance ciblée
```python
#!/usr/bin/env python3
"""
Script de surveillance ciblée sur un sujet spécifique.
"""

from smolagents import DuckDuckGoSearchTool
from oil_agent import (
    IranConflictTool,
    RefineryDamageTool,
    OPECSupplyTool,
)

# Initialisation des outils
ddg = DuckDuckGoSearchTool(max_results=5)
iran_tool = IranConflictTool(ddg)
refinery_tool = RefineryDamageTool(ddg, None)
opec_tool = OPECSupplyTool(ddg)

def monitor_specific_topic(topic: str):
    """Surveillance ciblée sur un sujet."""
    print(f"\n🎯 SURVEILLANCE : {topic.upper()}")
    print(f"{'='*60}\n")
    
    if topic == "iran":
        result = iran_tool.forward(days_back=1)
        print(result)
    elif topic == "refinery":
        result = refinery_tool.forward(region="global")
        print(result)
    elif topic == "opec":
        result = opec_tool.forward(focus="all")
        print(result)
    else:
        print(f"❌ Topic inconnu: {topic}")
        return
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        monitor_specific_topic(topic)
    else:
        print("Usage: python monitor_targeted.py <topic>")
        print("Topics disponibles: iran, refinery, opec")
```

---

## 📊 Comparaison des performances

| Méthode | Temps d'exécution | Coût LLM | Flexibilité |
|---------|------------------|-------------|-------------|
| **Agent complet** | ~30-60s | Élevé (plusieurs appels) | Automatique |
| **Outils directs** | ~5-15s | Faible (0-1 appel) | Manuel mais précis |
| **Outils ciblés** | ~2-5s | Nul | Maximum contrôle |

---

## 💡 Bonnes pratiques

### 1. Utiliser les outils récents en priorité
Pour une surveillance en temps réel, privilégiez :
- [`RecentNewsTool`](oil_agent.py:526) avec `timeframe="24h"`
- [`RSSFeedTool`](oil_agent.py:642) avec `hours_back=12` ou moins
- [`VIXTool`](oil_agent.py:737) pour la volatilité

### 2. Combiner les outils intelligemment
```python
# Stratégie recommandée pour une surveillance rapide
# 1. Vérifier la volatilité (VIX)
vix = vix_tool.forward()

# 2. Si VIX élevé, chercher les actualités récentes
if "high" in vix.lower() or "spike" in vix.lower():
    news = news_tool.forward(topic="all", timeframe="24h")
    rss = rss_tool.forward(feed="all", hours_back=6)
```

### 3. Filtrer les résultats
```python
# Exemple de filtrage des résultats
def filter_high_impact_news(news_result: str, min_score: int = 7):
    """Filtrer les actualités à fort impact."""
    lines = news_result.split('\n')
    high_impact = []
    
    for line in lines:
        if 'impact' in line.lower() or 'urgent' in line.lower():
            if any(str(min_score) <= c <= '9' for c in line):
                high_impact.append(line)
    
    return '\n'.join(high_impact)
```

### 4. Logger les résultats
```python
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/quick_monitor.log", encoding="utf-8"),
    ],
)

def log_tool_result(tool_name: str, result: str):
    """Logger le résultat d'un outil."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{tool_name}] {timestamp}")
    logging.info(f"Result: {result[:500]}...")  # Log tronqué
```

---

## 🚀 Exécution rapide

### Lancer une surveillance rapide
```bash
# Activer l'environnement virtuel
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows

# Exécuter le script de surveillance rapide
python quick_monitor.py
```

### Lancer une surveillance ciblée
```bash
# Surveiller l'Iran
python monitor_targeted.py iran

# Surveiller les raffineries
python monitor_targeted.py refinery

# Surveiller l'OPEC
python monitor_targeted.py opec
```

---

## 📝 Résumé

Ce skill permet d'utiliser les outils Python du projet **oil-agent** directement pour :

1. **Accélérer l'exécution** : Éviter les étapes intermédiaires de l'agent
2. **Réduire les coûts** : Moins d'appels au LLM (llama-server)
3. **Avoir un contrôle total** : Choisir exactement quels outils utiliser et comment
4. **Intégrer facilement** : Utiliser les outils dans d'autres scripts d'automatisation
5. **Surveiller en temps réel** : Utiliser les outils **RecentNewsTool**, **RSSFeedTool** et **VIXTool** avec des paramètres de temps courts (24h, 12h, 6h)

Pour une surveillance automatisée complète avec envoi d'emails, utilisez l'agent complet via `python oil_agent.py`.

---

## 🔗 Liens utiles

- [`oil_agent.py`](oil_agent.py) : Code principal avec tous les outils
- [`README.md`](README.md) : Documentation complète du projet
- [`pyproject.toml`](pyproject.toml) : Dépendances du projet
- [`config.json`](config.json) : Configuration du projet (llama-server, modèle, email, etc.)

---

**Note** : Ce skill est optimisé pour une utilisation directe des outils. Pour une surveillance automatisée complète avec envoi d'emails, utilisez l'agent complet via `python oil_agent.py`.
