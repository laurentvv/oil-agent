"""
Module DSPy amélioré pour l'analyse du marché pétrolier.

Améliorations par rapport au module original :
1. Fingerprint amélioré avec résumé
2. Déduplication basée sur le contenu complet
3. Consolidation avec déduplication interne
4. Validation JSON intégrée
"""

import dspy
import json
import hashlib
import logging

# Configuration du logging
log = logging.getLogger(__name__)

# Configuration pour la déduplication temporelle (24h)
DEDUPLICATION_WINDOW_HOURS = 24

class OilAnalysisSignature(dspy.Signature):
    """
    Analyse les données brutes d'intelligence sur le marché pétrolier.
    Le rapport doit inclure une liste d'événements à fort impact avec leur catégorie,
    score d'impact, urgence, résumé détaillé, impact sur les prix, et source.
    """
    raw_intelligence = dspy.InputField(desc="Données brutes collectées des outils et sources d'actualités.")
    current_date = dspy.InputField(desc="La date actuelle au format YYYY-MM-DD.")
    
    report = dspy.OutputField(
        desc='''Une liste JSON structurée d'événements avec les champs :
              category, title, impact_score (1-10), urgency (Breaking/Recent/Background),
              summary, price_impact, source_hint, publication_date.'''
    )


class OilAnalyst(dspy.Module):
    """Module d'analyse du marché pétrolier avec déduplication améliorée."""
    
    def __init__(self, num_trials=5):
        super().__init__()
        self.analyze = dspy.ChainOfThought(OilAnalysisSignature)
        self.num_trials = num_trials
        self.logger = logging.getLogger(__name__)
    
    def forward(self, raw_intelligence, current_date):
        """Exécute l'analyse avec multi-trial et consolidation."""
        reports = []
        
        for i in range(self.num_trials):
            prediction = self.analyze(
                raw_intelligence=raw_intelligence,
                current_date=current_date
            )
            reports.append(prediction.report)
            self.logger.info(f"  Trial {i+1}/{self.num_trials} complété")
        
        # Consolidation avec déduplication
        return self.consolidate(reports, raw_intelligence, current_date)
    
    def consolidate(self, reports, raw_intelligence, current_date):
        """Consolide plusieurs rapports en un seul avec déduplication."""
        # 1. Parser tous les rapports
        parsed_reports = []
        for report in reports:
            try:
                events = json.loads(report)
                parsed_reports.extend(events)
            except Exception as e:
                self.logger.warning(f"Erreur de parsing JSON: {e}")
                continue
        
        # 2. Dédupliquer les événements par contenu
        unique_events = []
        seen_hashes = set()
        
        for event in parsed_reports:
            event_hash = self.event_content_hash(event)
            
            if event_hash not in seen_hashes:
                unique_events.append(event)
                seen_hashes.add(event_hash)
        
        # 3. Retourner les événements uniques en JSON
        import json
        return json.dumps(unique_events, indent=2, ensure_ascii=False)
    
    def event_content_hash(self, event: dict) -> str:
        """Génère un hash basé sur le contenu de l'événement."""
        return event_content_hash(event)


def event_content_hash(event: dict) -> str:
    """Génère un hash basé sur le contenu de l'événement."""
    title = event.get("title", "").lower().strip()
    category = event.get("category", "").lower().strip()
    summary = event.get("summary", "")[:300]  # Tronquer pour éviter les variations mineures
    urgency = event.get("urgency", "").lower().strip()
    
    # Créer un hash basé sur titre + catégorie + résumé + urgence
    raw = f"{title}|{category}|{summary}|{urgency}"
    return hashlib.md5(raw.encode()).hexdigest()


def setup_dspy(model_id, api_base, temperature=0.3, max_tokens=2000):
    """
    Configure DSPy avec le modèle Ollama spécifié.
    
    Args:
        model_id: ID du modèle (ex: 'ollama_chat/qwen3.5:9b')
        api_base: URL de l'API Ollama (ex: 'http://127.0.0.1:11434')
        temperature: Température pour la créativité (0.0-1.0)
        max_tokens: Nombre maximum de tokens en sortie
    
    Returns:
        Instance LM configurée
    """
    model_name = model_id.split('/')[-1] if '/' in model_id else model_id
    
    try:
        lm = dspy.LM(
            f"ollama_chat/{model_name}",
            api_base=api_base,
            api_key="ollama",
            temperature=temperature,
            max_tokens=max_tokens
        )
        dspy.settings.configure(lm=lm)
        return lm
    except Exception as e:
        log.error(f"Erreur de configuration DSPy: {e}")
        raise


def event_fingerprint(title: str, category: str) -> str:
    """
    Hash stable pour identifier un événement déjà traité.
    Utilise le titre et la catégorie pour une meilleure déduplication.
    """
    raw = f"{title.lower().strip()}|{category.lower().strip()}"
    return hashlib.md5(raw.encode()).hexdigest()


def is_duplicate_event(new_event: dict, seen_events: set) -> bool:
    """
    Vérifie si un événement est un doublon basé sur le contenu.
    """
    new_hash = event_content_hash(new_event)
    
    for seen_hash in seen_events:
        if seen_hash == new_hash:
            return True
    
    return False


def is_recent_duplicate(event: dict, seen_events: dict) -> bool:
    """
    Vérifie si un événement est un doublon récent.
    Ignore les doublons détectés dans les dernières 24h.
    """
    event_id = event.get("id") or event_fingerprint(
        event.get("title", ""),
        event.get("category", "")
    )
    
    # Si l'événement n'est pas dans seen_events, ce n'est pas un doublon
    if event_id not in seen_events:
        return False
    
    # Récupérer le timestamp de l'événement vu
    seen_timestamp = seen_events.get(event_id)
    if not seen_timestamp:
        return False
    
    # Vérifier si l'événement a été vu dans les dernières 24h
    from datetime import datetime, timedelta
    event_time = datetime.now()
    seen_time = datetime.fromisoformat(seen_timestamp)
    
    time_diff = event_time - seen_time
    if abs(time_diff.total_seconds()) < DEDUPLICATION_WINDOW_HOURS * 3600:
        return True
    
    return False
