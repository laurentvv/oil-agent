# Oil Market Monitoring Agent (oil-agent)

## Project Overview
**Oil Market Monitoring Agent** is a Python-based system designed to track geopolitical and industrial events that impact global oil prices (Brent/WTI). It leverages **smolagents (v1.24.0)**, **LiteLLM**, and **Ollama (qwen2.5/3.5)** to analyze news and provide high-impact alerts.

### Key Technologies
- **smolagents**: Framework for building AI agents with code-execution capabilities.
- **LiteLLM**: Unified interface for various LLM providers (used here for Ollama).
- **Ollama**: Local LLM runner (defaults to `qwen3.5:9b`).
- **uv**: Modern Python package and project manager.
- **Postfix**: Used as a local SMTP relay for sending email alerts.

### Architecture
The project is centered around a `CodeAgent` that utilizes a suite of specialized tools:
- **IranConflictTool**: Monitors tensions in Iran and the Strait of Hormuz.
- **RefineryDamageTool**: Tracks attacks or accidents at oil refineries.
- **OPECSupplyTool**: Monitors OPEC+ production decisions.
- **RecentNewsTool / RSSFeedTool**: Fetches real-time news and RSS feeds from major sources (Reuters, Bloomberg, etc.).
- **VIXTool**: Monitors the CBOE Volatility Index for market sentiment.
- **DuckDuckGoSearchTool / VisitWebpageTool**: General web searching and scraping.

## Building and Running

### Prerequisites
- **Python 3.13+**
- **Ollama** installed and running with `qwen2.5:7b` or `qwen3.5:9b`.
- **Postfix** (optional, for email alerts).

### Installation
1. Install `uv` if not already present:
   ```bash
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
2. Synchronize dependencies (creates `.venv` automatically):
   ```bash
   uv sync
   ```

### Execution
- **Run the Agent**:
  ```bash
  uv run python oil-agent.py
  ```
- **Check Email History**:
  ```bash
  uv run python oil-agent.py history
  ```

## Development Conventions

### Code Structure
- **`oil-agent.py`**: The monolithic main script containing configuration, tool definitions, and the agent loop.
- **`CONFIG`**: Central dictionary in `oil-agent.py` for managing model settings, SMTP, and alert thresholds.
- **Tools**: Defined as classes inheriting from `smolagents.Tool`. They can also be used directly (see `skill.md`).
- **Persistence**: 
  - `logs/events_seen.json`: Tracks processed events to avoid duplicates.
  - `logs/email_history.json`: Stores sent alerts.
  - `logs/oil_monitor.log`: General application logs.

### Testing and Linting
- **pytest**: Used for testing (defined in `pyproject.toml`).
- **ruff / black**: Configured for linting and formatting.
- Run tests: `uv run pytest` (if tests exist).

## Key Files
- `oil-agent.py`: Main logic and tool implementations.
- `pyproject.toml`: Project metadata and dependencies.
- `skill.md`: Documentation on using tools directly without the agent for better performance.
- `plans/`: Detailed architectural and improvement plans.
- `README.md`: Comprehensive user guide and setup instructions.

## Usage Guidelines
- **Alert Threshold**: Controlled by `CONFIG["alert_threshold"]` (0-10). Alerts are only sent if the agent evaluates an event's impact above this value.
- **Simulation Mode**: Set `CONFIG["send_emails"] = False` to test the agent without sending actual emails.
- **Direct Tool Usage**: For faster execution or debugging, import tools from `oil_agent` as described in `skill.md`.
