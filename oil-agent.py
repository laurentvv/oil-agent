"""
Oil Market Monitoring Agent
============================
smolagents 1.24.0 + LiteLLM + Ollama (qwen2.5:7b)
Surveille les événements géopolitiques et industriels pouvant faire rebondir le cours du pétrole.
Envoie des alertes email via relais SMTP (Postfix local).
"""

import sys
import io
import json
import smtplib
import hashlib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

from dspy_oil_module_v2 import OilAnalyst, setup_dspy
from smolagents import (
    CodeAgent,
    LiteLLMModel,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
    Tool,
)

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
CONFIG = {
    # Ollama
    "ollama_model": "ollama_chat/qwen3.5:9b",
    "ollama_api_base": "http://127.0.0.1:11434",
    "ollama_num_ctx": 8192,
    # Email (relais Postfix local)
    "smtp_host": "smtp2.123ce.net",
    "smtp_port": 25,
    "email_from": "no-reply@123ce.net",
    "email_to": "laurentvv@gmail.com",       # ← Modifier ici
    "email_subject_prefix": "[OIL-ALERT]",
    "send_emails": True,                  # Désactiver l'envoi d'emails (True pour activer)
    # Fichiers de persistance
    "history_file": "logs/email_history.json",
    "events_db": "logs/events_seen.json",
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
        
        header = "=== IRAN CONFLICT SEARCH ===\n"
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
        
        header = "=== REFINERY DAMAGE SEARCH ===\n"
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
        
        header = "=== OPEC+ SUPPLY SEARCH ===\n"
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
        
        header = "=== NATURAL GAS DISRUPTION SEARCH ===\n"
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
        
        header = "=== SHIPPING DISRUPTION SEARCH ===\n"
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
        
        header = "=== GEOPOLITICAL ESCALATION SEARCH ===\n"
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
        
        header = "=== OIL PRICE DATA ===\n"
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
        
        # Calculer la date de début pour le filtrage
        now = datetime.now()
        if timeframe == "24h":
            date_start = now - timedelta(hours=24)
            date_str = date_start.strftime("%Y-%m-%d")
            time_keywords = ["today", "breaking", "just in", "last 24 hours"]
        elif timeframe == "48h":
            date_start = now - timedelta(hours=48)
            date_str = date_start.strftime("%Y-%m-%d")
            time_keywords = ["today", "yesterday", "breaking", "last 48 hours"]
        else:  # 7d
            date_start = now - timedelta(days=7)
            date_str = date_start.strftime("%Y-%m-%d")
            time_keywords = ["this week", "recent", "last 7 days"]
        
        current_date = now.strftime("%Y-%m-%d")
        
        # Sources d'actualités prioritaires
        news_sources = CONFIG.get("news_sources", [
            "reuters.com", "bloomberg.com", "apnews.com", 
            "bbc.com", "ft.com", "wsj.com"
        ])
        site_filter = " OR ".join([f"site:{s}" for s in news_sources])
        
        # Requêtes par sujet
        topic_queries = {
            "iran": [
                f"Iran military oil infrastructure {current_date} {site_filter}",
                f"Strait of Hormuz oil tanker {current_date} {site_filter}",
                f"Iran IRGC oil attack {current_date} {site_filter}",
            ],
            "refinery": [
                f"oil refinery explosion fire {current_date} {site_filter}",
                f"refinery drone attack oil {current_date} {site_filter}",
                f"Aramco refinery attack {current_date} {site_filter}",
            ],
            "opec": [
                f"OPEC production cut decision {current_date} {site_filter}",
                f"Saudi Arabia oil cut {current_date} {site_filter}",
                f"OPEC emergency meeting oil {current_date} {site_filter}",
            ],
            "gas": [
                f"natural gas pipeline explosion {current_date} {site_filter}",
                f"LNG terminal disruption {current_date} {site_filter}",
                f"Russia gas supply Europe {current_date} {site_filter}",
            ],
            "shipping": [
                f"Houthi attack oil tanker {current_date} {site_filter}",
                f"Red Sea shipping oil disruption {current_date} {site_filter}",
                f"Suez Canal oil tanker {current_date} {site_filter}",
            ],
            "geopolitical": [
                f"Russia Ukraine oil infrastructure {current_date} {site_filter}",
                f"Libya oil field shutdown {current_date} {site_filter}",
                f"Venezuela oil sanction {current_date} {site_filter}",
            ],
            "all": [
                f"oil market breaking news {current_date} {site_filter}",
                f"crude oil price spike {current_date} {site_filter}",
                f"oil supply disruption {current_date} {site_filter}",
            ],
        }
        
        queries = topic_queries.get(topic, topic_queries["all"])
        
        # Ajouter des mots-clés temporels pour améliorer la fraîcheur
        queries = [f"{q} {time_keywords[0]}" for q in queries]
        
        results = []
        for q in queries:
            try:
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[Query: {q}]\n{r[:800]}")
            except Exception as e:
                results.append(f"[Query: {q}] Error: {e}")
        
        header = "=== RECENT NEWS SEARCH ===\n"
        header += f"Topic: {topic} | Timeframe: {timeframe} | Current Date: {current_date}\n"
        header += f"Searching since: {date_str}\n"
        header += f"Sources: {', '.join(news_sources)}\n\n"
        
        return header + "\n\n---\n\n".join(results) if results else f"No recent news found for topic '{topic}' in the last {timeframe}."


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
        
        header = "=== RSS FEEDS ===\n"
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
            "VIX oil price correlation volatility",
        ]
        results = []
        for q in queries:
            try:
                r = self._search(q)
                if r and len(r) > 50:
                    results.append(f"[{q}]\n{r[:500]}")
            except Exception as e:
                results.append(f"[{q}] Error: {e}")
        
        header = "=== VIX (CBOE Volatility Index) ===\n"
        header += f"Current Date: {current_date}\n\n"
        
        return header + "\n\n".join(results) if results else "VIX data unavailable."


# ─────────────────────────────────────────────
# Construction de l'agent
# ─────────────────────────────────────────────

def build_agent() -> CodeAgent:
    """Initialise le modèle Ollama et l'agent avec tous les tools."""
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

    agent = CodeAgent(
        tools=tools,
        model=model,
        max_steps=20,
        additional_authorized_imports=["json", "datetime", "hashlib", "feedparser"],
    )
    return agent


# ─────────────────────────────────────────────
# Prompt principal
# ─────────────────────────────────────────────

def get_master_prompt() -> str:
    """Génère le prompt principal avec la date du jour dynamique."""
    from datetime import datetime
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    threshold = CONFIG["alert_threshold"]
    
    prompt = f"""
You are an expert oil market analyst monitoring geopolitical and industrial events 
that could cause oil prices (Brent crude, WTI) to spike or rebound.

CURRENT DATE: {current_date}
CURRENT DATETIME: {current_datetime}

Your mission for this analysis run:

1. Use ALL available specialized tools to gather current intelligence:
   - search_iran_conflict: Iran military tensions, IRGC, Strait of Hormuz
   - search_refinery_damage: Refinery attacks, fires, explosions globally
   - search_opec_supply: OPEC+ cuts, production quota decisions
   - search_gas_disruption: Natural gas pipeline/LNG disruptions
   - search_shipping_disruption: Houthi attacks, tanker seizures, maritime blockages
   - search_geopolitical_escalation: Russia/Ukraine, Libya, Venezuela, Nigeria, etc.
   - get_oil_price: Current Brent/WTI prices and context
   - search_recent_news: Very recent news from major sources (last 24h/48h/7d)
   - read_rss_feeds: Real-time RSS feeds from Reuters, Bloomberg, AP, BBC
    - get_vix_index: Current VIX volatility index (market fear indicator)

2. PERFORMANCE OPTIMIZATION: For faster execution, you can call tools directly 
   without intermediate analysis steps when appropriate:
   - For quick checks: Call search_recent_news(topic="all", timeframe="24h") directly
   - For real-time updates: Call read_rss_feeds(feed="all", hours_back=12) directly
   - For volatility assessment: Call get_vix_index() directly
   - For price checks: Call get_oil_price() directly
   - For targeted searches: Use specific tools with appropriate parameters (e.g., 
     search_iran_conflict(days_back=1), search_refinery_damage(region="middle_east"))
   - Direct tool calls are ~3-10x faster than full agent analysis
   - Use direct calls when: (a) You need quick information, (b) You're testing/debugging,
     (c) You're integrating into automation scripts, (d) You need minimal latency

3. IMPORTANT: Focus on events from TODAY ({current_date}) and the last 24-48 hours.
    When searching, use date-specific queries like "today", "breaking", "just in",
    and include the current date in search terms. Prioritize:
    - search_recent_news with timeframe="24h" for breaking news
    - read_rss_feeds for real-time updates
    - get_vix_index to gauge market volatility and fear levels

4. For each event or news item found, evaluate:
   - CATEGORY: (Iran/Refinery/OPEC/Gas/Shipping/Geopolitical/Other)
   - IMPACT SCORE: 1-10 (10 = immediate major oil price spike likely)
   - URGENCY: (Breaking/Recent/Developing/Background)
   - SUMMARY: 2-3 sentences explaining the event and price impact mechanism
   - SOURCE_TITLE: Brief title of the news
   - PUBLICATION_DATE: Date of the news (if available)

4. Filter to keep ONLY events with Impact Score >= {threshold}

5. Return your final answer as a JSON list with this structure:
[
  {{
    "id": "unique_slug",
    "category": "Iran|Refinery|OPEC|Gas|Shipping|Geopolitical",
    "title": "Short event title",
    "impact_score": 8,
    "urgency": "Breaking",
    "summary": "Detailed analysis of the event...",
    "price_impact": "+$3-5/barrel expected",
    "source_hint": "Brief source description",
    "publication_date": "{current_date}"
  }}
]

If no high-impact events found, return: []

Be thorough, analytical, and focus on ACTIONABLE intelligence for oil traders.
Remember: Current date is {current_date} - prioritize news from today and recent hours.
"""
    return prompt

MASTER_PROMPT = get_master_prompt()


# ─────────────────────────────────────────────
# Runner principal
# ─────────────────────────────────────────────

def run_monitoring_cycle():
    """Lance un cycle de surveillance et envoie les alertes email pour les nouveaux événements."""
    log.info("=" * 60)
    log.info("🛢️  Démarrage cycle de surveillance pétrole")
    log.info("=" * 60)

    seen_events = load_seen_events()
    agent = build_agent()

    try:
        # 1. Collect raw intelligence using the agent as a collector
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")

        collector_prompt = f"""
        Gather all current intelligence related to the oil market for today ({current_date}).
        Use all your tools to find news about Iran, refineries, OPEC, gas disruptions,
        shipping, and geopolitics.
        Just provide a detailed summary of all raw data you found.
        """
        raw_intelligence = agent.run(collector_prompt)
        log.info(f"Raw intelligence collected ({len(str(raw_intelligence))} chars)")

        # 2. Use DSPy to analyze and classify the intelligence
        log.info("Starting DSPy analysis (5 trials)...")
        setup_dspy(CONFIG["ollama_model"], CONFIG["ollama_api_base"])
        analyst = OilAnalyst(num_trials=5)
        raw_result = analyst(raw_intelligence=str(raw_intelligence), current_date=current_date)
        log.info(f"DSPy result: {str(raw_result)[:500]}")
    except Exception as e:
        log.error(f"Analysis error: {e}")
        import traceback
        log.error(traceback.format_exc())
        return

    # Parse JSON
    events = []
    if isinstance(raw_result, list):
        events = raw_result
    elif isinstance(raw_result, str):
        # Extraction du JSON depuis la réponse texte
        import re
        match = re.search(r'\[.*\]', raw_result, re.DOTALL)
        if match:
            try:
                events = json.loads(match.group())
            except json.JSONDecodeError:
                log.warning("Impossible de parser le JSON — pas d'alerte envoyée")
                events = []

    log.info(f"📊 {len(events)} événement(s) à impact élevé détectés")

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
    log.info(f"📋 Total événements dans historique : {len(load_email_history())}")


def format_email_body(event: dict) -> str:
    """Formate le corps d'un email d'alerte détaillé généré par DSPy."""
    lines = [
        "🛢️  OIL MARKET ANALYSIS REPORT (DSPy Powered)",
        f"{'='*60}",
        "",
        f"📌 EVENT TITLE   : {event.get('title', 'N/A')}",
        f"📂 CATEGORY      : {event.get('category', 'N/A')}",
        f"⚡ IMPACT SCORE  : {event.get('impact_score', 'N/A')}/10",
        f"🔔 URGENCY       : {event.get('urgency', 'N/A')}",
        f"💰 PRICE IMPACT  : {event.get('price_impact', 'N/A')}",
        f"📅 PUBLISHED ON  : {event.get('publication_date', 'N/A')}",
        "",
        "📝 DETAILED ANALYSIS & INSIGHTS:",
        f"{'-'*30}",
        f"{event.get('summary', 'N/A')}",
        f"{'-'*30}",
        "",
        f"🔗 SOURCE INFO   : {event.get('source_hint', 'N/A')}",
        "",
        f"{'='*60}",
        f"⏰ Analysis Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "🤖 Powered by DSPy (Multi-trial Validation) + smolagents + Ollama",
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

    if len(sys.argv) > 1 and sys.argv[1] == "history":
        show_history()
    else:
        run_monitoring_cycle()
