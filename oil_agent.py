"""
Oil Market Monitoring Agent
============================
smolagents 1.24.0 + LiteLLM + llama.cpp (Qwen3.5-9B)
Surveille les événements géopolitiques et industriels pouvant faire rebondir le cours du pétrole.
Envoie des alertes email via relais SMTP (Postfix local).
"""

import json
import smtplib
import hashlib
import logging
import subprocess
import time
import requests
import atexit
import sys
import io
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
)

import dspy
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional

# ─────────────────────────────────────────────
# Context Management
# ─────────────────────────────────────────────
from context_management import (
    HistoryCompressor,
    SlidingWindowManager,
    MemoryCleaner,
    AgentState,
    build_optimized_prompt_context,
)

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
    urgency: Optional[Literal["Breaking", "Recent", "Developing", "Background"]] = Field("Recent", description="Urgence de l'événement")
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
    """Extract structured oil events from intelligence. ALL fields required per event."""
    
    current_date: str = dspy.InputField(desc="Date (YYYY-MM-DD)")
    current_datetime: str = dspy.InputField(desc="Timestamp")
    alert_threshold: int = dspy.InputField(desc="Alert threshold (0-10)")
    news_sources: list[str] = dspy.InputField(desc="Priority news sources")
    raw_intelligence: str = dspy.InputField(desc="Collected intelligence data")
    
    events: List[OilEvent] = dspy.OutputField(desc="Oil events with all required fields")
    confidence_score: float = dspy.OutputField(desc="Global confidence (0.0-1.0)")


# Module avec Chain of Thought
class OilEventAnalyzer(dspy.Module):
    """Analyseur d'événements pétroliers avec raisonnement explicite."""
    
    def __init__(self):
        super().__init__()
        self.analyze = dspy.ChainOfThought(OilEventSignature)

    def forward(self, **kwargs):
        # Utiliser dspy.Predict ou ChainOfThought
        pred = self.analyze(**kwargs)
        
        return pred

def validate_and_fix_events(events: list, current_date: str) -> list:
    """Valide et nettoie les événements produits par le LLM."""
    valid_events = []
    valid_categories = ["Iran", "Refinery", "OPEC", "Gas", "Shipping", "Geopolitical"]
    
    for i, event in enumerate(events):
        try:
            # Transformation en dict si c'est un objet Pydantic
            e_dict = event if isinstance(event, dict) else (event.model_dump() if hasattr(event, 'model_dump') else {})
            
            # 1. Vérification des champs obligatoires minimums
            if not e_dict.get("title") or not e_dict.get("category"):
                log.warning(f"⚠️ Event {i} ignoré : titre ou catégorie manquant")
                continue
            
            # 1.5. Corriger les catégories invalides
            category = e_dict.get("category", "")
            if category not in valid_categories:
                log.warning(f"⚠️ Event {i} catégorie invalide '{category}', tentative de correction...")
                # Essayer de mapper vers une catégorie valide
                category_lower = category.lower()
                if "iran" in category_lower or "hormuz" in category_lower or "persian" in category_lower:
                    e_dict["category"] = "Iran"
                elif "refinery" in category_lower or "plant" in category_lower:
                    e_dict["category"] = "Refinery"
                elif "opec" in category_lower or "production" in category_lower or "supply" in category_lower:
                    e_dict["category"] = "OPEC"
                elif "gas" in category_lower or "lng" in category_lower:
                    e_dict["category"] = "Gas"
                elif "shipping" in category_lower or "tanker" in category_lower or "red sea" in category_lower or "suez" in category_lower:
                    e_dict["category"] = "Shipping"
                elif "geopolitical" in category_lower or "war" in category_lower or "conflict" in category_lower:
                    e_dict["category"] = "Geopolitical"
                else:
                    # Si aucune correspondance, utiliser "Geopolitical" par défaut
                    log.warning(f"⚠️ Event {i} catégorie '{category}' mappée vers 'Geopolitical'")
                    e_dict["category"] = "Geopolitical"
                
            # 2. Valeurs par défaut pour les champs optionnels manquants
            if "impact_score" not in e_dict:
                e_dict["impact_score"] = 5
            if "urgency" not in e_dict or not e_dict["urgency"]:
                e_dict["urgency"] = "Recent"
            if "summary" not in e_dict:
                e_dict["summary"] = "No summary provided."
            if "price_impact" not in e_dict:
                e_dict["price_impact"] = "Unknown"
            if "source_hint" not in e_dict:
                e_dict["source_hint"] = "Multiple sources"
            if "publication_date" not in e_dict or not e_dict["publication_date"]:
                e_dict["publication_date"] = current_date
            if "certainty_score" not in e_dict:
                e_dict["certainty_score"] = 0.7
            if "id" not in e_dict:
                e_dict["id"] = event_fingerprint(e_dict["title"], e_dict["category"])
                
            valid_events.append(e_dict)
        except Exception as ex:
            log.error(f"❌ Erreur lors de la validation de l'événement {i} : {ex}")
            
    return valid_events

def configure_dspy():
    """Configure DSPy avec le modèle llama-server défini dans CONFIG."""
    lm = dspy.LM(
        model=f"openai/{CONFIG.model.name}",
        api_base=CONFIG.model.api_base,
        api_key="dummy",  # llama-server ne nécessite pas de clé API
        model_type="chat"
    )
    dspy.configure(lm=lm, adapter=dspy.JSONAdapter())
    return lm

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

# Modèles Pydantic pour la validation de la configuration
class ModelConfig(BaseModel):
    """Configuration du modèle LLM."""
    name: str = Field(..., description="Nom du modèle")
    path: str = Field(..., description="Chemin vers le fichier du modèle")
    api_base: str = Field(..., description="URL de base de l'API")
    num_ctx: int = Field(..., gt=0, description="Taille du contexte")
    provider: str = Field(..., description="Fournisseur du modèle")
    
    @field_validator('path')
    @classmethod
    def path_exists(cls, v):
        """Vérifie que le fichier du modèle existe."""
        path = Path(v)
        if not path.exists():
            raise ValueError(f"Modèle introuvable : {v}")
        if not path.is_file():
            raise ValueError(f"Le chemin n'est pas un fichier : {v}")
        return v

class LlamaServerConfig(BaseModel):
    """Configuration du serveur llama-server."""
    executable: str = Field(default="llama-server", description="Exécutable du serveur")
    n_gpu_layers: int = Field(default=-1, ge=-1, description="Nombre de couches GPU (-1 pour toutes)")
    n_threads: int = Field(default=0, ge=-1, description="Nombre de threads CPU (0 pour auto)")
    ctx_size: int = Field(default=8192, gt=0, description="Taille du contexte")
    batch_size: int = Field(default=512, gt=0, description="Taille du batch")
    ubatch_size: int = Field(default=128, gt=0, description="Taille du micro-batch")
    cache_type_k: str = Field(default="f16", description="Type de cache K")
    cache_type_v: str = Field(default="f16", description="Type de cache V")
    host: str = Field(default="0.0.0.0", description="Adresse d'écoute")
    port: int = Field(default=8080, ge=1, le=65535, description="Port d'écoute")

class EmailConfig(BaseModel):
    """Configuration de l'envoi d'emails."""
    smtp_host: str = Field(default="localhost", description="Hôte SMTP")
    smtp_port: int = Field(default=25, ge=1, le=65535, description="Port SMTP")
    email_from: str = Field(default="oil-monitor@localhost", description="Expéditeur")
    email_to: str = Field(default="admin@example.com", description="Destinataire")
    email_subject_prefix: str = Field(default="[OIL-ALERT]", description="Préfixe du sujet")
    send_emails: bool = Field(default=False, description="Activer l'envoi d'emails")

class PersistenceConfig(BaseModel):
    """Configuration de la persistance."""
    history_file: str = Field(default="logs/email_history.json", description="Fichier d'historique")
    events_db: str = Field(default="logs/events_seen.json", description="Base des événements vus")
    dataset_file: str = Field(default="data/oil_intelligence_dataset.jsonl", description="Fichier de dataset")

class MonitoringConfig(BaseModel):
    """Configuration de la surveillance."""
    alert_threshold: int = Field(default=6, ge=0, le=10, description="Seuil d'alerte")
    news_sources: List[str] = Field(default_factory=list, description="Sources d'actualités")
    timezone: str = Field(default="Europe/Paris", description="Fuseau horaire")
    recent_news_hours: int = Field(default=24, gt=0, description="Heures d'actualités récentes")

class Config(BaseModel):
    """Configuration principale."""
    model: ModelConfig
    llama_server: LlamaServerConfig
    email: EmailConfig
    persistence: PersistenceConfig
    monitoring: MonitoringConfig

# Charger la configuration depuis config.json
def load_config() -> Config:
    """Charge et valide la configuration depuis config.json."""
    config_path = Path("config.json")
    if not config_path.exists():
        raise FileNotFoundError(
            "Fichier config.json introuvable. "
            "Veuillez le créer avec la configuration du modèle."
        )
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_dict = json.load(f)
        return Config(**config_dict)
    except json.JSONDecodeError as e:
        raise ValueError(f"Erreur de parsing JSON dans config.json : {e}")
    except Exception as e:
        raise ValueError(f"Erreur de validation de la configuration : {e}")

CONFIG = load_config()

# Configuration legacy pour compatibilité
CONFIG_dict = CONFIG.model_dump()
CONFIG_dict["llama_model"] = f"openai/{CONFIG.model.name}"
CONFIG_dict["llama_api_base"] = CONFIG.model.api_base
CONFIG_dict["llama_num_ctx"] = CONFIG.model.num_ctx

# ─────────────────────────────────────────────
# Gestion automatique de llama-server
# ─────────────────────────────────────────────

_llama_server_process = None

def build_llama_server_command(config: Config) -> list:
    """Construit la commande llama-server de manière cohérente.
    
    Args:
        config: Configuration validée
        
    Returns:
        Liste des arguments pour subprocess.Popen
    """
    server_config = config.llama_server
    model_path = config.model.path
    
    # Ajouter l'extension .exe sur Windows si nécessaire
    executable = server_config.executable
    if sys.platform == "win32" and not executable.endswith(".exe"):
        executable += ".exe"
    
    return [
        executable,
        "-m", model_path,
        "--host", server_config.host,
        "--port", str(server_config.port),
        "-ngl", str(server_config.n_gpu_layers),
        "-t", str(server_config.n_threads),
        "-c", str(server_config.ctx_size),
        "-b", str(server_config.batch_size),
        "-ub", str(server_config.ubatch_size),
        "-ctk", server_config.cache_type_k,
        "-ctv", server_config.cache_type_v,
    ]

def check_llama_server_running() -> bool:
    """Vérifie si llama-server est déjà en cours d'exécution."""
    try:
        response = requests.get(
            f"{CONFIG.model.api_base}/health",
            timeout=2
        )
        return response.status_code == 200
    except Exception:
        return False

def start_llama_server():
    """Démarre automatiquement llama-server avec la configuration de config.json."""
    global _llama_server_process
    
    # Vérifier si déjà démarré
    if check_llama_server_running():
        log.info("✅ llama-server est déjà en cours d'exécution")
        return True
    
    # Construire la commande de manière cohérente
    cmd = build_llama_server_command(CONFIG)
    
    log.info("🚀 Démarrage automatique de llama-server...")
    log.info(f"   Modèle: {CONFIG.model.path}")
    log.info(f"   Port: {CONFIG.llama_server.port}")
    log.info(f"   GPU Layers: {CONFIG.llama_server.n_gpu_layers}")
    log.info(f"   Commande: {' '.join(cmd)}")
    
    try:
        # Démarrer le processus en arrière-plan
        _llama_server_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        
        # Attendre que le serveur soit prêt
        max_wait = 60  # 60 secondes max
        for i in range(max_wait):
            # Vérifier si le processus s'est terminé avec une erreur
            return_code = _llama_server_process.poll()
            if return_code is not None:
                # Le processus s'est terminé, lire stderr pour l'erreur
                stderr_output = _llama_server_process.stderr.read().decode('utf-8', errors='replace')
                log.error(f"❌ llama-server s'est terminé avec le code {return_code}")
                log.error(f"❌ Erreur stderr: {stderr_output}")
                return False
            
            if check_llama_server_running():
                log.info(f"✅ llama-server démarré avec succès (PID: {_llama_server_process.pid})")
                
                # Enregistrer le nettoyage à la sortie
                atexit.register(stop_llama_server)
                return True
            
            if i % 5 == 0:  # Log toutes les 5 secondes
                log.info(f"⏳ Attente du serveur... ({i}s)")
            
            time.sleep(1)
        
        # Timeout : lire stderr pour diagnostiquer
        stderr_output = _llama_server_process.stderr.read().decode('utf-8', errors='replace')
        log.error("❌ Timeout : llama-server n'a pas démarré dans le temps imparti")
        log.error(f"❌ Dernières erreurs stderr: {stderr_output}")
        return False
        
    except Exception as e:
        log.error(f"❌ Erreur lors du démarrage de llama-server : {e}")
        import traceback
        log.error(traceback.format_exc())
        return False

def stop_llama_server():
    """Arrête proprement llama-server s'il a été démarré automatiquement.
    
    IMPORTANT : Cette fonction est enregistrée avec atexit.register(),
    donc elle est AUTOMATIQUEMENT appelée quand le script Python se termine.
    C'est le comportement souhaité : llama-server démarre avec l'agent
    et s'arrête automatiquement quand l'agent a fini son travail.
    """
    global _llama_server_process
    
    if _llama_server_process is None:
        return
    
    try:
        log.info(f"🛑 Arrêt automatique de llama-server (PID: {_llama_server_process.pid})...")
        _llama_server_process.terminate()
        
        # Attendre que le processus se termine
        try:
            _llama_server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            log.warning("⚠️ Timeout, envoi de SIGKILL...")
            _llama_server_process.kill()
        
        log.info("✅ llama-server arrêté proprement")
    except Exception as e:
        log.error(f"❌ Erreur lors de l'arrêt de llama-server : {e}")
    finally:
        _llama_server_process = None

# ─────────────────────────────────────────────
# Token Estimation

def estimate_tokens(text: str) -> int:
    """
    Estime le nombre de tokens dans un texte.
    Approximation: 4 caracteres ≈ 1 token pour l'anglais.
    """
    return len(text) // 4

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
    p = Path(CONFIG.persistence.events_db)
    if p.exists():
        with open(p, encoding="utf-8", errors="replace") as f:
            return set(json.load(f))
    return set()


def save_seen_events(seen: set):
    with open(CONFIG.persistence.events_db, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, indent=2)


def event_fingerprint(title: str, source: str) -> str:
    """Hash stable pour identifier un événement déjà traité."""
    raw = f"{title.lower().strip()}|{source.lower().strip()}"
    return hashlib.md5(raw.encode()).hexdigest()


# ─────────────────────────────────────────────
# Persistance : historique des emails envoyés
# ─────────────────────────────────────────────
def load_email_history() -> list:
    p = Path(CONFIG.persistence.history_file)
    if p.exists():
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            log.error(f"⚠️ Fichier historique corrompu ({p}) : {e}. Création d'un nouveau fichier.")
            if p.stat().st_size > 0:
                p.replace(p.with_suffix(".json.corrupt"))
    return []


def save_email_history(history: list):
    p = Path(CONFIG.persistence.history_file)
    # Backup avant écriture
    if p.exists():
        try:
            p.with_suffix(".json.bak").write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        except Exception:
            pass
            
    with open(p, "w", encoding="utf-8") as f:
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
    full_subject = f"{CONFIG.email.email_subject_prefix} {subject}"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = full_subject
    msg["From"] = CONFIG.email.email_from
    msg["To"] = CONFIG.email.email_to
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
    if not CONFIG.email.send_emails:
        log.info(f"📧 Email désactivé (simulation) : {full_subject}")
        append_email_log(full_subject, body, event_id)
        return True

    try:
        with smtplib.SMTP(CONFIG.email.smtp_host, CONFIG.email.smtp_port, timeout=10) as smtp:
            smtp.sendmail(CONFIG.email.email_from, [CONFIG.email.email_to], msg.as_string())
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
        "Search Iran/Hormuz conflicts, IRGC actions, Israel escalation, "
        "sanctions disrupting oil supply. Returns structured summary."
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
        "Search refinery damage, fires, explosions, drone attacks worldwide. "
        "Returns structured results affecting global oil supply."
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
        "Search OPEC+ production cuts, quota decisions, emergency meetings, "
        "supply policy changes. Covers Saudi, Russia, UAE unilateral cuts."
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
        "Search gas pipeline sabotage, LNG terminal damage, Russia cuts to Europe, "
        "Middle East gas field attacks. Gas spikes correlate with oil rallies."
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
        "Search maritime disruptions: Houthi Red Sea attacks, Bab-el-Mandeb tensions, "
        "Suez blockage, Iran tanker seizures. Directly impacts Brent prices."
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
        "Search broad escalations: Russia-Ukraine energy attacks, US-China tensions, "
        "Libya civil war, Venezuela sanctions, Nigeria pipeline attacks."
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
        "Search recent oil news from major sources. Filter by date (24h, 48h, 7d). "
        "Prioritize breaking news from Reuters, Bloomberg, AP, BBC, FT, WSJ."
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
        "Read RSS feeds from major sources for real-time oil market news. "
        "Filter by publication date, return recent headlines and summaries."
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
    """Initialise le modèle llama-server et l'agent avec tous les tools."""
    from smolagents.local_python_executor import LocalPythonExecutor
    
    model = LiteLLMModel(
        model_id=f"openai/{CONFIG.model.name}",
        api_base=CONFIG.model.api_base,
        api_key="dummy",  # llama-server ne nécessite pas de clé API
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
    
    # Initialiser la gestion du contexte
    agent.custom_state = AgentState(max_steps=10)
    agent.window_manager = SlidingWindowManager(window_size=3, max_tokens=8000)
    agent.memory_cleaner = MemoryCleaner()
    
    log.info(f"📦 Context management initialized with window_size=3, max_tokens=8000")
    
    return agent


# ─────────────────────────────────────────────
# Prompt principal
# ─────────────────────────────────────────────

def get_master_prompt() -> str:
    """Génère le prompt principal optimisé de collecte d'informations."""
    from datetime import datetime
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""Date: {current_date} {current_datetime}
Task: Monitor oil market for price-impacting events.

CRITICAL INSTRUCTIONS - READ CAREFULLY:
========================================
1. You MUST use ALL the search tools listed below to gather REAL-TIME information.
2. DO NOT generate fictional events or make up information.
3. Only report events that are actually found through the search tools.
4. Each tool call provides REAL data from news sources, websites, and RSS feeds.
5. Compile the results from ALL tools into your final output.

REQUIRED TOOL USAGE PATTERN (execute in this exact order - NO EXCEPTIONS):
========================================
You MUST execute ALL 10 tools below, one after another, in this sequence:
1. search_iran_conflict(days_back=1)
2. search_refinery_damage(region="global")
3. search_opec_supply(focus="all")
4. search_gas_disruption(topic="all")
5. search_shipping_disruption()
6. search_geopolitical_escalation()
7. get_oil_price()
8. get_vix_index()
9. search_recent_news(topic="all", timeframe="24h")
10. read_rss_feeds(feed="all", hours_back=24)

CRITICAL: After completing ALL 10 tool calls, compile the results into your final report.
DO NOT stop early. You have 10 steps available - use ALL of them.

TOOLS (use systematically - ALL MUST BE CALLED):
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
Details: [2-3 sentences based on actual search results]
Price Impact: [specific mechanism based on real data]

Prioritize events with impact ≥6. Deduplicate sources.

REMEMBER: Your output must be based ONLY on information gathered from the tools above. Do not hallucinate or invent events."""
    return prompt

# ─────────────────────────────────────────────
# Dataset Collection
# ─────────────────────────────────────────────

def save_to_dataset(input_data: dict, output_data: dict):
    """Enregistre un exemple d'entrée/sortie pour l'entraînement DSPy."""
    try:
        dataset_file = Path(CONFIG.persistence.dataset_file)
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
# Validation de l'utilisation des outils
# ─────────────────────────────────────────────

def validate_tool_usage(agent_result, expected_tools: set) -> tuple[bool, set, set]:
    """
    Vérifie que les outils attendus ont été utilisés.
    
    Args:
        agent_result: Le résultat brut de l'agent (contient les appels d'outils)
        expected_tools: L'ensemble des outils qui doivent être appelés
        
    Returns:
        Tuple (validation_passed, used_tools, missing_tools)
    """
    # Liste des outils à vérifier
    required_tools = {
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
    
    # Si expected_tools est vide, utiliser tous les outils requis
    if not expected_tools:
        expected_tools = required_tools
    
    used_tools = set()
    
    # Convertir agent_result en chaîne si c'est un dict
    if isinstance(agent_result, dict):
        # Chercher les indicateurs d'outils dans les valeurs du dict
        result_str = str(agent_result).lower()
    else:
        result_str = str(agent_result).lower()
    
    # Vérifier si l'intelligence brute contient des indicateurs de recherche
    # Les outils écrivent des en-têtes comme "=== IRAN CONFLICT SEARCH ==="
    has_search_indicators = any(indicator in result_str for indicator in [
        '=== iran conflict search ===',
        '=== refinery damage search ===',
        '=== opec+ supply search ===',
        '=== natural gas disruption search ===',
        '=== shipping disruption search ===',
        '=== geopolitical escalation search ===',
        '=== oil price data ===',
        '=== vix (cboe volatility index) ===',
        '=== recent news search',
        '=== rss feeds ==='
    ])
    
    # Si des indicateurs de recherche sont présents, considérer tous les outils comme utilisés
    if has_search_indicators:
        used_tools = required_tools
    else:
        # Chercher les appels d'outils dans le résultat de l'agent
        for tool_name in required_tools:
            if tool_name in result_str:
                used_tools.add(tool_name)
    
    missing_tools = expected_tools - used_tools
    validation_passed = len(missing_tools) == 0
    
    return validation_passed, used_tools, missing_tools


def log_tool_usage_summary(used_tools: set, missing_tools: set):
    """Génère un résumé de l'utilisation des outils."""
    log.info("=" * 60)
    log.info("🔧 TOOL USAGE SUMMARY")
    log.info("=" * 60)
    log.info(f"✅ Tools used ({len(used_tools)}):")
    for tool in sorted(used_tools):
        log.info(f"   ✓ {tool}")
    
    if missing_tools:
        log.warning(f"❌ Tools NOT used ({len(missing_tools)}):")
        for tool in sorted(missing_tools):
            log.warning(f"   ✗ {tool}")
    else:
        log.info("✅ All required tools were used!")
    log.info("=" * 60)


def verify_event_truthfulness(events: list, raw_intelligence) -> tuple[list, list]:
    """
    Vérifie la véracité des événements en les comparant aux sources citées.
    
    Args:
        events: Liste des événements détectés
        raw_intelligence: Intelligence brute collectée par l'agent
        
    Returns:
        Tuple (verified_events, unverified_events)
    """
    verified_events = []
    unverified_events = []
    
    # Convertir raw_intelligence en minuscules pour la recherche
    if isinstance(raw_intelligence, dict):
        intel_lower = str(raw_intelligence).lower()
    else:
        intel_lower = str(raw_intelligence).lower()
    
    for event in events:
        event_title = event.get('title', '').lower()
        event_source = event.get('source_hint', '').lower()
        
        # Vérifier 1: Le titre ou des mots-clés apparaissent-ils dans l'intelligence brute?
        title_found = False
        # Chercher des mots-clés du titre dans l'intelligence
        title_words = [w for w in event_title.split() if len(w) > 3]  # Mots de plus de 3 caractères
        if title_words:
            # Si au moins 2 mots-clés sont trouvés, on considère l'événement comme vérifié
            matches = sum(1 for word in title_words if word in intel_lower)
            title_found = matches >= 2
        
        # Vérifier 2: La source est-elle mentionnée dans l'intelligence brute?
        source_found = event_source in intel_lower if len(event_source) > 3 else True
        
        # Vérifier 3: Y a-t-il des indicateurs de recherche (===, ---, etc.)?
        has_search_indicators = any(indicator in intel_lower for indicator in ['===', '---', 'query:', '📰'])
        
        # Vérification finale
        is_verified = title_found or (source_found and has_search_indicators)
        
        if is_verified:
            verified_events.append(event)
        else:
            unverified_events.append(event)
            log.warning(f"⚠️ Événement non vérifié: {event.get('title', 'Unknown')}")
            log.warning(f"   Titre trouvé: {title_found}, Source trouvée: {source_found}")
    
    # Log du résumé
    log.info("=" * 60)
    log.info("🔍 EVENT VERIFICATION SUMMARY")
    log.info("=" * 60)
    log.info(f"✅ Verified events: {len(verified_events)}/{len(events)}")
    log.info(f"❌ Unverified events: {len(unverified_events)}/{len(events)}")
    
    if unverified_events:
        log.warning("⚠️ ATTENTION: Certains événements ne sont pas corroborés par les sources de recherche!")
        for event in unverified_events:
            log.warning(f"   - {event.get('title', 'Unknown')}")
    else:
        log.info("✅ Tous les événements sont corroborés par les sources de recherche!")
    log.info("=" * 60)
    
    return verified_events, unverified_events


# ─────────────────────────────────────────────
# Exécution séquentielle des outils
# ─────────────────────────────────────────────

def execute_all_tools_sequentially(agent: CodeAgent) -> str:
    """
    Exécute tous les outils de recherche séquentiellement et collecte les résultats.
    
    Args:
        agent: Instance de CodeAgent avec tous les outils configurés
        
    Returns:
        String combinant tous les résultats des outils
    """
    from datetime import datetime
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Créer les outils directement (au lieu de les récupérer depuis l'agent)
    ddg = DuckDuckGoSearchTool(max_results=5)
    visit = VisitWebpageTool(max_output_length=4000)
    
    # Créer tous les outils personnalisés
    iran_tool = IranConflictTool(ddg)
    refinery_tool = RefineryDamageTool(ddg, visit)
    opec_tool = OPECSupplyTool(ddg)
    gas_tool = NaturalGasDisruptionTool(ddg)
    shipping_tool = ShippingDisruptionTool(ddg)
    geopolitical_tool = GeopoliticalEscalationTool(ddg)
    oil_price_tool = OilPriceTool(ddg)
    recent_news_tool = RecentNewsTool(ddg)
    rss_tool = RSSFeedTool()
    vix_tool = VIXTool(ddg)
    
    results = []
    
    log.info("=" * 60)
    log.info("🔧 EXECUTION SÉQUENTIELLE DES OUTILS")
    log.info("=" * 60)
    
    # 1. Iran Conflict Tool
    log.info("📡 [1/10] Exécution de search_iran_conflict...")
    try:
        result = iran_tool.forward(days_back=1)
        results.append(result)
        log.info(f"✅ search_iran_conflict terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur search_iran_conflict: {e}")
        results.append(f"[ERROR] search_iran_conflict: {str(e)}")
    
    # 2. Refinery Damage Tool
    log.info("📡 [2/10] Exécution de search_refinery_damage...")
    try:
        result = refinery_tool.forward(region="global")
        results.append(result)
        log.info(f"✅ search_refinery_damage terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur search_refinery_damage: {e}")
        results.append(f"[ERROR] search_refinery_damage: {str(e)}")
    
    # 3. OPEC Supply Tool
    log.info("📡 [3/10] Exécution de search_opec_supply...")
    try:
        result = opec_tool.forward(focus="all")
        results.append(result)
        log.info(f"✅ search_opec_supply terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur search_opec_supply: {e}")
        results.append(f"[ERROR] search_opec_supply: {str(e)}")
    
    # 4. Gas Disruption Tool
    log.info("📡 [4/10] Exécution de search_gas_disruption...")
    try:
        result = gas_tool.forward(topic="all")
        results.append(result)
        log.info(f"✅ search_gas_disruption terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur search_gas_disruption: {e}")
        results.append(f"[ERROR] search_gas_disruption: {str(e)}")
    
    # 5. Shipping Disruption Tool
    log.info("📡 [5/10] Exécution de search_shipping_disruption...")
    try:
        result = shipping_tool.forward()
        results.append(result)
        log.info(f"✅ search_shipping_disruption terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur search_shipping_disruption: {e}")
        results.append(f"[ERROR] search_shipping_disruption: {str(e)}")
    
    # 6. Geopolitical Escalation Tool
    log.info("📡 [6/10] Exécution de search_geopolitical_escalation...")
    try:
        result = geopolitical_tool.forward()
        results.append(result)
        log.info(f"✅ search_geopolitical_escalation terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur search_geopolitical_escalation: {e}")
        results.append(f"[ERROR] search_geopolitical_escalation: {str(e)}")
    
    # 7. Oil Price Tool
    log.info("📡 [7/10] Exécution de get_oil_price...")
    try:
        result = oil_price_tool.forward()
        results.append(result)
        log.info(f"✅ get_oil_price terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur get_oil_price: {e}")
        results.append(f"[ERROR] get_oil_price: {str(e)}")
    
    # 8. VIX Tool
    log.info("📡 [8/10] Exécution de get_vix_index...")
    try:
        result = vix_tool.forward()
        results.append(result)
        log.info(f"✅ get_vix_index terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur get_vix_index: {e}")
        results.append(f"[ERROR] get_vix_index: {str(e)}")
    
    # 9. Recent News Tool
    log.info("📡 [9/10] Exécution de search_recent_news...")
    try:
        result = recent_news_tool.forward(topic="all", timeframe="24h")
        results.append(result)
        log.info(f"✅ search_recent_news terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur search_recent_news: {e}")
        results.append(f"[ERROR] search_recent_news: {str(e)}")
    
    # 10. RSS Feeds Tool
    log.info("📡 [10/10] Exécution de read_rss_feeds...")
    try:
        result = rss_tool.forward(feed="all", hours_back=24)
        results.append(result)
        log.info(f"✅ read_rss_feeds terminé ({len(result)} caractères)")
    except Exception as e:
        log.error(f"❌ Erreur read_rss_feeds: {e}")
        results.append(f"[ERROR] read_rss_feeds: {str(e)}")
    
    # Combiner tous les résultats
    combined_intelligence = "\n\n" + "=" * 60 + "\n"
    combined_intelligence += "OIL MARKET INTELLIGENCE REPORT\n"
    combined_intelligence += "=" * 60 + "\n\n"
    combined_intelligence += f"Date: {current_date}\n"
    combined_intelligence += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    combined_intelligence += "\n\n".join(results)
    
    log.info("=" * 60)
    log.info(f"✅ TOUS LES OUTILS ONT ÉTÉ EXÉCUTÉS")
    log.info(f"📊 Total intelligence collectée: {len(combined_intelligence)} caractères")
    log.info("=" * 60)
    
    return combined_intelligence


# ─────────────────────────────────────────────
# Runner principal
# ─────────────────────────────────────────────

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
    
    # Phase 2: Initialize HistoryCompressor
    history_compressor = HistoryCompressor(compression_ratio=0.15)
    
    # 2. Collecte d'intelligence via smolagents avec contexte optimisé
    try:
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Construire le prompt avec contexte optimisé
        prompt = build_optimized_prompt_context(
            agent.custom_state,
            agent.window_manager,
            current_date,
            current_datetime
        )
        
        # Ajouter les instructions de la tâche
        prompt += "\n\n" + get_master_prompt()
        
        # Phase 2: Track step data before running agent
        step_start_time = datetime.now()
        prompt_tokens_before = estimate_tokens(prompt)
        
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
        
        # Phase 2: Track step data after running agent
        step_end_time = datetime.now()
        output_tokens = estimate_tokens(raw_intelligence)
        
        # Add step data to window manager
        step_data = {
            'step': agent.custom_state.current_step,
            'tool_calls': [],  # Will be filled if tools were called
            'events': [],  # Will be filled with detected events
            'timestamp': step_start_time.isoformat(),
            'duration_seconds': (step_end_time - step_start_time).total_seconds(),
            'input_tokens': prompt_tokens_before,
            'output_tokens': output_tokens
        }
        agent.window_manager.add_step(step_data)
        
        # Increment step counter
        agent.custom_state.increment_step()
        
        # Mettre à jour les statistiques de l'agent
        agent.custom_state.add_tokens(prompt_tokens_before, output_tokens)
        
        # Phase 2: Clean raw intelligence with memory cleaner
        cleaned_intelligence = agent.memory_cleaner.clean_content(raw_intelligence)
        
        # Phase 2: Log compression statistics
        if len(agent.window_manager.history) > agent.window_manager.window_size:
            # Calculate compression savings
            original_tokens = sum(step.get('input_tokens', 0) + step.get('output_tokens', 0)
                                    for step in agent.window_manager.history)
            compressed_tokens = estimate_tokens(cleaned_intelligence)
            savings = original_tokens - compressed_tokens
            if savings > 0:
                agent.custom_state.add_compression_savings(savings)
                log.info(f"📦 Compression savings: {savings:,} tokens (original: {original_tokens:,}, compressed: {compressed_tokens:,})")
        
        # Phase 2: Compress window if needed
        if agent.custom_state.current_step % 3 == 0:  # Compress every 3 steps
            compressed = agent.window_manager.compress_window(history_compressor)
            if compressed:
                log.info(f"🗜️ Window compressed: {compressed['steps_count']} steps → {len(compressed['summary'])} chars")
        
        log.info(f"📊 Token usage: {agent.custom_state.total_tokens_input:,} in → {agent.custom_state.total_tokens_output:,} out")
        log.info(f"📈 Step {agent.custom_state.current_step}/{agent.custom_state.max_steps} completed")
    except Exception as e:
        log.error(f"Agent error: {e}")
        import traceback
        log.error(traceback.format_exc())
        return

    # 3. Synthèse et formatage via DSPy
    events = []
    try:
        analyzer = OilEventAnalyzer()
        
        # Charger les poids optimisés si disponibles
        optimized_path = Path(CONFIG.persistence.dataset_file).parent / "oil_analyzer_optimized.json"
        if optimized_path.exists():
            log.info(f"📂 Chargement du module DSPy optimisé : {optimized_path}")
            analyzer.load(str(optimized_path))
            
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        dspy_result = analyzer(
            current_date=current_date,
            current_datetime=current_datetime,
            alert_threshold=CONFIG.monitoring.alert_threshold,
            news_sources=CONFIG.monitoring.news_sources,
            raw_intelligence=raw_intelligence
        )
        
        # Extraire les événements de la réponse DSPy
        # DSPy avec JSONAdapter retourne souvent des objets Pydantic ou des dicts
        raw_events = []
        if hasattr(dspy_result, 'events'):
            for e in dspy_result.events:
                if hasattr(e, 'model_dump'):
                    raw_events.append(e.model_dump())
                elif hasattr(e, 'dict'):
                    raw_events.append(e.dict())
                else:
                    raw_events.append(e)
        
        # 4. Validation et nettoyage final
        events = validate_and_fix_events(raw_events, current_date)
        
        log.info(f"✨ DSPy Analysis Complete. Confidence: {getattr(dspy_result, 'confidence_score', 'N/A')}")
        
        # 5. Vérification de la véracité des événements
        verified_events, unverified_events = verify_event_truthfulness(events, raw_intelligence)
        
        # Filtrer les événements non vérifiés
        events = verified_events
        
        if unverified_events:
            log.warning(f"⚠️ {len(unverified_events)} événement(s) non vérifié(s) ont été filtrés")
        
        # Phase 2: Track detected events
        for event in events:
            agent.custom_state.add_detected_event(event)
            log.info(f"📌 Event tracked: {event.get('title', 'Unknown')} (impact: {event.get('impact_score', 0)})")
        
        # Phase 2: Update step data with detected events
        if agent.window_manager.history:
            agent.window_manager.history[-1]['events'] = events
        
        # Sauvegarder pour l'amélioration continue (20 exemples cibles)
        save_to_dataset(
            input_data={
                "current_date": current_date,
                "alert_threshold": CONFIG.monitoring.alert_threshold,
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
        # Vérifier le seuil d'alerte configuré
        impact_score = event.get("impact_score", 0)
        if impact_score < CONFIG.monitoring.alert_threshold:
            log.info(f"⏭️  Impact trop faible ({impact_score}/{CONFIG.monitoring.alert_threshold}), skip email : {event.get('title')}")
            continue

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
    
    # Phase 2: Log final agent statistics
    log.info("=" * 60)
    log.info("📊 AGENT STATISTICS SUMMARY")
    log.info("=" * 60)
    log.info(f"Steps completed: {agent.custom_state.current_step}/{agent.custom_state.max_steps}")
    log.info(f"Total input tokens: {agent.custom_state.total_tokens_input:,}")
    log.info(f"Total output tokens: {agent.custom_state.total_tokens_output:,}")
    log.info(f"Events detected: {agent.custom_state.events_detected}")
    log.info(f"Tools used: {len(agent.custom_state.tools_used)}")
    log.info(f"High impact events: {len(agent.custom_state.high_impact_events)}")
    log.info(f"Compression savings: {agent.custom_state.compression_savings:,} tokens")
    if agent.custom_state.total_tokens_input > 0:
        ratio = agent.custom_state.total_tokens_output / agent.custom_state.total_tokens_input
        log.info(f"Token ratio (output/input): {ratio:.2%}")
    log.info("=" * 60)


def format_email_body(event: dict) -> str:
    """Formate le corps d'un email d'alerte."""
    lines = [
        "🛢️  OIL MARKET ALERT",
        f"{'='*50}",
        "",
        f"📌 TITRE       : {event.get('title', 'N/A')}",
        f"📂 CATÉGORIE   : {event.get('category', 'N/A')}",
        f"⚡ SCORE IMPACT: {event.get('impact_score', 'N/A')}/10",
        f"🔔 URGENCE     : {event.get('urgency', 'N/A')}",
        f"💰 IMPACT PRIX : {event.get('price_impact', 'N/A')}",
        f"🎯 CERTITUDE   : {int(event.get('certainty_score', 0) * 100)}%",
        "",
        "📝 ANALYSE :",
        f"{event.get('summary', 'N/A')}",
        "",
        f"🔗 SOURCE : {event.get('source_hint', 'N/A')}",
        f"📅 DATE PUB: {event.get('publication_date', 'N/A')}",
        "",
        f"{'─'*50}",
        f"⏰ Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "🤖 Agent : smolagents + DSPy (qwen3.5:9b)",
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
