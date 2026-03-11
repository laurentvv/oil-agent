"""
Oil Market Monitoring Agent
============================
smolagents 1.24.0 + LiteLLM + Ollama (qwen2.5:7b)
Surveille les événements géopolitiques et industriels pouvant faire rebondir le cours du pétrole.
Envoie des alertes email via relais SMTP (Postfix local).
"""

import os
import json
import smtplib
import hashlib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

from smolagents import (
    CodeAgent,
    LiteLLMModel,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
    Tool,
    tool,
)

import dspy
from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional

# ─────────────────────────────────────────────
# DSPy Configuration & Models
# ─────────────────────────────────────────────

# Modèle Pydantic pour la sortie structurée
class OilEvent(BaseModel):
    """Structure d'un événement pétrolier."""
    id: str = Field(..., description="ID unique (ex: iran_hormuz_20240311)")
    category: Literal["Iran", "Refinery", "OPEC", "Gas", "Shipping", "Geopolitical"]
    title: str
    impact_score: int = Field(..., ge=0, le=10)
    certainty_score: Optional[float] = Field(0.7, ge=0.0, le=1.0, description="Niveau de certitude (0.0-1.0)")
    urgency: Literal["Breaking", "Recent", "Developing", "Background"]
    summary: str
    price_impact: str = Field(..., description="Ex: +$2-4/barrel")
    source_hint: str
    publication_date: Optional[str] = Field(None, description="Date de publication si disponible")

class OilEventsResponse(BaseModel):
    """Structure de réponse avec la liste des événements."""
    events: List[OilEvent]
    confidence_score: float = Field(..., description="Score de confiance global (0.0-1.0)")

# Signature DSPy
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

# Module avec Chain of Thought
class OilEventAnalyzer(dspy.Module):
    """Analyseur d'événements pétroliers avec raisonnement explicite."""
    
    def __init__(self):
        super().__init__()
        self.analyze = dspy.ChainOfThought(OilEventSignature)

    def forward(self, **kwargs):
        # Utiliser dspy.Predict ou ChainOfThought
        return self.analyze(**kwargs)

def validate_and_fix_events(events: list, current_date: str) -> list:
    """Valide et nettoie les événements produits par le LLM."""
    valid_events = []
    for i, event in enumerate(events):
        try:
            # Transformation en dict si c'est un objet Pydantic
            e_dict = event if isinstance(event, dict) else (event.model_dump() if hasattr(event, 'model_dump') else {})
            
            # 1. Vérification des champs obligatoires minimums
            if not e_dict.get("title") or not e_dict.get("category"):
                log.warning(f"⚠️ Event {i} ignoré : titre ou catégorie manquant")
                continue
                
            # 2. Valeurs par défaut pour les champs optionnels manquants
            if "impact_score" not in e_dict: e_dict["impact_score"] = 5
            if "urgency" not in e_dict: e_dict["urgency"] = "Recent"
            if "summary" not in e_dict: e_dict["summary"] = "No summary provided."
            if "price_impact" not in e_dict: e_dict["price_impact"] = "Unknown"
            if "source_hint" not in e_dict: e_dict["source_hint"] = "Multiple sources"
            if "publication_date" not in e_dict or not e_dict["publication_date"]:
                e_dict["publication_date"] = current_date
            if "certainty_score" not in e_dict: e_dict["certainty_score"] = 0.7
            if "id" not in e_dict:
                e_dict["id"] = event_fingerprint(e_dict["title"], e_dict["category"])
                
            valid_events.append(e_dict)
        except Exception as ex:
            log.error(f"❌ Erreur lors de la validation de l'événement {i} : {ex}")
            
    return valid_events

# Configurer DSPy par défaut (sera mis à jour dans build_agent si nécessaire)
def configure_dspy():
    """Configure DSPy avec le modèle Ollama défini dans CONFIG."""
    lm = dspy.LM(CONFIG["ollama_model"], api_base=CONFIG["ollama_api_base"])
    dspy.configure(lm=lm, adapter=dspy.JSONAdapter())
    return lm

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
CONFIG = {
    # Ollama
    "ollama_model": "ollama_chat/qwen3.5:9b",
    "ollama_api_base": "http://127.0.0.1:11434",
    "ollama_num_ctx": 8192,
    # Email (relais Postfix local)
    "smtp_host": "localhost",
    "smtp_port": 25,
    "email_from": "oil-monitor@localhost",
    "email_to": "admin@example.com",       # ← Modifier ici
    "email_subject_prefix": "[OIL-ALERT]",
    "send_emails": False,                  # Désactiver l'envoi d'emails (True pour activer)
    # Fichiers de persistance
    "history_file": "logs/email_history.json",
    "events_db": "logs/events_seen.json",
    "dataset_file": "data/oil_intelligence_dataset.jsonl",
    # Seuil de score d'impact (0-10) pour déclencher une alerte
    "alert_threshold": 6,
    # Sources d'actualités prioritaires
    "news_sources": [
        "reuters.com",
        "bloomberg.com",
        "apnews.com",
        "bbc.com",
        "ft.com",
        "wsj.com",
    ],
    # Fuseau horaire pour les dates
    "timezone": "Europe/Paris",
    # Délai maximal pour considérer une actualité comme "récente" (heures)
    "recent_news_hours": 24,
}

# ─────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────
import sys
import io

# Configurer stdout pour utiliser UTF-8 sur Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/oil_monitor.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

Path("logs").mkdir(exist_ok=True)


# ─────────────────────────────────────────────
# Persistance : historique des événements vus
# ─────────────────────────────────────────────
def load_seen_events() -> set:
    p = Path(CONFIG["events_db"])
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_seen_events(seen: set):
    with open(CONFIG["events_db"], "w", encoding="utf-8") as f:
        json.dump(list(seen), f, indent=2)


def event_fingerprint(title: str, source: str) -> str:
    """Hash stable pour identifier un événement déjà traité."""
    raw = f"{title.lower().strip()}|{source.lower().strip()}"
    return hashlib.md5(raw.encode()).hexdigest()


# ─────────────────────────────────────────────
# Persistance : historique des emails envoyés
# ─────────────────────────────────────────────
def load_email_history() -> list:
    p = Path(CONFIG["history_file"])
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_email_history(history: list):
    with open(CONFIG["history_file"], "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def append_email_log(subject: str, body_preview: str, event_id: str):
    history = load_email_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "event_id": event_id,
        "subject": subject,
        "preview": body_preview[:300],
    })
    save_email_history(history)
    log.info(f"📧 Historique email mis à jour ({len(history)} entrées)")


# ─────────────────────────────────────────────
# Envoi email via Postfix local
# ─────────────────────────────────────────────
def send_alert_email(subject: str, body: str, event_id: str) -> bool:
    """Envoie une alerte email via relais SMTP Postfix."""
    full_subject = f"{CONFIG['email_subject_prefix']} {subject}"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = full_subject
    msg["From"] = CONFIG["email_from"]
    msg["To"] = CONFIG["email_to"]
    msg["X-OilMonitor-EventID"] = event_id

    # Corps texte brut
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Corps HTML enrichi
    html_body = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 700px; margin: auto;">
      <div style="background:#c0392b; color:white; padding:12px 20px; border-radius:6px 6px 0 0;">
        <h2 style="margin:0;">⚠️ {full_subject}</h2>
      </div>
      <div style="border:1px solid #ddd; padding:20px; border-radius:0 0 6px 6px;">
        <pre style="white-space:pre-wrap; font-family:Arial; font-size:14px;">{body}</pre>
        <hr/>
        <small style="color:#888;">
          Oil Monitor Agent • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} •
          Event ID: {event_id}
        </small>
      </div>
    </body></html>
    """
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    # Vérifier si l'envoi d'emails est désactivé
    if not CONFIG.get("send_emails", True):
        log.info(f"📧 Email désactivé (simulation) : {full_subject}")
        append_email_log(full_subject, body, event_id)
        return True

    try:
        with smtplib.SMTP(CONFIG["smtp_host"], CONFIG["smtp_port"], timeout=10) as smtp:
            smtp.sendmail(CONFIG["email_from"], [CONFIG["email_to"]], msg.as_string())
        log.info(f"✅ Email envoyé : {full_subject}")
        append_email_log(full_subject, body, event_id)
        return True
    except Exception as e:
        log.error(f"❌ Échec envoi email : {e}")
        return False


# ─────────────────────────────────────────────
# TOOLS personnalisés
# ─────────────────────────────────────────────

class IranConflictTool(Tool):
    """Tool : conflits Iran / Détroit d'Ormuz / IRGC"""
    name = "search_iran_conflict"
    description = (
        "Searches for recent news about Iran military conflicts, IRGC actions, "
        "Strait of Hormuz tensions, Iran-Israel escalation, or Iran sanctions "
        "that could disrupt oil supply. Returns a structured summary."
    )
    inputs = {
        "days_back": {
            "type": "integer",
            "description": "How many days back to search (default: 1)",
            "default": 1,
            "nullable": True,
        }
    }
    output_type = "string"

    def __init__(self, search_tool: DuckDuckGoSearchTool):
        super().__init__()
        self._search = search_tool

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
        
        header = f"=== IRAN CONFLICT SEARCH ===\n"
        header += f"Current Date: {current_date} | Searching since: {date_str}\n\n"
        
        return header + "\n\n---\n\n".join(results) if results else "No relevant results found."


class RefineryDamageTool(Tool):
    """Tool : dommages raffineries (attaques, accidents, incendies)"""
    name = "search_refinery_damage"
    description = (
        "Searches for news about oil refinery damage, fires, explosions, drone attacks "
        "on refineries worldwide (Saudi Arabia, Russia, Iraq, UAE, Kazakhstan). "
        "Returns structured results that can affect global oil supply."
    )
    inputs = {
        "region": {
            "type": "string",
            "description": "Region to focus on: 'global', 'middle_east', 'russia', 'iraq'. Default: 'global'",
            "default": "global",
            "nullable": True,
        }
    }
    output_type = "string"

    def __init__(self, search_tool: DuckDuckGoSearchTool, visit_tool: VisitWebpageTool):
        super().__init__()
        self._search = search_tool
        self._visit = visit_tool

    def forward(self, region: str = "global") -> str:
        from datetime import datetime
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        region_map = {
            "middle_east": [
                f"Saudi Aramco refinery attack {current_date} today breaking",
                f"Iraq oil refinery fire drone {current_date} just in",
            ],
            "russia": [
                f"Russia oil refinery drone attack Saratov {current_date} recent",
                f"Russian refinery fire Ukraine drone {current_date} breaking",
            ],
            "iraq": [
                f"Iraq Basra oil field attack {current_date} today",
                f"Iraq Kurdistan pipeline disruption {current_date} recent",
            ],
            "global": [
                f"oil refinery explosion fire {current_date} today breaking",
                f"refinery drone attack oil production disruption {current_date} just in",
                f"Saudi Arabia Aramco infrastructure attack {current_date} recent",
            ],
        }
        queries = region_map.get(region, region_map["global"])
        results = []
        for q in queries:
            try:
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[{q}]\n{r[:600]}")
            except Exception as e:
                results.append(f"[{q}] Error: {e}")
        
        header = f"=== REFINERY DAMAGE SEARCH ===\n"
        header += f"Region: {region} | Current Date: {current_date}\n\n"
        
        return header + "\n\n---\n\n".join(results) if results else "No refinery damage news found."


class OPECSupplyTool(Tool):
    """Tool : décisions OPEC+, coupes de production, quotas"""
    name = "search_opec_supply"
    description = (
        "Searches for OPEC+ production cuts, quota decisions, emergency meetings, "
        "and supply policy changes that could drive oil prices higher. "
        "Also covers Saudi Arabia, Russia, UAE unilateral cuts."
    )
    inputs = {
        "focus": {
            "type": "string",
            "description": "Focus area: 'opec_meeting', 'production_cut', 'all'. Default: 'all'",
            "default": "all",
            "nullable": True,
        }
    }
    output_type = "string"

    def __init__(self, search_tool: DuckDuckGoSearchTool):
        super().__init__()
        self._search = search_tool

    def forward(self, focus: str = "all") -> str:
        from datetime import datetime
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        queries = [
            f"OPEC+ production cut decision {current_date} today breaking",
            f"Saudi Arabia voluntary oil cut barrel {current_date} just in",
            f"Russia oil export reduction barrel {current_date} recent",
            f"OPEC emergency meeting oil price {current_date} breaking news",
            f"UAE Kuwait oil output quota {current_date} today",
        ]
        results = []
        for q in queries:
            try:
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[{q}]\n{r[:600]}")
            except Exception as e:
                results.append(f"[{q}] Error: {e}")
        
        header = f"=== OPEC+ SUPPLY SEARCH ===\n"
        header += f"Focus: {focus} | Current Date: {current_date}\n\n"
        
        return header + "\n\n---\n\n".join(results) if results else "No OPEC news found."


class NaturalGasDisruptionTool(Tool):
    """Tool : perturbations gaz naturel (pipelines, LNG, Russie)"""
    name = "search_gas_disruption"
    description = (
        "Searches for natural gas supply disruptions: pipeline sabotage, LNG terminal damage, "
        "Russia gas cuts to Europe, Middle East gas field attacks. "
        "Gas price spikes often correlate with oil rallies."
    )
    inputs = {
        "topic": {
            "type": "string",
            "description": "Topic: 'pipeline', 'lng', 'russia_gas', 'all'. Default: 'all'",
            "default": "all",
            "nullable": True,
        }
    }
    output_type = "string"

    def __init__(self, search_tool: DuckDuckGoSearchTool):
        super().__init__()
        self._search = search_tool

    def forward(self, topic: str = "all") -> str:
        from datetime import datetime
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        queries = [
            f"natural gas pipeline explosion sabotage {current_date} today breaking",
            f"LNG terminal attack fire disruption {current_date} just in",
            f"Russia gas supply Europe cut {current_date} recent",
            f"Qatar North Field gas disruption {current_date} today",
            f"Azerbaijan Georgia gas pipeline attack {current_date} breaking news",
        ]
        results = []
        for q in queries:
            try:
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[{q}]\n{r[:600]}")
            except Exception as e:
                results.append(f"[{q}] Error: {e}")
        
        header = f"=== NATURAL GAS DISRUPTION SEARCH ===\n"
        header += f"Topic: {topic} | Current Date: {current_date}\n\n"
        
        return header + "\n\n---\n\n".join(results) if results else "No gas disruption news found."


class ShippingDisruptionTool(Tool):
    """Tool : perturbations maritimes (Houthis, pirates, blocage)"""
    name = "search_shipping_disruption"
    description = (
        "Searches for maritime oil shipping disruptions: Houthi attacks in Red Sea, "
        "Bab-el-Mandeb strait tensions, Suez Canal blockage, tanker seizures by Iran. "
        "Shipping disruptions directly impact Brent crude prices."
    )
    inputs = {}
    output_type = "string"

    def __init__(self, search_tool: DuckDuckGoSearchTool):
        super().__init__()
        self._search = search_tool

    def forward(self) -> str:
        from datetime import datetime
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        queries = [
            f"Houthi attack oil tanker Red Sea {current_date} today breaking",
            f"Bab-el-Mandeb shipping disruption oil {current_date} just in",
            f"Suez Canal closure tanker blockage {current_date} recent",
            f"Iran seize oil tanker Strait Hormuz {current_date} breaking news",
            f"oil tanker piracy attack {current_date} today",
        ]
        results = []
        for q in queries:
            try:
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[{q}]\n{r[:600]}")
            except Exception as e:
                results.append(f"[{q}] Error: {e}")
        
        header = f"=== SHIPPING DISRUPTION SEARCH ===\n"
        header += f"Current Date: {current_date}\n\n"
        
        return header + "\n\n---\n\n".join(results) if results else "No shipping disruption news found."


class GeopoliticalEscalationTool(Tool):
    """Tool : escalades géopolitiques générales impactant le pétrole"""
    name = "search_geopolitical_escalation"
    description = (
        "Searches for broad geopolitical escalations that could spike oil prices: "
        "Russia-Ukraine energy infrastructure attacks, US-China South China Sea tensions, "
        "Libya civil war oil fields, Venezuela sanctions, Nigeria pipeline attacks."
    )
    inputs = {}
    output_type = "string"

    def __init__(self, search_tool: DuckDuckGoSearchTool):
        super().__init__()
        self._search = search_tool

    def forward(self) -> str:
        from datetime import datetime
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        queries = [
            f"Russia Ukraine oil energy infrastructure attack {current_date} today breaking",
            f"Libya oil field shutdown civil war {current_date} just in",
            f"Venezuela oil sanction export {current_date} recent",
            f"Nigeria pipeline attack oil production {current_date} breaking news",
            f"US China South China Sea oil tension {current_date} today",
        ]
        results = []
        for q in queries:
            try:
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[{q}]\n{r[:600]}")
            except Exception as e:
                results.append(f"[{q}] Error: {e}")
        
        header = f"=== GEOPOLITICAL ESCALATION SEARCH ===\n"
        header += f"Current Date: {current_date}\n\n"
        
        return header + "\n\n---\n\n".join(results) if results else "No geopolitical escalation news found."


class OilPriceTool(Tool):
    """Tool : prix actuels Brent / WTI"""
    name = "get_oil_price"
    description = (
        "Fetches the current Brent crude and WTI crude oil prices, "
        "recent price movements, and analyst forecasts."
    )
    inputs = {}
    output_type = "string"

    def __init__(self, search_tool: DuckDuckGoSearchTool):
        super().__init__()
        self._search = search_tool

    def forward(self) -> str:
        from datetime import datetime
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        queries = [
            f"Brent crude oil price today {current_date}",
            f"WTI crude price today barrel {current_date}",
            f"oil price forecast analyst {current_date}",
        ]
        results = []
        for q in queries:
            try:
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[{q}]\n{r[:400]}")
            except Exception as e:
                results.append(f"[{q}] Error: {e}")
        
        header = f"=== OIL PRICE DATA ===\n"
        header += f"Current Date: {current_date}\n\n"
        
        return header + "\n\n".join(results) if results else "Oil price data unavailable."


class RecentNewsTool(Tool):
    """Tool : actualités très récentes sur le pétrole"""
    name = "search_recent_news"
    description = (
        "Searches for very recent oil-related news from major news sources. "
        "Filters results by date (last 24h, 48h, or 7 days) and prioritizes "
        "breaking news and developing stories from Reuters, Bloomberg, AP, BBC, FT, WSJ."
    )
    inputs = {
        "topic": {
            "type": "string",
            "description": "Topic to search: 'iran', 'refinery', 'opec', 'gas', 'shipping', 'geopolitical', 'all'. Default: 'all'",
            "default": "all",
            "nullable": True,
        },
        "timeframe": {
            "type": "string",
            "description": "Time period: '24h', '48h', '7d'. Default: '24h'",
            "default": "24h",
            "nullable": True,
        }
    }
    output_type = "string"

    def __init__(self, search_tool: DuckDuckGoSearchTool):
        super().__init__()
        self._search = search_tool

    def forward(self, topic: str = "all", timeframe: str = "24h") -> str:
        from datetime import datetime, timedelta
        
        now = datetime.now()
        # On utilise des termes relatifs au lieu de la date fixe qui bloque souvent les résultats
        if timeframe == "24h":
            time_query = "today"
            time_label = "Last 24 hours"
        elif timeframe == "48h":
            time_query = "yesterday OR today"
            time_label = "Last 48 hours"
        else:
            time_query = "this week"
            time_label = "Last 7 days"
        
        # Simplification des sources : on ne met que les 2 plus importantes pour ne pas surcharger la requête
        # L'agent trouvera les autres via une recherche plus large
        priority_sites = "site:reuters.com OR site:bloomberg.com"
        
        topic_queries = {
            "iran": [
                f"Iran oil attack {time_query} {priority_sites}",
                f"Strait of Hormuz tension {time_query}",
            ],
            "refinery": [
                f"oil refinery explosion fire {time_query}",
                f"refinery drone attack {time_query}",
            ],
            "opec": [
                f"OPEC production cut {time_query}",
                f"Saudi Arabia oil supply {time_query}",
            ],
            "all": [
                f"oil market breaking news {time_query}",
                f"crude oil supply disruption {time_query}",
                f"oil price spike {time_query}",
            ],
        }
        
        queries = topic_queries.get(topic, topic_queries["all"])
        results = []
        for q in queries:
            try:
                # Augmentation du nombre de résultats pour compenser la simplification
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[Query: {q}]\n{r[:1000]}")
            except Exception as e:
                log.warning(f"⚠️ Search error for query '{q}': {e}")
        
        header = f"=== RECENT NEWS SEARCH ({time_label}) ===\n\n"
        return header + "\n\n---\n\n".join(results) if results else f"No results found for {topic}."


class RSSFeedTool(Tool):
    """Tool : lecture des flux RSS d'actualités en temps réel"""
    name = "read_rss_feeds"
    description = (
        "Reads RSS feeds from major news sources to get real-time oil market news. "
        "Filters entries by publication date and returns recent headlines and summaries."
    )
    inputs = {
        "feed": {
            "type": "string",
            "description": "RSS feed to read: 'reuters_energy', 'bloomberg_energy', 'ap_business', 'all'. Default: 'all'",
            "default": "all",
            "nullable": True,
        },
        "hours_back": {
            "type": "integer",
            "description": "How many hours back to filter entries. Default: 24",
            "default": 24,
            "nullable": True,
        }
    }
    output_type = "string"

    def forward(self, feed: str = "all", hours_back: int = 24) -> str:
        try:
            import feedparser
            from datetime import datetime, timedelta
        except ImportError:
            return "Error: feedparser not installed. Run: pip install feedparser"
        
        # Flux RSS disponibles
        rss_feeds = {
            "reuters_energy": "https://www.reuters.com/rssFeed/businessNews",
            "bloomberg_energy": "https://feeds.bloomberg.com/markets/news.rss",
            "ap_business": "https://feeds.apnews.com/rss/apf-business",
            "bbc_business": "https://feeds.bbci.co.uk/news/business/rss.xml",
        }
        
        # Sélectionner les flux à lire
        if feed == "all":
            feeds_to_read = rss_feeds
        else:
            feeds_to_read = {feed: rss_feeds.get(feed)} if feed in rss_feeds else {}
        
        if not feeds_to_read:
            return f"Error: Unknown feed '{feed}'. Available: {', '.join(rss_feeds.keys())}"
        
        # Calculer la date limite
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        results = []
        for feed_name, feed_url in feeds_to_read.items():
            if not feed_url:
                continue
            
            try:
                parsed = feedparser.parse(feed_url)
                feed_results = []
                
                for entry in parsed.entries[:20]:  # Limiter aux 20 derniers entrées
                    # Extraire la date de publication
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime(*entry.updated_parsed[:6])
                    
                    # Filtrer par date
                    if pub_date and pub_date > cutoff_time:
                        title = entry.get('title', 'No title')
                        link = entry.get('link', '')
                        summary = entry.get('summary', entry.get('description', ''))[:200]
                        pub_str = pub_date.strftime("%Y-%m-%d %H:%M")
                        
                        feed_results.append(
                            f"📰 [{pub_str}] {title}\n"
                            f"   {summary}\n"
                            f"   🔗 {link}\n"
                        )
                
                if feed_results:
                    results.append(f"=== {feed_name.upper()} ===\n" + "\n".join(feed_results))
                else:
                    results.append(f"=== {feed_name.upper()} ===\nNo recent entries in the last {hours_back}h")
                    
            except Exception as e:
                results.append(f"=== {feed_name.upper()} ===\nError reading feed: {e}")
        
        header = f"=== RSS FEEDS ===\n"
        header += f"Feeds: {feed} | Timeframe: Last {hours_back} hours\n"
        header += f"Cutoff time: {cutoff_time.strftime('%Y-%m-%d %H:%M')}\n\n"
        
        return header + "\n\n---\n\n".join(results) if results else "No RSS feed data available."


class VIXTool(Tool):
    """Tool : indice de volatilité VIX (CBOE)"""
    name = "get_vix_index"
    description = (
        "Fetches the current VIX (CBOE Volatility Index) value, recent movements, "
        "and volatility trends. The VIX is a key indicator of market fear and "
        "can correlate with oil price volatility and geopolitical tensions."
    )
    inputs = {}
    output_type = "string"

    def __init__(self, search_tool: DuckDuckGoSearchTool):
        super().__init__()
        self._search = search_tool

    def forward(self) -> str:
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        queries = [
            f"VIX index value today {current_date}",
            f"CBOE Volatility Index current level {current_date}",
            f"VIX chart volatility market fear {current_date}",
            f"VIX oil price correlation volatility",
        ]
        results = []
        for q in queries:
            try:
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[{q}]\n{r[:500]}")
            except Exception as e:
                results.append(f"[{q}] Error: {e}")
        
        header = f"=== VIX (CBOE Volatility Index) ===\n"
        header += f"Current Date: {current_date}\n\n"
        
        return header + "\n\n".join(results) if results else "VIX data unavailable."


# ─────────────────────────────────────────────
# Construction de l'agent
# ─────────────────────────────────────────────

def build_agent() -> CodeAgent:
    """Initialise le modèle Ollama et l'agent avec tous les tools."""
    from smolagents.local_python_executor import LocalPythonExecutor
    
    model = LiteLLMModel(
        model_id=CONFIG["ollama_model"],
        api_base=CONFIG["ollama_api_base"],
        num_ctx=CONFIG["ollama_num_ctx"],
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
        timeout_seconds=60,  # Timeout augmenté de 30 à 60 secondes
    )

    # Créer l'agent avec le format markdown pour les balises de code
    agent = CodeAgent(
        tools=tools,
        model=model,
        max_steps=20,
        additional_authorized_imports=["json", "datetime", "hashlib", "feedparser"],
        executor=custom_executor,  # Utiliser l'executor personnalisé
        code_block_tags="markdown",  # ✅ CORRECTION: Accepter le format markdown standard (```python``` ou ```json```)
    )
    
    # LOG DE DEBUG : Logger les balises de code utilisées par le CodeAgent
    log.info(f"🔧 CodeAgent code_block_tags: {agent.code_block_tags}")
    log.info(f"🔧 CodeAgent attend le format: {agent.code_block_tags[0]}...{agent.code_block_tags[1]}")
    
    return agent


# ─────────────────────────────────────────────
# Prompt principal
# ─────────────────────────────────────────────

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

3. OUTPUT: Provide a detailed summary of each significant finding. For each event, specify the date, source, 
   and a brief explanation of how it might affect oil supply or prices. 
   Do NOT worry about JSON formatting, just be thorough and precise in your analysis.
"""
    return prompt

# ─────────────────────────────────────────────
# Dataset Collection
# ─────────────────────────────────────────────

def save_to_dataset(input_data: dict, output_data: dict):
    """Enregistre un exemple d'entrée/sortie pour l'entraînement DSPy."""
    try:
        dataset_file = Path(CONFIG["dataset_file"])
        dataset_file.parent.mkdir(exist_ok=True)
        
        example = {
            "input": input_data,
            "output": output_data,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(dataset_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")
            
        log.info(f"💾 Exemple ajouté au dataset ({dataset_file})")
    except Exception as e:
        log.error(f"❌ Erreur lors de la sauvegarde du dataset : {e}")


# ─────────────────────────────────────────────
# Runner principal
# ─────────────────────────────────────────────

def run_monitoring_cycle():
    """Lance un cycle de surveillance avec DSPy pour la synthèse finale."""
    log.info("=" * 60)
    log.info("🛢️  Démarrage cycle de surveillance pétrole (DSPy Mode)")
    log.info("=" * 60)

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

    # 3. Synthèse et formatage via DSPy
    events = []
    try:
        analyzer = OilEventAnalyzer()
        
        # Charger les poids optimisés si disponibles
        optimized_path = Path(CONFIG.get("dataset_file", "data/")).parent / "oil_analyzer_optimized.json"
        if optimized_path.exists():
            log.info(f"📂 Chargement du module DSPy optimisé : {optimized_path}")
            analyzer.load(str(optimized_path))
            
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        dspy_result = analyzer(
            current_date=current_date,
            current_datetime=current_datetime,
            alert_threshold=CONFIG["alert_threshold"],
            news_sources=CONFIG["news_sources"],
            raw_intelligence=raw_intelligence
        )
        
        # Extraire les événements de la réponse DSPy
        # DSPy avec JSONAdapter retourne souvent des objets Pydantic ou des dicts
        if hasattr(dspy_result, 'events'):
            # Convertir les objets Pydantic en dicts si nécessaire
            events = []
            for e in dspy_result.events:
                if hasattr(e, 'dict'):
                    events.append(e.dict())
                else:
                    events.append(e)
        
        log.info(f"✨ DSPy Analysis Complete. Confidence: {getattr(dspy_result, 'confidence_score', 'N/A')}")
        
        # Sauvegarder pour l'amélioration continue (20 exemples cibles)
        save_to_dataset(
            input_data={
                "current_date": current_date,
                "alert_threshold": CONFIG["alert_threshold"],
                "raw_intelligence": raw_intelligence
            },
            output_data={"events": events}
        )
        
    except Exception as e:
        log.error(f"❌ DSPy Synthesis Error: {e}")
        import traceback
        log.error(traceback.format_exc())
        return

    log.info(f"📊 {len(events)} événement(s) à impact élevé détectés")

    # 4. Envoi des alertes
    new_events_count = 0
    for event in events:
        event_id = event.get("id") or event_fingerprint(
            event.get("title", ""), event.get("category", "")
        )

        if event_id in seen_events:
            log.info(f"⏭️  Événement déjà vu, skip : {event.get('title', event_id)}")
            continue

        # Nouvel événement → email
        subject = f"{event.get('category','?')} | Score {event.get('impact_score','?')}/10 — {event.get('title','Unnamed event')}"
        body = format_email_body(event)

        success = send_alert_email(subject, body, event_id)
        if success:
            seen_events.add(event_id)
            new_events_count += 1

    save_seen_events(seen_events)

    log.info(f"✅ Cycle terminé — {new_events_count} nouvelle(s) alerte(s) envoyée(s)")


def format_email_body(event: dict) -> str:
    """Formate le corps d'un email d'alerte."""
    lines = [
        f"🛢️  OIL MARKET ALERT",
        f"{'='*50}",
        f"",
        f"📌 TITRE       : {event.get('title', 'N/A')}",
        f"📂 CATÉGORIE   : {event.get('category', 'N/A')}",
        f"⚡ SCORE IMPACT: {event.get('impact_score', 'N/A')}/10",
        f"🔔 URGENCE     : {event.get('urgency', 'N/A')}",
        f"💰 IMPACT PRIX : {event.get('price_impact', 'N/A')}",
        f"🎯 CERTITUDE   : {int(event.get('certainty_score', 0) * 100)}%",
        f"",
        f"📝 ANALYSE :",
        f"{event.get('summary', 'N/A')}",
        f"",
        f"🔗 SOURCE : {event.get('source_hint', 'N/A')}",
        f"📅 DATE PUB: {event.get('publication_date', 'N/A')}",
        f"",
        f"{'─'*50}",
        f"⏰ Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"🤖 Agent : smolagents + DSPy (qwen3.5:9b)",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────
# Affichage historique
# ─────────────────────────────────────────────

def show_history():
    """Affiche l'historique des emails envoyés."""
    history = load_email_history()
    if not history:
        print("📭 Aucun email envoyé pour l'instant.")
        return

    print(f"\n{'='*60}")
    print(f"📧 HISTORIQUE DES ALERTES EMAIL ({len(history)} total)")
    print(f"{'='*60}")
    for i, entry in enumerate(history[-20:], 1):  # 20 derniers
        print(f"\n[{i:02d}] {entry['timestamp']}")
        print(f"     Sujet   : {entry['subject']}")
        print(f"     ID      : {entry['event_id']}")
        print(f"     Aperçu  : {entry['preview'][:120]}...")
    print(f"\n{'='*60}\n")


# ─────────────────────────────────────────────
# Entrypoint
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "history":
        show_history()
    else:
        run_monitoring_cycle()
