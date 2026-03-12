# Oil Market Monitoring Agent (oil-agent)

## Project Overview
**Oil Market Monitoring Agent** is an advanced AI system designed to track geopolitical and industrial events impacting global oil prices (Brent/WTI). It uses a hybrid architecture combining **smolagents** for autonomous intelligence gathering and **DSPy** for structured synthesis and continuous improvement.

### Key Technologies
- **smolagents (v1.24.0)**: Powers the autonomous `CodeAgent` that uses tools to browse the web and search specialized sources.
- **DSPy (v3.1.3)**: Handles the final synthesis of "raw intelligence" into structured, high-quality JSON events. **Note: Assertions are handled via manual validation/fix logic in this version.**
- **LiteLLM / Ollama**: Interfaces with local LLMs (defaults to `qwen3.5:9b`).
- **uv**: Python package and project manager.

### Hybrid Architecture
1. **Intelligence Gathering (smolagents)**: The agent uses specialized tools (`IranConflictTool`, `RefineryDamageTool`, etc.) to find breaking news and market data.
2. **Synthesis & Formatting (DSPy)**: A DSPy module (`OilEventAnalyzer`) processes the raw findings and extracts structured events via Chain of Thought (CoT).
3. **Continuous Improvement**: Every execution saves a trace (input/output pair) to `data/oil_intelligence_dataset.jsonl`. These traces are used to optimize the agent's reasoning via `optimize_agent.py`.

## Building and Running

### Installation
```bash
uv sync
```

### Execution
- **Run the Agent**:
  ```bash
  uv run python oil_agent.py
  ```
- **Optimize the Agent**:
  ```bash
  uv run python optimize_agent.py
  ```
  *(Requires at least 5 collected examples in the dataset)*

- **Check History**:
  ```bash
  uv run python oil_agent.py history
  ```

## Development Conventions

### Data Pipeline
- **Logs**: `logs/oil_monitor.log`
- **Persistence**: `logs/events_seen.json` (avoids duplicate alerts).
- **History**: `logs/email_history.json` (tracked with robust JSON parsing and backup).
- **Dataset**: `data/oil_intelligence_dataset.jsonl` (raw data for DSPy optimization).
- **Optimized Prompt**: `data/oil_analyzer_optimized.json` (saved weights/demos for DSPy).

### Quality Control
- **Manual Validation**: `validate_and_fix_events` ensures the LLM provides all required fields (title, impact_score, etc.) after DSPy synthesis.
- **Error Handling**: Robust `try/except` blocks with `errors='replace'` and `.bak` backups for persistent JSON files to prevent data loss or corruption.
- **Retry Mechanism**: Controlled via smolagents `max_steps` and DSPy's internal reasoning loops.

## Usage Guidelines
- **Alert Threshold**: Controlled by `CONFIG["alert_threshold"]` (0-10).
- **Simulation Mode**: Set `CONFIG["send_emails"] = False` to test without sending SMTP alerts.
- **Model Configuration**: Defaults to `qwen3.5:9b`. Ensure Ollama is running and the model is pulled.
