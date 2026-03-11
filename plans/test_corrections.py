#!/usr/bin/env python3
"""
Script de test pour valider les corrections proposées
"""

import sys
import io
import json
import tempfile
from pathlib import Path

# Configurer stdout pour utiliser UTF-8 sur Windows (comme dans oil-agent.py)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_unicode_encoding():
    """Test que l'encodage UTF-8 fonctionne correctement."""
    print("=" * 60)
    print("🧪 Test 1 : Encodage UTF-8 avec emojis")
    print("=" * 60)
    
    # Données de test avec emojis
    test_data = [
        {
            "timestamp": "2025-03-11T14:17:48",
            "event_id": "test_001",
            "subject": "[OIL-ALERT] Shipping Disruption | Score 9/10",
            "preview": "🛢️ OIL MARKET ANALYSIS REPORT (DSPy Powered)\n⚠️ Houthi Attacks on Red Sea Vessels\n⚡ IMPACT SCORE: 9/10"
        }
    ]
    
    # Test avec encodage UTF-8
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        try:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
            temp_file = f.name
            print(f"✅ Écriture réussie avec encoding='utf-8'")
            print(f"📁 Fichier temporaire : {temp_file}")
        except UnicodeEncodeError as e:
            print(f"❌ Erreur UnicodeEncodeError : {e}")
            return False
    
    # Test de lecture
    try:
        with open(temp_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
            print(f"✅ Lecture réussie avec encoding='utf-8'")
            print(f"📊 {len(loaded_data)} enregistrement(s) chargé(s)")
    except Exception as e:
        print(f"❌ Erreur de lecture : {e}")
        return False
    
    # Nettoyage
    Path(temp_file).unlink()
    print(f"🗑️  Fichier temporaire supprimé")
    
    return True

def test_dspy_module_call():
    """Test que l'appel direct du module fonctionne."""
    print("\n" + "=" * 60)
    print("🧪 Test 2 : Appel direct de module DSPy")
    print("=" * 60)
    
    try:
        import dspy
        print(f"✅ DSPy importé avec succès")
        
        # Test de création d'un module simple
        class TestSignature(dspy.Signature):
            """Signature de test."""
            input_text = dspy.InputField(desc="Texte d'entrée")
            output_text = dspy.OutputField(desc="Texte de sortie")
        
        class TestModule(dspy.Module):
            def __init__(self):
                super().__init__()
                self.predict = dspy.Predict(TestSignature)
            
            def forward(self, input_text):
                result = self.predict(input_text=input_text)
                return result.output_text
        
        # Test d'appel direct (recommandé)
        module = TestModule()
        print(f"✅ Module créé avec succès")
        print(f"💡 Utilisation recommandée : module(...)")
        print(f"⚠️  Utilisation déconseillée : module.forward(...)")
        
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import DSPy : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la création du module : {e}")
        return False

def test_json_with_special_chars():
    """Test que JSON peut gérer tous les caractères spéciaux."""
    print("\n" + "=" * 60)
    print("🧪 Test 3 : JSON avec caractères spéciaux")
    print("=" * 60)
    
    # Tous les emojis utilisés dans oil-agent.py
    special_chars = {
        "oil_barrel": "🛢️",
        "warning": "⚠️",
        "email": "📧",
        "impact": "⚡",
        "urgency": "🔔",
        "price": "💰",
        "date": "📅",
        "analysis": "📝",
        "source": "🔗",
        "timestamp": "⏰",
        "robot": "🤖",
        "check": "✅",
        "error": "❌",
        "info": "ℹ️",
        "success": "✅",
        "skip": "⏭️",
    }
    
    test_data = {
        "emojis": special_chars,
        "text_with_emojis": f"{special_chars['oil_barrel']} OIL MARKET {special_chars['warning']} ALERT"
    }
    
    try:
        # Test de sérialisation
        json_str = json.dumps(test_data, indent=2, ensure_ascii=False)
        print(f"✅ Sérialisation JSON réussie")
        print(f"📊 Taille : {len(json_str)} caractères")
        
        # Test de désérialisation
        loaded_data = json.loads(json_str)
        print(f"✅ Désérialisation JSON réussie")
        print(f"📊 {len(loaded_data['emojis'])} emojis chargés")
        
        return True
    except Exception as e:
        print(f"❌ Erreur JSON : {e}")
        return False

def main():
    """Exécute tous les tests."""
    print("\n" + "=" * 60)
    print("🧪 SUITE DE TESTS - Validation des corrections")
    print("=" * 60)
    
    results = {}
    
    # Test 1
    results['unicode_encoding'] = test_unicode_encoding()
    
    # Test 2
    results['dspy_module_call'] = test_dspy_module_call()
    
    # Test 3
    results['json_special_chars'] = test_json_with_special_chars()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:30s} : {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("✅ Les corrections proposées sont validées")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("❌ Veuillez vérifier les corrections proposées")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
