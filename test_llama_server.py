#!/usr/bin/env python3
"""
Script de test pour vérifier que llama-server fonctionne correctement
avec l'agent de surveillance du marché pétrolier.
"""

import requests
import json
from pathlib import Path
import subprocess
import time
import sys
import signal
import os

# Variable globale pour stocker le processus llama-server
llama_server_process = None

def build_llama_server_command(config: dict) -> list:
    """Construit la commande llama-server de manière cohérente.
    
    Cette fonction est partagée avec oil_agent.py pour assurer la cohérence.
    
    Args:
        config: Dictionnaire de configuration
        
    Returns:
        Liste des arguments pour subprocess.Popen
    """
    server_config = config["llama_server"]
    model_path = config["model"]["path"]
    
    # Ajouter l'extension .exe sur Windows si nécessaire
    executable = server_config["executable"]
    if sys.platform == "win32" and not executable.endswith(".exe"):
        executable += ".exe"
    
    # Trouver le chemin complet de l'exécutable
    try:
        result = subprocess.run(["where", executable], capture_output=True, text=True)
        executable_path = result.stdout.strip().split('\n')[0]
    except:
        executable_path = executable
    
    return [
        executable_path,
        "-m", model_path,
        "--host", server_config["host"],
        "--port", str(server_config["port"]),
        "-ngl", str(server_config["n_gpu_layers"]),
        "-t", str(server_config["n_threads"]),
        "-c", str(server_config["ctx_size"]),
        "-b", str(server_config["batch_size"]),
        "-ub", str(server_config["ubatch_size"]),
        "-ctk", server_config["cache_type_k"],
        "-ctv", server_config["cache_type_v"],
    ]

def start_llama_server(config):
    """Démarre llama-server si nécessaire."""
    global llama_server_process
    
    # Vérifier si llama-server est déjà en cours d'exécution
    api_base = config["model"]["api_base"]
    
    try:
        response = requests.get(f"{api_base}/health", timeout=2)
        print(f"[INFO] llama-server est déjà en cours d'exécution sur {api_base}")
        return True
    except:
        pass
    
    # Construire la commande de manière cohérente
    cmd = build_llama_server_command(config)
    
    print(f"[INFO] Démarrage de llama-server...")
    print(f"[INFO] Commande: {' '.join(cmd)}")
    
    try:
        # Démarrer le processus
        llama_server_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        
        # Attendre que le serveur soit prêt
        max_attempts = 60
        for i in range(max_attempts):
            try:
                response = requests.get(f"{api_base}/health", timeout=2)
                if response.status_code == 200:
                    print(f"[OK] llama-server est prêt (tentative {i+1}/{max_attempts})")
                    return True
                elif response.status_code == 503:
                    print(f"[INFO] Modèle en cours de chargement... (tentative {i+1}/{max_attempts})")
                    time.sleep(1)
                else:
                    print(f"[ERREUR] Status code inattendu: {response.status_code}")
                    return False
            except:
                if i < max_attempts - 1:
                    time.sleep(1)
                else:
                    pass
        
        print(f"[ERREUR] llama-server n'a pas pu démarrer après {max_attempts} secondes")
        stop_llama_server()
        return False
        
    except Exception as e:
        print(f"[ERREUR] Impossible de démarrer llama-server: {e}")
        return False

def stop_llama_server():
    """Arrête llama-server si nécessaire."""
    global llama_server_process
    
    if llama_server_process is not None:
        try:
            print(f"[INFO] Arrêt de llama-server...")
            llama_server_process.terminate()
            llama_server_process.wait(timeout=5)
            print(f"[OK] llama-server arrêté")
        except subprocess.TimeoutExpired:
            try:
                llama_server_process.kill()
                llama_server_process.wait()
                print(f"[OK] llama-server forcé à s'arrêter")
            except:
                pass
        except Exception as e:
            print(f"[ERREUR] Erreur lors de l'arrêt de llama-server: {e}")
        finally:
            llama_server_process = None

def test_llama_server():
    """Test la connexion à llama-server."""
    
    # Charger la configuration
    config_path = Path("config.json")
    if not config_path.exists():
        print("[ERREUR] Fichier config.json introuvable")
        return False
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    api_base = config["model"]["api_base"]
    model_name = config["model"]["name"]
    
    print(f"[INFO] Test de connexion à {api_base}")
    print(f"[MODELE] {model_name}")
    print()
    
    # Test 1: Vérifier que le serveur répond
    try:
        response = requests.get(f"{api_base}/health", timeout=5)
        print(f"[OK] Serveur actif: {response.status_code}")
    except Exception as e:
        print(f"[ERREUR] Erreur de connexion: {e}")
        print("   Assurez-vous que llama-server est démarré")
        return False
    
    # Test 2: Envoyer une requête de complétion simple
    try:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": "Bonjour, réponds simplement par 'OK'."}
            ],
            "max_tokens": 10,
            "temperature": 0.0
        }
        
        print("[ENVOI] Envoi d'une requete de test...")
        response = requests.post(
            f"{api_base}/v1/chat/completions",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"[OK] Reponse recue: {content}")
            return True
        else:
            print(f"[ERREUR] Erreur HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la requete: {e}")
        return False

def test_dspy_integration():
    """Test l'intégration DSPy."""
    print("\n" + "="*60)
    print("[TEST] Test de l'integration DSPy")
    print("="*60)
    
    try:
        import dspy
        
        # Charger la configuration
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Configurer DSPy
        lm = dspy.LM(
            model=f"openai/{config['model']['name']}",
            api_base=config['model']['api_base'],
            api_key="dummy",
            model_type="chat"
        )
        dspy.configure(lm=lm, adapter=dspy.JSONAdapter())
        
        # Test simple
        result = lm("Réponds par 'OK DSPy'.")
        print(f"[OK] DSPy fonctionne: {result}")
        return True
        
    except Exception as e:
        print(f"[ERREUR] Erreur DSPy: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_smolagents_integration():
    """Test l'intégration smolagents."""
    print("\n" + "="*60)
    print("[TEST] Test de l'integration smolagents")
    print("="*60)
    
    try:
        from smolagents import LiteLLMModel
        
        # Charger la configuration
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Créer le modèle
        model = LiteLLMModel(
            model_id=f"openai/{config['model']['name']}",
            api_base=config['model']['api_base'],
            api_key="dummy",
            num_ctx=config['model']['num_ctx'],
        )
        
        # Test simple avec message correctement formaté
        from smolagents import ChatMessage, MessageRole
        messages = [ChatMessage(role=MessageRole.USER, content="Réponds par 'OK smolagents'.")]
        response = model(messages)
        print(f"[OK] smolagents fonctionne: {response}")
        return True
        
    except Exception as e:
        print(f"[ERREUR] Erreur smolagents: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_handler(signum, frame):
    """Gestionnaire de nettoyage pour les signaux."""
    print("\n[INFO] Interruption reçue, arrêt de llama-server...")
    stop_llama_server()
    sys.exit(1)

if __name__ == "__main__":
    # Configurer les gestionnaires de signaux
    signal.signal(signal.SIGINT, cleanup_handler)
    signal.signal(signal.SIGTERM, cleanup_handler)
    
    print("="*60)
    print("[TEST] Suite de tests de migration Ollama -> llama.cpp")
    print("="*60)
    print()
    
    success = True
    
    try:
        # Charger la configuration
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Démarrer llama-server si nécessaire
        if not start_llama_server(config):
            print("[ERREUR] Impossible de démarrer llama-server")
            success = False
        else:
            # Test 1: Connexion au serveur
            if not test_llama_server():
                success = False
            
            # Test 2: Intégration DSPy
            if not test_dspy_integration():
                success = False
            
            # Test 3: Intégration smolagents
            if not test_smolagents_integration():
                success = False
        
    except Exception as e:
        print(f"[ERREUR] Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        success = False
    finally:
        # Arrêter llama-server
        stop_llama_server()
    
    print("\n" + "="*60)
    if success:
        print("[OK] Tous les tests sont passes avec succes !")
        print("[SUCCES] La migration est prete.")
    else:
        print("[ERREUR] Certains tests ont echoue.")
        print("[INFO] Veuillez corriger les erreurs avant de continuer.")
    print("="*60)
