import dspy
from dspy.teleprompt import BootstrapFewShot
import json
import os
from pathlib import Path
from datetime import datetime
from oil_agent import OilEventAnalyzer, CONFIG, configure_dspy

# Configuration
OPTIMIZED_MODULE_PATH = "data/oil_analyzer_optimized.json"

def load_dataset():
    """Charge le dataset d'exemples collectés."""
    dataset_path = Path(CONFIG["persistence"]["dataset_file"])
    if not dataset_path.exists():
        print(f"❌ Dataset non trouvé : {dataset_path}")
        return []
    
    examples = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            # Créer un exemple DSPy
            # Note: Les entrées doivent correspondre aux champs de la signature
            example = dspy.Example(
                current_date=data["input"]["current_date"],
                current_datetime=data.get("timestamp", datetime.now().isoformat()),
                alert_threshold=data["input"]["alert_threshold"],
                news_sources=CONFIG["monitoring"]["news_sources"],
                raw_intelligence=data["input"]["raw_intelligence"],
                events=data["output"]["events"]
            ).with_inputs("current_date", "current_datetime", "alert_threshold", "news_sources", "raw_intelligence")
            examples.append(example)
            
    print(f"✅ {len(examples)} exemples chargés.")
    return examples

def metric(gold, pred, trace=None):
    """
    Métrique de validation pour l'optimisation.
    Score basé sur la validité du format et la pertinence.
    """
    score = 0.0
    
    # 1. Vérifier si on a des événements (si le gold en a)
    gold_has_events = len(gold.events) > 0
    pred_has_events = len(pred.events) > 0
    
    if gold_has_events == pred_has_events:
        score += 0.4
    
    if pred_has_events:
        # 2. Vérifier la structure des événements prédits
        valid_events = 0
        for event in pred.events:
            # Vérifier les champs obligatoires
            required_fields = ["category", "impact_score", "title", "summary", "publication_date"]
            if all(k in event and event[k] for k in required_fields):
                # Vérifier si le score d'impact est dans les bornes
                if 0 <= event["impact_score"] <= 10:
                    valid_events += 1
        
        if len(pred.events) > 0:
            score += 0.3 * (valid_events / len(pred.events))
            
        # 3. Vérifier le score de confiance
        if hasattr(pred, 'confidence_score') and 0.0 <= pred.confidence_score <= 1.0:
            score += 0.3
            
    elif not gold_has_events:
        # Si aucun événement n'était attendu et aucun n'est prédit, c'est parfait
        score += 0.6
        
    return score

def optimize():
    """Lance le processus d'optimisation DSPy."""
    # Configurer le modèle
    print("🚀 Configuration du modèle llama-server...")
    configure_dspy()
    
    # Charger les données
    trainset = load_dataset()
    if len(trainset) < 5:
        print("⚠️ Pas assez de données pour une optimisation efficace (min 5 exemples).")
        print("💡 Continuez à faire tourner oil_agent.py pour collecter plus de données.")
        return

    # Initialiser le module non-optimisé
    student = OilEventAnalyzer()
    
    # Configurer l'optimiseur
    # BootstrapFewShot va sélectionner les meilleurs exemples pour les inclure dans le prompt
    teleprompter = BootstrapFewShot(metric=metric, max_bootstrapped_demos=3)
    
    print("🧠 Début de l'optimisation (BootstrapFewShot)...")
    optimized_analyzer = teleprompter.compile(student, trainset=trainset)
    
    # Sauvegarder le module optimisé
    optimized_analyzer.save(OPTIMIZED_MODULE_PATH)
    print(f"💾 Module optimisé sauvegardé dans : {OPTIMIZED_MODULE_PATH}")
    
    return optimized_analyzer

if __name__ == "__main__":
    import sys
    
    if "run" in sys.argv:
        # Charger et tester le module optimisé
        if os.path.exists(OPTIMIZED_MODULE_PATH):
            print(f"📂 Chargement du module optimisé : {OPTIMIZED_MODULE_PATH}")
            analyzer = OilEventAnalyzer()
            analyzer.load(OPTIMIZED_MODULE_PATH)
            
            # Exemple de test rapide
            configure_dspy()
            test_intel = "Breaking: Houthi drones attacked a tanker in the Red Sea 2 hours ago. Reuters reports minor damage but Suez traffic is nervous."
            res = analyzer(
                current_date=datetime.now().strftime("%Y-%m-%d"),
                current_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                alert_threshold=6,
                news_sources=CONFIG["monitoring"]["news_sources"],
                raw_intelligence=test_intel
            )
            print("\n--- TEST RESULT ---")
            print(json.dumps(res.events, indent=2, ensure_ascii=False))
        else:
            print("❌ Aucun module optimisé trouvé. Lancez 'python optimize_agent.py' d'abord.")
    else:
        optimize()
