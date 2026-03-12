# 🛢️ Oil Market Monitoring Agent (Oil-Agent)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![smolagents](https://img.shields.io/badge/smolagents-1.24.0-orange.svg)](https://github.com/huggingface/smolagents)
[![DSPy](https://img.shields.io/badge/DSPy-3.1.3-blue.svg)](https://github.com/stanfordnlp/dspy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced autonomous AI system designed to track geopolitical and industrial events impacting global oil prices (Brent/WTI). This agent leverages a **hybrid architecture** combining **smolagents** for intelligence gathering and **DSPy** for structured synthesis and continuous prompt optimization.

---

## 🚀 Key Features

- **Autonomous Intelligence Gathering**: Uses `CodeAgent` with a suite of specialized tools to browse the web, search news, and parse RSS feeds.
- **Structured Synthesis (DSPy)**: Processes raw intelligence into high-quality, validated JSON events using a modular DSPy pipeline.
- **Continuous Learning**: Automatically saves successful traces to a local dataset for offline optimization and few-shot boosting.
- **Real-Time Monitoring**: Integrated with **RSS feeds**, **VIX volatility index**, and daily news filters for maximum reactivity.
- **Robust Alerting**: Sends rich HTML/Text alerts via SMTP (Postfix) when high-impact events are detected (Impact Score ≥ 6).
- **Failure Resilience**: Implements robust JSON parsing with auto-repair and backup mechanisms for data persistence.

---

## 🏗️ Architecture

The system operates in a two-stage pipeline:

1.  **Phase 1: Research (smolagents)**
    - The `CodeAgent` executes Python logic to orchestrate multiple tools.
    - It gathers "raw intelligence" from specialized sources (Iran tensions, refinery damage, OPEC decisions, etc.).
2.  **Phase 2: Synthesis (DSPy)**
    - A `dspy.Module` (`OilEventAnalyzer`) takes the raw text and current market context.
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
- **Ollama**: Install [Ollama](https://ollama.com/) and pull the required model:
  ```bash
  ollama pull qwen3.5:9b
  ```
- **uv**: The project uses [uv](https://astral.sh/uv) for lightning-fast dependency management.

### 2. Setup
```bash
# Clone the repository
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

Edit the `CONFIG` block in `oil-agent.py`:

```python
CONFIG = {
    "ollama_model": "ollama_chat/qwen3.5:9b", # Optimized for reasoning
    "ollama_api_base": "http://127.0.0.1:11434",
    "alert_threshold": 6,                    # Trigger email if score >= 6
    "send_emails": False,                   # Set to True for production
    "smtp_host": "localhost",
    "smtp_port": 25,
    "email_to": "your-email@example.com",
}
```

---

## 📈 DSPy Optimization (Learning)

One of the project's core strengths is its ability to **learn from experience**.

### 1. Dataset Collection
Every time the agent runs, it saves the `(raw_intelligence, structured_output)` pair into `data/oil_intelligence_dataset.jsonl`. 

### 2. Running Optimization
Once you have collected at least 5-10 examples, run the optimizer to improve the synthesis logic:
```bash
uv run python optimize_agent.py
```
This script uses the `BootstrapFewShot` teleprompter to:
- Evaluate candidate "demos" from your dataset.
- Select the most effective examples based on a custom metric (structure validation + content relevance).
- Save the optimized weights to `data/oil_analyzer_optimized.json`.

The next time `oil-agent.py` runs, it will **automatically load** these optimized weights to provide superior analysis.

---

## 🖥️ Usage

### Run a Monitoring Cycle
```bash
uv run python oil-agent.py
```

### View Alert History
```bash
uv run python oil-agent.py history
```

---

## 📝 License
MIT License. See [LICENSE](LICENSE) for details.
