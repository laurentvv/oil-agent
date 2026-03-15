# 🛢️ Oil Market Monitoring Agent (Oil-Agent)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![smolagents](https://img.shields.io/badge/smolagents-1.24.0-orange.svg)](https://github.com/huggingface/smolagents)
[![DSPy](https://img.shields.io/badge/DSPy-3.1.3-blue.svg)](https://github.com/stanfordnlp/dspy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


An advanced autonomous AI system designed to track geopolitical and industrial events impacting global oil prices (Brent/WTI). This agent leverages a **hybrid architecture** combining **smolagents** for intelligence gathering and **DSPy** for structured synthesis and continuous prompt optimization.

---

### 🛡️ État Actuel : Version Stable (v1.0-stable)
- **Cycle complet validé :** Recherche (smolagents) + Synthèse (DSPy) + Vérification.
- **Filtrage Anti-Hallucination :** Validation automatique des événements par rapport aux sources brutes (`verify_event_truthfulness`).
- **Gestion du Contexte :** Compression automatique de l'historique pour maintenir la performance.
- **Fiabilité :** 100% des outils de recherche systématiquement exécutés avant toute synthèse.

---

## 🚀 Key Features

- **Autonomous Intelligence Gathering**: Uses `CodeAgent` with a suite of specialized tools to browse web, search news, and parse RSS feeds.
- **Structured Synthesis (DSPy)**: Processes raw intelligence into high-quality, validated JSON events using a modular DSPy pipeline.
- **Continuous Learning**: Automatically saves successful traces to a local dataset for offline optimization and few-shot boosting.
- **Real-Time Monitoring**: Integrated with **RSS feeds**, **VIX volatility index**, and daily news filters for maximum reactivity.
- **Robust Alerting**: Sends rich HTML/Text alerts via SMTP (Postfix) when high-impact events are detected (Impact Score ≥ 6).
- **Failure Resilience**: Implements robust JSON parsing with auto-repair and backup mechanisms for data persistence.
- **Automatic LLM Server Management**: Automatically starts and stops llama-server when the agent runs, ensuring optimal resource usage.

---

## 🏗️ Architecture

The system operates in a two-stage pipeline:

1. **Phase 1: Research (smolagents)**
   - The `CodeAgent` executes Python logic to orchestrate multiple tools.
   - It gathers "raw intelligence" from specialized sources (Iran tensions, refinery damage, OPEC decisions, etc.).
2. **Phase 2: Synthesis (DSPy)**
   - A `dspy.Module` (`OilEventAnalyzer`) takes raw text and current market context.
   - It performs a **Chain of Thought (CoT)** reasoning to extract structured events.
   - Validates output using Pydantic models to ensure strict data integrity.

### Toolset

| Category | Description |
| :--- | :--- |
| **Geopolitics** | `IranConflictTool`, `GeopoliticalEscalationTool` |
| **Supply Chain** | `RefineryDamageTool`, `ShippingDisruptionTool`, `OPECSupplyTool` |
| **Market Data** | `OilPriceTool`, `VIXTool` (Market Fear Index) |
| **News** | `RecentNewsTool`, `RSSFeedTool`, `DuckDuckGoSearchTool` |

---

## 🛠️ Installation

### 1. Prerequisites
- **llama-server (llama.cpp)**: Install [llama-server](https://github.com/ggerganov/llama.cpp) and download required model:
  ```bash
  # Download llama-server for Windows
  # From: https://github.com/ggerganov/llama.cpp/releases
  llama-server.exe
  ```
  
  ```bash
  # Download the Qwen3.5-9B model (GGUF format)
  # From: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF
  # Place in: C:\Modeles_LLM\Qwen3.5-9B-Q4_K_S.gguf
  ```
- **uv**: The project uses [uv](https://astral.sh/uv) for lightning-fast dependency management.

### 2. Setup
```bash
# Clone repository
git clone https://github.com/youruser/oil-agent.git
cd oil_agent

# Sync dependencies (creates .venv automatically)
uv sync

# Activate environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

---

## ⚙️ Configuration

The project uses `config.json` for all configuration. Edit this file to customize behavior:

```json
{
  "model": {
    "name": "qwen3.5-9b",
    "path": "C:\\Modeles_LLM\\Qwen3.5-9B-Q4_K_S.gguf",
    "api_base": "http://127.0.0.1:8080",
    "num_ctx": 65536,
    "provider": "llama.cpp"
  },
  "llama_server": {
    "executable": "llama-server.exe",
    "n_gpu_layers": -1,
    "n_threads": 0,
    "ctx_size": 65536,
    "batch_size": 512,
    "ubatch_size": 128,
    "cache_type_k": "f16",
    "cache_type_v": "f16",
    "host": "0.0.0.0",
    "port": 8080
  },
  "email": {
    "smtp_host": "localhost",
    "smtp_port": 25,
    "email_from": "oil-monitor@localhost",
    "email_to": "your-email@example.com",
    "email_subject_prefix": "[OIL-ALERT]",
    "send_emails": false
  },
  "persistence": {
    "history_file": "logs/email_history.json",
    "events_db": "logs/events_seen.json",
    "dataset_file": "data/oil_intelligence_dataset.jsonl"
  },
  "monitoring": {
    "alert_threshold": 6,
    "news_sources": [
      "reuters.com",
      "bloomberg.com",
      "apnews.com",
      "bbc.com",
      "ft.com",
      "wsj.com"
    ],
    "timezone": "Europe/Paris",
    "recent_news_hours": 24
  }
}
```

**Important Configuration Options:**
- `model.num_ctx`: Context window size (default: 65536 tokens). Increase if you encounter context overflow errors.
- `llama_server.n_gpu_layers`: Number of layers to offload to GPU (-1 = all layers, 0 = CPU only).
- `email.send_emails`: Set to `false` for testing, `true` for production.
- `monitoring.alert_threshold`: Minimum impact score (0-10) to trigger email alerts.

---

## 📈 DSPy Optimization (Learning)

One of the project's core strengths is its ability to **learn from experience**.

### 1. Dataset Collection
Every time the agent runs, it saves a `(raw_intelligence, structured_output)` pair into `data/oil_intelligence_dataset.jsonl`.

### 2. Running Optimization
Once you have collected at least 5-10 examples, run the optimizer to improve synthesis logic:
```bash
uv run python optimize_agent.py
```
This script uses `BootstrapFewShot` teleprompter to:
- Evaluate candidate "demos" from your dataset.
- Select the most effective examples based on a custom metric (structure validation + content relevance).
- Save optimized weights to `data/oil_analyzer_optimized.json`.

The next time `oil_agent.py` runs, it will **automatically load** these optimized weights to provide superior analysis.

---

## 🖥️ Usage

### Run a Monitoring Cycle
```bash
uv run python oil_agent.py
```

**Automatic LLM Server Management:**
The agent automatically starts llama-server when needed and stops it when finished. No manual intervention required.

### View Alert History
```bash
uv run python oil_agent.py history
```

### Test LLM Server Connection
```bash
python test_llama_server.py
```
This script tests:
- llama-server connectivity (health endpoint)
- DSPy integration
- smolagents integration
- Automatic server start/stop

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.
