# 🔍 Diagnostic des problèmes DSPy dans oil-agent

## 📋 Sommaire

1. [Problème 1 : Avertissement DSPy sur module.forward()](#problème-1--avertissement-dspy-sur-moduleforward)
2. [Problème 2 : Erreur UnicodeEncodeError dans save_email_history()](#problème-2--erreur-unicodeencodeerror-dans-save_email_history)
3. [Solutions proposées](#solutions-proposées)
4. [Validation des corrections](#validation-des-corrections)

---

## Problème 1 : Avertissement DSPy sur module.forward()

### 📝 Symptôme

```
2026/03/11 14:01:50 WARNING dspy.primitives.module: Calling module.forward(...) on OilAnalyst directly is discouraged. Please use module(...) instead.
```

### 🔍 Localisation

**Fichier** : [`oil-agent.py`](oil-agent.py:934)  
**Ligne** : 934

```python
raw_result = analyst.forward(raw_intelligence=str(raw_intelligence), current_date=current_date)
```

### 🎯 Diagnostic

DSPy recommande d'appeler les modules directement via l'opérateur `__call__` (`module(...)`) au lieu d'appeler explicitement la méthode `forward()`.

**Raison** :
- L'appel direct `module(...)` permet à DSPy de gérer correctement le contexte d'exécution
- Permet le tracking des appels et la gestion des optimisations
- Meilleure compatibilité avec les futures versions de DSPy

### ✅ Solution proposée

**Remplacer** :
```python
raw_result = analyst.forward(raw_intelligence=str(raw_intelligence), current_date=current_date)
```

**Par** :
```python
raw_result = analyst(raw_intelligence=str(raw_intelligence), current_date=current_date)
```

**Avantages** :
- ✅ Élimine l'avertissement DSPy
- ✅ Meilleure compatibilité avec DSPy
- ✅ Plus propre et idiomatique

---

## Problème 2 : Erreur UnicodeEncodeError dans save_email_history()

### 📝 Symptôme

```
Traceback (most recent call last):
  File "D:\GIT\fork\oil-agent\oil-agent.py", line 1040, in <module>
    run_monitoring_cycle()
  File "D:\GIT\fork\oil-agent\oil-agent.py", line 973, in run_monitoring_cycle
    success = send_alert_email(subject, body, event_id)
  File "D:\GIT\fork\oil-agent\oil-agent.py", line 172, in send_alert_email
    append_email_log(full_subject, body, event_id)
  File "D:\GIT\fork\oil-agent\oil-agent.py", line 132, in append_email_log
    save_email_history(history)
  File "D:\GIT\fork\oil-agent\oil-agent.py", line 121, in save_email_history
    json.dump(history, f, indent=2, ensure_ascii=False)
  File "C:\Users\lvolff\AppData\Roaming\uv\python\cpython-3.14.0-windows-x86_64-none\Lib\json\__init__.py", line 180, in dump
    fp.write(chunk)
  File "C:\Users\lvolff\AppData\Roaming\uv\python\cpython-3.14.0-windows-x86_64-none\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 1-2: character maps to <undefined>
```

### 🔍 Localisation

**Fichier** : [`oil-agent.py`](oil-agent.py:119-121)  
**Lignes** : 119-121

```python
def save_email_history(history: list):
    with open(CONFIG["history_file"], "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
```

### 🎯 Diagnostic

Le problème est que le fichier est ouvert sans spécifier l'encodage. Sur Windows, l'encodage par défaut est `cp1252` (Windows-1252), qui ne peut pas encoder certains caractères Unicode.

**Caractères problématiques dans le code** :
- 🛢️ (baril de pétrole) - lignes 987, 1005
- ⚠️ (avertissement) - ligne 155
- 📧 (email) - lignes 133, 172, 1022
- ⚡ (impact) - ligne 992
- 🔔 (urgence) - ligne 993
- 💰 (prix) - ligne 994
- 📅 (date) - ligne 995
- 📝 (analyse) - ligne 997
- 🔗 (source) - ligne 1002
- ⏰ (timestamp) - ligne 1005
- 🤖 (robot) - ligne 1006

**Note** : Le code a déjà une correction pour stdout/stderr (lignes 69-71), mais pas pour les fichiers.

### ✅ Solution proposée

**Remplacer** :
```python
def save_email_history(history: list):
    with open(CONFIG["history_file"], "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
```

**Par** :
```python
def save_email_history(history: list):
    with open(CONFIG["history_file"], "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
```

**Avantages** :
- ✅ Support complet des caractères Unicode (emojis, caractères spéciaux)
- ✅ Compatible avec tous les systèmes d'exploitation
- ✅ Cohérent avec la configuration existante (stdout/stderr déjà en UTF-8)

### 🔧 Correction supplémentaire recommandée

Il y a aussi un problème potentiel dans [`save_seen_events()`](oil-agent.py:97-99) :

```python
def save_seen_events(seen: set):
    with open(CONFIG["events_db"], "w") as f:
        json.dump(list(seen), f, indent=2)
```

**Recommandation** : Ajouter également l'encodage UTF-8 :

```python
def save_seen_events(seen: set):
    with open(CONFIG["events_db"], "w", encoding="utf-8") as f:
        json.dump(list(seen), f, indent=2)
```

Et aussi dans [`load_seen_events()`](oil-agent.py:89-94) et [`load_email_history()`](oil-agent.py:111-116) :

```python
def load_seen_events() -> set:
    p = Path(CONFIG["events_db"])
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def load_email_history() -> list:
    p = Path(CONFIG["history_file"])
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return []
```

---

## Solutions proposées

### 📦 Correction complète

Voici les corrections à appliquer dans [`oil-agent.py`](oil-agent.py) :

#### Correction 1 : Appel DSPy (ligne 934)

```python
# AVANT (ligne 934)
raw_result = analyst.forward(raw_intelligence=str(raw_intelligence), current_date=current_date)

# APRÈS
raw_result = analyst(raw_intelligence=str(raw_intelligence), current_date=current_date)
```

#### Correction 2 : Encodage UTF-8 pour tous les fichiers

**Fonction `save_email_history()` (lignes 119-121)** :
```python
# AVANT
def save_email_history(history: list):
    with open(CONFIG["history_file"], "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

# APRÈS
def save_email_history(history: list):
    with open(CONFIG["history_file"], "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
```

**Fonction `load_email_history()` (lignes 111-116)** :
```python
# AVANT
def load_email_history() -> list:
    p = Path(CONFIG["history_file"])
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return []

# APRÈS
def load_email_history() -> list:
    p = Path(CONFIG["history_file"])
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return []
```

**Fonction `save_seen_events()` (lignes 97-99)** :
```python
# AVANT
def save_seen_events(seen: set):
    with open(CONFIG["events_db"], "w") as f:
        json.dump(list(seen), f, indent=2)

# APRÈS
def save_seen_events(seen: set):
    with open(CONFIG["events_db"], "w", encoding="utf-8") as f:
        json.dump(list(seen), f, indent=2)
```

**Fonction `load_seen_events()` (lignes 89-94)** :
```python
# AVANT
def load_seen_events() -> set:
    p = Path(CONFIG["events_db"])
    if p.exists():
        with open(p) as f:
            return set(json.load(f))
    return set()

# APRÈS
def load_seen_events() -> set:
    p = Path(CONFIG["events_db"])
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return set(json.load(f))
    return set()
```

---

## Validation des corrections

### ✅ Checklist de validation

- [ ] Appliquer la correction 1 (appel DSPy)
- [ ] Appliquer la correction 2 (encodage UTF-8 pour save_email_history)
- [ ] Appliquer la correction 3 (encodage UTF-8 pour load_email_history)
- [ ] Appliquer la correction 4 (encodage UTF-8 pour save_seen_events)
- [ ] Appliquer la correction 5 (encodage UTF-8 pour load_seen_events)
- [ ] Exécuter `oil-agent.py` et vérifier qu'il n'y a plus d'avertissement DSPy
- [ ] Exécuter `oil-agent.py` et vérifier qu'il n'y a plus d'erreur UnicodeEncodeError
- [ ] Vérifier que le fichier `logs/email_history.json` est correctement créé avec des emojis
- [ ] Vérifier que le fichier `logs/events_seen.json` est correctement créé

### 🧪 Test de validation

Après avoir appliqué les corrections, exécutez :

```bash
cd D:\GIT\fork\oil-agent
uv run python oil-agent.py
```

**Résultat attendu** :
- ✅ Aucun avertissement DSPy
- ✅ Aucune erreur UnicodeEncodeError
- ✅ Fichiers JSON créés correctement avec support Unicode

---

## 📊 Résumé des problèmes

| Problème | Sévérité | Localisation | Solution |
|----------|-----------|--------------|-----------|
| Avertissement DSPy | Faible | oil-agent.py:934 | Remplacer `forward()` par appel direct |
| UnicodeEncodeError | Critique | oil-agent.py:119-121 | Ajouter `encoding="utf-8"` |

---

## 🎯 Conclusion

Les deux problèmes identifiés sont :

1. **Avertissement DSPy** : Problème mineur de style/appel DSPy
2. **UnicodeEncodeError** : Problème critique empêchant l'exécution du programme

Les solutions proposées sont simples à mettre en œuvre et résolvent les deux problèmes de manière définitive.

---

**Document créé le :** 2025-03-11  
**Version :** 1.0  
**Auteur :** Kilo Code (Debug Mode)
