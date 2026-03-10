import dspy

class OilAnalysisSignature(dspy.Signature):
    """
    Analyzes raw intelligence data about the oil market and generates a detailed report.
    The report must include a list of high-impact events with their category, impact score,
    urgency, detailed summary, price impact, and source hint.
    """
    raw_intelligence = dspy.InputField(desc="Raw data collected from various tools and news sources.")
    current_date = dspy.InputField(desc="The current date.")

    report = dspy.OutputField(desc="A detailed structured report. Must be a list of events in JSON format with fields: category, title, impact_score (1-10), urgency (Breaking/Recent/Background), summary, price_impact, source_hint, publication_date.")

class OilAnalyst(dspy.Module):
    def __init__(self, num_trials=5):
        super().__init__()
        self.analyze = dspy.ChainOfThought(OilAnalysisSignature)
        self.num_trials = num_trials

    def forward(self, raw_intelligence, current_date):
        reports = []
        for i in range(self.num_trials):
            prediction = self.analyze(raw_intelligence=raw_intelligence, current_date=current_date)
            reports.append(prediction.report)

        # Consolidation logic: In this case, we'll pick the most comprehensive one or
        # let DSPy's multi-trial nature handle the refinement if we were using an optimizer.
        # Since we are doing "several trials to validate and improve", we can ask another
        # signature to consolidate or just pick the best.
        # For now, let's use a simpler approach: have a consolidation step.

        return self.consolidate(reports, raw_intelligence, current_date)

    def consolidate(self, reports, raw_intelligence, current_date):
        class ConsolidatorSignature(dspy.Signature):
            """
            Consolidates multiple analysis reports into one final, high-quality,
            accurate, and comprehensive report. Ensure all high-impact events are
            captured and the scores are validated.
            """
            raw_intelligence = dspy.InputField()
            reports = dspy.InputField(desc="List of candidate reports from multiple trials.")
            final_report = dspy.OutputField(desc="Final consolidated JSON list of high-impact events.")

        consolidator = dspy.Predict(ConsolidatorSignature)
        result = consolidator(raw_intelligence=raw_intelligence, reports=str(reports))
        return result.final_report

def setup_dspy(model_id, api_base):
    # Using Ollama via dspy.OllamaLocal or dspy.ChatOllama
    # dspy.OllamaLocal is usually for the older API, ChatOllama or similar might be better for newer ones
    # However, dspy often works well with OpenAI-compatible endpoints.
    # Ollama's /v1 is OpenAI compatible.

    # Extract model name from model_id (e.g., 'ollama_chat/qwen3.5:9b' -> 'qwen3.5:9b')
    model_name = model_id.split('/')[-1] if '/' in model_id else model_id

    lm = dspy.LM(f"ollama_chat/{model_name}", api_base=api_base, api_key="ollama")
    dspy.settings.configure(lm=lm)
    return lm
