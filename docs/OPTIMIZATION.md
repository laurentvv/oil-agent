# DSPy Optimization Guide

This project uses **DSPy** to handle the transformation of unstructured news and data into structured JSON events. To achieve consistent and high-quality results, the system implements an **offline optimization pipeline**.

---

## 1. The Role of DSPy

In the `oil-agent`, the **smolagents** component is responsible for gathering data (the "What"), while **DSPy** is responsible for reasoning and formatting (the "How"). 

Traditional LLM calls rely on static prompts that often fail or hallucinate when the input text (raw intelligence) becomes too large or complex. DSPy solves this by:
- Using a **Signature** to define the expected task.
- Using a **Module** (like `ChainOfThought`) to perform the reasoning.
- Using an **Optimizer** (Teleprompter) to refine the prompt based on real-world examples.

---

## 2. Data Collection (Traces)

Every successful execution of `oil_agent.py` contributes to a local dataset:
- **Location**: `data/oil_intelligence_dataset.jsonl`
- **Format**: Each line contains an input (raw intelligence + context) and its corresponding validated output (structured events).

**Goal**: Collect at least **10-20 high-quality examples** of how the agent *should* have analyzed a given set of news.

---

## 3. The Optimization Script (`optimize_agent.py`)

The optimization process uses the **BootstrapFewShot** strategy. This is not "training" in the traditional gradient descent sense; instead, it's a **few-shot prompt optimization**.

### How it works:
1.  **Loading**: The script loads your collected examples into a `trainset`.
2.  **Simulation**: It runs the `OilEventAnalyzer` on these examples without any optimization.
3.  **Validation (Metric)**: A custom `metric()` function checks the output for:
    - Proper JSON structure.
    - Required fields (title, category, etc.).
    - Impact score range (0-10).
    - Consistency with the "Golden" (expected) output.
4.  **Bootstrapping**: The optimizer identifies the **best-performing examples** (demos) and compiles them into a permanent prompt structure.
5.  **Saving**: The resulting "optimized program" (prompt weights + demos) is saved to `data/oil_analyzer_optimized.json`.

---

## 4. How to Optimize

1.  **Generate Data**: Run `uv run python oil_agent.py` multiple times over several days.
2.  **Review (Optional)**: Open `data/oil_intelligence_dataset.jsonl` and manually edit any incorrect outputs to serve as "gold" standards.
3.  **Run Optimizer**:
    ```bash
    uv run python optimize_agent.py
    ```
4.  **Test**: Run the optimizer with the `run` argument to see the improvement:
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
If the file exists, the agent will instantly benefit from the optimized few-shot demos, leading to higher confidence scores and fewer parsing errors.
