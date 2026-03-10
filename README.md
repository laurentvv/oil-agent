# 🛢️ Oil Market Monitoring Agent

Agent de surveillance du marché pétrolier basé sur **smolagents 1.24.0** + **LiteLLM** + **Ollama (qwen2.5:7b)**.

Surveille en continu les événements géopolitiques et industriels pouvant faire rebondir le cours du pétrole (Brent/WTI) et envoie des **alertes email** via relais **Postfix local** pour chaque nouvel événement à fort impact.

**Nouveauté** : L'agent utilise maintenant des informations très récentes (date du jour) avec des filtres temporels, des flux RSS en temps réel, et l'indice VIX pour une meilleure réactivité.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    oil_agent.py                          │
│                                                          │
│  CodeAgent (smolagents 1.24.0)                          │
│  └── LiteLLMModel → ollama_chat/qwen3.5:9b               │
│                                                          │
│  Tools :                                                 │
│  ├── IranConflictTool        (conflit Iran / Ormuz)      │
│  ├── RefineryDamageTool      (raffineries attaquées)     │
│  ├── OPECSupplyTool          (coupes production OPEC+)   │
│  ├── NaturalGasDisruptionTool (pipelines / LNG)          │
│  ├── ShippingDisruptionTool  (Houthis / mer Rouge)       │
│  ├── GeopoliticalEscalationTool (Russie / Libye / etc.)  │
│  ├── OilPriceTool            (prix Brent / WTI actuels)  │
│  ├── RecentNewsTool          (actualités très récentes) 🆕 │
│  ├── RSSFeedTool            (flux RSS temps réel) 🆕      │
│  ├── VIXTool                (indice de volatilité) 🆕       │
│  ├── DuckDuckGoSearchTool    (recherche web DDG)         │
│  └── VisitWebpageTool        (lecture pages web)         │
│                                                          │
│  Persistance :                                           │
│  ├── logs/events_seen.json   (événements déjà vus)       │
│  ├── logs/email_history.json (historique emails envoyés) │
│  └── logs/oil_monitor.log    (logs d'exécution)          │
└─────────────────────────────────────────────────────────┘
         │
         ▼ (alerte si Impact Score ≥ 6)
┌─────────────────────┐
│  Postfix SMTP :25   │ → email HTML + texte brut
└─────────────────────┘
```

---

## Prérequis

### 1. Ollama installé et en cours d'exécution
```bash
# Installation Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Télécharger le modèle
ollama pull qwen2.5:7b

# Vérifier que le serveur tourne
curl http://localhost:11434/api/tags
```

### 2. Python 3.10+
```bash
python3 --version
```

### 3. Postfix configuré comme relais local
```bash
# AlmaLinux / RHEL
dnf install postfix -y
systemctl enable --now postfix

# Vérifier
echo "Test" | mail -s "Test" admin@example.com
```

---

## Installation

```bash
git clone <repo>
cd oil_monitor

# Installer uv (si pas déjà installé)
# Sur Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Sur Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Synchroniser les dépendances avec uv (crée automatiquement .venv)
uv sync

# Activer l'environnement virtuel
# Sur Linux/macOS:
source .venv/bin/activate
# Sur Windows:
.venv\Scripts\activate
```

---

## Configuration

Éditer le bloc `CONFIG` dans `oil-agent.py` :

```python
CONFIG = {
    # Modèle Ollama (qwen2.5:7b recommandé, ou llama3.1:8b)
    "ollama_model": "ollama_chat/qwen3.5:9b",
    "ollama_api_base": "http://127.0.0.1:11434",  # Adapter si Ollama distant
    "ollama_num_ctx": 8192,

    # Email (OBLIGATOIRE à modifier)
    "smtp_host": "localhost",
    "smtp_port": 25,
    "email_from": "oil-monitor@localhost",
    "email_to": "admin@example.com",       # ← Votre adresse
    "send_emails": False,                 # False pour désactiver l'envoi d'emails (simulation uniquement)

    # Seuil d'alerte (0–10). 6 = impact significatif
    "alert_threshold": 6,

    # Sources d'actualités prioritaires 🆕
    "news_sources": [
        "reuters.com",
        "bloomberg.com",
        "apnews.com",
        "bbc.com",
        "ft.com",
        "wsj.com",
    ],

    # Fuseau horaire pour les dates 🆕
    "timezone": "Europe/Paris",

    # Délai maximal pour considérer une actualité comme "récente" (heures) 🆕
    "recent_news_hours": 24,
}
```

---

## Utilisation

### Lancement manuel
```bash
# Activer l'environnement virtuel (si pas déjà activé)
# Sur Linux/macOS:
source .venv/bin/activate
# Sur Windows:
.venv\Scripts\activate

# Lancer l'agent
python oil-agent.py
```

### Afficher l'historique des emails envoyés
```bash
python oil-agent.py history
```

### Via le script wrapper
```bash
chmod +x run.sh
./run.sh
```

Note: Le script wrapper doit pointer vers `.venv/bin/python` et `oil-agent.py`.

### Automatisation avec cron (toutes les heures)
```bash
crontab -e
```
Ajouter :
```cron
0 * * * * /chemin/complet/vers/oil_monitor/run.sh
```

Ou exécuter directement avec uv :
```cron
0 * * * * cd /chemin/complet/vers/oil_monitor && /chemin/vers/uv run python oil-agent.py
```

### Service systemd (recommandé)
```bash
sudo tee /etc/systemd/system/oil-monitor.service << 'EOF'
[Unit]
Description=Oil Market Monitoring Agent
After=network.target

[Service]
Type=oneshot
User=youruser
WorkingDirectory=/chemin/vers/oil_monitor
ExecStart=/chemin/vers/uv run python oil-agent.py
StandardOutput=append:/chemin/vers/oil_monitor/logs/oil_monitor.log
StandardError=append:/chemin/vers/oil_monitor/logs/oil_monitor.log
EOF

sudo tee /etc/systemd/system/oil-monitor.timer << 'EOF'
[Unit]
Description=Oil Monitor - run every hour

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now oil-monitor.timer

# Vérifier
sudo systemctl status oil-monitor.timer
sudo systemctl list-timers oil-monitor.timer
```

---

## Exemple d'email reçu

```
Sujet: [OIL-ALERT] Iran | Score 9/10 — Iranian drones strike Saudi Aramco Abqaiq facility

🛢️  OIL MARKET ALERT
==================================================

📌 TITRE       : Iranian drones strike Saudi Aramco Abqaiq facility
📂 CATÉGORIE   : Iran
⚡ SCORE IMPACT: 9/10
🔔 URGENCE     : Breaking
💰 IMPACT PRIX : +$8-12/barrel expected

📝 ANALYSE :
Drone strikes attributed to Iranian-backed forces hit the Abqaiq processing 
facility, responsible for ~7% of global oil supply. Temporary shutdown of 
1.5 Mb/d expected. Saudi Aramco confirms force majeure on some contracts.

🔗 SOURCE : Reuters Breaking News, Bloomberg Energy

──────────────────────────────────────────────────
⏰ Généré le : 2025-03-10 14:32:07
🤖 Agent : smolagents 1.24.0 + Ollama qwen2.5:7b
```

---

## Fichiers de persistance

| Fichier | Description |
|---------|-------------|
| `logs/events_seen.json` | Hash MD5 des événements déjà traités (anti-doublon) |
| `logs/email_history.json` | Historique complet des emails envoyés (timestamp, sujet, aperçu) |
| `logs/oil_monitor.log` | Logs détaillés des cycles d'exécution |
| `logs/scheduler.log` | Logs du script wrapper bash |
| `pyproject.toml` | Configuration du projet et dépendances |
| `.venv/` | Environnement virtuel créé par uv |

---

## Catégories surveillées

| Tool | Catégorie | Signaux recherchés |
|------|-----------|-------------------|
| `IranConflictTool` | Iran | IRGC, Ormuz, attaques, sanctions |
| `RefineryDamageTool` | Raffineries | Explosions, drones, incendies |
| `OPECSupplyTool` | OPEC+ | Coupes production, réunions d'urgence |
| `NaturalGasDisruptionTool` | Gaz | Pipelines, LNG, coupures russes |
| `ShippingDisruptionTool` | Maritime | Houthis, mer Rouge, saisies Iran |
| `GeopoliticalEscalationTool` | Géopolitique | Russie/Ukraine, Libye, Venezuela |
| `OilPriceTool` | Prix | Brent spot, WTI, prévisions analystes |
| `RecentNewsTool` 🆕 | Actualités récentes | Breaking news, dernières 24h/48h/7j |
| `RSSFeedTool` 🆕 | Flux RSS temps réel | Reuters, Bloomberg, AP, BBC |
| `VIXTool` 🆕 | Volatilité marché | Indice VIX, peur du marché |

---

## Dépendances

Les dépendances sont définies dans [`pyproject.toml`](pyproject.toml):

```toml
smolagents[litellm]
duckduckgo-search
ddgs
requests
beautifulsoup4
markdownify
feedparser  # 🆕 Pour les flux RSS
```

Pour installer les dépendances avec uv:
```bash
uv sync
```

Cette commande crée automatiquement l'environnement virtuel `.venv` et installe toutes les dépendances requises.

---

## Nouvelles fonctionnalités 🆕

### Informations très récentes

L'agent utilise maintenant la date du jour dynamiquement dans toutes les recherches et le prompt principal, ce qui permet de cibler les actualités les plus fraîches.

- **Date du jour injectée** : La date actuelle est automatiquement incluse dans toutes les requêtes de recherche
- **Filtres temporels** : Recherche avec des mots-clés comme "today", "breaking", "just in", "last 24 hours"
- **Priorisation des sources** : Recherche ciblée sur les sites d'actualités majeurs (Reuters, Bloomberg, AP, BBC, FT, WSJ)

### RecentNewsTool

Tool dédié à la recherche d'actualités très récentes avec filtrage par date.

**Paramètres** :
- `topic` : Sujet à rechercher ('iran', 'refinery', 'opec', 'gas', 'shipping', 'geopolitical', 'all')
- `timeframe` : Période temporelle ('24h', '48h', '7d')

**Exemple d'utilisation** :
```python
# Recherche d'actualités sur l'Iran des dernières 24h
agent.run("Use search_recent_news with topic='iran' and timeframe='24h'")
```

### RSSFeedTool

Tool pour lire les flux RSS en temps réel depuis les sources d'actualités majeures.

**Sources disponibles** :
- Reuters Energy
- Bloomberg Energy
- AP Business
- BBC Business

**Paramètres** :
- `feed` : Flux à lire ('reuters_energy', 'bloomberg_energy', 'ap_business', 'bbc_business', 'all')
- `hours_back` : Nombre d'heures en arrière pour filtrer les entrées (défaut: 24)

**Exemple d'utilisation** :
```python
# Lecture de tous les flux RSS des dernières 24h
agent.run("Use read_rss_feeds with feed='all' and hours_back=24")
```

### VIXTool

Tool pour récupérer l'indice VIX (CBOE Volatility Index), un indicateur clé de la peur du marché.

**Pourquoi le VIX ?**
- Le VIX mesure la volatilité attendue du marché
- Une hausse du VIX peut indiquer une augmentation de l'incertitude géopolitique
- Corrélation souvent observée entre le VIX et les mouvements du prix du pétrole

**Exemple d'utilisation** :
```python
# Récupération de la valeur actuelle du VIX
agent.run("Use get_vix_index to get current volatility levels")
```

### Améliorations des tools existants

Tous les tools existants ont été mis à jour avec :
- **Filtrage par date** : Inclusion de la date du jour dans toutes les requêtes
- **Mots-clés temporels** : Ajout de "today", "breaking", "just in", "recent"
- **En-têtes informatifs** : Affichage de la date actuelle et de la période de recherche

---
