# DSPy Optimization Guide

This project uses **DSPy** to handle transformation of unstructured news and data into structured JSON events. To achieve consistent and high-quality results, the system implements an **offline optimization pipeline**.

---

## 1. The Role of DSPy

In `oil-agent`, **smolagents** component is responsible for gathering data (the "What"), while **DSPy** is responsible for reasoning and formatting (the "How").

Traditional LLM calls rely on static prompts that often fail or hallucinate when the input text (raw intelligence) becomes too large or complex. DSPy solves this by:
- Using a **Signature** to define the expected task.
- Using a **Module** (like `ChainOfThought`) to perform reasoning.
- Using an **Optimizer** (Teleprompter) to refine the prompt based on real-world examples.

---

## 2. Data Collection (Traces)

Every successful execution of `oil_agent.py` contributes to a local dataset:
- **Location**: `data/oil_intelligence_dataset.jsonl`
- **Format**: Each line contains an input (raw intelligence + context) and its corresponding validated output (structured events).

**Goal**: Collect at least **10-20 high-quality examples** of how the agent *should* have analyzed a given set of news.

---

## 3. The Optimization Script (`optimize_agent.py`)

The optimization process uses **BootstrapFewShot** strategy. This is not "training" in the traditional gradient descent sense; instead, it's a **few-shot prompt optimization**.

### How it works:

#### 1. Loading
The script loads your collected examples into a `trainset`.

#### 2. Simulation
It runs `OilEventAnalyzer` on these examples without any optimization.

#### 3. Validation (Metric)
A custom `metric()` function checks the output for:
- Proper JSON structure.
- Required fields (title, category, etc.).
- Impact score range (0-10).
- Consistency with "Golden" (expected) output.

#### 4. Bootstrapping
The optimizer identifies **best-performing examples** (demos) and compiles them into a permanent prompt structure.

#### 5. Saving
The resulting "optimized program" (prompt weights + demos) is saved to `data/oil_analyzer_optimized.json`.

---

## 4. How to Optimize

### 1. Generate Data
Run `uv run python oil_agent.py` multiple times over several days.

**Tips for high-quality data:**
- Run during different times of day to capture various news sources.
- Monitor different types of events (Iran conflicts, refinery damage, OPEC decisions, etc.).
- Ensure the agent successfully completes and saves traces.

### 2. Review (Optional)
Open `data/oil_intelligence_dataset.jsonl` and manually edit any incorrect outputs to serve as "gold" standards.

### 3. Run Optimizer
```bash
uv run python optimize_agent.py
```

### 4. Test
Run the optimizer with `run` argument to see improvement:
```bash
uv run python optimize_agent.py run
```

---

## 5. Automatic Loading

The main `oil_agent.py` script is designed to detect the optimized file:

```python
optimized_path = Path("data/oil_analyzer_optimized.json")
if optimized_path.exists():
    analyzer.load(str(optimized_path))
```

If the file exists, the agent will instantly benefit from optimized few-shot demos, leading to:
- Higher confidence scores
- Fewer parsing errors
- Better structured output
- More consistent category classification

---

## 6. Key Benefits of Optimization

- **Improved Accuracy**: The model learns from real examples, reducing hallucinations.
- **Better Consistency**: Standardized output format across all events.
- **Faster Convergence**: Few-shot examples guide the reasoning process.
- **Continuous Improvement**: As you collect more data, the model gets better over time.

---

## 7. Troubleshooting

### Low Confidence Scores
If confidence scores remain low after optimization:
- Collect more diverse examples covering all event types.
- Review dataset for incorrect or low-quality examples.
- Increase context size in `config.json` if needed.

### Parsing Errors
If you see JSON parsing errors:
- Check that examples have all required fields (title, category, impact_score, etc.).
- Verify that impact scores are within the valid range (0-10).
- Ensure categories match the allowed values (Iran, Refinery, OPEC, Gas, Shipping, Geopolitical).

### Context Overflow
If you encounter "request exceeds available context size" errors:
- Increase `model.num_ctx` in `config.json` (default: 65536 tokens).
- Reduce the amount of raw intelligence collected by tools.
- Optimize the prompt to be more concise.

---

## 8. Best Practices

### Data Quality
- **Diversity**: Collect examples from all event types (Iran, Refinery, OPEC, Gas, Shipping, Geopolitical).
- **Accuracy**: Ensure examples have correct impact scores and realistic price impacts.
- **Consistency**: Maintain consistent formatting across all examples.

### Optimization Frequency
- **Initial**: Run optimizer after collecting 5-10 examples.
- **Regular**: Re-optimize every 20-30 new examples.
- **After Major Changes**: Re-optimize after significant model or configuration changes.

### Monitoring
- **Track Confidence**: Monitor average confidence scores before and after optimization.
- **Track Errors**: Count parsing errors and track improvement over time.
- **Compare Results**: Compare optimized vs. non-optimized performance on held-out data.

---

## 9. Integration with llama-server

The optimization process works seamlessly with llama-server:
- **OpenAI-Compatible API**: llama-server exposes an OpenAI-compatible API at `http://127.0.0.1:8080`.
- **DSPy Integration**: DSPy's `dspy.LM` uses the OpenAI format with `api_base` and `api_key="dummy"`.
- **Automatic Management**: The agent automatically starts llama-server when needed and stops it when finished.

This ensures that optimization benefits are available immediately when the agent runs, without requiring manual LLM server management.
