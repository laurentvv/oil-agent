# DSPy Documentation

> Complete documentation for DSPy — the framework for programming (rather than prompting) language models.
> 
> **Source:** https://dspy.ai  
> **GitHub:** https://github.com/stanfordnlp/dspy  
> **Generated:** March 2026

---


## Table of Contents

- [Get Started](#get-started)

**Learn DSPy**
  - [Learning DSPy](#learning-dspy)

  **DSPy Programming**
    - [Programming Overview](#programming-overview)
    - [Language Models](#language-models)
    - [Signatures](#signatures)
    - [Modules](#modules)
    - [Adapters](#adapters)
    - [Tools](#tools)
    - [MCP](#mcp)

  **DSPy Evaluation**
    - [Evaluation Overview](#evaluation-overview)
    - [Data Handling](#data-handling)
    - [Metrics](#metrics)

  **DSPy Optimization**
    - [Optimization Overview](#optimization-overview)
    - [Optimizers](#optimizers)

**Tutorials**
  - [Tutorials Overview](#tutorials-overview)

  **Build AI Programs with DSPy**
    - [Overview](#overview)
    - [Managing Conversation History](#managing-conversation-history)
    - [Classification](#classification)
    - [Privacy-Conscious Delegation](#privacy-conscious-delegation)

  **Optimize AI Programs with DSPy**
    - [Overview](#overview)

  **Reflective Prompt Evolution with dspy.GEPA**
    - [Overview](#overview)

  **Experimental RL Optimization for DSPy**
    - [Overview](#overview)

  **Tools, Development, and Deployment**
    - [Overview](#overview)
    - [Use MCP in DSPy](#use-mcp-in-dspy)
    - [Output Refinement](#output-refinement)
    - [Saving and Loading](#saving-and-loading)
    - [Cache](#cache)
    - [Deployment](#deployment)
    - [Debugging & Observability](#debugging--observability)
    - [Tracking DSPy Optimizers](#tracking-dspy-optimizers)
    - [Streaming](#streaming)
    - [Async](#async)

  **Real-World Examples**
    - [Overview](#overview)
    - [Generating llms.txt](#generating-llmstxt)
    - [Memory-Enabled ReAct Agents](#memory-enabled-react-agents)
    - [Financial Analysis with Yahoo Finance](#financial-analysis-with-yahoo-finance)
    - [Email Information Extraction](#email-information-extraction)
    - [Code Generation for Unfamiliar Libraries](#code-generation-for-unfamiliar-libraries)
    - [Building a Creative Text-Based AI Game](#building-a-creative-text-based-ai-game)
- [DSPy in Production](#dspy-in-production)

**Community**
  - [Community Resources](#community-resources)
  - [Use Cases](#use-cases)
  - [Community Ports](#community-ports)
  - [Contributing](#contributing)

**FAQ**
  - [FAQ](#faq)
  - [Cheatsheet](#cheatsheet)

**API Reference**
  - [API Reference](#api-reference)

  **Adapters**
    - [Adapter](#adapter)
    - [ChatAdapter](#chatadapter)
    - [JSONAdapter](#jsonadapter)
    - [TwoStepAdapter](#twostepadapter)

  **Evaluation**
    - [CompleteAndGrounded](#completeandgrounded)
    - [Evaluate](#evaluate)
    - [EvaluationResult](#evaluationresult)
    - [SemanticF1](#semanticf1)
    - [answer_exact_match](#answerexactmatch)
    - [answer_passage_match](#answerpassagematch)

  **Experimental**
    - [Citations](#citations)
    - [Document](#document)

  **Models**
    - [Embedder](#embedder)
    - [LM](#lm)

  **Modules**
    - [BestOfN](#bestofn)
    - [ChainOfThought](#chainofthought)
    - [CodeAct](#codeact)
    - [Module](#module)
    - [MultiChainComparison](#multichaincomparison)
    - [Parallel](#parallel)
    - [Predict](#predict)
    - [ProgramOfThought](#programofthought)
    - [ReAct](#react)
    - [Refine](#refine)
    - [RLM](#rlm)

  **Optimizers**

    **GEPA**
      - [1. GEPA Overview](#1-gepa-overview)
      - [2. GEPA Advanced](#2-gepa-advanced)
    - [BetterTogether](#bettertogether)
    - [BootstrapFewShot](#bootstrapfewshot)
    - [BootstrapFewShotWithRandomSearch](#bootstrapfewshotwithrandomsearch)
    - [BootstrapFinetune](#bootstrapfinetune)
    - [BootstrapRS](#bootstraprs)
    - [COPRO](#copro)
    - [Ensemble](#ensemble)
    - [InferRules](#inferrules)
    - [KNN](#knn)
    - [KNNFewShot](#knnfewshot)
    - [LabeledFewShot](#labeledfewshot)
    - [MIPROv2](#miprov2)
    - [SIMBA](#simba)

  **Primitives**
    - [Audio](#audio)
    - [Code](#code)
    - [Example](#example)
    - [History](#history)
    - [Image](#image)
    - [Prediction](#prediction)
    - [Tool](#tool)
    - [ToolCalls](#toolcalls)

  **Signatures**
    - [InputField](#inputfield)
    - [OutputField](#outputfield)
    - [Signature](#signature)

  **Tools**
    - [ColBERTv2](#colbertv2)
    - [Embeddings](#embeddings)
    - [PythonInterpreter](#pythoninterpreter)

  **Utils**
    - [StatusMessage](#statusmessage)
    - [StatusMessageProvider](#statusmessageprovider)
    - [StreamListener](#streamlistener)
    - [asyncify](#asyncify)
    - [configure_cache](#configurecache)
    - [disable_litellm_logging](#disablelitellmlogging)
    - [disable_logging](#disablelogging)
    - [enable_litellm_logging](#enablelitellmlogging)
    - [enable_logging](#enablelogging)
    - [inspect_history](#inspecthistory)
    - [load](#load)
    - [streamify](#streamify)

---


# Get Started {#get-started}

*Source: `index.md`*

![DSPy](static/img/dspy_logo.png){ width="200", align=left }

# _Programming_—not prompting—_LMs_

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/dspy?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/dspy) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/dspy?period=monthly)](https://pepy.tech/projects/dspy)

DSPy is a declarative framework for building modular AI software. It allows you to **iterate fast on structured code**, rather than brittle strings, and offers algorithms that **compile AI programs into effective prompts and weights** for your language models, whether you're building simple classifiers, sophisticated RAG pipelines, or Agent loops.

Instead of wrangling prompts or training jobs, DSPy (Declarative Self-improving Python) enables you to **build AI software from natural-language modules** and to _generically compose them_ with different models, inference strategies, or learning algorithms. This makes AI software **more reliable, maintainable, and portable** across models and strategies.

*tl;dr* Think of DSPy as a higher-level language for AI programming, like the shift from assembly to C or pointer arithmetic to SQL. Meet the community, seek help, or start contributing via [GitHub](https://github.com/stanfordnlp/dspy) and [Discord](https://discord.gg/XCGy2WDCQB).

<!-- Its abstractions make your AI software more reliable and maintainable, and allow it to become more portable as new models and learning techniques emerge. It's also just rather elegant! -->

!!! info "Getting Started I: Install DSPy and set up your LM"

    ```bash
    > pip install -U dspy
    ```

    === "OpenAI"
        You can authenticate by setting the `OPENAI_API_KEY` env variable or passing `api_key` below.

        ```python linenums="1"
        import dspy
        lm = dspy.LM("openai/gpt-5-mini", api_key="YOUR_OPENAI_API_KEY")
        dspy.configure(lm=lm)
        ```

    === "Anthropic"
        You can authenticate by setting the `ANTHROPIC_API_KEY` env variable or passing `api_key` below.

        ```python linenums="1"
        import dspy
        lm = dspy.LM("anthropic/claude-sonnet-4-5-20250929", api_key="YOUR_ANTHROPIC_API_KEY")
        dspy.configure(lm=lm)
        ```

    === "Databricks"
        If you're on the Databricks platform, authentication is automatic via their SDK. If not, you can set the env variables `DATABRICKS_API_KEY` and `DATABRICKS_API_BASE`, or pass `api_key` and `api_base` below.

        ```python linenums="1"
        import dspy
        lm = dspy.LM(
            "databricks/databricks-llama-4-maverick",
            api_key="YOUR_DATABRICKS_ACCESS_TOKEN",
            api_base="YOUR_DATABRICKS_WORKSPACE_URL",  # e.g.: https://dbc-64bf4923-e39e.cloud.databricks.com/serving-endpoints
        )
        dspy.configure(lm=lm)
        ```

    === "Gemini"
        You can authenticate by setting the `GEMINI_API_KEY` env variable or passing `api_key` below.

        ```python linenums="1"
        import dspy
        lm = dspy.LM("gemini/gemini-2.5-flash", api_key="YOUR_GEMINI_API_KEY")
        dspy.configure(lm=lm)
        ```

    === "Local LMs on your laptop"
          First, install [Ollama](https://github.com/ollama/ollama) and launch its server with your LM.

          ```bash
          > curl -fsSL https://ollama.ai/install.sh | sh
          > ollama run llama3.2:1b
          ```

          Then, connect to it from your DSPy code.

        ```python linenums="1"
        import dspy
        lm = dspy.LM("ollama_chat/llama3.2:1b", api_base="http://localhost:11434", api_key="")
        dspy.configure(lm=lm)
        ```

    === "Local LMs on a GPU server"
          First, install [SGLang](https://docs.sglang.ai/get_started/install.html) and launch its server with your LM.

          ```bash
          > pip install "sglang[all]"
          > pip install flashinfer -i https://flashinfer.ai/whl/cu121/torch2.4/ 

          > CUDA_VISIBLE_DEVICES=0 python -m sglang.launch_server --port 7501 --model-path meta-llama/Llama-3.1-8B-Instruct
          ```
        
        If you don't have access from Meta to download `meta-llama/Llama-3.1-8B-Instruct`, use `Qwen/Qwen2.5-7B-Instruct` for example.

        Next, connect to your local LM from your DSPy code as an `OpenAI`-compatible endpoint.

          ```python linenums="1"
          lm = dspy.LM("openai/meta-llama/Llama-3.1-8B-Instruct",
                       api_base="http://localhost:7501/v1",  # ensure this points to your port
                       api_key="local", model_type="chat")
          dspy.configure(lm=lm)
          ```

    === "Other providers"
        In DSPy, you can use any of the dozens of [LLM providers supported by LiteLLM](https://docs.litellm.ai/docs/providers). Simply follow their instructions for which `{PROVIDER}_API_KEY` to set and how to write pass the `{provider_name}/{model_name}` to the constructor.

        Some examples:

        - `anyscale/mistralai/Mistral-7B-Instruct-v0.1`, with `ANYSCALE_API_KEY`
        - `together_ai/togethercomputer/llama-2-70b-chat`, with `TOGETHERAI_API_KEY`
        - `sagemaker/<your-endpoint-name>`, with `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION_NAME`
        - `azure/<your_deployment_name>`, with `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION`, and the optional `AZURE_AD_TOKEN` and `AZURE_API_TYPE`

        
        If your provider offers an OpenAI-compatible endpoint, just add an `openai/` prefix to your full model name.

        ```python linenums="1"
        import dspy
        lm = dspy.LM("openai/your-model-name", api_key="PROVIDER_API_KEY", api_base="YOUR_PROVIDER_URL")
        dspy.configure(lm=lm)
        ```

??? "Calling the LM directly."

     Idiomatic DSPy involves using _modules_, which we define in the rest of this page. However, it's still easy to call the `lm` you configured above directly. This gives you a unified API and lets you benefit from utilities like automatic caching.

     ```python linenums="1"       
     lm("Say this is a test!", temperature=0.7)  # => ['This is a test!']
     lm(messages=[{"role": "user", "content": "Say this is a test!"}])  # => ['This is a test!']
     ``` 


## 1) **Modules** help you describe AI behavior as _code_, not strings.

To build reliable AI systems, you must iterate fast. But maintaining prompts makes that hard: it forces you to tinker with strings or data _every time you change your LM, metrics, or pipeline_. Having built over a dozen best-in-class compound LM systems since 2020, we learned this the hard way—and so built DSPy to decouple AI system design from messy incidental choices about specific LMs or prompting strategies.

DSPy shifts your focus from tinkering with prompt strings to **programming with structured and declarative natural-language modules**. For every AI component in your system, you specify input/output behavior as a _signature_ and select a _module_ to assign a strategy for invoking your LM. DSPy expands your signatures into prompts and parses your typed outputs, so you can compose different modules together into ergonomic, portable, and optimizable AI systems.


!!! info "Getting Started II: Build DSPy modules for various tasks"
    Try the examples below after configuring your `lm` above. Adjust the fields to explore what tasks your LM can do well out of the box. Each tab below sets up a DSPy module, like `dspy.Predict`, `dspy.ChainOfThought`, or `dspy.ReAct`, with a task-specific _signature_. For example, `question -> answer: float` tells the module to take a question and to produce a `float` answer.

    === "Math"

        ```python linenums="1"
        math = dspy.ChainOfThought("question -> answer: float")
        math(question="Two dice are tossed. What is the probability that the sum equals two?")
        ```
        
        **Possible Output:**
        ```text
        Prediction(
            reasoning='When two dice are tossed, each die has 6 faces, resulting in a total of 6 x 6 = 36 possible outcomes. The sum of the numbers on the two dice equals two only when both dice show a 1. This is just one specific outcome: (1, 1). Therefore, there is only 1 favorable outcome. The probability of the sum being two is the number of favorable outcomes divided by the total number of possible outcomes, which is 1/36.',
            answer=0.0277776
        )
        ```

    === "RAG"

        ```python linenums="1"       
        def search_wikipedia(query: str) -> list[str]:
            results = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")(query, k=3)
            return [x["text"] for x in results]
        
        rag = dspy.ChainOfThought("context, question -> response")

        question = "What's the name of the castle that David Gregory inherited?"
        rag(context=search_wikipedia(question), question=question)
        ```
        
        **Possible Output:**
        ```text
        Prediction(
            reasoning='The context provides information about David Gregory, a Scottish physician and inventor. It specifically mentions that he inherited Kinnairdy Castle in 1664. This detail directly answers the question about the name of the castle that David Gregory inherited.',
            response='Kinnairdy Castle'
        )
        ```

    === "Classification"

        ```python linenums="1"
        from typing import Literal

        class Classify(dspy.Signature):
            """Classify sentiment of a given sentence."""
            
            sentence: str = dspy.InputField()
            sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField()
            confidence: float = dspy.OutputField()

        classify = dspy.Predict(Classify)
        classify(sentence="This book was super fun to read, though not the last chapter.")
        ```
        
        **Possible Output:**

        ```text
        Prediction(
            sentiment='positive',
            confidence=0.75
        )
        ```

    === "Information Extraction"

        ```python linenums="1"        
        class ExtractInfo(dspy.Signature):
            """Extract structured information from text."""
            
            text: str = dspy.InputField()
            title: str = dspy.OutputField()
            headings: list[str] = dspy.OutputField()
            entities: list[dict[str, str]] = dspy.OutputField(desc="a list of entities and their metadata")
        
        module = dspy.Predict(ExtractInfo)

        text = "Apple Inc. announced its latest iPhone 14 today." \
            "The CEO, Tim Cook, highlighted its new features in a press release."
        response = module(text=text)

        print(response.title)
        print(response.headings)
        print(response.entities)
        ```
        
        **Possible Output:**
        ```text
        Apple Inc. Announces iPhone 14
        ['Introduction', "CEO's Statement", 'New Features']
        [{'name': 'Apple Inc.', 'type': 'Organization'}, {'name': 'iPhone 14', 'type': 'Product'}, {'name': 'Tim Cook', 'type': 'Person'}]
        ```

    === "Agents"

        ```python linenums="1"       
        def evaluate_math(expression: str):
            return dspy.PythonInterpreter({}).execute(expression)

        def search_wikipedia(query: str):
            results = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")(query, k=3)
            return [x["text"] for x in results]

        react = dspy.ReAct("question -> answer: float", tools=[evaluate_math, search_wikipedia])

        pred = react(question="What is 9362158 divided by the year of birth of David Gregory of Kinnairdy castle?")
        print(pred.answer)
        ```
        
        **Possible Output:**

        ```text
        5761.328
        ```
    
    === "Multi-Stage Pipelines"

        ```python linenums="1"       
        class Outline(dspy.Signature):
            """Outline a thorough overview of a topic."""
            
            topic: str = dspy.InputField()
            title: str = dspy.OutputField()
            sections: list[str] = dspy.OutputField()
            section_subheadings: dict[str, list[str]] = dspy.OutputField(desc="mapping from section headings to subheadings")

        class DraftSection(dspy.Signature):
            """Draft a top-level section of an article."""
            
            topic: str = dspy.InputField()
            section_heading: str = dspy.InputField()
            section_subheadings: list[str] = dspy.InputField()
            content: str = dspy.OutputField(desc="markdown-formatted section")

        class DraftArticle(dspy.Module):
            def __init__(self):
                self.build_outline = dspy.ChainOfThought(Outline)
                self.draft_section = dspy.ChainOfThought(DraftSection)

            def forward(self, topic):
                outline = self.build_outline(topic=topic)
                sections = []
                for heading, subheadings in outline.section_subheadings.items():
                    section, subheadings = f"## {heading}", [f"### {subheading}" for subheading in subheadings]
                    section = self.draft_section(topic=outline.title, section_heading=section, section_subheadings=subheadings)
                    sections.append(section.content)
                return dspy.Prediction(title=outline.title, sections=sections)

        draft_article = DraftArticle()
        article = draft_article(topic="World Cup 2002")
        ```
        
        **Possible Output:**

        A 1500-word article on the topic, e.g.

        ```text
        ## Qualification Process

        The qualification process for the 2002 FIFA World Cup involved a series of..... [shortened here for presentation].

        ### UEFA Qualifiers

        The UEFA qualifiers involved 50 teams competing for 13..... [shortened here for presentation].

        .... [rest of the article]
        ```

        Note that DSPy makes it straightforward to optimize multi-stage modules like this. As long as you can evaluate the _final_ output of the system, every DSPy optimizer can tune all of the intermediate modules.

??? "Using DSPy in practice: from quick scripting to building sophisticated systems."

    Standard prompts conflate interface ("what should the LM do?") with implementation ("how do we tell it to do that?"). DSPy isolates the former as _signatures_ so we can infer the latter or learn it from data — in the context of a bigger program.
    
    Even before you start using optimizers, DSPy's modules allow you to script effective LM systems as ergonomic, portable _code_. Across many tasks and LMs, we maintain _signature test suites_ that assess the reliability of the built-in DSPy adapters. Adapters are the components that map signatures to prompts prior to optimization. If you find a task where a simple prompt consistently outperforms idiomatic DSPy for your LM, consider that a bug and [file an issue](https://github.com/stanfordnlp/dspy/issues). We'll use this to improve the built-in adapters.


## 2) **Optimizers** tune the prompts and weights of your AI modules.

DSPy provides you with the tools to compile high-level code with natural language annotations into the low-level computations, prompts, or weight updates that align your LM with your program's structure and metrics. If you change your code or your metrics, you can simply re-compile accordingly.

Given a few tens or hundreds of representative _inputs_ of your task and a _metric_ that can measure the quality of your system's outputs, you can use a DSPy optimizer. Different optimizers in DSPy work by **synthesizing good few-shot examples** for every module, like `dspy.BootstrapRS`,<sup>[1](https://arxiv.org/abs/2310.03714)</sup> **proposing and intelligently exploring better natural-language instructions** for every prompt, like [`dspy.GEPA`](https://dspy.ai/tutorials/gepa_ai_program/)<sup>[2](https://arxiv.org/abs/2507.19457)</sup>, `dspy.MIPROv2`,<sup>[3](https://arxiv.org/abs/2406.11695)</sup> and **building datasets for your modules and using them to finetune the LM weights** in your system, like `dspy.BootstrapFinetune`.<sup>[4](https://arxiv.org/abs/2407.10930)</sup> For detailed tutorials on running `dspy.GEPA`, please take a look at [dspy.GEPA tutorials](https://dspy.ai/tutorials/gepa_ai_program/).


!!! info "Getting Started III: Optimizing the LM prompts or weights in DSPy programs"
    A typical simple optimization run costs on the order of $2 USD and takes around 20 minutes, but be careful when running optimizers with very large LMs or very large datasets.
    Optimization can cost as little as a few cents or up to tens of dollars, depending on your LM, dataset, and configuration.

    Examples below rely on HuggingFace/datasets, you can install it by the command below.

    ```bash
    > pip install -U datasets
    ```

    === "Optimizing prompts for a ReAct agent"
        This is a minimal but fully runnable example of setting up a `dspy.ReAct` agent that answers questions via
        search from Wikipedia and then optimizing it using `dspy.MIPROv2` in the cheap `light` mode on 500
        question-answer pairs sampled from the `HotPotQA` dataset.

        ```python linenums="1"
        import dspy
        from dspy.datasets import HotPotQA

        dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

        def search_wikipedia(query: str) -> list[str]:
            results = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")(query, k=3)
            return [x["text"] for x in results]

        trainset = [x.with_inputs('question') for x in HotPotQA(train_seed=2024, train_size=500).train]
        react = dspy.ReAct("question -> answer", tools=[search_wikipedia])

        tp = dspy.MIPROv2(metric=dspy.evaluate.answer_exact_match, auto="light", num_threads=24)
        optimized_react = tp.compile(react, trainset=trainset)
        ```

        An informal run like this raises ReAct's score from 24% to 51%, by teaching `gpt-4o-mini` more about the specifics of the task.

    === "Optimizing prompts for RAG"
        Given a retrieval index to `search`, your favorite `dspy.LM`, and a small `trainset` of questions and ground-truth responses, the following code snippet can optimize your RAG system with long outputs against the built-in `SemanticF1` metric, which is implemented as a DSPy module.

        ```python linenums="1"
        class RAG(dspy.Module):
            def __init__(self, num_docs=5):
                self.num_docs = num_docs
                self.respond = dspy.ChainOfThought("context, question -> response")

            def forward(self, question):
                context = search(question, k=self.num_docs)   # defined in tutorial linked below
                return self.respond(context=context, question=question)

        tp = dspy.MIPROv2(metric=dspy.evaluate.SemanticF1(decompositional=True), auto="medium", num_threads=24)
        optimized_rag = tp.compile(RAG(), trainset=trainset, max_bootstrapped_demos=2, max_labeled_demos=2)
        ```

        For a complete RAG example that you can run, start this [tutorial](tutorials/rag/index.ipynb). It improves the quality of a RAG system over a subset of StackExchange communities by 10% relative gain.

    === "Optimizing weights for Classification"
        <details><summary>Click to show dataset setup code.</summary>

        ```python linenums="1"
        import random
        from typing import Literal

        from datasets import load_dataset

        import dspy
        from dspy.datasets import DataLoader

        # Load the Banking77 dataset.
        CLASSES = load_dataset("PolyAI/banking77", split="train", trust_remote_code=True).features["label"].names
        kwargs = {"fields": ("text", "label"), "input_keys": ("text",), "split": "train", "trust_remote_code": True}

        # Load the first 2000 examples from the dataset, and assign a hint to each *training* example.
        trainset = [
            dspy.Example(x, hint=CLASSES[x.label], label=CLASSES[x.label]).with_inputs("text", "hint")
            for x in DataLoader().from_huggingface(dataset_name="PolyAI/banking77", **kwargs)[:2000]
        ]
        random.Random(0).shuffle(trainset)
        ```
        </details>

        ```python linenums="1"
        import dspy
        lm=dspy.LM('openai/gpt-4o-mini-2024-07-18')

        # Define the DSPy module for classification. It will use the hint at training time, if available.
        signature = dspy.Signature("text, hint -> label").with_updated_fields("label", type_=Literal[tuple(CLASSES)])
        classify = dspy.ChainOfThought(signature)
        classify.set_lm(lm)

        # Optimize via BootstrapFinetune.
        optimizer = dspy.BootstrapFinetune(metric=(lambda x, y, trace=None: x.label == y.label), num_threads=24)
        optimized = optimizer.compile(classify, trainset=trainset)

        optimized(text="What does a pending cash withdrawal mean?")
        
        # For a complete fine-tuning tutorial, see: https://dspy.ai/tutorials/classification_finetuning/
        ```

        **Possible Output (from the last line):**
        ```text
        Prediction(
            reasoning='A pending cash withdrawal indicates that a request to withdraw cash has been initiated but has not yet been completed or processed. This status means that the transaction is still in progress and the funds have not yet been deducted from the account or made available to the user.',
            label='pending_cash_withdrawal'
        )
        ```

        An informal run similar to this on DSPy 2.5.29 raises GPT-4o-mini's score 66% to 87%.


??? "What's an example of a DSPy optimizer? How do different optimizers work?"

    Take the `dspy.MIPROv2` optimizer as an example. First, MIPRO starts with the **bootstrapping stage**. It takes your program, which may be unoptimized at this point, and runs it many times across different inputs to collect traces of input/output behavior for each one of your modules. It filters these traces to keep only those that appear in trajectories scored highly by your metric. Second, MIPRO enters its **grounded proposal stage**. It previews your DSPy program's code, your data, and traces from running your program, and uses them to draft many potential instructions for every prompt in your program. Third, MIPRO launches the **discrete search stage**. It samples mini-batches from your training set, proposes a combination of instructions and traces to use for constructing every prompt in the pipeline, and evaluates the candidate program on the mini-batch. Using the resulting score, MIPRO updates a surrogate model that helps the proposals get better over time.

    One thing that makes DSPy optimizers so powerful is that they can be composed. You can run `dspy.MIPROv2` and use the produced program as an input to `dspy.MIPROv2` again or, say, to `dspy.BootstrapFinetune` to get better results. This is partly the essence of `dspy.BetterTogether`. Alternatively, you can run the optimizer and then extract the top-5 candidate programs and build a `dspy.Ensemble` of them. This allows you to scale _inference-time compute_ (e.g., ensembles) as well as DSPy's unique _pre-inference time compute_ (i.e., optimization budget) in highly systematic ways.


<!-- Future:
BootstrapRS or MIPRO on ??? with a local SGLang LM
BootstrapFS on MATH with a tiny LM like Llama-3.2 with Ollama (maybe with a big teacher) -->


## 3) **DSPy's Ecosystem** advances open-source AI research.

Compared to monolithic LMs, DSPy's modular paradigm enables a large community to improve the compositional architectures, inference-time strategies, and optimizers for LM programs in an open, distributed way. This gives DSPy users more control, helps them iterate much faster, and allows their programs to get better over time by applying the latest optimizers or modules.

The DSPy research effort started at Stanford NLP in Feb 2022, building on what we had learned from developing early [compound LM systems](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/) like [ColBERT-QA](https://arxiv.org/abs/2007.00814), [Baleen](https://arxiv.org/abs/2101.00436), and [Hindsight](https://arxiv.org/abs/2110.07752). The first version was released as [DSP](https://arxiv.org/abs/2212.14024) in Dec 2022 and evolved by Oct 2023 into [DSPy](https://arxiv.org/abs/2310.03714). Thanks to [250 contributors](https://github.com/stanfordnlp/dspy/graphs/contributors), DSPy has introduced hundreds of thousands of people to building and optimizing modular LM programs.

Since then, DSPy's community has produced a large body of work on optimizers, like [MIPROv2](https://arxiv.org/abs/2406.11695), [BetterTogether](https://arxiv.org/abs/2407.10930), and [LeReT](https://arxiv.org/abs/2410.23214), on program architectures, like [STORM](https://arxiv.org/abs/2402.14207), [IReRa](https://arxiv.org/abs/2401.12178), and [DSPy Assertions](https://arxiv.org/abs/2312.13382), and on successful applications to new problems, like [PAPILLON](https://arxiv.org/abs/2410.17127), [PATH](https://arxiv.org/abs/2406.11706), [WangLab@MEDIQA](https://arxiv.org/abs/2404.14544), [UMD's Prompting Case Study](https://arxiv.org/abs/2406.06608), and [Haize's Red-Teaming Program](https://blog.haizelabs.com/posts/dspy/), in addition to many open-source projects, production applications, and other [use cases](community/use-cases.md).

---


## Learning DSPy {#learning-dspy}

*Source: `learn/index.md`*

# Learning DSPy: An Overview

DSPy exposes a very small API that you can learn quickly. However, building a new AI system is a more open-ended journey of iterative development, in which you compose the tools and design patterns of DSPy to optimize for _your_ objectives. The three stages of building AI systems in DSPy are:

1) **DSPy Programming.** This is about defining your task, its constraints, exploring a few examples, and using that to inform your initial pipeline design.

2) **DSPy Evaluation.** Once your system starts working, this is the stage where you collect an initial development set, define your DSPy metric, and use these to iterate on your system more systematically.

3) **DSPy Optimization.** Once you have a way to evaluate your system, you use DSPy optimizers to tune the prompts or weights in your program.

We suggest learning and applying DSPy in this order. For example, it's unproductive to launch optimization runs using a poorly designed program or a bad metric.

---


### Programming Overview {#programming-overview}

*Source: `learn/programming/overview.md`*

# Programming in DSPy

DSPy is a bet on _writing code instead of strings_. In other words, building the right control flow is crucial. Start by **defining your task**. What are the inputs to your system and what should your system produce as output? Is it a chatbot over your data or perhaps a code assistant? Or maybe a system for translation, for highlighting snippets from search results, or for generating reports with citations?

Next, **define your initial pipeline**. Can your DSPy program just be a single module or do you need to break it down into a few steps? Do you need retrieval or other tools, like a calculator or a calendar API? Is there a typical workflow for solving your problem in multiple well-scoped steps, or do you want more open-ended tool use with agents for your task? Think about these but start simple, perhaps with just a single `dspy.ChainOfThought` module, then add complexity incrementally based on observations.

As you do this, **craft and try a handful of examples** of the inputs to your program. Consider using a powerful LM at this point, or a couple of different LMs, just to understand what's possible. Record interesting (both easy and hard) examples you try. This will be useful when you are doing evaluation and optimization later.


??? "Beyond encouraging good design patterns, how does DSPy help here?"

    Conventional prompts couple your fundamental system architecture with incidental choices not portable to new LMs, objectives, or pipelines. A conventional prompt asks the LM to take some inputs and produce some outputs of certain types (a _signature_), formats the inputs in certain ways and requests outputs in a form it can parse accurately (an _adapter_), asks the LM to apply certain strategies like "thinking step by step" or using tools (a _module_'s logic), and relies on substantial trial-and-error to discover the right way to ask each LM to do this (a form of manual _optimization_).
    
    DSPy separates these concerns and automates the lower-level ones until you need to consider them. This allow you to write much shorter code, with much higher portability. For example, if you write a program using DSPy modules, you can swap the LM or its adapter without changing the rest of your logic. Or you can exchange one _module_, like `dspy.ChainOfThought`, with another, like `dspy.ProgramOfThought`, without modifying your signatures. When you're ready to use optimizers, the same program can have its prompts optimized or its LM weights fine-tuned.

---


### Language Models {#language-models}

*Source: `learn/programming/language_models.md`*

# Language Models

The first step in any DSPy code is to set up your language model. For example, you can configure OpenAI's GPT-4o-mini as your default LM as follows.

```python linenums="1"
# Authenticate via `OPENAI_API_KEY` env: import os; os.environ['OPENAI_API_KEY'] = 'here'
lm = dspy.LM('openai/gpt-4o-mini')
dspy.configure(lm=lm)
```

!!! info "A few different LMs"

    === "OpenAI"
        You can authenticate by setting the `OPENAI_API_KEY` env variable or passing `api_key` below.

        ```python linenums="1"
        import dspy
        lm = dspy.LM('openai/gpt-4o-mini', api_key='YOUR_OPENAI_API_KEY')
        dspy.configure(lm=lm)
        ```

    === "Gemini (AI Studio)"
        You can authenticate by setting the GEMINI_API_KEY env variable or passing `api_key` below.

        ```python linenums="1"
        import dspy
        lm = dspy.LM('gemini/gemini-2.5-pro-preview-03-25', api_key='GEMINI_API_KEY')
        dspy.configure(lm=lm)
        ```

    === "Anthropic"
        You can authenticate by setting the ANTHROPIC_API_KEY env variable or passing `api_key` below.

        ```python linenums="1"
        import dspy
        lm = dspy.LM('anthropic/claude-sonnet-4-5-20250929', api_key='YOUR_ANTHROPIC_API_KEY')
        dspy.configure(lm=lm)
        ```

    === "Vertex AI (GCP)"
        For Google Cloud's Vertex AI, authenticate with a service account JSON key or Application Default Credentials. You can pass credentials directly in code or set environment variables.

        ```python linenums="1"
        import dspy
        import json

        # Load the service account JSON and convert to a string
        with open("service_account.json") as f:
            credentials = json.dumps(json.load(f))

        lm = dspy.LM(
            "vertex_ai/gemini-2.0-flash",
            vertex_credentials=credentials,
            vertex_project="your-gcp-project-id",
            vertex_location="us-central1",
        )
        dspy.configure(lm=lm)
        ```

        Alternatively, set environment variables and skip the kwargs:

        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service_account.json"
        export VERTEXAI_PROJECT="your-gcp-project-id"
        export VERTEXAI_LOCATION="us-central1"
        ```

        ```python linenums="1"
        import dspy
        lm = dspy.LM("vertex_ai/gemini-2.0-flash")
        dspy.configure(lm=lm)
        ```

        !!! warning "Common pitfalls"
            - Use the `vertex_ai/` model prefix, not `gemini/`. The `gemini/` prefix routes to the Gemini API which requires an API key instead of GCP credentials.
            - Use `vertex_project` and `vertex_location`, not `project` or `location`. Parameters without the `vertex_` prefix are silently ignored and LiteLLM falls back to defaults, which may cause requests to land in an unintended region.

    === "Databricks"
        If you're on the Databricks platform, authentication is automatic via their SDK. If not, you can set the env variables `DATABRICKS_API_KEY` and `DATABRICKS_API_BASE`, or pass `api_key` and `api_base` below.

        ```python linenums="1"
        import dspy
        lm = dspy.LM('databricks/databricks-meta-llama-3-1-70b-instruct')
        dspy.configure(lm=lm)
        ```

    === "Local LMs on a GPU server"
          First, install [SGLang](https://sgl-project.github.io/start/install.html) and launch its server with your LM.

          ```bash
          > pip install "sglang[all]"
          > pip install flashinfer -i https://flashinfer.ai/whl/cu121/torch2.4/ 

          > CUDA_VISIBLE_DEVICES=0 python -m sglang.launch_server --port 7501 --model-path meta-llama/Meta-Llama-3-8B-Instruct
          ```

          Then, connect to it from your DSPy code as an OpenAI-compatible endpoint.

          ```python linenums="1"
          lm = dspy.LM("openai/meta-llama/Meta-Llama-3-8B-Instruct",
                           api_base="http://localhost:7501/v1",  # ensure this points to your port
                           api_key="", model_type='chat')
          dspy.configure(lm=lm)
          ```

    === "Local LMs on your laptop"
          First, install [Ollama](https://github.com/ollama/ollama) and launch its server with your LM.

          ```bash
          > curl -fsSL https://ollama.ai/install.sh | sh
          > ollama run llama3.2:1b
          ```

          Then, connect to it from your DSPy code.

        ```python linenums="1"
        import dspy
        lm = dspy.LM('ollama_chat/llama3.2', api_base='http://localhost:11434', api_key='')
        dspy.configure(lm=lm)
        ```

    === "Other providers"
        In DSPy, you can use any of the dozens of [LLM providers supported by LiteLLM](https://docs.litellm.ai/docs/providers). Simply follow their instructions for which `{PROVIDER}_API_KEY` to set and how to write pass the `{provider_name}/{model_name}` to the constructor. 

        Some examples:

        - `anyscale/mistralai/Mistral-7B-Instruct-v0.1`, with `ANYSCALE_API_KEY`
        - `together_ai/togethercomputer/llama-2-70b-chat`, with `TOGETHERAI_API_KEY`
        - `sagemaker/<your-endpoint-name>`, with `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION_NAME`
        - `azure/<your_deployment_name>`, with `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION`, and the optional `AZURE_AD_TOKEN` and `AZURE_API_TYPE` as environment variables. If you are initiating external models without setting environment variables, use the following:
        `lm = dspy.LM('azure/<your_deployment_name>', api_key = 'AZURE_API_KEY' , api_base = 'AZURE_API_BASE', api_version = 'AZURE_API_VERSION')`


        
        If your provider offers an OpenAI-compatible endpoint, just add an `openai/` prefix to your full model name.

        ```python linenums="1"
        import dspy
        lm = dspy.LM('openai/your-model-name', api_key='PROVIDER_API_KEY', api_base='YOUR_PROVIDER_URL')
        dspy.configure(lm=lm)
        ```
If you run into errors, please refer to the [LiteLLM Docs](https://docs.litellm.ai/docs/providers) to verify if you are using the same variable names/following the right procedure.

## Calling the LM directly.

It's easy to call the `lm` you configured above directly. This gives you a unified API and lets you benefit from utilities like automatic caching.

```python linenums="1"       
lm("Say this is a test!", temperature=0.7)  # => ['This is a test!']
lm(messages=[{"role": "user", "content": "Say this is a test!"}])  # => ['This is a test!']
``` 

## Using the LM with DSPy modules.

Idiomatic DSPy involves using _modules_, which we discuss in the next guide.

```python linenums="1" 
# Define a module (ChainOfThought) and assign it a signature (return an answer, given a question).
qa = dspy.ChainOfThought('question -> answer')

# Run with the default LM configured with `dspy.configure` above.
response = qa(question="How many floors are in the castle David Gregory inherited?")
print(response.answer)
```
**Possible Output:**
```text
The castle David Gregory inherited has 7 floors.
```

## Using multiple LMs.

You can change the default LM globally with `dspy.configure` or change it inside a block of code with `dspy.context`.

!!! tip
    Using `dspy.configure` and `dspy.context` is thread-safe!


```python linenums="1" 
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))
response = qa(question="How many floors are in the castle David Gregory inherited?")
print('GPT-4o-mini:', response.answer)

with dspy.context(lm=dspy.LM('openai/gpt-3.5-turbo')):
    response = qa(question="How many floors are in the castle David Gregory inherited?")
    print('GPT-3.5-turbo:', response.answer)
```
**Possible Output:**
```text
GPT-4o-mini: The number of floors in the castle David Gregory inherited cannot be determined with the information provided.
GPT-3.5-turbo: The castle David Gregory inherited has 7 floors.
```

## Configuring LM generation.

For any LM, you can configure any of the following attributes at initialization or in each subsequent call.

```python linenums="1" 
gpt_4o_mini = dspy.LM('openai/gpt-4o-mini', temperature=0.9, max_tokens=3000, stop=None, cache=False)
```

By default LMs in DSPy are cached. If you repeat the same call, you will get the same outputs. But you can turn off caching by setting `cache=False`.

If you want to keep caching enabled but force a new request (for example, to obtain diverse outputs),
pass a unique `rollout_id` and set a non-zero `temperature` in your call. DSPy hashes both the inputs
and the `rollout_id` when looking up a cache entry, so different values force a new LM request while
still caching future calls with the same inputs and `rollout_id`. The ID is also recorded in
`lm.history`, which makes it easy to track or compare different rollouts during experiments. Changing
only the `rollout_id` while keeping `temperature=0` will not affect the LM's output.

```python linenums="1"
lm("Say this is a test!", rollout_id=1, temperature=1.0)
```

You can pass these LM kwargs directly to DSPy modules as well. Supplying them at
initialization sets the defaults for every call:

```python linenums="1"
predict = dspy.Predict("question -> answer", rollout_id=1, temperature=1.0)
```

To override them for a single invocation, provide a ``config`` dictionary when
calling the module:

```python linenums="1"
predict = dspy.Predict("question -> answer")
predict(question="What is 1 + 52?", config={"rollout_id": 5, "temperature": 1.0})
```

In both cases, ``rollout_id`` is forwarded to the underlying LM, affects
its caching behavior, and is stored alongside each response so you can
replay or analyze specific rollouts later.


## Inspecting output and usage metadata.

Every LM object maintains the history of its interactions, including inputs, outputs, token usage (and $$$ cost), and metadata.

```python linenums="1" 
len(lm.history)  # e.g., 3 calls to the LM

lm.history[-1].keys()  # access the last call to the LM, with all metadata
```

**Output:**
```text
dict_keys(['prompt', 'messages', 'kwargs', 'response', 'outputs', 'usage', 'cost', 'timestamp', 'uuid', 'model', 'response_model', 'model_type])
```

## Using the Responses API

By default, DSPy calls language models (LMs) using LiteLLM's [Chat Completions API](https://docs.litellm.ai/docs/completion), which is suitable for most standard models and tasks. However, some advanced models, such as OpenAI's reasoning models (e.g., `gpt-5` or other future models), may offer improved quality or additional features when accessed via the [Responses API](https://docs.litellm.ai/docs/response_api), which is supported in DSPy.

**When should you use the Responses API?**

- If you are working with models that support or require the `responses` endpoint (such as OpenAI's reasoning models).
- When you want to leverage enhanced reasoning, multi-turn, or richer output capabilities provided by certain models.

**How to enable the Responses API in DSPy:**

To enable the Responses API, just set `model_type="responses"` when creating the `dspy.LM` instance.

```python
import dspy

# Configure DSPy to use the Responses API for your language model
dspy.configure(
    lm=dspy.LM(
        "openai/gpt-5-mini",
        model_type="responses",
        temperature=1.0,
        max_tokens=16000,
    ),
)
```

Please note that not all models or providers support the Responses API, check [LiteLLM's documentation](https://docs.litellm.ai/docs/response_api) for more details.


## Advanced: Building custom LMs and writing your own Adapters.

Though rarely needed, you can write custom LMs by inheriting from `dspy.BaseLM`. Another advanced layer in the DSPy ecosystem is that of _adapters_, which sit between DSPy signatures and LMs. A future version of this guide will discuss these advanced features, though you likely don't need them.

---


### Signatures {#signatures}

*Source: `learn/programming/signatures.md`*

# Signatures

When we assign tasks to LMs in DSPy, we specify the behavior we need as a Signature.

**A signature is a declarative specification of input/output behavior of a DSPy module.** Signatures allow you to tell the LM _what_ it needs to do, rather than specify _how_ we should ask the LM to do it.

You're probably familiar with function signatures, which specify the input and output arguments and their types. DSPy signatures are similar, but with a couple of differences. While typical function signatures just _describe_ things, DSPy Signatures _declare and initialize the behavior_ of modules. Moreover, the field names matter in DSPy Signatures. You express semantic roles in plain English: a `question` is different from an `answer`, a `sql_query` is different from `python_code`.

## Why should I use a DSPy Signature?

For modular and clean code, in which LM calls can be optimized into high-quality prompts (or automatic finetunes). Most people coerce LMs to do tasks by hacking long, brittle prompts. Or by collecting/generating data for fine-tuning. Writing signatures is far more modular, adaptive, and reproducible than hacking at prompts or finetunes. The DSPy compiler will figure out how to build a highly-optimized prompt for your LM (or finetune your small LM) for your signature, on your data, and within your pipeline. In many cases, we found that compiling leads to better prompts than humans write. Not because DSPy optimizers are more creative than humans, but simply because they can try more things and tune the metrics directly.

## **Inline** DSPy Signatures

Signatures can be defined as a short string, with argument names and optional types that define semantic roles for inputs/outputs.

1. Question Answering: `"question -> answer"`, which is equivalent to `"question: str -> answer: str"` as the default type is always `str`

2. Sentiment Classification: `"sentence -> sentiment: bool"`, e.g. `True` if positive

3. Summarization: `"document -> summary"`

Your signatures can also have multiple input/output fields with types:

4. Retrieval-Augmented Question Answering: `"context: list[str], question: str -> answer: str"`

5. Multiple-Choice Question Answering with Reasoning: `"question, choices: list[str] -> reasoning: str, selection: int"`

**Tip:** For fields, any valid variable names work! Field names should be semantically meaningful, but start simple and don't prematurely optimize keywords! Leave that kind of hacking to the DSPy compiler. For example, for summarization, it's probably fine to say `"document -> summary"`, `"text -> gist"`, or `"long_context -> tldr"`.

You can also add instructions to your inline signature, which can use variables at runtime. Use the `instructions` keyword argument to add instructions to your signature.

```python
toxicity = dspy.Predict(
    dspy.Signature(
        "comment -> toxic: bool",
        instructions="Mark as 'toxic' if the comment includes insults, harassment, or sarcastic derogatory remarks.",
    )
)
comment = "you are beautiful."
toxicity(comment=comment).toxic
```

**Output:**
```text
False
```


### Example A: Sentiment Classification

```python
sentence = "it's a charming and often affecting journey."  # example from the SST-2 dataset.

classify = dspy.Predict('sentence -> sentiment: bool')  # we'll see an example with Literal[] later
classify(sentence=sentence).sentiment
```
**Output:**
```text
True
```

### Example B: Summarization

```python
# Example from the XSum dataset.
document = """The 21-year-old made seven appearances for the Hammers and netted his only goal for them in a Europa League qualification round match against Andorran side FC Lustrains last season. Lee had two loan spells in League One last term, with Blackpool and then Colchester United. He scored twice for the U's but was unable to save them from relegation. The length of Lee's contract with the promoted Tykes has not been revealed. Find all the latest football transfers on our dedicated page."""

summarize = dspy.ChainOfThought('document -> summary')
response = summarize(document=document)

print(response.summary)
```
**Possible Output:**
```text
The 21-year-old Lee made seven appearances and scored one goal for West Ham last season. He had loan spells in League One with Blackpool and Colchester United, scoring twice for the latter. He has now signed a contract with Barnsley, but the length of the contract has not been revealed.
```

Many DSPy modules (except `dspy.Predict`) return auxiliary information by expanding your signature under the hood.

For example, `dspy.ChainOfThought` also adds a `reasoning` field that includes the LM's reasoning before it generates the output `summary`.

```python
print("Reasoning:", response.reasoning)
```
**Possible Output:**
```text
Reasoning: We need to highlight Lee's performance for West Ham, his loan spells in League One, and his new contract with Barnsley. We also need to mention that his contract length has not been disclosed.
```

## **Class-based** DSPy Signatures

For some advanced tasks, you need more verbose signatures. This is typically to:

1. Clarify something about the nature of the task (expressed below as a `docstring`).

2. Supply hints on the nature of an input field, expressed as a `desc` keyword argument for `dspy.InputField`.

3. Supply constraints on an output field, expressed as a `desc` keyword argument for `dspy.OutputField`.

### Example C: Classification

```python
from typing import Literal

class Emotion(dspy.Signature):
    """Classify emotion."""
    
    sentence: str = dspy.InputField()
    sentiment: Literal['sadness', 'joy', 'love', 'anger', 'fear', 'surprise'] = dspy.OutputField()

sentence = "i started feeling a little vulnerable when the giant spotlight started blinding me"  # from dair-ai/emotion

classify = dspy.Predict(Emotion)
classify(sentence=sentence)
```
**Possible Output:**
```text
Prediction(
    sentiment='fear'
)
```

**Tip:** There's nothing wrong with specifying your requests to the LM more clearly. Class-based Signatures help you with that. However, don't prematurely tune the keywords of your signature by hand. The DSPy optimizers will likely do a better job (and will transfer better across LMs).

### Example D: A metric that evaluates faithfulness to citations

```python
class CheckCitationFaithfulness(dspy.Signature):
    """Verify that the text is based on the provided context."""

    context: str = dspy.InputField(desc="facts here are assumed to be true")
    text: str = dspy.InputField()
    faithfulness: bool = dspy.OutputField()
    evidence: dict[str, list[str]] = dspy.OutputField(desc="Supporting evidence for claims")

context = "The 21-year-old made seven appearances for the Hammers and netted his only goal for them in a Europa League qualification round match against Andorran side FC Lustrains last season. Lee had two loan spells in League One last term, with Blackpool and then Colchester United. He scored twice for the U's but was unable to save them from relegation. The length of Lee's contract with the promoted Tykes has not been revealed. Find all the latest football transfers on our dedicated page."

text = "Lee scored 3 goals for Colchester United."

faithfulness = dspy.ChainOfThought(CheckCitationFaithfulness)
faithfulness(context=context, text=text)
```
**Possible Output:**
```text
Prediction(
    reasoning="Let's check the claims against the context. The text states Lee scored 3 goals for Colchester United, but the context clearly states 'He scored twice for the U's'. This is a direct contradiction.",
    faithfulness=False,
    evidence={'goal_count': ["scored twice for the U's"]}
)
```

### Example E: Multi-modal image classification

```python
class DogPictureSignature(dspy.Signature):
    """Output the dog breed of the dog in the image."""
    image_1: dspy.Image = dspy.InputField(desc="An image of a dog")
    answer: str = dspy.OutputField(desc="The dog breed of the dog in the image")

image_url = "https://picsum.photos/id/237/200/300"
classify = dspy.Predict(DogPictureSignature)
classify(image_1=dspy.Image.from_url(image_url))
```

**Possible Output:**

```text
Prediction(
    answer='Labrador Retriever'
)
```

## Type Resolution in Signatures

DSPy signatures support various annotation types:

1. **Basic types** like `str`, `int`, `bool`
2. **Typing module types** like `list[str]`, `dict[str, int]`, `Optional[float]`. `Union[str, int]`
3. **Custom types** defined in your code
4. **Dot notation** for nested types with proper configuration
5. **Special data types** like `dspy.Image, dspy.History`

### Working with Custom Types

```python
# Simple custom type
class QueryResult(pydantic.BaseModel):
    text: str
    score: float

signature = dspy.Signature("query: str -> result: QueryResult")

class MyContainer:
    class Query(pydantic.BaseModel):
        text: str
    class Score(pydantic.BaseModel):
        score: float

signature = dspy.Signature("query: MyContainer.Query -> score: MyContainer.Score")
```

## Using signatures to build modules & compiling them

While signatures are convenient for prototyping with structured inputs/outputs, that's not the only reason to use them!

You should compose multiple signatures into bigger [DSPy modules](modules.md) and [compile these modules into optimized prompts](../optimization/optimizers.md) and finetunes.

---


### Modules {#modules}

*Source: `learn/programming/modules.md`*

# Modules

A **DSPy module** is a building block for programs that use LMs.

- Each built-in module abstracts a **prompting technique** (like chain of thought or ReAct). Crucially, they are generalized to handle any signature.

- A DSPy module has **learnable parameters** (i.e., the little pieces comprising the prompt and the LM weights) and can be invoked (called) to process inputs and return outputs.

- Multiple modules can be composed into bigger modules (programs). DSPy modules are inspired directly by NN modules in PyTorch, but applied to LM programs.


## How do I use a built-in module, like `dspy.Predict` or `dspy.ChainOfThought`?

Let's start with the most fundamental module, `dspy.Predict`. Internally, all other DSPy modules are built using `dspy.Predict`. We'll assume you are already at least a little familiar with [DSPy signatures](signatures.md), which are declarative specs for defining the behavior of any module we use in DSPy.

To use a module, we first **declare** it by giving it a signature. Then we **call** the module with the input arguments, and extract the output fields!

```python
sentence = "it's a charming and often affecting journey."  # example from the SST-2 dataset.

# 1) Declare with a signature.
classify = dspy.Predict('sentence -> sentiment: bool')

# 2) Call with input argument(s). 
response = classify(sentence=sentence)

# 3) Access the output.
print(response.sentiment)
```
**Output:**
```text
True
```

When we declare a module, we can pass configuration keys to it.

Below, we'll pass a simple config key like `temperature`. You can also pass other generation keys like `max_tokens`.

Let's use `dspy.ChainOfThought`. In many cases, simply swapping `dspy.ChainOfThought` in place of `dspy.Predict` improves quality.

```python
question = "What's something great about the ColBERT retrieval model?"

# 1) Declare with a signature, and pass some config.
classify = dspy.ChainOfThought('question -> answer', temperature=0.7)

# 2) Call with input argument.
response = classify(question=question)

# 3) Access the output.
response.answer
```
**Possible Output:**
```text
'One great thing about the ColBERT retrieval model is its superior efficiency and effectiveness compared to other models.'
```

Let's discuss the output object here. The `dspy.ChainOfThought` module will generally inject a `reasoning` before the output field(s) of your signature.

Let's inspect the (first) reasoning and answer!

```python
print(f"Reasoning: {response.reasoning}")
print(f"Answer: {response.answer}")
```
**Possible Output:**
```text
Reasoning: We can consider the fact that ColBERT has shown to outperform other state-of-the-art retrieval models in terms of efficiency and effectiveness. It uses contextualized embeddings and performs document retrieval in a way that is both accurate and scalable.
Answer: One great thing about the ColBERT retrieval model is its superior efficiency and effectiveness compared to other models.
```

## What other DSPy modules are there? How can I use them?

The others are very similar. They mainly change the internal behavior with which your signature is implemented!

1. **`dspy.Predict`**: Basic predictor. Does not modify the signature. Handles the key forms of learning (i.e., storing the instructions and demonstrations and updates to the LM).

2. **`dspy.ChainOfThought`**: Teaches the LM to think step-by-step before committing to the signature's response.

3. **`dspy.ProgramOfThought`**: Teaches the LM to output code, whose execution results will dictate the response.

4. **`dspy.ReAct`**: An agent that can use tools to implement the given signature.

5. **`dspy.MultiChainComparison`**: Can compare multiple outputs from `ChainOfThought` to produce a final prediction.

6. **`dspy.RLM`**: A [Recursive Language Model](../../api/modules/RLM.md) that explores large contexts through a sandboxed Python REPL with recursive sub-LLM calls. Use when context is too large to fit in the prompt effectively.

We also have some function-style modules:

7. **`dspy.majority`**: Can do basic voting to return the most popular response from a set of predictions.


!!! info "A few examples of DSPy modules on simple tasks."
    Try the examples below after configuring your `lm`. Adjust the fields to explore what tasks your LM can do well out of the box.

    === "Math"

        ```python linenums="1"
        math = dspy.ChainOfThought("question -> answer: float")
        math(question="Two dice are tossed. What is the probability that the sum equals two?")
        ```
        
        **Possible Output:**
        ```text
        Prediction(
            reasoning='When two dice are tossed, each die has 6 faces, resulting in a total of 6 x 6 = 36 possible outcomes. The sum of the numbers on the two dice equals two only when both dice show a 1. This is just one specific outcome: (1, 1). Therefore, there is only 1 favorable outcome. The probability of the sum being two is the number of favorable outcomes divided by the total number of possible outcomes, which is 1/36.',
            answer=0.0277776
        )
        ```

    === "Retrieval-Augmented Generation"

        ```python linenums="1"       
        def search(query: str) -> list[str]:
            """Retrieves abstracts from Wikipedia."""
            results = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
            return [x['text'] for x in results]
        
        rag = dspy.ChainOfThought('context, question -> response')

        question = "What's the name of the castle that David Gregory inherited?"
        rag(context=search(question), question=question)
        ```
        
        **Possible Output:**
        ```text
        Prediction(
            reasoning='The context provides information about David Gregory, a Scottish physician and inventor. It specifically mentions that he inherited Kinnairdy Castle in 1664. This detail directly answers the question about the name of the castle that David Gregory inherited.',
            response='Kinnairdy Castle'
        )
        ```

    === "Classification"

        ```python linenums="1"
        from typing import Literal

        class Classify(dspy.Signature):
            """Classify sentiment of a given sentence."""
            
            sentence: str = dspy.InputField()
            sentiment: Literal['positive', 'negative', 'neutral'] = dspy.OutputField()
            confidence: float = dspy.OutputField()

        classify = dspy.Predict(Classify)
        classify(sentence="This book was super fun to read, though not the last chapter.")
        ```
        
        **Possible Output:**

        ```text
        Prediction(
            sentiment='positive',
            confidence=0.75
        )
        ```

    === "Information Extraction"

        ```python linenums="1"        
        text = "Apple Inc. announced its latest iPhone 14 today. The CEO, Tim Cook, highlighted its new features in a press release."

        module = dspy.Predict("text -> title, headings: list[str], entities_and_metadata: list[dict[str, str]]")
        response = module(text=text)

        print(response.title)
        print(response.headings)
        print(response.entities_and_metadata)
        ```
        
        **Possible Output:**
        ```text
        Apple Unveils iPhone 14
        ['Introduction', 'Key Features', "CEO's Statement"]
        [{'entity': 'Apple Inc.', 'type': 'Organization'}, {'entity': 'iPhone 14', 'type': 'Product'}, {'entity': 'Tim Cook', 'type': 'Person'}]
        ```

    === "Agents"

        ```python linenums="1"       
        def evaluate_math(expression: str) -> float:
            return dspy.PythonInterpreter({}).execute(expression)

        def search_wikipedia(query: str) -> str:
            results = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
            return [x['text'] for x in results]

        react = dspy.ReAct("question -> answer: float", tools=[evaluate_math, search_wikipedia])

        pred = react(question="What is 9362158 divided by the year of birth of David Gregory of Kinnairdy castle?")
        print(pred.answer)
        ```
        
        **Possible Output:**

        ```text
        5761.328
        ```


## How do I compose multiple modules into a bigger program?

DSPy is just Python code that uses modules in any control flow you like, with a little magic internally at `compile` time to trace your LM calls. What this means is that, you can just call the modules freely.

See tutorials like [multi-hop search](https://dspy.ai/tutorials/multihop_search/), whose module is reproduced below as an example.

```python linenums="1"        
class Hop(dspy.Module):
    def __init__(self, num_docs=10, num_hops=4):
        self.num_docs, self.num_hops = num_docs, num_hops
        self.generate_query = dspy.ChainOfThought('claim, notes -> query')
        self.append_notes = dspy.ChainOfThought('claim, notes, context -> new_notes: list[str], titles: list[str]')

    def forward(self, claim: str) -> list[str]:
        notes = []
        titles = []

        for _ in range(self.num_hops):
            query = self.generate_query(claim=claim, notes=notes).query
            context = search(query, k=self.num_docs)
            prediction = self.append_notes(claim=claim, notes=notes, context=context)
            notes.extend(prediction.new_notes)
            titles.extend(prediction.titles)
        
        return dspy.Prediction(notes=notes, titles=list(set(titles)))
```

Then you can create a instance of the custom module class `Hop`, then invoke it by the `__call__` method:

```
hop = Hop()
print(hop(claim="Stephen Curry is the best 3 pointer shooter ever in the human history"))
```

## How do I track LM usage?

!!! note "Version Requirement"
    LM usage tracking is available in DSPy version 2.6.16 and later.

DSPy provides built-in tracking of language model usage across all module calls. To enable tracking:

```python
dspy.configure(track_usage=True)
```

Once enabled, you can access usage statistics from any `dspy.Prediction` object:

```python
usage = prediction_instance.get_lm_usage()
```

The usage data is returned as a dictionary that maps each language model name to its usage statistics. Here's a complete example:

```python
import dspy

# Configure DSPy with tracking enabled
dspy.configure(
    lm=dspy.LM("openai/gpt-4o-mini", cache=False),
    track_usage=True
)

# Define a simple program that makes multiple LM calls
class MyProgram(dspy.Module):
    def __init__(self):
        self.predict1 = dspy.ChainOfThought("question -> answer")
        self.predict2 = dspy.ChainOfThought("question, answer -> score")

    def __call__(self, question: str) -> str:
        answer = self.predict1(question=question)
        score = self.predict2(question=question, answer=answer)
        return score

# Run the program and check usage
program = MyProgram()
output = program(question="What is the capital of France?")
print(output.get_lm_usage())
```

This will output usage statistics like:

```python
{
    'openai/gpt-4o-mini': {
        'completion_tokens': 61,
        'prompt_tokens': 260,
        'total_tokens': 321,
        'completion_tokens_details': {
            'accepted_prediction_tokens': 0,
            'audio_tokens': 0,
            'reasoning_tokens': 0,
            'rejected_prediction_tokens': 0,
            'text_tokens': None
        },
        'prompt_tokens_details': {
            'audio_tokens': 0,
            'cached_tokens': 0,
            'text_tokens': None,
            'image_tokens': None
        }
    }
}
```

When using DSPy's caching features (either in-memory or on-disk via litellm), cached responses won't count toward usage statistics. For example:

```python
# Enable caching
dspy.configure(
    lm=dspy.LM("openai/gpt-4o-mini", cache=True),
    track_usage=True
)

program = MyProgram()

# First call - will show usage statistics
output = program(question="What is the capital of Zambia?")
print(output.get_lm_usage())  # Shows token usage

# Second call - same question, will use cache
output = program(question="What is the capital of Zambia?")
print(output.get_lm_usage())  # Shows empty dict: {}
```

---


### Adapters {#adapters}

*Source: `learn/programming/adapters.md`*

# Understanding DSPy Adapters

## What are Adapters?

Adapters are the bridge between `dspy.Predict` and the actual Language Model (LM). When you call a DSPy module, the
adapter takes your signature, user inputs, and other attributes like `demos` (few-shot examples) and converts them
into multi-turn messages that get sent to the LM.

The adapter system is responsible for:

- Translating DSPy signatures into system messages that define the task and request/response structure.
- Formatting input data according to the request structure outlined in DSPy signatures.
- Parsing LM responses back into structured DSPy outputs, such as `dspy.Prediction` instances.
- Managing conversation history and function calls.
- Converting pre-built DSPy types into LM prompt messages, e.g., `dspy.Tool`, `dspy.Image`, etc.

## Configure Adapters

You can use `dspy.configure(adapter=...)` to choose the adapter for the entire Python process, or
`with dspy.context(adapter=...):` to only affect a certain namespace.

If no adapter is specified in the DSPy workflow, each `dspy.Predict.__call__` defaults to using the `dspy.ChatAdapter`. Thus, the two code snippets below are equivalent:

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

predict = dspy.Predict("question -> answer")
result = predict(question="What is the capital of France?")
```

```python
import dspy

dspy.configure(
    lm=dspy.LM("openai/gpt-4o-mini"),
    adapter=dspy.ChatAdapter(),  # This is the default value
)

predict = dspy.Predict("question -> answer")
result = predict(question="What is the capital of France?")
```

## Where Adapters Fit in the System

The flow works as follows:

1. The user calls their DSPy agent, typically a `dspy.Module` with inputs.
2. The inner `dspy.Predict` is invoked to obtain the LM response.
3. `dspy.Predict` calls **Adapter.format()**, which converts its signature, inputs, and demos into multi-turn messages sent to the `dspy.LM`. `dspy.LM` is a thin wrapper around `litellm`, which communicates with the LM endpoint.
4. The LM receives the messages and generates a response.
5. **Adapter.parse()** converts the LM response into structured DSPy outputs, as specified in the signature.
6. The caller of `dspy.Predict` receives the parsed outputs.

You can explicitly call `Adapter.format()` to view the messages sent to the LM.

```python
# Simplified flow example
signature = dspy.Signature("question -> answer")
inputs = {"question": "What is 2+2?"}
demos = [{"question": "What is 1+1?", "answer": "2"}]

adapter = dspy.ChatAdapter()
print(adapter.format(signature, demos, inputs))
```

The output should resemble:

```
{'role': 'system', 'content': 'Your input fields are:\n1. `question` (str):\nYour output fields are:\n1. `answer` (str):\nAll interactions will be structured in the following way, with the appropriate values filled in.\n\n[[ ## question ## ]]\n{question}\n\n[[ ## answer ## ]]\n{answer}\n\n[[ ## completed ## ]]\nIn adhering to this structure, your objective is: \n        Given the fields `question`, produce the fields `answer`.'}
{'role': 'user', 'content': '[[ ## question ## ]]\nWhat is 1+1?'}
{'role': 'assistant', 'content': '[[ ## answer ## ]]\n2\n\n[[ ## completed ## ]]\n'}
{'role': 'user', 'content': '[[ ## question ## ]]\nWhat is 2+2?\n\nRespond with the corresponding output fields, starting with the field `[[ ## answer ## ]]`, and then ending with the marker for `[[ ## completed ## ]]`.'}
```

You can also only fetch the system message by calling `adapter.format_system_message(signature)`.

```python
import dspy

signature = dspy.Signature("question -> answer")
system_message = dspy.ChatAdapter().format_system_message(signature)
print(system_message)
```

The output should resemble:

```
Your input fields are:
1. `question` (str):
Your output fields are:
1. `answer` (str):
All interactions will be structured in the following way, with the appropriate values filled in.

[[ ## question ## ]]
{question}
[[ ## answer ## ]]
{answer}
[[ ## completed ## ]]
In adhering to this structure, your objective is: 
        Given the fields `question`, produce the fields `answer`.
```

## Types of Adapters

DSPy offers several adapter types, each tailored for specific use cases:

### ChatAdapter

**ChatAdapter** is the default adapter and works with all language models. It uses a field-based format with special markers.

#### Format Structure

ChatAdapter uses `[[ ## field_name ## ]]` markers to delineate fields. For fields of non-primitive Python types, it includes the JSON schema of the type. Below, we use `dspy.inspect_history()` to display the formatted messages by `dspy.ChatAdapter` clearly.

```python
import dspy
import pydantic

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"), adapter=dspy.ChatAdapter())


class ScienceNews(pydantic.BaseModel):
    text: str
    scientists_involved: list[str]


class NewsQA(dspy.Signature):
    """Get news about the given science field"""

    science_field: str = dspy.InputField()
    year: int = dspy.InputField()
    num_of_outputs: int = dspy.InputField()
    news: list[ScienceNews] = dspy.OutputField(desc="science news")


predict = dspy.Predict(NewsQA)
predict(science_field="Computer Theory", year=2022, num_of_outputs=1)
dspy.inspect_history()
```

The output looks like:

```
[2025-08-15T22:24:29.378666]

System message:

Your input fields are:
1. `science_field` (str):
2. `year` (int):
3. `num_of_outputs` (int):
Your output fields are:
1. `news` (list[ScienceNews]): science news
All interactions will be structured in the following way, with the appropriate values filled in.

[[ ## science_field ## ]]
{science_field}

[[ ## year ## ]]
{year}

[[ ## num_of_outputs ## ]]
{num_of_outputs}

[[ ## news ## ]]
{news}        # note: the value you produce must adhere to the JSON schema: {"type": "array", "$defs": {"ScienceNews": {"type": "object", "properties": {"scientists_involved": {"type": "array", "items": {"type": "string"}, "title": "Scientists Involved"}, "text": {"type": "string", "title": "Text"}}, "required": ["text", "scientists_involved"], "title": "ScienceNews"}}, "items": {"$ref": "#/$defs/ScienceNews"}}

[[ ## completed ## ]]
In adhering to this structure, your objective is:
        Get news about the given science field


User message:

[[ ## science_field ## ]]
Computer Theory

[[ ## year ## ]]
2022

[[ ## num_of_outputs ## ]]
1

Respond with the corresponding output fields, starting with the field `[[ ## news ## ]]` (must be formatted as a valid Python list[ScienceNews]), and then ending with the marker for `[[ ## completed ## ]]`.


Response:

[[ ## news ## ]]
[
    {
        "scientists_involved": ["John Doe", "Jane Smith"],
        "text": "In 2022, researchers made significant advancements in quantum computing algorithms, demonstrating their potential to solve complex problems faster than classical computers. This breakthrough could revolutionize fields such as cryptography and optimization."
    }
]

[[ ## completed ## ]]
```

!!! info "Practice: locate Signature information in the printed LM history"

    Try adjusting the signature, and observe how the changes are reflected in the printed LM message.


Each field is preceded by a marker `[[ ## field_name ## ]]`. If an output field has non-primitive types, the instruction includes the type's JSON schema, and the output is formatted accordingly. Because the output field is structured as defined by ChatAdapter, it can be automatically parsed into structured data.

#### When to Use ChatAdapter

`ChatAdapter` offers the following advantages:

- **Universal compatibility**: Works with all language models, though smaller models may generate responses that do not match the required format.
- **Fallback protection**: If `ChatAdapter` fails, it automatically retries with `JSONAdapter`.

In general, `ChatAdapter` is a reliable choice if you don't have specific requirements.

#### When Not to Use ChatAdapter

Avoid using `ChatAdapter` if you are:

- **Latency sensitive**: `ChatAdapter` includes more boilerplate output tokens compared to other adapters, so if you're building a system sensitive to latency, consider using a different adapter.

### JSONAdapter

**JSONAdapter** prompts the LM to return JSON data containing all output fields as specified in the signature. It is effective for models that support structured output via the `response_format` parameter, leveraging native JSON generation capabilities for more reliable parsing.

#### Format Structure

The input part of the prompt formatted by `JSONAdapter` is similar to `ChatAdapter`, but the output part differs, as shown below:

```python
import dspy
import pydantic

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"), adapter=dspy.JSONAdapter())


class ScienceNews(pydantic.BaseModel):
    text: str
    scientists_involved: list[str]


class NewsQA(dspy.Signature):
    """Get news about the given science field"""

    science_field: str = dspy.InputField()
    year: int = dspy.InputField()
    num_of_outputs: int = dspy.InputField()
    news: list[ScienceNews] = dspy.OutputField(desc="science news")


predict = dspy.Predict(NewsQA)
predict(science_field="Computer Theory", year=2022, num_of_outputs=1)
dspy.inspect_history()
```

```
System message:

Your input fields are:
1. `science_field` (str):
2. `year` (int):
3. `num_of_outputs` (int):
Your output fields are:
1. `news` (list[ScienceNews]): science news
All interactions will be structured in the following way, with the appropriate values filled in.

Inputs will have the following structure:

[[ ## science_field ## ]]
{science_field}

[[ ## year ## ]]
{year}

[[ ## num_of_outputs ## ]]
{num_of_outputs}

Outputs will be a JSON object with the following fields.

{
  "news": "{news}        # note: the value you produce must adhere to the JSON schema: {\"type\": \"array\", \"$defs\": {\"ScienceNews\": {\"type\": \"object\", \"properties\": {\"scientists_involved\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}, \"title\": \"Scientists Involved\"}, \"text\": {\"type\": \"string\", \"title\": \"Text\"}}, \"required\": [\"text\", \"scientists_involved\"], \"title\": \"ScienceNews\"}}, \"items\": {\"$ref\": \"#/$defs/ScienceNews\"}}"
}
In adhering to this structure, your objective is:
        Get news about the given science field


User message:

[[ ## science_field ## ]]
Computer Theory

[[ ## year ## ]]
2022

[[ ## num_of_outputs ## ]]
1

Respond with a JSON object in the following order of fields: `news` (must be formatted as a valid Python list[ScienceNews]).


Response:

{
  "news": [
    {
      "text": "In 2022, researchers made significant advancements in quantum computing algorithms, demonstrating that quantum systems can outperform classical computers in specific tasks. This breakthrough could revolutionize fields such as cryptography and complex system simulations.",
      "scientists_involved": [
        "Dr. Alice Smith",
        "Dr. Bob Johnson",
        "Dr. Carol Lee"
      ]
    }
  ]
}
```

#### When to Use JSONAdapter

`JSONAdapter` is good at:

- **Structured output support**: When the model supports the `response_format` parameter.
- **Low latency**: Minimal boilerplate in the LM response results in faster responses.

#### When Not to Use JSONAdapter

Avoid using `JSONAdapter` if you are:

- Using a model that does not natively support structured output, such as a small open-source model hosted on Ollama.

## Summary

Adapters are a crucial component of DSPy that bridge the gap between structured DSPy signatures and language model APIs.
Understanding when and how to use different adapters will help you build more reliable and efficient DSPy programs.

---


### Tools {#tools}

*Source: `learn/programming/tools.md`*

# Tools

DSPy provides powerful support for **tool-using agents** that can interact with external functions, APIs, and services. Tools enable language models to go beyond text generation by performing actions, retrieving information, and processing data dynamically.

There are two main approaches to using tools in DSPy:

1. **`dspy.ReAct`** - A fully managed tool agent that handles reasoning and tool calls automatically
2. **Manual tool handling** - Direct control over tool calls using `dspy.Tool`, `dspy.ToolCalls`, and custom signatures

## Approach 1: Using `dspy.ReAct` (Fully Managed)

The `dspy.ReAct` module implements the Reasoning and Acting (ReAct) pattern, where the language model iteratively reasons about the current situation and decides which tools to call.

### Basic Example

```python
import dspy

# Define your tools as functions
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # In a real implementation, this would call a weather API
    return f"The weather in {city} is sunny and 75°F"

def search_web(query: str) -> str:
    """Search the web for information."""
    # In a real implementation, this would call a search API
    return f"Search results for '{query}': [relevant information...]"

# Create a ReAct agent
react_agent = dspy.ReAct(
    signature="question -> answer",
    tools=[get_weather, search_web],
    max_iters=5
)

# Use the agent
result = react_agent(question="What's the weather like in Tokyo?")
print(result.answer)
print("Tool calls made:", result.trajectory)
```

### ReAct Features

- **Automatic reasoning**: The model thinks through the problem step by step
- **Tool selection**: Automatically chooses which tool to use based on the situation
- **Iterative execution**: Can make multiple tool calls to gather information
- **Error handling**: Built-in error recovery for failed tool calls
- **Trajectory tracking**: Complete history of reasoning and tool calls

### ReAct Parameters

```python
react_agent = dspy.ReAct(
    signature="question -> answer",  # Input/output specification
    tools=[tool1, tool2, tool3],     # List of available tools
    max_iters=10                     # Maximum number of tool call iterations
)
```

## Approach 2: Manual Tool Handling

For more control over the tool calling process, you can manually handle tools using DSPy's tool types.

!!! note "Version Requirement"
    The `ToolCall.execute()` method used in the examples below is available from **dspy 3.0.4b2** onwards. If you're using version 3.0.3 or earlier, you'll need to upgrade to use this feature.

### Basic Setup

```python
import dspy

class ToolSignature(dspy.Signature):
    """Signature for manual tool handling."""
    question: str = dspy.InputField()
    tools: list[dspy.Tool] = dspy.InputField()
    outputs: dspy.ToolCalls = dspy.OutputField()

def weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny"

def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)  # Note: Use safely in production
        return f"The result is {result}"
    except:
        return "Invalid expression"

# Create tool instances
tools = {
    "weather": dspy.Tool(weather),
    "calculator": dspy.Tool(calculator)
}

# Create predictor
predictor = dspy.Predict(ToolSignature)

# Make a prediction
response = predictor(
    question="What's the weather in New York?",
    tools=list(tools.values())
)

# Execute the tool calls
for call in response.outputs.tool_calls:
    # Execute the tool call
    result = call.execute()
    # For versions earlier than 3.0.4b2, use: result = tools[call.name](**call.args)
    print(f"Tool: {call.name}")
    print(f"Args: {call.args}")
    print(f"Result: {result}")
```

### Understanding `dspy.Tool`

The `dspy.Tool` class wraps regular Python functions to make them compatible with DSPy's tool system:

```python
def my_function(param1: str, param2: int = 5) -> str:
    """A sample function with parameters."""
    return f"Processed {param1} with value {param2}"

# Create a tool
tool = dspy.Tool(my_function)

# Tool properties
print(tool.name)        # "my_function"
print(tool.desc)        # The function's docstring
print(tool.args)        # Parameter schema
print(str(tool))        # Full tool description
```

### Understanding `dspy.ToolCalls`

!!! note "Version Requirement"
    The `ToolCall.execute()` method is available from **dspy 3.0.4b2** onwards. If you're using an earlier version, you'll need to upgrade to use this feature.

The `dspy.ToolCalls` type represents the output from a model that can make tool calls. Each individual tool call can be executed using the `execute` method:

```python
# After getting a response with tool calls
for call in response.outputs.tool_calls:
    print(f"Tool name: {call.name}")
    print(f"Arguments: {call.args}")
    
    # Execute individual tool calls with different options:
    
    # Option 1: Automatic discovery (finds functions in locals/globals)
    result = call.execute()  # Automatically finds functions by name

    # Option 2: Pass tools as a dict (most explicit)
    result = call.execute(functions={"weather": weather, "calculator": calculator})
    
    # Option 3: Pass Tool objects as a list
    result = call.execute(functions=[dspy.Tool(weather), dspy.Tool(calculator)])
    
    # Option 4: For versions earlier than 3.0.4b2 (manual tool lookup)
    # tools_dict = {"weather": weather, "calculator": calculator}
    # result = tools_dict[call.name](**call.args)
    
    print(f"Result: {result}")
```

## Using Native Tool Calling

DSPy adapters support **native function calling**, which leverages the underlying language model's built-in tool calling capabilities rather
than relying on text-based parsing. This approach can provide more reliable tool execution and better integration with models that support
native function calling.

!!! warning "Native tool calling doesn't guarantee better quality"

    It's possible that native tool calling produces lower quality than custom tool calling.

### Adapter Behavior

Different DSPy adapters have different defaults for native function calling:

- **`ChatAdapter`** - Uses `use_native_function_calling=False` by default (relies on text parsing)
- **`JSONAdapter`** - Uses `use_native_function_calling=True` by default (uses native function calling)

You can override these defaults by explicitly setting the `use_native_function_calling` parameter when creating an adapter.

### Configuration

```python
import dspy

# ChatAdapter with native function calling enabled
chat_adapter_native = dspy.ChatAdapter(use_native_function_calling=True)

# JSONAdapter with native function calling disabled
json_adapter_manual = dspy.JSONAdapter(use_native_function_calling=False)

# Configure DSPy to use the adapter
dspy.configure(lm=dspy.LM(model="openai/gpt-4o"), adapter=chat_adapter_native)
```

You can enable the [MLflow tracing](https://dspy.ai/tutorials/observability/) to check how native tool
calling is being used. If you use `JSONAdapter` or `ChatAdapter` with native function calling enabled on the code snippet
as provided in [the section above](tools.md#basic-setup), you should see native function calling arg `tools` is set like
the screenshot below:

![native tool calling](../figures/native_tool_call.png)


### Model Compatibility

Native function calling automatically detects model support using `litellm.supports_function_calling()`. If the model doesn't support native function calling, DSPy will fall back to manual text-based parsing even when `use_native_function_calling=True` is set.

## Async Tools

DSPy tools support both synchronous and asynchronous functions. When working with async tools, you have two options:

### Using `acall` for Async Tools

The recommended approach is to use `acall` when working with async tools:

```python
import asyncio
import dspy

async def async_weather(city: str) -> str:
    """Get weather information asynchronously."""
    await asyncio.sleep(0.1)  # Simulate async API call
    return f"The weather in {city} is sunny"

tool = dspy.Tool(async_weather)

# Use acall for async tools
result = await tool.acall(city="New York")
print(result)
```

### Running Async Tools in Sync Mode

If you need to call an async tool from synchronous code, you can enable automatic conversion using the `allow_tool_async_sync_conversion` setting:

```python
import asyncio
import dspy

async def async_weather(city: str) -> str:
    """Get weather information asynchronously."""
    await asyncio.sleep(0.1)
    return f"The weather in {city} is sunny"

tool = dspy.Tool(async_weather)

# Enable async-to-sync conversion
with dspy.context(allow_tool_async_sync_conversion=True):
    # Now you can use __call__ on async tools
    result = tool(city="New York")
    print(result)
```

## Best Practices

### 1. Tool Function Design

- **Clear docstrings**: Tools work better with descriptive documentation
- **Type hints**: Provide clear parameter and return types
- **Simple parameters**: Use basic types (str, int, bool, dict, list) or Pydantic models

```python
def good_tool(city: str, units: str = "celsius") -> str:
    """
    Get weather information for a specific city.
    
    Args:
        city: The name of the city to get weather for
        units: Temperature units, either 'celsius' or 'fahrenheit'
    
    Returns:
        A string describing the current weather conditions
    """
    # Implementation with proper error handling
    if not city.strip():
        return "Error: City name cannot be empty"
    
    # Weather logic here...
    return f"Weather in {city}: 25°{units[0].upper()}, sunny"
```

### 2. Choosing Between ReAct and Manual Handling

**Use `dspy.ReAct` when:**

- You want automatic reasoning and tool selection
- The task requires multiple tool calls
- You need built-in error recovery
- You want to focus on tool implementation rather than orchestration

**Use manual tool handling when:**

- You need precise control over tool execution
- You want custom error handling logic
- You want to minimize the latency
- Your tool returns nothing (void function)


Tools in DSPy provide a powerful way to extend language model capabilities beyond text generation. Whether using the fully automated ReAct approach or manual tool handling, you can build sophisticated agents that interact with the world through code.

---


### MCP {#mcp}

*Source: `learn/programming/mcp.md`*

# Model Context Protocol (MCP)

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open protocol that standardizes how applications provide context to language models. DSPy supports MCP, allowing you to use tools from any MCP server with DSPy agents.

## Installation

Install DSPy with MCP support:

```bash
pip install -U "dspy[mcp]"
```

## Overview

MCP enables you to:

- **Use standardized tools** - Connect to any MCP-compatible server.
- **Share tools across stacks** - Use the same tools across different frameworks.
- **Simplify integration** - Convert MCP tools to DSPy tools with one line.

DSPy does not handle MCP server connections directly. You can use client interfaces of the `mcp` library to establish the connection and pass `mcp.ClientSession` to `dspy.Tool.from_mcp_tool` in order to convert mcp tools into DSPy tools.

## Using MCP with DSPy

### 1. HTTP Server (Remote)

For remote MCP servers over HTTP, use the streamable HTTP transport:

```python
import asyncio
import dspy
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    # Connect to HTTP MCP server
    async with streamablehttp_client("http://localhost:8000/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # List and convert tools
            response = await session.list_tools()
            dspy_tools = [
                dspy.Tool.from_mcp_tool(session, tool)
                for tool in response.tools
            ]

            # Create and use ReAct agent
            class TaskSignature(dspy.Signature):
                task: str = dspy.InputField()
                result: str = dspy.OutputField()

            react_agent = dspy.ReAct(
                signature=TaskSignature,
                tools=dspy_tools,
                max_iters=5
            )

            result = await react_agent.acall(task="Check the weather in Tokyo")
            print(result.result)

asyncio.run(main())
```

### 2. Stdio Server (Local Process)

The most common way to use MCP is with a local server process communicating via stdio:

```python
import asyncio
import dspy
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Configure the stdio server
    server_params = StdioServerParameters(
        command="python",                    # Command to run
        args=["path/to/your/mcp_server.py"], # Server script path
        env=None,                            # Optional environment variables
    )

    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # List available tools
            response = await session.list_tools()

            # Convert MCP tools to DSPy tools
            dspy_tools = [
                dspy.Tool.from_mcp_tool(session, tool)
                for tool in response.tools
            ]

            # Create a ReAct agent with the tools
            class QuestionAnswer(dspy.Signature):
                """Answer questions using available tools."""
                question: str = dspy.InputField()
                answer: str = dspy.OutputField()

            react_agent = dspy.ReAct(
                signature=QuestionAnswer,
                tools=dspy_tools,
                max_iters=5
            )

            # Use the agent
            result = await react_agent.acall(
                question="What is 25 + 17?"
            )
            print(result.answer)

# Run the async function
asyncio.run(main())
```

## Tool Conversion

DSPy automatically handles the conversion from MCP tools to DSPy tools:

```python
# MCP tool from session
mcp_tool = response.tools[0]

# Convert to DSPy tool
dspy_tool = dspy.Tool.from_mcp_tool(session, mcp_tool)

# The DSPy tool preserves:
# - Tool name and description
# - Parameter schemas and types
# - Argument descriptions
# - Async execution support

# Use it like any DSPy tool
result = await dspy_tool.acall(param1="value", param2=123)
```

## Learn More

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [DSPy MCP Tutorial](https://dspy.ai/tutorials/mcp/)
- [DSPy Tools Documentation](./tools.md)

MCP integration in DSPy makes it easy to use standardized tools from any MCP server, enabling powerful agent capabilities with minimal setup.

---


### Evaluation Overview {#evaluation-overview}

*Source: `learn/evaluation/overview.md`*

# Evaluation in DSPy

Once you have an initial system, it's time to **collect an initial development set** so you can refine it more systematically. Even 20 input examples of your task can be useful, though 200 goes a long way. Depending on your _metric_, you either just need inputs and no labels at all, or you need inputs and the _final_ outputs of your system. (You almost never need labels for the intermediate steps in your program in DSPy.) You can probably find datasets that are adjacent to your task on, say, HuggingFace datasets or in a naturally occurring source like StackExchange. If there's data whose licenses are permissive enough, we suggest you use them. Otherwise, you can label a few examples by hand or start deploying a demo of your system and collect initial data that way.

Next, you should **define your DSPy metric**. What makes outputs from your system good or bad? Invest in defining metrics and improving them incrementally over time; it's hard to consistently improve what you aren't able to define. A metric is a function that takes examples from your data and takes the output of your system, and returns a score. For simple tasks, this could be just "accuracy", e.g. for simple classification or short-form QA tasks. For most applications, your system will produce long-form outputs, so your metric will be a smaller DSPy program that checks multiple properties of the output. Getting this right on the first try is unlikely: start with something simple and iterate.

Now that you have some data and a metric, run development evaluations on your pipeline designs to understand their tradeoffs. Look at the outputs and the metric scores. This will probably allow you to spot any major issues, and it will define a baseline for your next steps.


??? "If your metric is itself a DSPy program..."
    If your metric is itself a DSPy program, a powerful way to iterate is to optimize your metric itself. That's usually easy because the output of the metric is usually a simple value (e.g., a score out of 5), so the metric's metric is easy to define and optimize by collecting a few examples.

---


### Data Handling {#data-handling}

*Source: `learn/evaluation/data.md`*

# Data

DSPy is a machine learning framework, so working in it involves training sets, development sets, and test sets. For each example in your data, we distinguish typically between three types of values: the inputs, the intermediate labels, and the final label. You can use DSPy effectively without any intermediate or final labels, but you will need at least a few example inputs.


## DSPy `Example` objects

The core data type for data in DSPy is `Example`. You will use **Examples** to represent items in your training set and test set. 

DSPy **Examples** are similar to Python `dict`s but have a few useful utilities. Your DSPy modules will return values of the type `Prediction`, which is a special sub-class of `Example`.

When you use DSPy, you will do a lot of evaluation and optimization runs. Your individual datapoints will be of type `Example`:

```python
qa_pair = dspy.Example(question="This is a question?", answer="This is an answer.")

print(qa_pair)
print(qa_pair.question)
print(qa_pair.answer)
```
**Output:**
```text
Example({'question': 'This is a question?', 'answer': 'This is an answer.'}) (input_keys=None)
This is a question?
This is an answer.
```

Examples can have any field keys and any value types, though usually values are strings.

```text
object = Example(field1=value1, field2=value2, field3=value3, ...)
```

You can now express your training set for example as:

```python
trainset = [dspy.Example(report="LONG REPORT 1", summary="short summary 1"), ...]
```


### Specifying Input Keys

In traditional ML, there are separated "inputs" and "labels".

In DSPy, the `Example` objects have a `with_inputs()` method, which can mark specific fields as inputs. (The rest are just metadata or labels.)

```python
# Single Input.
print(qa_pair.with_inputs("question"))

# Multiple Inputs; be careful about marking your labels as inputs unless you mean it.
print(qa_pair.with_inputs("question", "answer"))
```

Values can be accessed using the `.`(dot) operator. You can access the value of key `name` in defined object `Example(name="John Doe", job="sleep")` through `object.name`. 

To access or exclude certain keys, use `inputs()` and `labels()` methods to return new Example objects containing only input or non-input keys, respectively.

```python
article_summary = dspy.Example(article= "This is an article.", summary= "This is a summary.").with_inputs("article")

input_key_only = article_summary.inputs()
non_input_key_only = article_summary.labels()

print("Example object with Input fields only:", input_key_only)
print("Example object with Non-Input fields only:", non_input_key_only)
```

**Output**
```
Example object with Input fields only: Example({'article': 'This is an article.'}) (input_keys={'article'})
Example object with Non-Input fields only: Example({'summary': 'This is a summary.'}) (input_keys=None)
```

<!-- ## Loading Dataset from sources

One of the most convenient way to import datasets in DSPy is by using `DataLoader`. The first step is to declare an object, this object can then be used to call utilities to load datasets in different formats:

```python
from dspy.datasets import DataLoader

dl = DataLoader()
```

For most dataset formats, it's quite straightforward you pass the file path to the corresponding method of the format and you'll get the list of `Example` for the dataset in return:

```python
import pandas as pd

csv_dataset = dl.from_csv(
    "sample_dataset.csv",
    fields=("instruction", "context", "response"),
    input_keys=("instruction", "context")
)

json_dataset = dl.from_json(
    "sample_dataset.json",
    fields=("instruction", "context", "response"),
    input_keys=("instruction", "context")
)

parquet_dataset = dl.from_parquet(
    "sample_dataset.parquet",
    fields=("instruction", "context", "response"),
    input_keys=("instruction", "context")
)

pandas_dataset = dl.from_pandas(
    pd.read_csv("sample_dataset.csv"),    # DataFrame
    fields=("instruction", "context", "response"),
    input_keys=("instruction", "context")
)
```

These are some formats that `DataLoader` supports to load from file directly. In the backend, most of these methods leverage the `load_dataset` method from `datasets` library to load these formats. But when working with text data you often use HuggingFace datasets, in order to import HF datasets in list of `Example` format we can use `from_huggingface` method:

```python
blog_alpaca = dl.from_huggingface(
    "intertwine-expel/expel-blog",
    input_keys=("title",)
)
```

You can access the splits of the dataset by accessing the corresponding key:

```python
train_split = blog_alpaca['train']

# Since this is the only split in the dataset we can split this into 
# train and test split ourselves by slicing or sampling 75 rows from the train
# split for testing.
testset = train_split[:75]
trainset = train_split[75:]
```

The way you load a HuggingFace dataset using `load_dataset` is exactly how you load data it via `from_huggingface` as well. This includes passing specific splits, subsplits, read instructions, etc. For code snippets, you can refer to the [cheatsheet snippets](/cheatsheet/#dspy-dataloaders) for loading from HF. -->

---


### Metrics {#metrics}

*Source: `learn/evaluation/metrics.md`*

# Metrics

DSPy is a machine learning framework, so you must think about your **automatic metrics** for evaluation (to track your progress) and optimization (so DSPy can make your programs more effective).


## What is a metric and how do I define a metric for my task?

A metric is just a function that will take examples from your data and the output of your system and return a score that quantifies how good the output is. What makes outputs from your system good or bad? 

For simple tasks, this could be just "accuracy" or "exact match" or "F1 score". This may be the case for simple classification or short-form QA tasks.

However, for most applications, your system will output long-form outputs. There, your metric should probably be a smaller DSPy program that checks multiple properties of the output (quite possibly using AI feedback from LMs).

Getting this right on the first try is unlikely, but you should start with something simple and iterate. 


## Simple metrics

A DSPy metric is just a function in Python that takes `example` (e.g., from your training or dev set) and the output `pred` from your DSPy program, and outputs a `float` (or `int` or `bool`) score.

Your metric should also accept an optional third argument called `trace`. You can ignore this for a moment, but it will enable some powerful tricks if you want to use your metric for optimization.

Here's a simple example of a metric that's comparing `example.answer` and `pred.answer`. This particular metric will return a `bool`.

```python
def validate_answer(example, pred, trace=None):
    return example.answer.lower() == pred.answer.lower()
```

Some people find these utilities (built-in) convenient:

- `dspy.evaluate.metrics.answer_exact_match`
- `dspy.evaluate.metrics.answer_passage_match`

Your metrics could be more complex, e.g. check for multiple properties. The metric below will return a `float` if `trace is None` (i.e., if it's used for evaluation or optimization), and will return a `bool` otherwise (i.e., if it's used to bootstrap demonstrations).

```python
def validate_context_and_answer(example, pred, trace=None):
    # check the gold label and the predicted answer are the same
    answer_match = example.answer.lower() == pred.answer.lower()

    # check the predicted answer comes from one of the retrieved contexts
    context_match = any((pred.answer.lower() in c) for c in pred.context)

    if trace is None: # if we're doing evaluation or optimization
        return (answer_match + context_match) / 2.0
    else: # if we're doing bootstrapping, i.e. self-generating good demonstrations of each step
        return answer_match and context_match
```

Defining a good metric is an iterative process, so doing some initial evaluations and looking at your data and outputs is key.


## Evaluation

Once you have a metric, you can run evaluations in a simple Python loop.

```python
scores = []
for x in devset:
    pred = program(**x.inputs())
    score = metric(x, pred)
    scores.append(score)
```

If you need some utilities, you can also use the built-in `Evaluate` utility. It can help with things like parallel evaluation (multiple threads) or showing you a sample of inputs/outputs and the metric scores.

```python
from dspy.evaluate import Evaluate

# Set up the evaluator, which can be re-used in your code.
evaluator = Evaluate(devset=YOUR_DEVSET, num_threads=1, display_progress=True, display_table=5)

# Launch evaluation.
evaluator(YOUR_PROGRAM, metric=YOUR_METRIC)
```


## Intermediate: Using AI feedback for your metric

For most applications, your system will output long-form outputs, so your metric should check multiple dimensions of the output using AI feedback from LMs.

This simple signature could come in handy.

```python
# Define the signature for automatic assessments.
class Assess(dspy.Signature):
    """Assess the quality of a tweet along the specified dimension."""

    assessed_text = dspy.InputField()
    assessment_question = dspy.InputField()
    assessment_answer: bool = dspy.OutputField()
```

For example, below is a simple metric that checks a generated tweet (1) answers a given question correctly and (2) whether it's also engaging. We also check that (3) `len(tweet) <= 280` characters.

```python
def metric(gold, pred, trace=None):
    question, answer, tweet = gold.question, gold.answer, pred.output

    engaging = "Does the assessed text make for a self-contained, engaging tweet?"
    correct = f"The text should answer `{question}` with `{answer}`. Does the assessed text contain this answer?"
    
    correct =  dspy.Predict(Assess)(assessed_text=tweet, assessment_question=correct)
    engaging = dspy.Predict(Assess)(assessed_text=tweet, assessment_question=engaging)

    correct, engaging = [m.assessment_answer for m in [correct, engaging]]
    score = (correct + engaging) if correct and (len(tweet) <= 280) else 0

    if trace is not None: return score >= 2
    return score / 2.0
```

When compiling, `trace is not None`, and we want to be strict about judging things, so we will only return `True` if `score >= 2`. Otherwise, we return a score out of 1.0 (i.e., `score / 2.0`).


## Advanced: Using a DSPy program as your metric

If your metric is itself a DSPy program, one of the most powerful ways to iterate is to compile (optimize) your metric itself. That's usually easy because the output of the metric is usually a simple value (e.g., a score out of 5) so the metric's metric is easy to define and optimize by collecting a few examples.


### Advanced: Accessing the `trace`

When your metric is used during evaluation runs, DSPy will not try to track the steps of your program.

But during compiling (optimization), DSPy will trace your LM calls. The trace will contain inputs/outputs to each DSPy predictor and you can leverage that to validate intermediate steps for optimization.


```python
def validate_hops(example, pred, trace=None):
    hops = [example.question] + [outputs.query for *_, outputs in trace if 'query' in outputs]

    if max([len(h) for h in hops]) > 100: return False
    if any(dspy.evaluate.answer_exact_match_str(hops[idx], hops[:idx], frac=0.8) for idx in range(2, len(hops))): return False

    return True
```

---


### Optimization Overview {#optimization-overview}

*Source: `learn/optimization/overview.md`*

# Optimization in DSPy

Once you have a system and a way to evaluate it, you can use DSPy optimizers to tune the prompts or weights in your program. Now it's useful to expand your data collection effort into building a training set and a held-out test set, in addition to the development set you've been using for exploration. For the training set (and its subset, validation set), you can often get substantial value out of 30 examples, but aim for at least 300 examples. Some optimizers accept a `trainset` only. Others ask for a `trainset` and a `valset`. When splitting data for most prompt optimizers, we recommend an unusual split compared to deep neural networks: 20% for training, 80% for validation. This reverse allocation emphasizes stable validation, since prompt-based optimizers often overfit to small training sets. In contrast, the [dspy.GEPA](https://dspy.ai/tutorials/gepa_ai_program/) optimizer follows the more standard ML convention: Maximize the training set size, while keeping the validation set just large enough to reflect the distribution of the downstream tasks (test set).

After your first few optimization runs, you are either very happy with everything or you've made a lot of progress but you don't like something about the final program or the metric. At this point, go back to step 1 (Programming in DSPy) and revisit the major questions. Did you define your task well? Do you need to collect (or find online) more data for your problem? Do you want to update your metric? And do you want to use a more sophisticated optimizer? Do you need to consider advanced features like DSPy Assertions? Or, perhaps most importantly, do you want to add some more complexity or steps in your DSPy program itself? Do you want to use multiple optimizers in a sequence?

Iterative development is key. DSPy gives you the pieces to do that incrementally: iterating on your data, your program structure, your metric, and your optimization steps. Optimizing complex LM programs is an entirely new paradigm that only exists in DSPy at the time of writing (update: there are now numerous DSPy extension frameworks, so this part is no longer true :-), so naturally the norms around what to do are still emerging. If you need help, we recently created a [Discord server](https://discord.gg/XCGy2WDCQB) for the community.

---


### Optimizers {#optimizers}

*Source: `learn/optimization/optimizers.md`*

# DSPy Optimizers (formerly Teleprompters)


A **DSPy optimizer** is an algorithm that can tune the parameters of a DSPy program (i.e., the prompts and/or the LM weights) to maximize the metrics you specify, like accuracy.


A typical DSPy optimizer takes three things:

- Your **DSPy program**. This may be a single module (e.g., `dspy.Predict`) or a complex multi-module program.

- Your **metric**. This is a function that evaluates the output of your program, and assigns it a score (higher is better).

- A few **training inputs**. This may be very small (i.e., only 5 or 10 examples) and incomplete (only inputs to your program, without any labels).

If you happen to have a lot of data, DSPy can leverage that. But you can start small and get strong results.

**Note:** Formerly called teleprompters. We are making an official name update, which will be reflected throughout the library and documentation.


## What does a DSPy Optimizer tune? How does it tune them?

Different optimizers in DSPy will tune your program's quality by **synthesizing good few-shot examples** for every module, like `dspy.BootstrapRS`,<sup>[1](https://arxiv.org/abs/2310.03714)</sup> **proposing and intelligently exploring better natural-language instructions** for every prompt, like `dspy.MIPROv2`,<sup>[2](https://arxiv.org/abs/2406.11695)</sup> and `dspy.GEPA`,<sup>[3](https://arxiv.org/abs/2507.19457)</sup> and **building datasets for your modules and using them to finetune the LM weights** in your system, like `dspy.BootstrapFinetune`.<sup>[4](https://arxiv.org/abs/2407.10930)</sup>

??? "What's an example of a DSPy optimizer? How do different optimizers work?"

    Take the `dspy.MIPROv2` optimizer as an example. First, MIPRO starts with the **bootstrapping stage**. It takes your program, which may be unoptimized at this point, and runs it many times across different inputs to collect traces of input/output behavior for each one of your modules. It filters these traces to keep only those that appear in trajectories scored highly by your metric. Second, MIPRO enters its **grounded proposal stage**. It previews your DSPy program's code, your data, and traces from running your program, and uses them to draft many potential instructions for every prompt in your program. Third, MIPRO launches the **discrete search stage**. It samples mini-batches from your training set, proposes a combination of instructions and traces to use for constructing every prompt in the pipeline, and evaluates the candidate program on the mini-batch. Using the resulting score, MIPRO updates a surrogate model that helps the proposals get better over time.

    One thing that makes DSPy optimizers so powerful is that they can be composed. You can run `dspy.MIPROv2` and use the produced program as an input to `dspy.MIPROv2` again or, say, to `dspy.BootstrapFinetune` to get better results. This is partly the essence of `dspy.BetterTogether`. Alternatively, you can run the optimizer and then extract the top-5 candidate programs and build a `dspy.Ensemble` of them. This allows you to scale _inference-time compute_ (e.g., ensembles) as well as DSPy's unique _pre-inference time compute_ (i.e., optimization budget) in highly systematic ways.


## What DSPy Optimizers are currently available?

Optimizers can be accessed via `from dspy.teleprompt import *`.

### Automatic Few-Shot Learning

These optimizers extend the signature by automatically generating and including **optimized** examples within the prompt sent to the model, implementing few-shot learning.

1. [**`LabeledFewShot`**](../../api/optimizers/LabeledFewShot.md): Simply constructs few-shot examples (demos) from provided labeled input and output data points.  Requires `k` (number of examples for the prompt) and `trainset` to randomly select `k` examples from.

2. [**`BootstrapFewShot`**](../../api/optimizers/BootstrapFewShot.md): Uses a `teacher` module (which defaults to your program) to generate complete demonstrations for every stage of your program, along with labeled examples in `trainset`. Parameters include `max_labeled_demos` (the number of demonstrations randomly selected from the `trainset`) and `max_bootstrapped_demos` (the number of additional examples generated by the `teacher`). The bootstrapping process employs the metric to validate demonstrations, including only those that pass the metric in the "compiled" prompt. Advanced: Supports using a `teacher` program that is a *different* DSPy program that has compatible structure, for harder tasks.

3. [**`BootstrapFewShotWithRandomSearch`**](../../api/optimizers/BootstrapFewShotWithRandomSearch.md): Applies `BootstrapFewShot` several times with random search over generated demonstrations, and selects the best program over the optimization. Parameters mirror those of `BootstrapFewShot`, with the addition of `num_candidate_programs`, which specifies the number of random programs evaluated over the optimization, including candidates of the uncompiled program, `LabeledFewShot` optimized program, `BootstrapFewShot` compiled program with unshuffled examples and `num_candidate_programs` of `BootstrapFewShot` compiled programs with randomized example sets.

4. [**`KNNFewShot`**](../../api/optimizers/KNNFewShot.md). Uses k-Nearest Neighbors algorithm to find the nearest training example demonstrations for a given input example. These nearest neighbor demonstrations are then used as the trainset for the BootstrapFewShot optimization process.


### Automatic Instruction Optimization

These optimizers produce optimal instructions for the prompt and, in the case of MIPROv2 can also optimize the set of few-shot demonstrations.

5. [**`COPRO`**](../../api/optimizers/COPRO.md): Generates and refines new instructions for each step, and optimizes them with coordinate ascent (hill-climbing using the metric function and the `trainset`). Parameters include `depth` which is the number of iterations of prompt improvement the optimizer runs over.

6. [**`MIPROv2`**](../../api/optimizers/MIPROv2.md): Generates instructions *and* few-shot examples in each step. The instruction generation is data-aware and demonstration-aware. Uses Bayesian Optimization to effectively search over the space of generation instructions/demonstrations across your modules.

7. [**`SIMBA`**](../../api/optimizers/SIMBA.md): Uses stochastic mini-batch sampling to identify challenging examples with high output variability, then applies the LLM to introspectively analyze failures and generate self-reflective improvement rules or add successful demonstrations.

8. [**`GEPA`**](../../api/optimizers/GEPA/overview.md): Uses LM's to reflect on the DSPy program's trajectory, to identify what worked, what didn't and propose prompts addressing the gaps. Additionally, GEPA can leverage domain-specific textual feedback to rapidly improve the DSPy program. Detailed tutorials on using GEPA are available at [dspy.GEPA Tutorials](../../tutorials/gepa_ai_program/index.md).

### Automatic Finetuning

This optimizer is used to fine-tune the underlying LLM(s).

9. [**`BootstrapFinetune`**](/api/optimizers/BootstrapFinetune): Distills a prompt-based DSPy program into weight updates. The output is a DSPy program that has the same steps, but where each step is conducted by a finetuned model instead of a prompted LM. [See the classification fine-tuning tutorial](https://dspy.ai/tutorials/classification_finetuning/) for a complete example.


### Program Transformations

10. [**`Ensemble`**](../../api/optimizers/Ensemble.md): Ensembles a set of DSPy programs and either uses the full set or randomly samples a subset into a single program.

### Meta-Optimizers

11. [**`BetterTogether`**](../../api/optimizers/BetterTogether.md): A meta-optimizer that combines prompt optimization and weight optimization (fine-tuning) in configurable sequences. Prompt optimization can discover effective task decompositions and reasoning strategies, while weight optimization can specialize the model to execute these patterns more efficiently. Using these approaches together in sequences (e.g., prompt → weight → prompt) may allow each to build on the improvements made by the other. Empirically, this approach often outperforms either strategy alone. Detailed tutorial available at [BetterTogether AIME Tutorial](../../tutorials/bettertogether_aime/index.ipynb).


## Which optimizer should I use?

Ultimately, finding the ‘right’ optimizer to use & the best configuration for your task will require experimentation. Success in DSPy is still an iterative process - getting the best performance on your task will require you to explore and iterate.  

That being said, here's the general guidance on getting started:

- If you have **very few examples** (around 10), start with `BootstrapFewShot`.
- If you have **more data** (50 examples or more), try  `BootstrapFewShotWithRandomSearch`.
- If you prefer to do **instruction optimization only** (i.e. you want to keep your prompt 0-shot), use `MIPROv2` [configured for 0-shot optimization](../../api/optimizers/MIPROv2.md). 
- If you’re willing to use more inference calls to perform **longer optimization runs** (e.g. 40 trials or more), and have enough data (e.g. 200 examples or more to prevent overfitting) then try `MIPROv2`. 
- If you have been able to use one of these with a large LM (e.g., 7B parameters or above) and need a very **efficient program**, finetune a small LM for your task with `BootstrapFinetune`.

## How do I use an optimizer?

They all share this general interface, with some differences in the keyword arguments (hyperparameters). A full list can be found in the [API reference](../../api/optimizers/BetterTogether.md).

Let's see this with the most common one, `BootstrapFewShotWithRandomSearch`.

```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

# Set up the optimizer: we want to "bootstrap" (i.e., self-generate) 8-shot examples of your program's steps.
# The optimizer will repeat this 10 times (plus some initial attempts) before selecting its best attempt on the devset.
config = dict(max_bootstrapped_demos=4, max_labeled_demos=4, num_candidate_programs=10, num_threads=4)

teleprompter = BootstrapFewShotWithRandomSearch(metric=YOUR_METRIC_HERE, **config)
optimized_program = teleprompter.compile(YOUR_PROGRAM_HERE, trainset=YOUR_TRAINSET_HERE)
```


!!! info "Getting Started III: Optimizing the LM prompts or weights in DSPy programs"
    A typical simple optimization run costs on the order of $2 USD and takes around ten minutes, but be careful when running optimizers with very large LMs or very large datasets.
    Optimizer runs can cost as little as a few cents or up to tens of dollars, depending on your LM, dataset, and configuration.
    
    === "Optimizing prompts for a ReAct agent"
        This is a minimal but fully runnable example of setting up a `dspy.ReAct` agent that answers questions via
        search from Wikipedia and then optimizing it using `dspy.MIPROv2` in the cheap `light` mode on 500
        question-answer pairs sampled from the `HotPotQA` dataset.

        ```python linenums="1"
        import dspy
        from dspy.datasets import HotPotQA

        dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))

        def search(query: str) -> list[str]:
            """Retrieves abstracts from Wikipedia."""
            results = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
            return [x['text'] for x in results]

        trainset = [x.with_inputs('question') for x in HotPotQA(train_seed=2024, train_size=500).train]
        react = dspy.ReAct("question -> answer", tools=[search])

        tp = dspy.MIPROv2(metric=dspy.evaluate.answer_exact_match, auto="light", num_threads=24)
        optimized_react = tp.compile(react, trainset=trainset)
        ```

        An informal run similar to this on DSPy 2.5.29 raises ReAct's score from 24% to 51%.

    === "Optimizing prompts for RAG"
        Given a retrieval index to `search`, your favorite `dspy.LM`, and a small `trainset` of questions and ground-truth responses, the following code snippet can optimize your RAG system with long outputs against the built-in `dspy.SemanticF1` metric, which is implemented as a DSPy module.

        ```python linenums="1"
        class RAG(dspy.Module):
            def __init__(self, num_docs=5):
                self.num_docs = num_docs
                self.respond = dspy.ChainOfThought('context, question -> response')

            def forward(self, question):
                context = search(question, k=self.num_docs)   # not defined in this snippet, see link above
                return self.respond(context=context, question=question)

        tp = dspy.MIPROv2(metric=dspy.SemanticF1(), auto="medium", num_threads=24)
        optimized_rag = tp.compile(RAG(), trainset=trainset, max_bootstrapped_demos=2, max_labeled_demos=2)
        ```

        For a complete RAG example that you can run, start this [tutorial](../../tutorials/rag/index.ipynb). It improves the quality of a RAG system over a subset of StackExchange communities from 53% to 61%.

    === "Optimizing weights for Classification"
        <details><summary>Click to show dataset setup code.</summary>

        ```python linenums="1"
        import random
        from typing import Literal

        from datasets import load_dataset

        import dspy
        from dspy.datasets import DataLoader

        # Load the Banking77 dataset.
        CLASSES = load_dataset("PolyAI/banking77", split="train", trust_remote_code=True).features["label"].names
        kwargs = {"fields": ("text", "label"), "input_keys": ("text",), "split": "train", "trust_remote_code": True}

        # Load the first 2000 examples from the dataset, and assign a hint to each *training* example.
        trainset = [
            dspy.Example(x, hint=CLASSES[x.label], label=CLASSES[x.label]).with_inputs("text", "hint")
            for x in DataLoader().from_huggingface(dataset_name="PolyAI/banking77", **kwargs)[:2000]
        ]
        random.Random(0).shuffle(trainset)
        ```
        </details>

        ```python linenums="1"
        import dspy
        lm=dspy.LM('openai/gpt-4o-mini-2024-07-18')

        # Define the DSPy module for classification. It will use the hint at training time, if available.
        signature = dspy.Signature("text, hint -> label").with_updated_fields('label', type_=Literal[tuple(CLASSES)])
        classify = dspy.ChainOfThought(signature)
        classify.set_lm(lm)

        # Optimize via BootstrapFinetune.
        optimizer = dspy.BootstrapFinetune(metric=(lambda x, y, trace=None: x.label == y.label), num_threads=24)
        optimized = optimizer.compile(classify, trainset=trainset)

        optimized(text="What does a pending cash withdrawal mean?")
        
        # For a complete fine-tuning tutorial, see: https://dspy.ai/tutorials/classification_finetuning/
        ```

        **Possible Output (from the last line):**
        ```text
        Prediction(
            reasoning='A pending cash withdrawal indicates that a request to withdraw cash has been initiated but has not yet been completed or processed. This status means that the transaction is still in progress and the funds have not yet been deducted from the account or made available to the user.',
            label='pending_cash_withdrawal'
        )
        ```

        An informal run similar to this on DSPy 2.5.29 raises GPT-4o-mini's score 66% to 87%.


## Saving and loading optimizer output

After running a program through an optimizer, it's useful to also save it. At a later point, a program can be loaded from a file and used for inference. For this, the `load` and `save` methods can be used.

```python
optimized_program.save(YOUR_SAVE_PATH)
```

The resulting file is in plain-text JSON format. It contains all the parameters and steps in the source program. You can always read it and see what the optimizer generated.


To load a program from a file, you can instantiate an object from that class and then call the load method on it.

```python
loaded_program = YOUR_PROGRAM_CLASS()
loaded_program.load(path=YOUR_SAVE_PATH)
```

---


## Tutorials Overview {#tutorials-overview}

*Source: `tutorials/index.md`*

Welcome to DSPy tutorials! We've organized our tutorials into three main categories to help you get started:

- **Build AI Programs with DSPy**: These hands-on tutorials guide you through building production-ready AI
  applications. From implementing RAG systems to creating intelligent agents, each tutorial demonstrates
  practical use cases. You'll also learn how to leverage DSPy optimizers to enhance your program's performance.

- **Optimize AI Programs with DSPy Optimizers**: These tutorials deep dive into DSPy's optimization capabilities. While
  lighter on programming concepts, they focus on how to systematically improve your AI programs using DSPy
  optimizers, and showcase how DSPy optimizers help improve the quality automatically.

- **DSPy Core Development**: These tutorials cover essential DSPy features and best practices. Learn how to implement
  key functionalities like streaming, caching, deployment, and monitoring in your DSPy applications.


- Build AI Programs with DSPy
    - [Managing Conversation History](conversation_history/index.md)
    - [Building AI Agents with DSPy](customer_service_agent/index.ipynb)
    - [Building AI Applications by Customizing DSPy Modules](custom_module/index.ipynb)
    - [Retrieval-Augmented Generation (RAG)](rag/index.ipynb)
    - [Building RAG as Agent](agents/index.ipynb)
    - [Entity Extraction](entity_extraction/index.ipynb)
    - [Classification](classification/index.md)
    - [Multi-Hop RAG](multihop_search/index.ipynb)
    - [Privacy-Conscious Delegation](papillon/index.md)
    - [Program Of Thought](program_of_thought/index.ipynb)
    - [Image Generation Prompt iteration](image_generation_prompting/index.ipynb)
    - [Audio](audio/index.ipynb)


- Optimize AI Programs with DSPy
    - [Math Reasoning](math/index.ipynb)
    - [Classification Finetuning](classification_finetuning/index.ipynb)
    - [Advanced Tool Use](tool_use/index.ipynb)
    - [Finetuning Agents](games/index.ipynb)


- Reflective Prompt Evolution with dspy.GEPA:
    - [Overview](gepa_ai_program/index.md)
    - [GEPA for AIME](gepa_aime/index.ipynb)
    - [GEPA for PAPILLON](gepa_papillon/index.ipynb)
    - [GEPA for Enterprise classification task](gepa_facilitysupportanalyzer/index.ipynb)
    - [GEPA for Code Backdoor Classification (AI control)](gepa_trusted_monitor/index.ipynb)


- Experimental RL Optimization:
    - [Overview](rl_ai_program/index.md)
    - [RL for Privacy-Conscious Delegation](rl_papillon/index.ipynb)
    - [RL for Multi-Hop Research](rl_multihop/index.ipynb)


- Tools, Development, and Deployment
    - [Use MCP in DSPy](mcp/index.md)
    - [Output Refinement](output_refinement/best-of-n-and-refine.md)
    - [Saving and Loading](saving/index.md)
    - [Cache](cache/index.md)
    - [Deployment](deployment/index.md)
    - [Debugging & Observability](observability/index.md)
    - [Tracking DSPy Optimizers](optimizer_tracking/index.md)
    - [Streaming](streaming/index.md)
    - [Async](async/index.md)


- Real-World Examples:
    - [Overview](real_world_examples/index.md)
    - [Generating llms.txt](llms_txt_generation/index.md)
    - [Email Information Extraction](email_extraction/index.md)
    - [Memory-Enabled ReAct Agents with Mem0](mem0_react_agent/index.md)
    - [Financial Analysis with Yahoo Finance](yahoo_finance_react/index.md)
    - [Automated Code Generation from Documentation](sample_code_generation/index.md)
    - [Building a Creative Text-Based AI Game](ai_text_game/index.md)

---


### Overview {#overview}

*Source: `tutorials/build_ai_program/index.md`*

# Build AI Programs with DSPy

This section contains hands-on tutorials that guide you through building production-ready AI applications using DSPy. Each tutorial demonstrates practical use cases and shows you how to leverage DSPy's modular programming approach to create robust, maintainable AI systems.

## Core Applications

### [Managing Conversation History](../conversation_history/index.md)
Learn how to manage conversation history in DSPy applications.

### [Building AI Agents with DSPy](../customer_service_agent/index.ipynb)
Learn to create intelligent agents that can handle complex customer service scenarios. This tutorial shows how to build agents that can understand context, maintain conversation state, and provide helpful responses.

### [Building AI Applications by Customizing DSPy Modules](../custom_module/index.ipynb)
Discover how to create custom DSPy modules tailored to your specific needs. Learn the patterns for building reusable, composable components that can be shared across different applications.

## Retrieval-Augmented Generation (RAG)

### [Retrieval-Augmented Generation (RAG)](../rag/index.ipynb)
Master the fundamentals of RAG systems with DSPy. Learn how to combine retrieval mechanisms with language models to build systems that can answer questions using external knowledge sources.

### [Building RAG as Agent](../agents/index.ipynb)
Take RAG to the next level by building `ReAct` agent-based systems that can reason about when and how to retrieve information, making your RAG systems more intelligent and adaptive.

### [Multi-Hop RAG](../multihop_search/index.ipynb)
Build sophisticated RAG systems that can perform multi-step reasoning across multiple information sources, perfect for complex research and analysis tasks.

## Specialized Use Cases

### [Entity Extraction](../entity_extraction/index.ipynb)
Learn to build systems that can identify and extract specific entities from text, essential for information processing and data analysis applications.

### [Classification](../classification/index.md)
Build robust text classification systems using DSPy's modular approach with a topic classification example.

### [Privacy-Conscious Delegation](../papillon/index.md)
Explore advanced techniques for building AI systems that respect privacy constraints while maintaining high performance by combining a small local model and an advanced external model.

## Advanced Reasoning

### [Program Of Thought](../program_of_thought/index.ipynb)
Learn to build systems that can generate and execute code to solve complex problems, combining the power of language models with programmatic reasoning.

## Multimodal Applications

### [Image Generation Prompt iteration](../image_generation_prompting/index.ipynb)
Discover how to use DSPy to iteratively improve image generation prompts, creating better visual content through systematic optimization.

### [Audio](../audio/index.ipynb)
Explore audio processing applications with DSPy, learning to build systems that can understand, process, and generate audio content.

---


### Managing Conversation History {#managing-conversation-history}

*Source: `tutorials/conversation_history/index.md`*

# Managing Conversation History

Maintaining conversation history is a fundamental feature when building AI applications such as chatbots. While DSPy does not provide automatic conversation history management within `dspy.Module`, it offers the `dspy.History` utility to help you manage conversation history effectively.

## Using `dspy.History` to Manage Conversation History

The `dspy.History` class can be used as an input field type, containing a `messages: list[dict[str, Any]]` attribute that stores the conversation history. Each entry in this list is a dictionary with keys corresponding to the fields defined in your signature. See the example below:

```python
import dspy
import os

os.environ["OPENAI_API_KEY"] = "{your_openai_api_key}"

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

class QA(dspy.Signature):
    question: str = dspy.InputField()
    history: dspy.History = dspy.InputField()
    answer: str = dspy.OutputField()

predict = dspy.Predict(QA)
history = dspy.History(messages=[])

while True:
    question = input("Type your question, end conversation by typing 'finish': ")
    if question == "finish":
        break
    outputs = predict(question=question, history=history)
    print(f"\n{outputs.answer}\n")
    history.messages.append({"question": question, **outputs})

dspy.inspect_history()
```

There are two key steps when using the conversation history:

- **Include a field of type `dspy.History` in your Signature.**
- **Maintain a history instance at runtime, appending new conversation turns to it.** Each entry should include all relevant input and output field information.

A sample run might look like this:

```
Type your question, end conversation by typing 'finish': do you know the competition between pytorch and tensorflow?

Yes, there is a notable competition between PyTorch and TensorFlow, which are two of the most popular deep learning frameworks. PyTorch, developed by Facebook, is known for its dynamic computation graph, which allows for more flexibility and ease of use, especially in research settings. TensorFlow, developed by Google, initially used a static computation graph but has since introduced eager execution to improve usability. TensorFlow is often favored in production environments due to its scalability and deployment capabilities. Both frameworks have strong communities and extensive libraries, and the choice between them often depends on specific project requirements and personal preference.

Type your question, end conversation by typing 'finish': which one won the battle? just tell me the result, don't include any reasoning, thanks!

There is no definitive winner; both PyTorch and TensorFlow are widely used and have their own strengths.
Type your question, end conversation by typing 'finish': finish


[2025-07-11T16:35:57.592762]

System message:

Your input fields are:
1. `question` (str): 
2. `history` (History):
Your output fields are:
1. `answer` (str):
All interactions will be structured in the following way, with the appropriate values filled in.

[[ ## question ## ]]
{question}

[[ ## history ## ]]
{history}

[[ ## answer ## ]]
{answer}

[[ ## completed ## ]]
In adhering to this structure, your objective is: 
        Given the fields `question`, `history`, produce the fields `answer`.


User message:

[[ ## question ## ]]
do you know the competition between pytorch and tensorflow?


Assistant message:

[[ ## answer ## ]]
Yes, there is a notable competition between PyTorch and TensorFlow, which are two of the most popular deep learning frameworks. PyTorch, developed by Facebook, is known for its dynamic computation graph, which allows for more flexibility and ease of use, especially in research settings. TensorFlow, developed by Google, initially used a static computation graph but has since introduced eager execution to improve usability. TensorFlow is often favored in production environments due to its scalability and deployment capabilities. Both frameworks have strong communities and extensive libraries, and the choice between them often depends on specific project requirements and personal preference.

[[ ## completed ## ]]


User message:

[[ ## question ## ]]
which one won the battle? just tell me the result, don't include any reasoning, thanks!

Respond with the corresponding output fields, starting with the field `[[ ## answer ## ]]`, and then ending with the marker for `[[ ## completed ## ]]`.


Response:

[[ ## answer ## ]]
There is no definitive winner; both PyTorch and TensorFlow are widely used and have their own strengths.

[[ ## completed ## ]]
```

Notice how each user input and assistant response is appended to the history, allowing the model to maintain context across turns.

The actual prompt sent to the language model is a multi-turn message, as shown by the output of `dspy.inspect_history`. Each conversation turn is represented as a user message followed by an assistant message.

## History in Few-shot Examples

You may notice that `history` does not appear in the input fields section of the prompt, even though it is listed as an input field (e.g., "2. `history` (History):" in the system message). This is intentional: when formatting few-shot examples that include conversation history, DSPy does not expand the history into multiple turns. Instead, to remain compatible with the OpenAI standard format, each few-shot example is represented as a single turn.

For example:

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))


class QA(dspy.Signature):
    question: str = dspy.InputField()
    history: dspy.History = dspy.InputField()
    answer: str = dspy.OutputField()


predict = dspy.Predict(QA)
history = dspy.History(messages=[])

predict.demos.append(
    dspy.Example(
        question="What is the capital of France?",
        history=dspy.History(
            messages=[{"question": "What is the capital of Germany?", "answer": "The capital of Germany is Berlin."}]
        ),
        answer="The capital of France is Paris.",
    )
)

predict(question="What is the capital of America?", history=dspy.History(messages=[]))
dspy.inspect_history()
```

The resulting history will look like this:

```
[2025-07-11T16:53:10.994111]

System message:

Your input fields are:
1. `question` (str): 
2. `history` (History):
Your output fields are:
1. `answer` (str):
All interactions will be structured in the following way, with the appropriate values filled in.

[[ ## question ## ]]
{question}

[[ ## history ## ]]
{history}

[[ ## answer ## ]]
{answer}

[[ ## completed ## ]]
In adhering to this structure, your objective is: 
        Given the fields `question`, `history`, produce the fields `answer`.


User message:

[[ ## question ## ]]
What is the capital of France?

[[ ## history ## ]]
{"messages": [{"question": "What is the capital of Germany?", "answer": "The capital of Germany is Berlin."}]}


Assistant message:

[[ ## answer ## ]]
The capital of France is Paris.

[[ ## completed ## ]]


User message:

[[ ## question ## ]]
What is the capital of America?

Respond with the corresponding output fields, starting with the field `[[ ## answer ## ]]`, and then ending with the marker for `[[ ## completed ## ]]`.


Response:

[[ ## answer ## ]]
The capital of the United States of America is Washington, D.C.

[[ ## completed ## ]]
```

As you can see, the few-shot example does not expand the conversation history into multiple turns. Instead, it represents the history as JSON data within its section:

```
[[ ## history ## ]]
{"messages": [{"question": "What is the capital of Germany?", "answer": "The capital of Germany is Berlin."}]}
```

This approach ensures compatibility with standard prompt formats while still providing the model with relevant conversational context.

---


### Classification {#classification}

*Source: `tutorials/classification/index.md`*

Please refer to [this tutorial from Drew Breunig](https://www.dbreunig.com/2024/12/12/pipelines-prompt-optimization-with-dspy.html) using DSPy.

This tutorial demonstrates a few aspects of using DSPy in a highly-accessible, concrete context for categorizing historic events with a tiny LM.

---


### Privacy-Conscious Delegation {#privacy-conscious-delegation}

*Source: `tutorials/papillon/index.md`*

Please refer to [this tutorial from the PAPILLON authors](https://colab.research.google.com/github/Columbia-NLP-Lab/PAPILLON/blob/main/papillon_tutorial.ipynb) using DSPy.

This tutorial demonstrates a few aspects of using DSPy in a more advanced context:

1. It builds a multi-stage `dspy.Module` that involves a small local LM using an external tool.
2. It builds a multi-stage _judge_ in DSPy, and uses it as a metric for evaluation.
3. It uses this judge for optimizing the `dspy.Module`, using a large model as a teacher for a small local LM.

---


### Overview {#overview}

*Source: `tutorials/optimize_ai_program/index.md`*

# Optimize AI Programs with DSPy

This section focuses on DSPy's powerful optimization capabilities, demonstrating how to systematically improve your AI programs using various optimizers. These tutorials are lighter on programming concepts and instead showcase how DSPy optimizers can automatically enhance the quality and performance of your applications.

## Mathematical and Reasoning Tasks

### [Math Reasoning](../math/index.ipynb)
Learn how to optimize DSPy programs for mathematical reasoning tasks. This tutorial demonstrates how optimizers can dramatically improve performance on complex math problems by finding better prompting strategies and few-shot examples.

## Model Optimization

### [Classification Finetuning](../classification_finetuning/index.ipynb)
Discover how to use DSPy's finetuning optimizers to distill knowledge from large language models into smaller, more efficient models. Learn the complete workflow from prompt optimization to model finetuning for classification tasks.

## Advanced Tool Integration

### [Advanced Tool Use](../tool_use/index.ipynb)
Explore how to optimize AI programs that use external tools and APIs. This tutorial shows how DSPy optimizers can learn to use tools more effectively, improving both accuracy and efficiency in tool-calling scenarios.

### [Finetuning Agents](../games/index.ipynb)
Learn to optimize complex agent-based systems through finetuning. This tutorial demonstrates how to improve agent performance in interactive environments like games, where strategic thinking and adaptation are crucial.

---


### Overview {#overview}

*Source: `tutorials/gepa_ai_program/index.md`*

# Reflective Prompt Evolution with GEPA

This section introduces GEPA, a reflective prompt optimizer for DSPy. GEPA works by leveraging LM's ability to reflect on the DSPy program's trajectory, identifying what went well, what didn't, and what can be improved. Based on this reflection, GEPA proposes new prompts, building a tree of evolved prompt candidates, accumulating improvements as the optimization progresses. Since GEPA can leverage domain-specific text feedback (as opposed to only the scalar metric), GEPA can often propose high performing prompts in very few rollouts. GEPA was introduced in the paper [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457) and available as `dspy.GEPA` which internally uses the GEPA implementation provided in [gepa-ai/gepa](https://github.com/gepa-ai/gepa).

## `dspy.GEPA` Tutorials

### [GEPA for AIME (Math)](../gepa_aime/index.ipynb)
This tutorial explores how GEPA can optimize a single `dspy.ChainOfThought` based program to achieve 10% gains on AIME 2025 with GPT-4.1 Mini!

### [GEPA for Structured Information Extraction for Enterprise Tasks](../gepa_facilitysupportanalyzer/index.ipynb)
This tutorial explores how GEPA leverages predictor-level feedback to improve GPT-4.1 Nano's performance on a three-part task for structured information extraction and classification in an enterprise setting.

### [GEPA for Privacy-Conscious Delegation](../gepa_papillon/index.ipynb)
This tutorial explores how GEPA can improve rapidly in as few as 1 iteration, while leveraging a simple feedback provided by a LLM-as-a-judge metric. The tutorial also explores how GEPA benefits from the textual feedback showing a breakdown of aggregate metrics into sub-components, allowing the reflection LM to identify what aspects of the task need improvement.

### [GEPA for Code Backdoor Classification (AI control)](../gepa_trusted_monitor/index.ipynb)
This tutorial explores how GEPA can optimize a GPT-4.1 Nano classifier to identify backdoors in code written by a larger LM, using `dspy.GEPA` and a comparative metric! The comparative metric allows the prompt optimizer to create a prompt that identifies the signals in the code that are indicative of a backdoor, teasing apart positive samples from negative samples.

---


### Overview {#overview}

*Source: `tutorials/rl_ai_program/index.md`*

# Experimental RL Optimization for DSPy

This section explores cutting-edge reinforcement learning (RL) approaches for optimizing DSPy programs. These experimental techniques represent the frontier of AI program optimization, combining the power of RL with DSPy's modular programming paradigm to achieve even better performance on complex tasks.

## Advanced RL Optimization Techniques

### [RL for Privacy-Conscious Delegation](../rl_papillon/index.ipynb)
Explore how reinforcement learning can optimize privacy-conscious AI systems. This tutorial demonstrates how RL agents can learn to balance task performance with privacy constraints, making intelligent decisions about when and how to delegate sensitive operations.

### [RL for Multi-Hop Research](../rl_multihop/index.ipynb)
Learn to apply reinforcement learning to multi-hop reasoning tasks. This advanced tutorial shows how RL can optimize the search strategy in complex information retrieval scenarios, learning to navigate through multiple information sources more effectively.

---


### Overview {#overview}

*Source: `tutorials/core_development/index.md`*

# Tools, Development, and Deployment

This section covers essential DSPy features and best practices for professional AI development. Learn how to implement key functionalities like streaming, caching, deployment, and monitoring in your DSPy applications. These tutorials focus on the practical aspects of building production-ready systems.

## Integration and Tooling

### [Use MCP in DSPy](../mcp/index.md)
Learn to integrate Model Context Protocol (MCP) with DSPy applications. This tutorial shows how to leverage MCP for enhanced context management and more sophisticated AI interactions.

### [Output Refinement](../output_refinement/best-of-n-and-refine.md)
Master techniques for improving output quality through refinement strategies. Learn how to implement best-of-N sampling and iterative refinement to get higher-quality results from your DSPy programs.

## Data Management and Persistence

### [Saving and Loading](../saving/index.md)
Understand how to persist and restore DSPy programs and their optimized states. Learn best practices for model versioning, checkpoint management, and program serialization.

### [Cache](../cache/index.md)
Implement efficient caching strategies to improve performance and reduce API costs. Learn how to configure and use DSPy's caching mechanisms effectively in different scenarios.

## Production Deployment

### [Deployment](../deployment/index.md)
Learn to deploy DSPy applications in production environments. This tutorial covers multiple deployment strategies such as FastAPI and MLflow.

### [Streaming](../streaming/index.md)
Implement real-time streaming capabilities in your DSPy applications. Learn how to handle streaming responses for better user experience in interactive applications.

### [Async](../async/index.md)
Build asynchronous DSPy applications for improved performance and scalability. Learn async/await patterns and concurrent execution strategies for high-throughput systems.

## Monitoring and Optimization

### [Debugging & Observability](../observability/index.md)
Master debugging and monitoring techniques for DSPy applications. Learn to use comprehensive logging, tracing, and error handling for production systems.

### [Tracking DSPy Optimizers](../optimizer_tracking/index.md)
Learn to track and analyze optimizer performance and behavior. Understand how to monitor optimization processes and enhance the reproducibility of the optimization.

---


### Use MCP in DSPy {#use-mcp-in-dspy}

*Source: `tutorials/mcp/index.md`*

# Tutorial: Use MCP tools in DSPy

MCP, standing for Model Context Protocol, is an open protocol that standardizes how applications
provide context to LLMs. Despite some development overhead, MCP offers a valuable opportunity to
share tools, resources, and prompts with other developers regardless of the technical stack you are
using. Likewise, you can use the tools built by other developers without rewriting code.

In this guide, we will walk you through how to use MCP tools in DSPy. For demonstration purposes,
we will build an airline service agent that can help users book flights and modify or cancel
existing bookings. This will rely on an MCP server with custom tools, but it should be easy to generalize
to [MCP servers built by the community](https://modelcontextprotocol.io/examples).

??? "How to run this tutorial"
    This tutorial cannot be run in hosted IPython notebooks like Google Colab or Databricks notebooks.
    To run the code, you will need to follow the guide to write code on your local device. The code
    is tested on macOS and should work the same way in Linux environments.

## Install Dependencies

Before starting, let's install the required dependencies:

```shell
pip install -U "dspy[mcp]"
```

## MCP Server Setup

Let's first set up the MCP server for the airline agent, which contains:

- A set of databases
  - User database, storing user information.
  - Flight database, storing flight information.
  - Ticket database, storing customer tickets.
- A set of tools
  - fetch_flight_info: get flight information for specific dates.
  - fetch_itinerary: get information about booked itineraries.
  - book_itinerary: book a flight on behalf of the user.
  - modify_itinerary: modify an itinerary, either through flight changes or cancellation.
  - get_user_info: get user information.
  - file_ticket: file a backlog ticket for human assistance.

In your working directory, create a file `mcp_server.py`, and paste the following content into
it:

```python
import random
import string

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

# Create an MCP server
mcp = FastMCP("Airline Agent")


class Date(BaseModel):
    # Somehow LLM is bad at specifying `datetime.datetime`
    year: int
    month: int
    day: int
    hour: int


class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str


class Flight(BaseModel):
    flight_id: str
    date_time: Date
    origin: str
    destination: str
    duration: float
    price: float


class Itinerary(BaseModel):
    confirmation_number: str
    user_profile: UserProfile
    flight: Flight


class Ticket(BaseModel):
    user_request: str
    user_profile: UserProfile


user_database = {
    "Adam": UserProfile(user_id="1", name="Adam", email="adam@gmail.com"),
    "Bob": UserProfile(user_id="2", name="Bob", email="bob@gmail.com"),
    "Chelsie": UserProfile(user_id="3", name="Chelsie", email="chelsie@gmail.com"),
    "David": UserProfile(user_id="4", name="David", email="david@gmail.com"),
}

flight_database = {
    "DA123": Flight(
        flight_id="DA123",
        origin="SFO",
        destination="JFK",
        date_time=Date(year=2025, month=9, day=1, hour=1),
        duration=3,
        price=200,
    ),
    "DA125": Flight(
        flight_id="DA125",
        origin="SFO",
        destination="JFK",
        date_time=Date(year=2025, month=9, day=1, hour=7),
        duration=9,
        price=500,
    ),
    "DA456": Flight(
        flight_id="DA456",
        origin="SFO",
        destination="SNA",
        date_time=Date(year=2025, month=10, day=1, hour=1),
        duration=2,
        price=100,
    ),
    "DA460": Flight(
        flight_id="DA460",
        origin="SFO",
        destination="SNA",
        date_time=Date(year=2025, month=10, day=1, hour=9),
        duration=2,
        price=120,
    ),
}

itinery_database = {}
ticket_database = {}


@mcp.tool()
def fetch_flight_info(date: Date, origin: str, destination: str):
    """Fetch flight information from origin to destination on the given date"""
    flights = []

    for flight_id, flight in flight_database.items():
        if (
            flight.date_time.year == date.year
            and flight.date_time.month == date.month
            and flight.date_time.day == date.day
            and flight.origin == origin
            and flight.destination == destination
        ):
            flights.append(flight)
    return flights


@mcp.tool()
def fetch_itinerary(confirmation_number: str):
    """Fetch a booked itinerary information from database"""
    return itinery_database.get(confirmation_number)


@mcp.tool()
def pick_flight(flights: list[Flight]):
    """Pick up the best flight that matches users' request."""
    sorted_flights = sorted(
        flights,
        key=lambda x: (
            x.get("duration") if isinstance(x, dict) else x.duration,
            x.get("price") if isinstance(x, dict) else x.price,
        ),
    )
    return sorted_flights[0]


def generate_id(length=8):
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))


@mcp.tool()
def book_itinerary(flight: Flight, user_profile: UserProfile):
    """Book a flight on behalf of the user."""
    confirmation_number = generate_id()
    while confirmation_number in itinery_database:
        confirmation_number = generate_id()
    itinery_database[confirmation_number] = Itinerary(
        confirmation_number=confirmation_number,
        user_profile=user_profile,
        flight=flight,
    )
    return confirmation_number, itinery_database[confirmation_number]


@mcp.tool()
def cancel_itinerary(confirmation_number: str, user_profile: UserProfile):
    """Cancel an itinerary on behalf of the user."""
    if confirmation_number in itinery_database:
        del itinery_database[confirmation_number]
        return
    raise ValueError("Cannot find the itinerary, please check your confirmation number.")


@mcp.tool()
def get_user_info(name: str):
    """Fetch the user profile from database with given name."""
    return user_database.get(name)


@mcp.tool()
def file_ticket(user_request: str, user_profile: UserProfile):
    """File a customer support ticket if this is something the agent cannot handle."""
    ticket_id = generate_id(length=6)
    ticket_database[ticket_id] = Ticket(
        user_request=user_request,
        user_profile=user_profile,
    )
    return ticket_id


if __name__ == "__main__":
    mcp.run()
```

Before we start the server, let's take a look at the code.

We first create a `FastMCP` instance, which is a utility that helps quickly build an MCP server:

```python
mcp = FastMCP("Airline Agent")
```

Then we define our data structures, which in a real-world application would be the database schema, e.g.:

```python
class Flight(BaseModel):
    flight_id: str
    date_time: Date
    origin: str
    destination: str
    duration: float
    price: float
```

Following that, we initialize our database instances. In a real-world application, these would be connectors to
actual databases, but for simplicity, we just use dictionaries:

```python
user_database = {
    "Adam": UserProfile(user_id="1", name="Adam", email="adam@gmail.com"),
    "Bob": UserProfile(user_id="2", name="Bob", email="bob@gmail.com"),
    "Chelsie": UserProfile(user_id="3", name="Chelsie", email="chelsie@gmail.com"),
    "David": UserProfile(user_id="4", name="David", email="david@gmail.com"),
}
```

The next step is to define the tools and mark them with `@mcp.tool()` so that they are discoverable by
MCP clients as MCP tools:

```python
@mcp.tool()
def fetch_flight_info(date: Date, origin: str, destination: str):
    """Fetch flight information from origin to destination on the given date"""
    flights = []

    for flight_id, flight in flight_database.items():
        if (
            flight.date_time.year == date.year
            and flight.date_time.month == date.month
            and flight.date_time.day == date.day
            and flight.origin == origin
            and flight.destination == destination
        ):
            flights.append(flight)
    return flights
```

The last step is spinning up the server:

```python
if __name__ == "__main__":
    mcp.run()
```

Now we have finished writing the server! Let's launch it:

```shell
python path_to_your_working_directory/mcp_server.py
```

## Write a DSPy Program That Utilizes Tools in MCP Server

Now that the server is running, let's build the actual airline service agent which
utilizes the MCP tools in our server to assist users. In your working directory,
create a file named `dspy_mcp_agent.py`, and follow the guide to add code to it.

### Gather Tools from MCP Servers

We first need to gather all available tools from the MCP server and make them
usable by DSPy. DSPy provides an API [`dspy.Tool`](https://dspy.ai/api/primitives/Tool/)
as the standard tool interface. Let's convert all the MCP tools to `dspy.Tool`.

We need to create an MCP client instance to communicate with the MCP server, fetch all available
tools, and convert them to `dspy.Tool` using the static method `from_mcp_tool`:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["path_to_your_working_directory/mcp_server.py"],
    env=None,
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools = await session.list_tools()

            # Convert MCP tools to DSPy tools
            dspy_tools = []
            for tool in tools.tools:
                dspy_tools.append(dspy.Tool.from_mcp_tool(session, tool))

            print(len(dspy_tools))
            print(dspy_tools[0].args)

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
```

With the code above, we have successfully collected all available MCP tools and converted
them to DSPy tools.


### Build a DSPy Agent to Handle Customer Requests

Now we will use `dspy.ReAct` to build the agent for handling customer requests. `ReAct` stands
for "reasoning and acting," which asks the LLM to decide whether to call a tool or wrap up the process.
If a tool is required, the LLM takes responsibility for deciding which tool to call and providing
the appropriate arguments.

As usual, we need to create a `dspy.Signature` to define the input and output of our agent:

```python
import dspy

class DSPyAirlineCustomerService(dspy.Signature):
    """You are an airline customer service agent. You are given a list of tools to handle user requests. You should decide the right tool to use in order to fulfill users' requests."""

    user_request: str = dspy.InputField()
    process_result: str = dspy.OutputField(
        desc=(
            "Message that summarizes the process result, and the information users need, "
            "e.g., the confirmation_number if it's a flight booking request."
        )
    )
```

And choose an LM for our agent:

```python
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
```

Then we create the ReAct agent by passing the tools and signature into the `dspy.ReAct` API. We can now
put together the complete code script:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import dspy

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["script_tmp/mcp_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


class DSPyAirlineCustomerService(dspy.Signature):
    """You are an airline customer service agent. You are given a list of tools to handle user requests.
    You should decide the right tool to use in order to fulfill users' requests."""

    user_request: str = dspy.InputField()
    process_result: str = dspy.OutputField(
        desc=(
            "Message that summarizes the process result, and the information users need, "
            "e.g., the confirmation_number if it's a flight booking request."
        )
    )


dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))


async def run(user_request):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools = await session.list_tools()

            # Convert MCP tools to DSPy tools
            dspy_tools = []
            for tool in tools.tools:
                dspy_tools.append(dspy.Tool.from_mcp_tool(session, tool))

            # Create the agent
            react = dspy.ReAct(DSPyAirlineCustomerService, tools=dspy_tools)

            result = await react.acall(user_request=user_request)
            print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run("please help me book a flight from SFO to JFK on 09/01/2025, my name is Adam"))
```

Note that we must call `react.acall` because MCP tools are async by default. Let's execute the script:

```shell
python path_to_your_working_directory/dspy_mcp_agent.py
```

You should see output similar to this:

```
Prediction(
    trajectory={'thought_0': 'I need to fetch flight information for Adam from SFO to JFK on 09/01/2025 to find available flights for booking.', 'tool_name_0': 'fetch_flight_info', 'tool_args_0': {'date': {'year': 2025, 'month': 9, 'day': 1, 'hour': 0}, 'origin': 'SFO', 'destination': 'JFK'}, 'observation_0': ['{"flight_id": "DA123", "date_time": {"year": 2025, "month": 9, "day": 1, "hour": 1}, "origin": "SFO", "destination": "JFK", "duration": 3.0, "price": 200.0}', '{"flight_id": "DA125", "date_time": {"year": 2025, "month": 9, "day": 1, "hour": 7}, "origin": "SFO", "destination": "JFK", "duration": 9.0, "price": 500.0}'], ..., 'tool_name_4': 'finish', 'tool_args_4': {}, 'observation_4': 'Completed.'},
    reasoning="I successfully booked a flight for Adam from SFO to JFK on 09/01/2025. I found two available flights, selected the more economical option (flight DA123 at 1 AM for $200), retrieved Adam's user profile, and completed the booking process. The confirmation number for the flight is 8h7clk3q.",
    process_result='Your flight from SFO to JFK on 09/01/2025 has been successfully booked. Your confirmation number is 8h7clk3q.'
)
```

The `trajectory` field contains the entire thinking and acting process. If you're curious about what's happening
under the hood, check out the [Observability Guide](https://dspy.ai/tutorials/observability/) to set up MLflow,
which visualizes every step happening inside `dspy.ReAct`!


## Conclusion

In this guide, we built an airline service agent that utilizes a custom MCP server and the `dspy.ReAct` module. In the context
of MCP support, DSPy provides a simple interface for interacting with MCP tools, giving you the flexibility to implement
any functionality you need.

---


### Output Refinement {#output-refinement}

*Source: `tutorials/output_refinement/best-of-n-and-refine.md`*

# Output Refinement: BestOfN and Refine

Both `BestOfN` and `Refine` are DSPy modules designed to improve the reliability and quality of predictions by making multiple `LM` calls with different rollout IDs to bypass caching. Both modules stop when they have reached `N` attempts or when the `reward_fn` returns an award above the `threshold`.

## BestOfN

`BestOfN` is a module that runs the provided module multiple times (up to `N`) with different rollout IDs. It returns either the first prediction that passes a specified threshold or the one with the highest reward if none meets the threshold.

### Basic Usage

Lets say we wanted to have the best chance of getting a one word answer from the model. We could use `BestOfN` to try multiple rollout IDs and return the best result.

```python
import dspy

def one_word_answer(args, pred: dspy.Prediction) -> float:
    return 1.0 if len(pred.answer.split()) == 1 else 0.0

best_of_3 = dspy.BestOfN(
    module=dspy.ChainOfThought("question -> answer"), 
    N=3, 
    reward_fn=one_word_answer, 
    threshold=1.0
)

result = best_of_3(question="What is the capital of Belgium?")
print(result.answer)  # Brussels
```

### Error Handling

By default, if the module encounters an error during an attempt, it will continue trying until it reaches `N` attempts. You can adjust this behavior with the `fail_count` parameter:

```python
best_of_3 = dspy.BestOfN(
    module=qa, 
    N=3, 
    reward_fn=one_word_answer, 
    threshold=1.0,
    fail_count=1
)

best_of_3(question="What is the capital of Belgium?")
# raises an error after the first failure
```

## Refine

`Refine` extends the functionality of `BestOfN` by adding an automatic feedback loop. After each unsuccessful attempt (except the final one), it automatically generates detailed feedback about the module's performance and uses this feedback as hints for subsequent runs.

### Basic Usage

```python
import dspy

def one_word_answer(args, pred: dspy.Prediction) -> float:
    return 1.0 if len(pred.answer.split()) == 1 else 0.0

refine = dspy.Refine(
    module=dspy.ChainOfThought("question -> answer"), 
    N=3, 
    reward_fn=one_word_answer, 
    threshold=1.0
)

result = refine(question="What is the capital of Belgium?")
print(result.answer)  # Brussels
```

### Error Handling

Like `BestOfN`, `Refine` will try up to `N` times by default, even if errors occur. You can control this with the `fail_count` parameter:

```python
# Stop after the first error
refine = dspy.Refine(
    module=qa, 
    N=3, 
    reward_fn=one_word_answer, 
    threshold=1.0,
    fail_count=1
)
```

## Comparison: BestOfN vs. Refine

Both modules serve similar purposes but differ in their approach:

- `BestOfN` simply tries different rollout IDs and selects the best resulting prediction as defined by the `reward_fn`.
- `Refine` adds an feedback loop, using the lm to generate a detailed feedback about the module's own performance using the previous prediction and the code in the `reward_fn`. This feedback is then used as hints for subsequent runs.

## Practical Examples

### Ensuring Factual Correctness

```python
import dspy

class FactualityJudge(dspy.Signature):
    """Determine if a statement is factually accurate."""
    statement: str = dspy.InputField()
    is_factual: bool = dspy.OutputField()

factuality_judge = dspy.ChainOfThought(FactualityJudge)

def factuality_reward(args, pred: dspy.Prediction) -> float:
    statement = pred.answer    
    result = factuality_judge(statement)    
    return 1.0 if result.is_factual else 0.0

refined_qa = dspy.Refine(
    module=dspy.ChainOfThought("question -> answer"),
    N=3,
    reward_fn=factuality_reward,
    threshold=1.0
)

result = refined_qa(question="Tell me about Belgium's capital city.")
print(result.answer)
```

### Summarization - Controlling Response Length

```python
import dspy

def ideal_length_reward(args, pred: dspy.Prediction) -> float:
    """
    Reward the summary for being close to 75 words with a tapering off for longer summaries.
    """
    word_count = len(pred.summary.split())
    distance = abs(word_count - 75)
    return max(0.0, 1.0 - (distance / 125))

optimized_summarizer = dspy.BestOfN(
    module=dspy.ChainOfThought("text -> summary"),
    N=50,
    reward_fn=ideal_length_reward,
    threshold=0.9
)

result = optimized_summarizer(
    text="[Long text to summarize...]"
)
print(result.summary)
```

## Migration from `dspy.Suggest` and `dspy.Assert`

`BestOfN` and `Refine` are the replacements for `dspy.Suggest` and `dspy.Assert` as of DSPy 2.6.

---


### Saving and Loading {#saving-and-loading}

*Source: `tutorials/saving/index.md`*

# Tutorial: Saving and Loading your DSPy program

This guide demonstrates how to save and load your DSPy program. At a high level, there are two ways to save your DSPy program:

1. Save the state of the program only, similar to weights-only saving in PyTorch.
2. Save the whole program, including both the architecture and the state, which is supported by `dspy>=2.6.0`.

## State-only Saving

State represents the DSPy program's internal state, including the signature, demos (few-shot examples), and other information like
the `lm` to use for each `dspy.Predict` in the program. It also includes configurable attributes of other DSPy modules like
`k` for `dspy.retrievers.Retriever`. To save the state of a program, use the `save` method and set `save_program=False`. You can
choose to save the state to a JSON file or a pickle file. We recommend saving the state to a JSON file because it is safer and readable.
But sometimes your program contains non-serializable objects like `dspy.Image` or `datetime.datetime`, in which case you should save
the state to a pickle file.

Let's say we have compiled a program with some data, and we want to save the program for future usage:

```python
import dspy
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

gsm8k = GSM8K()
gsm8k_trainset = gsm8k.train[:10]
dspy_program = dspy.ChainOfThought("question -> answer")

optimizer = dspy.BootstrapFewShot(metric=gsm8k_metric, max_bootstrapped_demos=4, max_labeled_demos=4, max_rounds=5)
compiled_dspy_program = optimizer.compile(dspy_program, trainset=gsm8k_trainset)
```

To save the state of your program to json file:

```python
compiled_dspy_program.save("./dspy_program/program.json", save_program=False)
```

To save the state of your program to a pickle file:

!!! danger "Security Warning: Pickle Files Can Execute Arbitrary Code"
    Loading `.pkl` files can execute arbitrary code and may be dangerous. Only load pickle files from trusted sources in secure environments. **Prefer using `.json` files whenever possible**. If you must use pickle files, ensure you trust the source and use the `allow_pickle=True` parameter when loading.

```python
compiled_dspy_program.save("./dspy_program/program.pkl", save_program=False)
```

To load your saved state, you need to **recreate the same program**, then load the state using the `load` method.

```python
loaded_dspy_program = dspy.ChainOfThought("question -> answer") # Recreate the same program.
loaded_dspy_program.load("./dspy_program/program.json")

assert len(compiled_dspy_program.demos) == len(loaded_dspy_program.demos)
for original_demo, loaded_demo in zip(compiled_dspy_program.demos, loaded_dspy_program.demos):
    # Loaded demo is a dict, while the original demo is a dspy.Example.
    assert original_demo.toDict() == loaded_demo
assert str(compiled_dspy_program.signature) == str(loaded_dspy_program.signature)
```

Or load the state from a pickle file:

!!! danger "Security Warning"
    Remember to use `allow_pickle=True` when loading pickle files, and only load from trusted sources.

```python
loaded_dspy_program = dspy.ChainOfThought("question -> answer") # Recreate the same program.
loaded_dspy_program.load("./dspy_program/program.pkl", allow_pickle=True)

assert len(compiled_dspy_program.demos) == len(loaded_dspy_program.demos)
for original_demo, loaded_demo in zip(compiled_dspy_program.demos, loaded_dspy_program.demos):
    # Loaded demo is a dict, while the original demo is a dspy.Example.
    assert original_demo.toDict() == loaded_demo
assert str(compiled_dspy_program.signature) == str(loaded_dspy_program.signature)
```

## Whole Program Saving

!!! warning "Security Notice: Whole Program Saving Uses Pickle"
    Whole program saving uses `cloudpickle` for serialization, which has the same security risks as pickle files. Only load programs from trusted sources in secure environments.

Starting from `dspy>=2.6.0`, DSPy supports saving the whole program, including the architecture and the state. This feature
is powered by `cloudpickle`, which is a library for serializing and deserializing Python objects.

To save the whole program, use the `save` method and set `save_program=True`, and specify a directory path to save the program
instead of a file name. We require a directory path because we also save some metadata, e.g., the dependency versions along
with the program itself.

```python
compiled_dspy_program.save("./dspy_program/", save_program=True)
```

To load the saved program, directly use `dspy.load` method:

```python
loaded_dspy_program = dspy.load("./dspy_program/")

assert len(compiled_dspy_program.demos) == len(loaded_dspy_program.demos)
for original_demo, loaded_demo in zip(compiled_dspy_program.demos, loaded_dspy_program.demos):
    # Loaded demo is a dict, while the original demo is a dspy.Example.
    assert original_demo.toDict() == loaded_demo
assert str(compiled_dspy_program.signature) == str(loaded_dspy_program.signature)
```

With whole program saving, you don't need to recreate the program, but can directly load the architecture along with the state.
You can pick the suitable saving approach based on your needs.

### Serializing Imported Modules

When saving a program with `save_program=True`, you might need to include custom modules that your program depends on. This is
necessary if your program depends on these modules, but at loading time these modules are not imported before calling `dspy.load`.

You can specify which custom modules should be serialized with your program by passing them to the `modules_to_serialize`
parameter when calling `save`. This ensures that any dependencies your program relies on are included during serialization and
available when loading the program later.

Under the hood this uses cloudpickle's `cloudpickle.register_pickle_by_value` function to register a module as picklable by value.
When a module is registered this way, cloudpickle will serialize the module by value rather than by reference, ensuring that the
module contents are preserved with the saved program.

For example, if your program uses custom modules:

```python
import dspy
import my_custom_module

compiled_dspy_program = dspy.ChainOfThought(my_custom_module.custom_signature)

# Save the program with the custom module
compiled_dspy_program.save(
    "./dspy_program/",
    save_program=True,
    modules_to_serialize=[my_custom_module]
)
```

This ensures that the required modules are properly serialized and available when loading the program later. Any number of
modules can be passed to `modules_to_serialize`. If you don't specify `modules_to_serialize`, no additional modules will be
registered for serialization.

## Backward Compatibility

As of `dspy<3.0.0`, we don't guarantee the backward compatibility of the saved program. For example, if you save the program with `dspy==2.5.35`,
at loading time please make sure to use the same version of DSPy to load the program, otherwise the program may not work as expected. Chances
are that loading a saved file in a different version of DSPy will not raise an error, but the performance could be different from when
the program was saved.

Starting from `dspy>=3.0.0`, we will guarantee the backward compatibility of the saved program in major releases, i.e., programs saved in `dspy==3.0.0`
should be loadable in `dspy==3.7.10`.

---


### Cache {#cache}

*Source: `tutorials/cache/index.md`*

# Use and Customize DSPy Cache

In this tutorial, we will explore the design of DSPy's caching mechanism and demonstrate how to effectively use and customize it.

## DSPy Cache Structure

DSPy's caching system is architected in three distinct layers:

1.  **In-memory cache**: Implemented using `cachetools.LRUCache`, this layer provides fast access to frequently used data.
2.  **On-disk cache**: Leveraging `diskcache.FanoutCache`, this layer offers persistent storage for cached items.
3.  **Prompt cache (Server-side cache)**: This layer is managed by the LLM service provider (e.g., OpenAI, Anthropic).

While DSPy does not directly control the server-side prompt cache, it offers users the flexibility to enable, disable, and customize the in-memory and on-disk caches to suit their specific requirements.

## Using DSPy Cache

By default, both in-memory and on-disk caching are automatically enabled in DSPy. No specific action is required to start using the cache. When a cache hit occurs, you will observe a significant reduction in the module call's execution time. Furthermore, if usage tracking is enabled, the usage metrics for a cached call will be `None`.

Consider the following example:

```python
import dspy
import os
import time

os.environ["OPENAI_API_KEY"] = "{your_openai_key}"

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"), track_usage=True)

predict = dspy.Predict("question->answer")

start = time.time()
result1 = predict(question="Who is the GOAT of basketball?")
print(f"Time elapse: {time.time() - start: 2f}\n\nTotal usage: {result1.get_lm_usage()}")

start = time.time()
result2 = predict(question="Who is the GOAT of basketball?")
print(f"Time elapse: {time.time() - start: 2f}\n\nTotal usage: {result2.get_lm_usage()}")
```

A sample output looks like:

```
Time elapse:  4.384113
Total usage: {'openai/gpt-4o-mini': {'completion_tokens': 97, 'prompt_tokens': 144, 'total_tokens': 241, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0, 'text_tokens': None, 'image_tokens': None}}}

Time elapse:  0.000529
Total usage: {}
```

## Using Provider-Side Prompt Caching

In addition to DSPy's built-in caching mechanism, you can leverage provider-side prompt caching offered by LLM providers like Anthropic and OpenAI. This feature is particularly useful when working with modules like `dspy.ReAct()` that send similar prompts repeatedly, as it reduces both latency and costs by caching prompt prefixes on the provider's servers.

You can enable prompt caching by passing the `cache_control_injection_points` parameter to `dspy.LM()`. This works with supported providers like Anthropic and OpenAI. For more details on this feature, see the [LiteLLM prompt caching documentation](https://docs.litellm.ai/docs/tutorials/prompt_caching#configuration).

```python
import dspy
import os

os.environ["ANTHROPIC_API_KEY"] = "{your_anthropic_key}"
lm = dspy.LM(
    "anthropic/claude-sonnet-4-5-20250929",
    cache_control_injection_points=[
        {
            "location": "message",
            "role": "system",
        }
    ],
)
dspy.configure(lm=lm)

# Use with any DSPy module
predict = dspy.Predict("question->answer")
result = predict(question="What is the capital of France?")
```

This is especially beneficial when:

- Using `dspy.ReAct()` with the same instructions
- Working with long system prompts that remain constant
- Making multiple requests with similar context

## Disabling/Enabling DSPy Cache

There are scenarios where you might need to disable caching, either entirely or selectively for in-memory or on-disk caches. For instance:

- You require different responses for identical LM requests.
- You lack disk write permissions and need to disable the on-disk cache.
- You have limited memory resources and wish to disable the in-memory cache.

DSPy provides the `dspy.configure_cache()` utility function for this purpose. You can use the corresponding flags to control the enabled/disabled state of each cache type:

```python
dspy.configure_cache(
    enable_disk_cache=False,
    enable_memory_cache=False,
)
```

In additions, you can manage the capacity of the in-memory and on-disk caches:

```python
dspy.configure_cache(
    enable_disk_cache=True,
    enable_memory_cache=True,
    disk_size_limit_bytes=YOUR_DESIRED_VALUE,
    memory_max_entries=YOUR_DESIRED_VALUE,
)
```

Please note that `disk_size_limit_bytes` defines the maximum size in bytes for the on-disk cache, while `memory_max_entries` specifies the maximum number of entries for the in-memory cache.

## Understanding and Customizing the Cache

In specific situations, you might want to implement a custom cache, for example, to gain finer control over how cache keys are generated. By default, the cache key is derived from a hash of all request arguments sent to `litellm`, excluding credentials like `api_key`.

To create a custom cache, you need to subclass `dspy.clients.Cache` and override the relevant methods:

```python
class CustomCache(dspy.clients.Cache):
    def __init__(self, **kwargs):
        {write your own constructor}

    def cache_key(self, request: dict[str, Any], ignored_args_for_cache_key: Optional[list[str]] = None) -> str:
        {write your logic of computing cache key}

    def get(self, request: dict[str, Any], ignored_args_for_cache_key: Optional[list[str]] = None) -> Any:
        {write your cache read logic}

    def put(
        self,
        request: dict[str, Any],
        value: Any,
        ignored_args_for_cache_key: Optional[list[str]] = None,
        enable_memory_cache: bool = True,
    ) -> None:
        {write your cache write logic}
```

To ensure seamless integration with the rest of DSPy, it is recommended to implement your custom cache using the same method signatures as the base class, or at a minimum, include `**kwargs` in your method definitions to prevent runtime errors during cache read/write operations.

Once your custom cache class is defined, you can instruct DSPy to use it:

```python
dspy.cache = CustomCache()
```

Let's illustrate this with a practical example. Suppose we want the cache key computation to depend solely on the request message content, ignoring other parameters like the specific LM being called. We can create a custom cache as follows:

```python
class CustomCache(dspy.clients.Cache):

    def cache_key(self, request: dict[str, Any], ignored_args_for_cache_key: Optional[list[str]] = None) -> str:
        messages = request.get("messages", [])
        return sha256(orjson.dumps(messages, option=orjson.OPT_SORT_KEYS)).hexdigest()

dspy.cache = CustomCache(enable_disk_cache=True, enable_memory_cache=True, disk_cache_dir=dspy.clients.DISK_CACHE_DIR)
```

For comparison, consider executing the code below without the custom cache:

```python
import dspy
import os
import time

os.environ["OPENAI_API_KEY"] = "{your_openai_key}"

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

predict = dspy.Predict("question->answer")

start = time.time()
result1 = predict(question="Who is the GOAT of soccer?")
print(f"Time elapse: {time.time() - start: 2f}")

start = time.time()
with dspy.context(lm=dspy.LM("openai/gpt-4.1-mini")):
    result2 = predict(question="Who is the GOAT of soccer?")
print(f"Time elapse: {time.time() - start: 2f}")
```

The time elapsed will indicate that the cache is not hit on the second call. However, when using the custom cache:

```python
import dspy
import os
import time
from typing import Dict, Any, Optional
import orjson
from hashlib import sha256

os.environ["OPENAI_API_KEY"] = "{your_openai_key}"

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

class CustomCache(dspy.clients.Cache):

    def cache_key(self, request: dict[str, Any], ignored_args_for_cache_key: Optional[list[str]] = None) -> str:
        messages = request.get("messages", [])
        return sha256(orjson.dumps(messages, option=orjson.OPT_SORT_KEYS)).hexdigest()

dspy.cache = CustomCache(enable_disk_cache=True, enable_memory_cache=True, disk_cache_dir=dspy.clients.DISK_CACHE_DIR)

predict = dspy.Predict("question->answer")

start = time.time()
result1 = predict(question="Who is the GOAT of volleyball?")
print(f"Time elapse: {time.time() - start: 2f}")

start = time.time()
with dspy.context(lm=dspy.LM("openai/gpt-4.1-mini")):
    result2 = predict(question="Who is the GOAT of volleyball?")
print(f"Time elapse: {time.time() - start: 2f}")
```

You will observe that the cache is hit on the second call, demonstrating the effect of the custom cache key logic.

---


### Deployment {#deployment}

*Source: `tutorials/deployment/index.md`*

# Tutorial: Deploying your DSPy program

This guide demonstrates two potential ways to deploy your DSPy program in production: FastAPI for lightweight deployments and MLflow for more production-grade deployments with program versioning and management.

Below, we'll assume you have the following simple DSPy program that you want to deploy. You can replace this with something more sophisticated.

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
dspy_program = dspy.ChainOfThought("question -> answer")
```

## Deploying with FastAPI

FastAPI offers a straightforward way to serve your DSPy program as a REST API. This is ideal when you have direct access to your program code and need a lightweight deployment solution.

```bash
> pip install fastapi uvicorn
> export OPENAI_API_KEY="your-openai-api-key"
```

Let's create a FastAPI application to serve your `dspy_program` defined above.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import dspy

app = FastAPI(
    title="DSPy Program API",
    description="A simple API serving a DSPy Chain of Thought program",
    version="1.0.0"
)

# Define request model for better documentation and validation
class Question(BaseModel):
    text: str

# Configure your language model and 'asyncify' your DSPy program.
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm, async_max_workers=4) # default is 8
dspy_program = dspy.ChainOfThought("question -> answer")
dspy_program = dspy.asyncify(dspy_program)

@app.post("/predict")
async def predict(question: Question):
    try:
        result = await dspy_program(question=question.text)
        return {
            "status": "success",
            "data": result.toDict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

In the code above, we call `dspy.asyncify` to convert the dspy program to run in async mode for high-throughput FastAPI
deployments. Currently, this runs the dspy program in a separate thread and awaits its result.

By default, the limit of spawned threads is 8. Think of this like a worker pool.
If you have 8 in-flight programs and call it once more, the 9th call will wait until one of the 8 returns.
You can configure the async capacity using the new `async_max_workers` setting.

??? "Streaming, in DSPy 2.6.0+"

    Streaming is also supported in DSPy 2.6.0+, which can be installed via `pip install -U dspy`.

    We can use `dspy.streamify` to convert the dspy program to a streaming mode. This is useful when you want to stream
    the intermediate outputs (i.e. O1-style reasoning) to the client before the final prediction is ready. This uses
    asyncify under the hood and inherits the execution semantics.

    ```python
    dspy_program = dspy.asyncify(dspy.ChainOfThought("question -> answer"))
    streaming_dspy_program = dspy.streamify(dspy_program)

    @app.post("/predict/stream")
    async def stream(question: Question):
        async def generate():
            async for value in streaming_dspy_program(question=question.text):
                if isinstance(value, dspy.Prediction):
                    data = {"prediction": value.labels().toDict()}
                elif isinstance(value, litellm.ModelResponse):
                    data = {"chunk": value.json()}
                yield f"data: {orjson.dumps(data).decode()}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")

    # Since you're often going to want to stream the result of a DSPy program as server-sent events,
    # we've included a helper function for that, which is equivalent to the code above.

    from dspy.utils.streaming import streaming_response

    @app.post("/predict/stream")
    async def stream(question: Question):
        stream = streaming_dspy_program(question=question.text)
        return StreamingResponse(streaming_response(stream), media_type="text/event-stream")
    ```

Write your code to a file, e.g., `fastapi_dspy.py`. Then you can serve the app with:

```bash
> uvicorn fastapi_dspy:app --reload
```

It will start a local server at `http://127.0.0.1:8000/`. You can test it with the python code below:

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"text": "What is the capital of France?"}
)
print(response.json())
```

You should see the response like below:

```json
{
  "status": "success",
  "data": {
    "reasoning": "The capital of France is a well-known fact, commonly taught in geography classes and referenced in various contexts. Paris is recognized globally as the capital city, serving as the political, cultural, and economic center of the country.",
    "answer": "The capital of France is Paris."
  }
}
```

## Deploying with MLflow

We recommend deploying with MLflow if you are looking to package your DSPy program and deploy in an isolated environment.
MLflow is a popular platform for managing machine learning workflows, including versioning, tracking, and deployment.

```bash
> pip install mlflow>=2.18.0
```

Let's spin up the MLflow tracking server, where we will store our DSPy program. The command below will start a local server at
`http://127.0.0.1:5000/`.

```bash
> mlflow ui
```

Then we can define the DSPy program and log it to the MLflow server. "log" is an overloaded term in MLflow, basically it means
we store the program information along with environment requirements in the MLflow server. This is done via the `mlflow.dspy.log_model()`
function, please see the code below:

> [!NOTE]
> As of MLflow 2.22.0, there is a caveat that you must wrap your DSPy program in a custom DSPy Module class when deploying with MLflow.
> This is because MLflow requires positional arguments while DSPy pre-built modules disallow positional arguments, e.g., `dspy.Predict`
> or `dspy.ChainOfThought`. To work around this, create a wrapper class that inherits from `dspy.Module` and implement your program's
> logic in the `forward()` method, as shown in the example below.

```python
import dspy
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("deploy_dspy_program")

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

class MyProgram(dspy.Module):
    def __init__(self):
        super().__init__()
        self.cot = dspy.ChainOfThought("question -> answer")

    def forward(self, messages):
        return self.cot(question=messages[0]["content"])

dspy_program = MyProgram()

with mlflow.start_run():
    mlflow.dspy.log_model(
        dspy_program,
        "dspy_program",
        input_example={"messages": [{"role": "user", "content": "What is LLM agent?"}]},
        task="llm/v1/chat",
    )
```

We recommend you to set `task="llm/v1/chat"` so that the deployed program automatically takes input and generate output in
the same format as the OpenAI chat API, which is a common interface for LM applications. Write the code above into
a file, e.g. `mlflow_dspy.py`, and run it.

After you logged the program, you can view the saved information in MLflow UI. Open `http://127.0.0.1:5000/` and select
the `deploy_dspy_program` experiment, then select the run your just created, under the `Artifacts` tab, you should see the
logged program information, similar to the following screenshot:

![MLflow UI](./dspy_mlflow_ui.png)

Grab your run id from UI (or the console print when you execute `mlflow_dspy.py`), now you can deploy the logged program
with the following command:

```bash
> mlflow models serve -m runs:/{run_id}/model -p 6000
```

After the program is deployed, you can test it with the following command:

```bash
> curl http://127.0.0.1:6000/invocations -H "Content-Type:application/json"  --data '{"messages": [{"content": "what is 2 + 2?", "role": "user"}]}'
```

You should see the response like below:

```json
{
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "{\"reasoning\": \"The question asks for the sum of 2 and 2. To find the answer, we simply add the two numbers together: 2 + 2 = 4.\", \"answer\": \"4\"}"
      },
      "finish_reason": "stop"
    }
  ]
}
```

For complete guide on how to deploy a DSPy program with MLflow, and how to customize the deployment, please refer to the
[MLflow documentation](https://mlflow.org/docs/latest/llms/dspy/index.html).

### Best Practices for MLflow Deployment

1. **Environment Management**: Always specify your Python dependencies in a `conda.yaml` or `requirements.txt` file.
2. **Versioning**: Use meaningful tags and descriptions for your model versions.
3. **Input Validation**: Define clear input schemas and examples.
4. **Monitoring**: Set up proper logging and monitoring for production deployments.

For production deployments, consider using MLflow with containerization:

```bash
> mlflow models build-docker -m "runs:/{run_id}/model" -n "dspy-program"
> docker run -p 6000:8080 dspy-program
```

For a complete guide on production deployment options and best practices, refer to the
[MLflow documentation](https://mlflow.org/docs/latest/llms/dspy/index.html).

---


### Debugging & Observability {#debugging--observability}

*Source: `tutorials/observability/index.md`*

# Tutorial: Debugging and Observability in DSPy

This guide demonstrates how to debug problems and improve observability in DSPy. Modern AI programs often involve multiple components, such as language models, retrievers, and tools. DSPy allows you to build and optimize such complex AI systems in a clean and modular way.

However, as systems grow more sophisticated, the ability to **understand what your system is doing** becomes critical. Without transparency, the prediction process can easily become a black box, making failures or quality issues difficult to diagnose and production maintenance challenging.

By the end of this tutorial, you'll understand how to debug an issue and improve observability using [MLflow Tracing](#tracing). You'll also explore how to build a custom logging solution using callbacks.


## Define a Program

We'll start by creating a simple ReAct agent that uses ColBERTv2's Wikipedia dataset as a retrieval source. You can replace this with a more sophisticated program.

```python
import dspy
import os

os.environ["OPENAI_API_KEY"] = "{your_openai_api_key}"

lm = dspy.LM("openai/gpt-4o-mini")
colbert = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
dspy.configure(lm=lm)


def retrieve(query: str):
    """Retrieve top 3 relevant information from ColBert"""
    results = colbert(query, k=3)
    return [x["text"] for x in results]


agent = dspy.ReAct("question -> answer", tools=[retrieve], max_iters=3)
```

Now, let's ask the agent a simple question:

```python
prediction = agent(question="Which baseball team does Shohei Ohtani play for in June 2025?")
print(prediction.answer)
```

```
Shohei Ohtani is expected to play for the Hokkaido Nippon-Ham Fighters in June 2025, based on the available information.
```

Oh, this is incorrect. He no longer plays for the Hokkaido Nippon-Ham Fighters; he moved to the Dodgers and won the World Series in 2024! Let's debug the program and explore potential fixes.

## Using ``inspect_history``

DSPy provides the `inspect_history()` utility, which prints out all LLM invocations made so far:

```python
# Print out 5 LLM calls
dspy.inspect_history(n=5)
```

```
[2024-12-01T10:23:29.144257]

System message:

Your input fields are:
1. `question` (str)

...

Response:

Response:

[[ ## reasoning ## ]]
The search for information regarding Shohei Ohtani's team in June 2025 did not yield any specific results. The retrieved data consistently mentioned that he plays for the Hokkaido Nippon-Ham Fighters, but there was no indication of any changes or updates regarding his team for the specified date. Given the lack of information, it is reasonable to conclude that he may still be with the Hokkaido Nippon-Ham Fighters unless there are future developments that are not captured in the current data.

[[ ## answer ## ]]
Shohei Ohtani is expected to play for the Hokkaido Nippon-Ham Fighters in June 2025, based on the available information.

[[ ## completed ## ]]

```
The log reveals that the agent could not retrieve helpful information from the search tool. However, what exactly did the retriever return? While useful, `inspect_history` has some limitations:

* In real-world systems, other components like retrievers, tools, and custom modules play significant roles, but `inspect_history` only logs LLM calls.
* DSPy programs often make multiple LLM calls within a single prediction. Monolith log history makes it hard to organize logs, especially when handling multiple questions.
* Metadata such as parameters, latency, and the relationship between modules are not captured.

**Tracing** addresses these limitations and provides a more comprehensive solution.

## Tracing

[MLflow](https://mlflow.org/docs/latest/llms/tracing/index.html) is an end-to-end machine learning platform that is integrated seamlessly with DSPy to support best practices in LLMOps. Using MLflow's automatic tracing capability with DSPy is straightforward; **No sign up for services or an API key is required**. You just need to install MLflow and call `mlflow.dspy.autolog()` in your notebook or script.

```bash
pip install -U mlflow>=2.18.0
```

After installation, spin up your server via the command below.

```
# It is highly recommended to use SQL store when using MLflow tracing
mlflow server --backend-store-uri sqlite:///mydb.sqlite
```

If you don't specify a different port via `--port` flag, you MLflow server will be hosted at port 5000.

Now let's change our code snippet to enable MLflow tracing. We need to:

- Tell MLflow where the server is hosted.
- Apply `mlflow.autolog()` so that DSPy tracing is automatically captured.

The full code is as below, now let's run it again!

```python
import dspy
import os
import mlflow

os.environ["OPENAI_API_KEY"] = "{your_openai_api_key}"

# Tell MLflow about the server URI.
mlflow.set_tracking_uri("http://127.0.0.1:5000")
# Create a unique name for your experiment.
mlflow.set_experiment("DSPy")

lm = dspy.LM("openai/gpt-4o-mini")
colbert = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
dspy.configure(lm=lm)


def retrieve(query: str):
    """Retrieve top 3 relevant information from ColBert"""
    results = colbert(query, k=3)
    return [x["text"] for x in results]


agent = dspy.ReAct("question -> answer", tools=[retrieve], max_iters=3)
print(agent(question="Which baseball team does Shohei Ohtani play for?"))
```


MLflow automatically generates a **trace** for each prediction and records it within your experiment. To explore these traces visually, open `http://127.0.0.1:5000/`
in your browser, then select the experiment you just created and navigate to the Traces tab:

![MLflow Trace UI](./mlflow_trace_ui.png)

Click on the most recent trace to view its detailed breakdown:

![MLflow Trace View](./mlflow_trace_view.png)

Here, you can examine the input and output of every step in your workflow. For example, the screenshot above shows the `retrieve` function's input and output. By inspecting the retriever's output, you can see that it returned outdated information, which is not sufficient to determine which team Shohei Ohtani plays for in June 2025. You can also inspect
other steps, e.g, language model's input, output, and configuration.

To address the issue of outdated information, you can replace the `retrieve` function with a web search tool powered by [Tavily search](https://www.tavily.com/).

```python
from tavily import TavilyClient
import dspy
import mlflow

# Tell MLflow about the server URI.
mlflow.set_tracking_uri("http://127.0.0.1:5000")
# Create a unique name for your experiment.
mlflow.set_experiment("DSPy")

search_client = TavilyClient(api_key="<YOUR_TAVILY_API_KEY>")

def web_search(query: str) -> list[str]:
    """Run a web search and return the content from the top 5 search results"""
    response = search_client.search(query)
    return [r["content"] for r in response["results"]]

agent = dspy.ReAct("question -> answer", tools=[web_search])

prediction = agent(question="Which baseball team does Shohei Ohtani play for?")
print(agent.answer)
```

```
Los Angeles Dodgers
```

Below is a GIF demonstrating how to navigate through the MLflow UI:

![MLflow Trace UI Navigation](./mlflow_trace_ui_navigation.gif)


For a complete guide on how to use MLflow tracing, please refer to
the [MLflow Tracing Guide](https://mlflow.org/docs/3.0.0rc0/tracing).


!!! info Learn more about MLflow

    MLflow is an end-to-end LLMOps platform that offers extensive features like experiment tracking, evaluation, and deployment. To learn more about DSPy and MLflow integration, visit [this tutorial](../deployment/index.md#deploying-with-mlflow).


## Building a Custom Logging Solution

Sometimes, you may want to implement a custom logging solution. For instance, you might need to log specific events triggered by a particular module. DSPy's **callback** mechanism supports such use cases. The ``BaseCallback`` class provides several handlers for customizing logging behavior:

|Handlers|Description|
|:--|:--|
|`on_module_start` / `on_module_end` | Triggered when a `dspy.Module` subclass is invoked. |
|`on_lm_start` / `on_lm_end` | Triggered when a `dspy.LM` subclass is invoked. |
|`on_adapter_format_start` / `on_adapter_format_end`| Triggered when a `dspy.Adapter` subclass formats the input prompt. |
|`on_adapter_parse_start` / `on_adapter_parse_end`| Triggered when a `dspy.Adapter` subclass postprocess the output text from an LM. |
|`on_tool_start` / `on_tool_end` | Triggered when a `dspy.Tool` subclass is invoked. |
|`on_evaluate_start` / `on_evaluate_end` | Triggered when a `dspy.Evaluate` instance is invoked. |

Here's an example of custom callback that logs the intermediate steps of a ReAct agent:

```python
import dspy
from dspy.utils.callback import BaseCallback

# 1. Define a custom callback class that extends BaseCallback class
class AgentLoggingCallback(BaseCallback):

    # 2. Implement on_module_end handler to run a custom logging code.
    def on_module_end(self, call_id, outputs, exception):
        step = "Reasoning" if self._is_reasoning_output(outputs) else "Acting"
        print(f"== {step} Step ===")
        for k, v in outputs.items():
            print(f"  {k}: {v}")
        print("\n")

    def _is_reasoning_output(self, outputs):
        return any(k.startswith("Thought") for k in outputs.keys())

# 3. Set the callback to DSPy setting so it will be applied to program execution
dspy.configure(callbacks=[AgentLoggingCallback()])
```


```
== Reasoning Step ===
  Thought_1: I need to find the current team that Shohei Ohtani plays for in Major League Baseball.
  Action_1: Search[Shohei Ohtani current team 2023]

== Acting Step ===
  passages: ["Shohei Ohtani ..."]

...
```

!!! info Handling Inputs and Outputs in Callbacks

    Be cautious when working with input or output data in callbacks. Mutating them in-place can modify the original data passed to the program, potentially leading to unexpected behavior. To avoid this, it's strongly recommended to create a copy of the data before performing any operations that may alter it.

---


### Tracking DSPy Optimizers {#tracking-dspy-optimizers}

*Source: `tutorials/optimizer_tracking/index.md`*

# Tracking DSPy Optimizers with MLflow

This tutorial demonstrates how to use MLflow to track and analyze your DSPy optimization process. MLflow's built-in integration for DSPy provides traceability and debuggability for your DSPy optimization experience. It allows you to understand the intermediate trials during the optimization, store the optimized program and its results, and provides observability into your program execution.

Through the autologging capability, MLflow tracks the following information:

* **Optimizer Parameters**
    * Number of few-shot examples
    * Number of candidates
    * Other configuration settings

* **Program States**
    * Initial instructions and few-shot examples
    * Optimized instructions and few-shot examples
    * Intermediate instructions and few-shot examples during optimization

* **Datasets**
    * Training data used
    * Evaluation data used

* **Performance Progression**
    * Overall metric progression
    * Performance at each evaluation step

* **Traces**
    * Program execution traces
    * Model responses
    * Intermediate prompts

## Getting Started

### 1. Install MLflow
First, install MLflow (version 2.21.1 or later):

```bash
pip install mlflow>=2.21.1
```

### 2. Start MLflow Tracking Server

Let's spin up the MLflow tracking server with the following command. This will start a local server at `http://127.0.0.1:5000/`:

```bash
# It is highly recommended to use SQL store when using MLflow tracing
mlflow server --backend-store-uri sqlite:///mydb.sqlite
```

### 3. Enable Autologging

Configure MLflow to track your DSPy optimization:

```python
import mlflow
import dspy

# Enable autologging with all features
mlflow.dspy.autolog(
    log_compiles=True,    # Track optimization process
    log_evals=True,       # Track evaluation results
    log_traces_from_compile=True  # Track program traces during optimization
)

# Configure MLflow tracking
mlflow.set_tracking_uri("http://localhost:5000")  # Use local MLflow server
mlflow.set_experiment("DSPy-Optimization")
```

### 4. Optimizing Your Program

Here's a complete example showing how to track the optimization of a math problem solver:

```python
import dspy
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric

# Configure your language model
lm = dspy.LM(model="openai/gpt-4o")
dspy.configure(lm=lm)

# Load dataset
gsm8k = GSM8K()
trainset, devset = gsm8k.train, gsm8k.dev

# Define your program
program = dspy.ChainOfThought("question -> answer")

# Create and run optimizer with tracking
teleprompter = dspy.teleprompt.MIPROv2(
    metric=gsm8k_metric,
    auto="light",
)

# The optimization process will be automatically tracked
optimized_program = teleprompter.compile(
    program,
    trainset=trainset,
)
```

### 5. Viewing Results

Once your optimization is complete, you can analyze the results through MLflow's UI. Let's walk through how to explore your optimization runs.

#### Step 1: Access the MLflow UI
Navigate to `http://localhost:5000` in your web browser to access the MLflow tracking server UI.

#### Step 2: Understanding the Experiment Structure
When you open the experiment page, you'll see a hierarchical view of your optimization process. The parent run represents your overall optimization process, while the child runs show each intermediate version of your program that was created during optimization.

![Experiments](./experiment.png)

#### Step 3: Analyzing the Parent Run
Clicking on the parent run reveals the big picture of your optimization process. You'll find detailed information about your optimizer's configuration parameters and how your evaluation metrics progressed over time. The parent run also stores your final optimized program, including the instructions, signature definitions, and few-shot examples that were used. Additionally, you can review the training data that was used during the optimization process.

![Parent Run](./parent_run.png)

#### Step 4: Examining Child Runs
Each child run provides a detailed snapshot of a specific optimization attempt. When you select a child run from the experiment page, you can explore several aspects of that particular intermediate program.
On the run parameter tab or artifact tab, you can review the instructions and few-shot examples used for the intermediate program.
One of the most powerful features is the Traces tab, which provides a step-by-step view of your program's execution. Here you can understand exactly how your DSPy program processes inputs and generates outputs.

![Child Run](./child_run.png)

### 6. Loading Models for Inference
You can load the optimized program directly from the MLflow tracking server for inference:

```python
model_path = mlflow.artifacts.download_artifacts("mlflow-artifacts:/path/to/best_model.json")
program.load(model_path)
```

## Troubleshooting

- If traces aren't appearing, ensure `log_traces_from_compile=True`
- For large datasets, consider setting `log_traces_from_compile=False` to avoid memory issues
- Use `mlflow.get_run(run_id)` to programmatically access MLflow run data

For more features, explore the [MLflow Documentation](https://mlflow.org/docs/latest/llms/dspy).

---


### Streaming {#streaming}

*Source: `tutorials/streaming/index.md`*

# Streaming

In this guide, we will walk you through how to enable streaming in your DSPy program. DSPy Streaming
consists of two parts:

- **Output Token Streaming**: Stream individual tokens as they're generated, rather than waiting for the complete response.
- **Intermediate Status Streaming**: Provide real-time updates about the program's execution state (e.g., "Calling web search...", "Processing results...").

## Output Token Streaming

DSPy's token streaming feature works with any module in your pipeline, not just the final output. The only requirement is that the streamed field must be of type `str`. To enable token streaming:

1. Wrap your program with `dspy.streamify`
2. Create one or more `dspy.streaming.StreamListener` objects to specify which fields to stream

Here's a basic example:

```python
import os

import dspy

os.environ["OPENAI_API_KEY"] = "your_api_key"

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

predict = dspy.Predict("question->answer")

# Enable streaming for the 'answer' field
stream_predict = dspy.streamify(
    predict,
    stream_listeners=[dspy.streaming.StreamListener(signature_field_name="answer")],
)
```

To consume the streamed output:

```python
import asyncio

async def read_output_stream():
    output_stream = stream_predict(question="Why did a chicken cross the kitchen?")

    async for chunk in output_stream:
        print(chunk)

asyncio.run(read_output_stream())
```

This will produce output like:

```
StreamResponse(predict_name='self', signature_field_name='answer', chunk='To')
StreamResponse(predict_name='self', signature_field_name='answer', chunk=' get')
StreamResponse(predict_name='self', signature_field_name='answer', chunk=' to')
StreamResponse(predict_name='self', signature_field_name='answer', chunk=' the')
StreamResponse(predict_name='self', signature_field_name='answer', chunk=' other')
StreamResponse(predict_name='self', signature_field_name='answer', chunk=' side of the frying pan!')
Prediction(
    answer='To get to the other side of the frying pan!'
)
```

Note: Since `dspy.streamify` returns an async generator, you must use it within an async context. If you're using an environment like Jupyter or Google Colab that already has an event loop (async context), you can use the generator directly.

You may have noticed that the above streaming contains two different entities: `StreamResponse`
and `Prediction.` `StreamResponse` is the wrapper over streaming tokens on the field being listened to, and in
this example it is the `answer` field. `Prediction` is the program's final output. In DSPy, streaming is
implemented in a sidecar fashion: we enable streaming on the LM so that LM outputs a stream of tokens. We send these
tokens to a side channel, which is being continuously read by the user-defined listeners. Listeners keep interpreting
the stream, and decides if the `signature_field_name` it is listening to has started to appear and has finalized.
Once it decides that the field appears, the listener begins outputting tokens to the async generator users can
read. Listeners' internal mechanism changes according to the adapter behind the scene, and because usually
we cannot decide if a field has finalized until seeing the next field, the listener buffers the output tokens
before sending to the final generator, which is why you will usually see the last chunk of type `StreamResponse`
has more than one token. The program's output is also written to the stream, which is the chunk of `Prediction`
as in the sample output above.

To handle these different types and implement custom logic:

```python
import asyncio

async def read_output_stream():
  output_stream = stream_predict(question="Why did a chicken cross the kitchen?")

  return_value = None
  async for chunk in output_stream:
    if isinstance(chunk, dspy.streaming.StreamResponse):
      print(f"Output token of field {chunk.signature_field_name}: {chunk.chunk}")
    elif isinstance(chunk, dspy.Prediction):
      return_value = chunk
  return return_value


program_output = asyncio.run(read_output_stream())
print("Final output: ", program_output)
```

### Understand `StreamResponse`

`StreamResponse` (`dspy.streaming.StreamResponse`) is the wrapper class of streaming tokens. It comes with 3
fields:

- `predict_name`: the name of the predict that holds the `signature_field_name`. The name is the
  same name of keys as you run `your_program.named_predictors()`. In the code above because `answer` is from
  the `predict` itself, so the `predict_name` shows up as `self`, which is the only key as your run
  `predict.named_predictors()`.
- `signature_field_name`: the output field that these tokens map to. `predict_name` and `signature_field_name`
  together form the unique identifier of the field. We will demonstrate how to handle multiple fields streaming
  and duplicated field name later in this guide.
- `chunk`: the value of the stream chunk.

### Streaming with Cache

When a cached result is found, the stream will skip individual tokens and only yield the final `Prediction`. For example:

```
Prediction(
    answer='To get to the other side of the dinner plate!'
)
```

### Streaming Multiple Fields

You can monitor multiple fields by creating a `StreamListener` for each one. Here's an example with a multi-module program:

```python
import asyncio

import dspy

lm = dspy.LM("openai/gpt-4o-mini", cache=False)
dspy.configure(lm=lm)


class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()

        self.predict1 = dspy.Predict("question->answer")
        self.predict2 = dspy.Predict("answer->simplified_answer")

    def forward(self, question: str, **kwargs):
        answer = self.predict1(question=question)
        simplified_answer = self.predict2(answer=answer)
        return simplified_answer


predict = MyModule()
stream_listeners = [
    dspy.streaming.StreamListener(signature_field_name="answer"),
    dspy.streaming.StreamListener(signature_field_name="simplified_answer"),
]
stream_predict = dspy.streamify(
    predict,
    stream_listeners=stream_listeners,
)

async def read_output_stream():
    output = stream_predict(question="why did a chicken cross the kitchen?")

    return_value = None
    async for chunk in output:
        if isinstance(chunk, dspy.streaming.StreamResponse):
            print(chunk)
        elif isinstance(chunk, dspy.Prediction):
            return_value = chunk
    return return_value

program_output = asyncio.run(read_output_stream())
print("Final output: ", program_output)
```

The output will look like:

```
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk='To')
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk=' get')
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk=' to')
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk=' the')
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk=' other side of the recipe!')
StreamResponse(predict_name='predict2', signature_field_name='simplified_answer', chunk='To')
StreamResponse(predict_name='predict2', signature_field_name='simplified_answer', chunk=' reach')
StreamResponse(predict_name='predict2', signature_field_name='simplified_answer', chunk=' the')
StreamResponse(predict_name='predict2', signature_field_name='simplified_answer', chunk=' other side of the recipe!')
Final output:  Prediction(
    simplified_answer='To reach the other side of the recipe!'
)
```

### Streaming the Same Field Multiple Times (as in dspy.ReAct)

By default, a `StreamListener` automatically closes itself after completing a single streaming session.
This design helps prevent performance issues, since every token is broadcast to all configured stream listeners,
and having too many active listeners can introduce significant overhead.

However, in scenarios where a DSPy module is used repeatedly in a loop—such as with `dspy.ReAct` — you may want to stream
the same field from each prediction, every time it is used. To enable this behavior, set allow_reuse=True when creating
your `StreamListener`. See the example below:

```python
import asyncio

import dspy

lm = dspy.LM("openai/gpt-4o-mini", cache=False)
dspy.configure(lm=lm)


def fetch_user_info(user_name: str):
    """Get user information like name, birthday, etc."""
    return {
        "name": user_name,
        "birthday": "2009-05-16",
    }


def get_sports_news(year: int):
    """Get sports news for a given year."""
    if year == 2009:
        return "Usane Bolt broke the world record in the 100m race."
    return None


react = dspy.ReAct("question->answer", tools=[fetch_user_info, get_sports_news])

stream_listeners = [
    # dspy.ReAct has a built-in output field called "next_thought".
    dspy.streaming.StreamListener(signature_field_name="next_thought", allow_reuse=True),
]
stream_react = dspy.streamify(react, stream_listeners=stream_listeners)


async def read_output_stream():
    output = stream_react(question="What sports news happened in the year Adam was born?")
    return_value = None
    async for chunk in output:
        if isinstance(chunk, dspy.streaming.StreamResponse):
            print(chunk)
        elif isinstance(chunk, dspy.Prediction):
            return_value = chunk
    return return_value


print(asyncio.run(read_output_stream()))
```

In this example, by setting `allow_reuse=True` in the StreamListener, you ensure that streaming for "next_thought" is
available for every iteration, not just the first. When you run this code, you will see the streaming tokens for `next_thought`
output each time the field is produced.

#### Handling Duplicate Field Names

When streaming fields with the same name from different modules, specify both the `predict` and `predict_name` in the `StreamListener`:

```python
import asyncio

import dspy

lm = dspy.LM("openai/gpt-4o-mini", cache=False)
dspy.configure(lm=lm)


class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()

        self.predict1 = dspy.Predict("question->answer")
        self.predict2 = dspy.Predict("question, answer->answer, score")

    def forward(self, question: str, **kwargs):
        answer = self.predict1(question=question)
        simplified_answer = self.predict2(answer=answer)
        return simplified_answer


predict = MyModule()
stream_listeners = [
    dspy.streaming.StreamListener(
        signature_field_name="answer",
        predict=predict.predict1,
        predict_name="predict1"
    ),
    dspy.streaming.StreamListener(
        signature_field_name="answer",
        predict=predict.predict2,
        predict_name="predict2"
    ),
]
stream_predict = dspy.streamify(
    predict,
    stream_listeners=stream_listeners,
)


async def read_output_stream():
    output = stream_predict(question="why did a chicken cross the kitchen?")

    return_value = None
    async for chunk in output:
        if isinstance(chunk, dspy.streaming.StreamResponse):
            print(chunk)
        elif isinstance(chunk, dspy.Prediction):
            return_value = chunk
    return return_value


program_output = asyncio.run(read_output_stream())
print("Final output: ", program_output)
```

The output will be like:

```
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk='To')
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk=' get')
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk=' to')
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk=' the')
StreamResponse(predict_name='predict1', signature_field_name='answer', chunk=' other side of the recipe!')
StreamResponse(predict_name='predict2', signature_field_name='answer', chunk="I'm")
StreamResponse(predict_name='predict2', signature_field_name='answer', chunk=' ready')
StreamResponse(predict_name='predict2', signature_field_name='answer', chunk=' to')
StreamResponse(predict_name='predict2', signature_field_name='answer', chunk=' assist')
StreamResponse(predict_name='predict2', signature_field_name='answer', chunk=' you')
StreamResponse(predict_name='predict2', signature_field_name='answer', chunk='! Please provide a question.')
Final output:  Prediction(
    answer="I'm ready to assist you! Please provide a question.",
    score='N/A'
)
```

## Intermediate Status Streaming

Status streaming keeps users informed about the program's progress, especially useful for long-running operations like tool calls or complex AI pipelines. To implement status streaming:

1. Create a custom status message provider by subclassing `dspy.streaming.StatusMessageProvider`
2. Override the desired hook methods to provide custom status messages
3. Pass your provider to `dspy.streamify`

Example:

```python
class MyStatusMessageProvider(dspy.streaming.StatusMessageProvider):
    def lm_start_status_message(self, instance, inputs):
        return f"Calling LM with inputs {inputs}..."

    def lm_end_status_message(self, outputs):
        return f"Tool finished with output: {outputs}!"
```

Available hooks:

- lm_start_status_message: status message at the start of calling dspy.LM.
- lm_end_status_message: status message at the end of calling dspy.LM.
- module_start_status_message: status message at the start of calling a dspy.Module.
- module_end_status_message: status message at the start of calling a dspy.Module.
- tool_start_status_message: status message at the start of calling dspy.Tool.
- tool_end_status_message: status message at the end of calling dspy.Tool.

Each hook should return a string containing the status message.

After creating the message provider, just pass it to `dspy.streamify`, and you can enable both
status message streaming and output token streaming. Please see the example below. The intermediate
status message is represented in the class `dspy.streaming.StatusMessage`, so we need to have
another condition check to capture it.

```python
import asyncio

import dspy

lm = dspy.LM("openai/gpt-4o-mini", cache=False)
dspy.configure(lm=lm)


class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()

        self.tool = dspy.Tool(lambda x: 2 * x, name="double_the_number")
        self.predict = dspy.ChainOfThought("num1, num2->sum")

    def forward(self, num, **kwargs):
        num2 = self.tool(x=num)
        return self.predict(num1=num, num2=num2)


class MyStatusMessageProvider(dspy.streaming.StatusMessageProvider):
    def tool_start_status_message(self, instance, inputs):
        return f"Calling Tool {instance.name} with inputs {inputs}..."

    def tool_end_status_message(self, outputs):
        return f"Tool finished with output: {outputs}!"


predict = MyModule()
stream_listeners = [
    # dspy.ChainOfThought has a built-in output field called "reasoning".
    dspy.streaming.StreamListener(signature_field_name="reasoning"),
]
stream_predict = dspy.streamify(
    predict,
    stream_listeners=stream_listeners,
    status_message_provider=MyStatusMessageProvider(),
)


async def read_output_stream():
    output = stream_predict(num=3)

    return_value = None
    async for chunk in output:
        if isinstance(chunk, dspy.streaming.StreamResponse):
            print(chunk)
        elif isinstance(chunk, dspy.Prediction):
            return_value = chunk
        elif isinstance(chunk, dspy.streaming.StatusMessage):
            print(chunk)
    return return_value


program_output = asyncio.run(read_output_stream())
print("Final output: ", program_output)
```

Sample output:

```
StatusMessage(message='Calling tool double_the_number...')
StatusMessage(message='Tool calling finished! Querying the LLM with tool calling results...')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk='To')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' find')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' the')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' sum')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' of')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' the')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' two')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' numbers')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=',')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' we')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' simply')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' add')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' them')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' together')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk='.')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' Here')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=',')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' ')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk='3')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' plus')
StreamResponse(predict_name='predict.predict', signature_field_name='reasoning', chunk=' 6 equals 9.')
Final output:  Prediction(
    reasoning='To find the sum of the two numbers, we simply add them together. Here, 3 plus 6 equals 9.',
    sum='9'
)
```

## Synchronous Streaming

By default calling a streamified DSPy program produces an async generator. In order to get back
a sync generator, you can set the flag `async_streaming=False`:


```python
import os

import dspy

os.environ["OPENAI_API_KEY"] = "your_api_key"

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

predict = dspy.Predict("question->answer")

# Enable streaming for the 'answer' field
stream_predict = dspy.streamify(
    predict,
    stream_listeners=[dspy.streaming.StreamListener(signature_field_name="answer")],
    async_streaming=False,
)

output = stream_predict(question="why did a chicken cross the kitchen?")

program_output = None
for chunk in output:
    if isinstance(chunk, dspy.streaming.StreamResponse):
        print(chunk)
    elif isinstance(chunk, dspy.Prediction):
        program_output = chunk
print(f"Program output: {program_output}")
```

---


### Async {#async}

*Source: `tutorials/async/index.md`*

# Async DSPy Programming

DSPy provides native support for asynchronous programming, allowing you to build more efficient and
scalable applications. This guide will walk you through how to leverage async capabilities in DSPy,
covering both built-in modules and custom implementations.

## Why Use Async in DSPy?

Asynchronous programming in DSPy offers several benefits:
- Improved performance through concurrent operations
- Better resource utilization
- Reduced waiting time for I/O-bound operations
- Enhanced scalability for handling multiple requests

## When Should I use Sync or Async?

Choosing between synchronous and asynchronous programming in DSPy depends on your specific use case.
Here's a guide to help you make the right choice:

Use Synchronous Programming When

- You're exploring or prototyping new ideas
- You're conducting research or experiments
- You're building small to medium-sized applications
- You need simpler, more straightforward code
- You want easier debugging and error tracking

Use Asynchronous Programming When:

- You're building a high-throughput service (high QPS)
- You're working with tools that only support async operations
- You need to handle multiple concurrent requests efficiently
- You're building a production service that requires high scalability

### Important Considerations

While async programming offers performance benefits, it comes with some trade-offs:

- More complex error handling and debugging
- Potential for subtle, hard-to-track bugs
- More complex code structure
- Different code between ipython (Colab, Jupyter lab, Databricks notebooks, ...) and normal python runtime.

We recommend starting with synchronous programming for most development scenarios and switching to async
only when you have a clear need for its benefits. This approach allows you to focus on the core logic of
your application before dealing with the additional complexity of async programming.

## Using Built-in Modules Asynchronously

Most DSPy built-in modules support asynchronous operations through the `acall()` method. This method
maintains the same interface as the synchronous `__call__` method but operates asynchronously.

Here's a basic example using `dspy.Predict`:

```python
import dspy
import asyncio
import os

os.environ["OPENAI_API_KEY"] = "your_api_key"

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
predict = dspy.Predict("question->answer")

async def main():
    # Use acall() for async execution
    output = await predict.acall(question="why did a chicken cross the kitchen?")
    print(output)


asyncio.run(main())
```

### Working with Async Tools

DSPy's `Tool` class seamlessly integrates with async functions. When you provide an async
function to `dspy.Tool`, you can execute it using `acall()`. This is particularly useful
for I/O-bound operations or when working with external services.

```python
import asyncio
import dspy
import os

os.environ["OPENAI_API_KEY"] = "your_api_key"

async def foo(x):
    # Simulate an async operation
    await asyncio.sleep(0.1)
    print(f"I get: {x}")

# Create a tool from the async function
tool = dspy.Tool(foo)

async def main():
    # Execute the tool asynchronously
    await tool.acall(x=2)

asyncio.run(main())
```

#### Using Async Tools in Synchronous Contexts

If you need to call an async tool from synchronous code, you can enable automatic async-to-sync conversion:

```python
import dspy

async def async_tool(x: int) -> int:
    """An async tool that doubles a number."""
    await asyncio.sleep(0.1)
    return x * 2

tool = dspy.Tool(async_tool)

# Option 1: Use context manager for temporary conversion
with dspy.context(allow_tool_async_sync_conversion=True):
    result = tool(x=5)  # Works in sync context
    print(result)  # 10

# Option 2: Configure globally
dspy.configure(allow_tool_async_sync_conversion=True)
result = tool(x=5)  # Now works everywhere
print(result)  # 10
```

For more details on async tools, see the [Tools documentation](../../learn/programming/tools.md#async-tools).

Note: When using `dspy.ReAct` with tools, calling `acall()` on the ReAct instance will automatically
execute all tools asynchronously using their `acall()` methods.

## Creating Custom Async DSPy Modules

To create your own async DSPy module, implement the `aforward()` method instead of `forward()`. This method
should contain your module's async logic. Here's an example of a custom module that chains two async operations:

```python
import dspy
import asyncio
import os

os.environ["OPENAI_API_KEY"] = "your_api_key"
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

class MyModule(dspy.Module):
    def __init__(self):
        self.predict1 = dspy.ChainOfThought("question->answer")
        self.predict2 = dspy.ChainOfThought("answer->simplified_answer")

    async def aforward(self, question, **kwargs):
        # Execute predictions sequentially but asynchronously
        answer = await self.predict1.acall(question=question)
        return await self.predict2.acall(answer=answer)


async def main():
    mod = MyModule()
    result = await mod.acall(question="Why did a chicken cross the kitchen?")
    print(result)


asyncio.run(main())
```

---


### Overview {#overview}

*Source: `tutorials/real_world_examples/index.md`*

# Real-World Examples

This section demonstrates practical applications of DSPy across different domains and use cases. Each tutorial shows how to build production-ready AI systems using DSPy's modular programming approach.

## Featured Examples

### 📄 [Generating llms.txt](../llms_txt_generation/index.md)
Learn how to create AI-powered documentation generators that analyze codebases and produce structured, LLM-friendly documentation following the llms.txt standard.

**Key Concepts:** Repository analysis, meta-programming, documentation generation

### 📧 [Email Information Extraction](../email_extraction/index.md)
Build intelligent email processing systems that classify messages, extract entities, and identify action items using DSPy's structured prediction capabilities.

**Key Concepts:** Information extraction, classification, text processing

### 🧠 [Memory-Enabled ReAct Agents with Mem0](../mem0_react_agent/index.md)
Create conversational agents with persistent memory using DSPy ReAct and Mem0 integration for context-aware interactions across sessions.

**Key Concepts:** Memory systems, conversational AI, agent persistence

### 💰 [Financial Analysis with Yahoo Finance](../yahoo_finance_react/index.md)
Develop financial analysis agents that fetch real-time market data, analyze news sentiment, and provide investment insights using LangChain tool integration.

**Key Concepts:** Tool integration, financial data, real-time analysis

### 🔄 [Automated Code Generation from Documentation](../sample_code_generation/index.md)
Build a system that automatically fetches documentation from URLs and generates working code examples for any library using DSPy's intelligent analysis.

**Key Concepts:** Web scraping, documentation parsing, automated learning, code generation

### 🎮 [Building a Creative Text-Based AI Game](../ai_text_game/index.md)
Create an interactive text-based adventure game with dynamic storytelling, AI-powered NPCs, and adaptive gameplay using DSPy's modular programming approach.

**Key Concepts:** Interactive storytelling, game state management, character progression, AI-driven narratives

---


### Generating llms.txt {#generating-llmstxt}

*Source: `tutorials/llms_txt_generation/index.md`*

# Generating llms.txt for Code Documentation with DSPy

This tutorial demonstrates how to use DSPy to automatically generate an `llms.txt` file for the DSPy repository itself. The `llms.txt` standard provides LLM-friendly documentation that helps AI systems better understand codebases.

## What is llms.txt?

`llms.txt` is a proposed standard for providing structured, LLM-friendly documentation about a project. It typically includes:

- Project overview and purpose
- Key concepts and terminology
- Architecture and structure
- Usage examples
- Important files and directories

## Building a DSPy Program for llms.txt Generation

Let's create a DSPy program that analyzes a repository and generates comprehensive `llms.txt` documentation.

### Step 1: Define Our Signatures

First, we'll define signatures for different aspects of documentation generation:

```python
import dspy
from typing import List

class AnalyzeRepository(dspy.Signature):
    """Analyze a repository structure and identify key components."""
    repo_url: str = dspy.InputField(desc="GitHub repository URL")
    file_tree: str = dspy.InputField(desc="Repository file structure")
    readme_content: str = dspy.InputField(desc="README.md content")
    
    project_purpose: str = dspy.OutputField(desc="Main purpose and goals of the project")
    key_concepts: list[str] = dspy.OutputField(desc="List of important concepts and terminology")
    architecture_overview: str = dspy.OutputField(desc="High-level architecture description")

class AnalyzeCodeStructure(dspy.Signature):
    """Analyze code structure to identify important directories and files."""
    file_tree: str = dspy.InputField(desc="Repository file structure")
    package_files: str = dspy.InputField(desc="Key package and configuration files")
    
    important_directories: list[str] = dspy.OutputField(desc="Key directories and their purposes")
    entry_points: list[str] = dspy.OutputField(desc="Main entry points and important files")
    development_info: str = dspy.OutputField(desc="Development setup and workflow information")

class GenerateLLMsTxt(dspy.Signature):
    """Generate a comprehensive llms.txt file from analyzed repository information."""
    project_purpose: str = dspy.InputField()
    key_concepts: list[str] = dspy.InputField()
    architecture_overview: str = dspy.InputField()
    important_directories: list[str] = dspy.InputField()
    entry_points: list[str] = dspy.InputField()
    development_info: str = dspy.InputField()
    usage_examples: str = dspy.InputField(desc="Common usage patterns and examples")
    
    llms_txt_content: str = dspy.OutputField(desc="Complete llms.txt file content following the standard format")
```

### Step 2: Create the Repository Analyzer Module

```python
class RepositoryAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.analyze_repo = dspy.ChainOfThought(AnalyzeRepository)
        self.analyze_structure = dspy.ChainOfThought(AnalyzeCodeStructure)
        self.generate_examples = dspy.ChainOfThought("repo_info -> usage_examples")
        self.generate_llms_txt = dspy.ChainOfThought(GenerateLLMsTxt)
    
    def forward(self, repo_url, file_tree, readme_content, package_files):
        # Analyze repository purpose and concepts
        repo_analysis = self.analyze_repo(
            repo_url=repo_url,
            file_tree=file_tree,
            readme_content=readme_content
        )
        
        # Analyze code structure
        structure_analysis = self.analyze_structure(
            file_tree=file_tree,
            package_files=package_files
        )
        
        # Generate usage examples
        usage_examples = self.generate_examples(
            repo_info=f"Purpose: {repo_analysis.project_purpose}\nConcepts: {repo_analysis.key_concepts}"
        )
        
        # Generate final llms.txt
        llms_txt = self.generate_llms_txt(
            project_purpose=repo_analysis.project_purpose,
            key_concepts=repo_analysis.key_concepts,
            architecture_overview=repo_analysis.architecture_overview,
            important_directories=structure_analysis.important_directories,
            entry_points=structure_analysis.entry_points,
            development_info=structure_analysis.development_info,
            usage_examples=usage_examples.usage_examples
        )
        
        return dspy.Prediction(
            llms_txt_content=llms_txt.llms_txt_content,
            analysis=repo_analysis,
            structure=structure_analysis
        )
```

### Step 3: Gather Repository Information

Let's create helper functions to extract repository information:

```python
import requests
import os
from pathlib import Path

os.environ["GITHUB_ACCESS_TOKEN"] = "<your_access_token>"

def get_github_file_tree(repo_url):
    """Get repository file structure from GitHub API."""
    # Extract owner/repo from URL
    parts = repo_url.rstrip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    response = requests.get(api_url, headers={
        "Authorization": f"Bearer {os.environ.get('GITHUB_ACCESS_TOKEN')}"
    })
    
    if response.status_code == 200:
        tree_data = response.json()
        file_paths = [item['path'] for item in tree_data['tree'] if item['type'] == 'blob']
        return '\n'.join(sorted(file_paths))
    else:
        raise Exception(f"Failed to fetch repository tree: {response.status_code}")

def get_github_file_content(repo_url, file_path):
    """Get specific file content from GitHub."""
    parts = repo_url.rstrip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(api_url, headers={
        "Authorization": f"Bearer {os.environ.get('GITHUB_ACCESS_TOKEN')}"
    })
    
    if response.status_code == 200:
        import base64
        content = base64.b64decode(response.json()['content']).decode('utf-8')
        return content
    else:
        return f"Could not fetch {file_path}"

def gather_repository_info(repo_url):
    """Gather all necessary repository information."""
    file_tree = get_github_file_tree(repo_url)
    readme_content = get_github_file_content(repo_url, "README.md")
    
    # Get key package files
    package_files = []
    for file_path in ["pyproject.toml", "setup.py", "requirements.txt", "package.json"]:
        try:
            content = get_github_file_content(repo_url, file_path)
            if "Could not fetch" not in content:
                package_files.append(f"=== {file_path} ===\n{content}")
        except:
            continue
    
    package_files_content = "\n\n".join(package_files)
    
    return file_tree, readme_content, package_files_content
```

### Step 4: Configure DSPy and Generate llms.txt

```python
def generate_llms_txt_for_dspy():
    # Configure DSPy (use your preferred LM)
    lm = dspy.LM(model="gpt-4o-mini")
    dspy.configure(lm=lm)
    os.environ["OPENAI_API_KEY"] = "<YOUR OPENAI KEY>"
    
    # Initialize our analyzer
    analyzer = RepositoryAnalyzer()
    
    # Gather DSPy repository information
    repo_url = "https://github.com/stanfordnlp/dspy"
    file_tree, readme_content, package_files = gather_repository_info(repo_url)
    
    # Generate llms.txt
    result = analyzer(
        repo_url=repo_url,
        file_tree=file_tree,
        readme_content=readme_content,
        package_files=package_files
    )
    
    return result

# Run the generation
if __name__ == "__main__":
    result = generate_llms_txt_for_dspy()
    
    # Save the generated llms.txt
    with open("llms.txt", "w") as f:
        f.write(result.llms_txt_content)
    
    print("Generated llms.txt file!")
    print("\nPreview:")
    print(result.llms_txt_content[:500] + "...")
```

## Expected Output Structure

The generated `llms.txt` for DSPy would follow this structure:

```
# DSPy: Programming Language Models

## Project Overview
DSPy is a framework for programming—rather than prompting—language models...

## Key Concepts
- **Modules**: Building blocks for LM programs
- **Signatures**: Input/output specifications  
- **Teleprompters**: Optimization algorithms
- **Predictors**: Core reasoning components

## Architecture
- `/dspy/`: Main package directory
  - `/adapters/`: Input/output format handlers
  - `/clients/`: LM client interfaces
  - `/predict/`: Core prediction modules
  - `/teleprompt/`: Optimization algorithms

## Usage Examples
1. **Building a Classifier**: Using DSPy, a user can define a modular classifier that takes in text data and categorizes it into predefined classes. The user can specify the classification logic declaratively, allowing for easy adjustments and optimizations.
2. **Creating a RAG Pipeline**: A developer can implement a retrieval-augmented generation pipeline that first retrieves relevant documents based on a query and then generates a coherent response using those documents. DSPy facilitates the integration of retrieval and generation components seamlessly.
3. **Optimizing Prompts**: Users can leverage DSPy to create a system that automatically optimizes prompts for language models based on performance metrics, improving the quality of responses over time without manual intervention.
4. **Implementing Agent Loops**: A user can design an agent loop that continuously interacts with users, learns from feedback, and refines its responses, showcasing the self-improving capabilities of the DSPy framework.
5. **Compositional Code**: Developers can write compositional code that allows different modules of the AI system to interact with each other, enabling complex workflows that can be easily modified and extended.
```

The resulting `llms.txt` file provides a comprehensive, LLM-friendly overview of the DSPy repository that can help other AI systems better understand and work with the codebase.

## Next Steps

- Extend the program to analyze multiple repositories
- Add support for different documentation formats
- Create metrics for documentation quality assessment
- Build a web interface for interactive repository analysis

---


### Memory-Enabled ReAct Agents {#memory-enabled-react-agents}

*Source: `tutorials/mem0_react_agent/index.md`*

# Building Memory-Enabled Agents with DSPy ReAct and Mem0

This tutorial demonstrates how to build intelligent conversational agents that can remember information across interactions using DSPy's ReAct framework combined with [Mem0](https://docs.mem0.ai/)'s memory capabilities. You'll learn to create agents that can store, retrieve, and use contextual information to provide personalized and coherent responses.

## What You'll Build

By the end of this tutorial, you'll have a memory-enabled agent that can:

- **Remember user preferences** and past conversations
- **Store and retrieve factual information** about users and topics
- **Use memory to inform decisions** and provide personalized responses
- **Handle complex multi-turn conversations** with context awareness
- **Manage different types of memories** (facts, preferences, experiences)

## Prerequisites

- Basic understanding of DSPy and ReAct agents
- Python 3.9+ installed
- API keys for your preferred LLM provider

## Installation and Setup

```bash
pip install dspy mem0ai
```

## Step 1: Understanding Mem0 Integration

Mem0 provides a memory layer that can store, search, and retrieve memories for AI agents. Let's start by understanding how to integrate it with DSPy:

```python
import dspy
from mem0 import Memory
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configure environment
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Initialize Mem0 memory system
config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "temperature": 0.1
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    }
}
```

## Step 2: Create Memory-Aware Tools

Let's create tools that can interact with the memory system:

```python
import datetime

class MemoryTools:
    """Tools for interacting with the Mem0 memory system."""

    def __init__(self, memory: Memory):
        self.memory = memory

    def store_memory(self, content: str, user_id: str = "default_user") -> str:
        """Store information in memory."""
        try:
            self.memory.add(content, user_id=user_id)
            return f"Stored memory: {content}"
        except Exception as e:
            return f"Error storing memory: {str(e)}"

    def search_memories(self, query: str, user_id: str = "default_user", limit: int = 5) -> str:
        """Search for relevant memories."""
        try:
            results = self.memory.search(query, user_id=user_id, limit=limit)
            if not results:
                return "No relevant memories found."

            memory_text = "Relevant memories found:\n"
            for i, result in enumerate(results["results"]):
                memory_text += f"{i}. {result['memory']}\n"
            return memory_text
        except Exception as e:
            return f"Error searching memories: {str(e)}"

    def get_all_memories(self, user_id: str = "default_user") -> str:
        """Get all memories for a user."""
        try:
            results = self.memory.get_all(user_id=user_id)
            if not results:
                return "No memories found for this user."

            memory_text = "All memories for user:\n"
            for i, result in enumerate(results["results"]):
                memory_text += f"{i}. {result['memory']}\n"
            return memory_text
        except Exception as e:
            return f"Error retrieving memories: {str(e)}"

    def update_memory(self, memory_id: str, new_content: str) -> str:
        """Update an existing memory."""
        try:
            self.memory.update(memory_id, new_content)
            return f"Updated memory with new content: {new_content}"
        except Exception as e:
            return f"Error updating memory: {str(e)}"

    def delete_memory(self, memory_id: str) -> str:
        """Delete a specific memory."""
        try:
            self.memory.delete(memory_id)
            return "Memory deleted successfully."
        except Exception as e:
            return f"Error deleting memory: {str(e)}"

def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

## Step 3: Build the Memory-Enhanced ReAct Agent

Now let's create our main ReAct agent that can use memory:

```python
class MemoryQA(dspy.Signature):
    """
    You're a helpful assistant and have access to memory method.
    Whenever you answer a user's input, remember to store the information in memory
    so that you can use it later.
    """
    user_input: str = dspy.InputField()
    response: str = dspy.OutputField()

class MemoryReActAgent(dspy.Module):
    """A ReAct agent enhanced with Mem0 memory capabilities."""

    def __init__(self, memory: Memory):
        super().__init__()
        self.memory_tools = MemoryTools(memory)

        # Create tools list for ReAct
        self.tools = [
            self.memory_tools.store_memory,
            self.memory_tools.search_memories,
            self.memory_tools.get_all_memories,
            get_current_time,
            self.set_reminder,
            self.get_preferences,
            self.update_preferences,
        ]

        # Initialize ReAct with our tools
        self.react = dspy.ReAct(
            signature=MemoryQA,
            tools=self.tools,
            max_iters=6
        )

    def forward(self, user_input: str):
        """Process user input with memory-aware reasoning."""
        
        return self.react(user_input=user_input)

    def set_reminder(self, reminder_text: str, date_time: str = None, user_id: str = "default_user") -> str:
        """Set a reminder for the user."""
        reminder = f"Reminder set for {date_time}: {reminder_text}"
        return self.memory_tools.store_memory(
            f"REMINDER: {reminder}", 
            user_id=user_id
        )

    def get_preferences(self, category: str = "general", user_id: str = "default_user") -> str:
        """Get user preferences for a specific category."""
        query = f"user preferences {category}"
        return self.memory_tools.search_memories(
            query=query,
            user_id=user_id
        )

    def update_preferences(self, category: str, preference: str, user_id: str = "default_user") -> str:
        """Update user preferences."""
        preference_text = f"User preference for {category}: {preference}"
        return self.memory_tools.store_memory(
            preference_text,
            user_id=user_id
        )
```

## Step 4: Running the Memory-Enhanced Agent

Let's create a simple interface to interact with our memory-enabled agent:

```python
import time
def run_memory_agent_demo():
    """Demonstration of memory-enhanced ReAct agent."""

    # Configure DSPy
    lm = dspy.LM(model='openai/gpt-4o-mini')
    dspy.configure(lm=lm)

    # Initialize memory system
    memory = Memory.from_config(config)

    # Create our agent
    agent = MemoryReActAgent(memory)

    # Sample conversation demonstrating memory capabilities
    print("🧠 Memory-Enhanced ReAct Agent Demo")
    print("=" * 50)

    conversations = [
        "Hi, I'm Alice and I love Italian food, especially pasta carbonara.",
        "I'm Alice. I prefer to exercise in the morning around 7 AM.",
        "I'm Alice. What do you remember about my food preferences?",
        "I'm Alice. Set a reminder for me to go grocery shopping tomorrow.",
        "I'm Alice. What are my exercise preferences?",
        "I'm Alice. I also enjoy hiking on weekends.",
        "I'm Alice. What do you know about me so far?"
    ]

    for i, user_input in enumerate(conversations, 1):
        print(f"\n📝 User: {user_input}")

        try:
            response = agent(user_input=user_input)
            print(f"🤖 Agent: {response.response}")
            time.sleep(1)

        except Exception as e:
            print(f"❌ Error: {e}")

# Run the demonstration
if __name__ == "__main__":
    run_memory_agent_demo()
```

## Expected Output
```
🧠 Memory-Enhanced ReAct Agent Demo
==================================================

📝 User: Hi, I'm Alice and I love Italian food, especially pasta carbonara.

🤖 Agent: Hi Alice! It's great to meet you! Pasta carbonara is a delicious choice. Do you have a favorite place to get it, or do you enjoy making it at home?

📝 User: I'm Alice. I prefer to exercise in the morning around 7 AM.

🤖 Agent: Nice to meet you, Alice! I've noted that you prefer to exercise in the morning around 7 AM. If you have any questions or need tips related to your morning workouts, feel free to ask!

📝 User: I'm Alice. What do you remember about my food preferences?

🤖 Agent: I remember that you love Italian food, and your favorite dish is pasta carbonara!

📝 User: I'm Alice. Set a reminder for me to go grocery shopping tomorrow.

🤖 Agent: I have set a reminder for you, Alice, to go grocery shopping tomorrow.

📝 User: I'm Alice. What are my exercise preferences?

🤖 Agent: Your exercise preference is to work out in the morning around 7 AM.

📝 User: I'm Alice. I also enjoy hiking on weekends.

🤖 Agent: Nice to meet you, Alice! It's great to hear that you enjoy hiking on weekends. If you need any recommendations for trails or tips for your hikes, feel free to ask!

📝 User: I'm Alice. What do you know about me so far?

🤖 Agent: So far, I know that you enjoy hiking on weekends, prefer to exercise in the morning around 7 AM, and love Italian food, especially pasta carbonara. Additionally, you have a reminder set for grocery shopping on October 7, 2023.
```

## Next Steps

- **Implement memory persistence** with databases (PostgreSQL, MongoDB)
- **Add memory categorization** and tagging for better organization
- **Create memory expiration policies** for data management
- **Build multi-user memory isolation** for production applications
- **Add memory analytics** and insights
- **Integrate with vector databases** for enhanced semantic search
- **Implement memory compression** for long-term storage efficiency

This tutorial demonstrates how DSPy's ReAct framework can be enhanced with Mem0's memory capabilities to create intelligent, context-aware agents that can learn and remember information across interactions, making them more useful for real-world applications.

---


### Financial Analysis with Yahoo Finance {#financial-analysis-with-yahoo-finance}

*Source: `tutorials/yahoo_finance_react/index.md`*

# Financial Analysis with DSPy ReAct and Yahoo Finance News

This tutorial shows how to build a financial analysis agent using DSPy ReAct with [LangChain's Yahoo Finance News tool](https://python.langchain.com/docs/integrations/tools/yahoo_finance_news/) for real-time market analysis.

## What You'll Build

A financial agent that fetches news, analyzes sentiment, and provides investment insights.

## Setup

```bash
pip install dspy langchain langchain-community yfinance
```

## Step 1: Convert LangChain Tool to DSPy

```python
import dspy
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from dspy.adapters.types.tool import Tool
import json
import yfinance as yf

# Configure DSPy
lm = dspy.LM(model='openai/gpt-4o-mini')
dspy.configure(lm=lm, allow_tool_async_sync_conversion=True)

# Convert LangChain Yahoo Finance tool to DSPy
yahoo_finance_tool = YahooFinanceNewsTool()
finance_news_tool = Tool.from_langchain(yahoo_finance_tool)
```

## Step 2: Create Supporting Financial Tools

```python
def get_stock_price(ticker: str) -> str:
    """Get current stock price and basic info."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1d")
        
        if hist.empty:
            return f"Could not retrieve data for {ticker}"
        
        current_price = hist['Close'].iloc[-1]
        prev_close = info.get('previousClose', current_price)
        change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0
        
        result = {
            "ticker": ticker,
            "price": round(current_price, 2),
            "change_percent": round(change_pct, 2),
            "company": info.get('longName', ticker)
        }
        
        return json.dumps(result)
    except Exception as e:
        return f"Error: {str(e)}"

def compare_stocks(tickers: str) -> str:
    """Compare multiple stocks (comma-separated)."""
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(',')]
        comparison = []
        
        for ticker in ticker_list:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1d")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_close = info.get('previousClose', current_price)
                change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0
                
                comparison.append({
                    "ticker": ticker,
                    "price": round(current_price, 2),
                    "change_percent": round(change_pct, 2)
                })
        
        return json.dumps(comparison)
    except Exception as e:
        return f"Error: {str(e)}"
```

## Step 3: Build the Financial ReAct Agent

```python
class FinancialAnalysisAgent(dspy.Module):
    """ReAct agent for financial analysis using Yahoo Finance data."""
    
    def __init__(self):
        super().__init__()
        
        # Combine all tools
        self.tools = [
            finance_news_tool,  # LangChain Yahoo Finance News
            get_stock_price,
            compare_stocks
        ]
        
        # Initialize ReAct
        self.react = dspy.ReAct(
            signature="financial_query -> analysis_response",
            tools=self.tools,
            max_iters=6
        )
    
    def forward(self, financial_query: str):
        return self.react(financial_query=financial_query)
```

## Step 4: Run Financial Analysis

```python
def run_financial_demo():
    """Demo of the financial analysis agent."""
    
    # Initialize agent
    agent = FinancialAnalysisAgent()
    
    # Example queries
    queries = [
        "What's the latest news about Apple (AAPL) and how might it affect the stock price?",
        "Compare AAPL, GOOGL, and MSFT performance",
        "Find recent Tesla news and analyze sentiment"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        response = agent(financial_query=query)
        print(f"Analysis: {response.analysis_response}")
        print("-" * 50)

# Run the demo
if __name__ == "__main__":
    run_financial_demo()
```

## Example Output

When you run the agent with a query like "What's the latest news about Apple?", it will:

1. Use the Yahoo Finance News tool to fetch recent Apple news
2. Get current stock price data
3. Analyze the information and provide insights

**Sample Response:**
```
Analysis: Given the current price of Apple (AAPL) at $196.58 and the slight increase of 0.48%, it appears that the stock is performing steadily in the market. However, the inability to access the latest news means that any significant developments that could influence investor sentiment and stock price are unknown. Investors should keep an eye on upcoming announcements or market trends that could impact Apple's performance, especially in comparison to other tech stocks like Microsoft (MSFT), which is also showing a positive trend.
```

## Working with Async Tools

Many Langchain tools use async operations for better performance. For details on async tools, see the [Tools documentation](../../learn/programming/tools.md#async-tools).

## Key Benefits

- **Tool Integration**: Seamlessly combine LangChain tools with DSPy ReAct
- **Real-time Data**: Access current market data and news
- **Extensible**: Easy to add more financial analysis tools
- **Intelligent Reasoning**: ReAct framework provides step-by-step analysis

This tutorial shows how DSPy's ReAct framework works with LangChain's financial tools to create intelligent market analysis agents.

---


### Email Information Extraction {#email-information-extraction}

*Source: `tutorials/email_extraction/index.md`*

# Extracting Information from Emails with DSPy

This tutorial demonstrates how to build an intelligent email processing system using DSPy. We'll create a system that can automatically extract key information from various types of emails, classify their intent, and structure the data for further processing.

## What You'll Build

By the end of this tutorial, you'll have a DSPy-powered email processing system that can:

- **Classify email types** (order confirmation, support request, meeting invitation, etc.)
- **Extract key entities** (dates, amounts, product names, contact info)
- **Determine urgency levels** and required actions
- **Structure extracted data** into consistent formats
- **Handle multiple email formats** robustly

## Prerequisites

- Basic understanding of DSPy modules and signatures
- Python 3.9+ installed
- OpenAI API key (or access to another supported LLM)

## Installation and Setup

```bash
pip install dspy
```

<details>
<summary>Recommended: Set up MLflow Tracing to understand what's happening under the hood.</summary>

### MLflow DSPy Integration

<a href="https://mlflow.org/">MLflow</a> is an LLMOps tool that natively integrates with DSPy and offer explainability and experiment tracking. In this tutorial, you can use MLflow to visualize prompts and optimization progress as traces to understand the DSPy's behavior better. You can set up MLflow easily by following the four steps below.

![MLflow Trace](./mlflow-tracing-email-extraction.png)

1. Install MLflow

```bash
%pip install mlflow>=3.0.0
```

2. Start MLflow UI in a separate terminal
```bash
mlflow ui --port 5000 --backend-store-uri sqlite:///mlruns.db
```

3. Connect the notebook to MLflow
```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("DSPy")
```

4. Enabling tracing.
```python
mlflow.dspy.autolog()
```


To learn more about the integration, visit [MLflow DSPy Documentation](https://mlflow.org/docs/latest/llms/dspy/index.html) as well.
</details>

## Step 1: Define Our Data Structures

First, let's define the types of information we want to extract from emails:

```python
import dspy
from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class EmailType(str, Enum):
    ORDER_CONFIRMATION = "order_confirmation"
    SUPPORT_REQUEST = "support_request"
    MEETING_INVITATION = "meeting_invitation"
    NEWSLETTER = "newsletter"
    PROMOTIONAL = "promotional"
    INVOICE = "invoice"
    SHIPPING_NOTIFICATION = "shipping_notification"
    OTHER = "other"

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ExtractedEntity(BaseModel):
    entity_type: str
    value: str
    confidence: float
```

## Step 2: Create DSPy Signatures

Now let's define the signatures for our email processing pipeline:

```python
class ClassifyEmail(dspy.Signature):
    """Classify the type and urgency of an email based on its content."""

    email_subject: str = dspy.InputField(desc="The subject line of the email")
    email_body: str = dspy.InputField(desc="The main content of the email")
    sender: str = dspy.InputField(desc="Email sender information")

    email_type: EmailType = dspy.OutputField(desc="The classified type of email")
    urgency: UrgencyLevel = dspy.OutputField(desc="The urgency level of the email")
    reasoning: str = dspy.OutputField(desc="Brief explanation of the classification")

class ExtractEntities(dspy.Signature):
    """Extract key entities and information from email content."""

    email_content: str = dspy.InputField(desc="The full email content including subject and body")
    email_type: EmailType = dspy.InputField(desc="The classified type of email")

    key_entities: list[ExtractedEntity] = dspy.OutputField(desc="List of extracted entities with type, value, and confidence")
    financial_amount: Optional[float] = dspy.OutputField(desc="Any monetary amounts found (e.g., '$99.99')")
    important_dates: list[str] = dspy.OutputField(desc="List of important dates found in the email")
    contact_info: list[str] = dspy.OutputField(desc="Relevant contact information extracted")

class GenerateActionItems(dspy.Signature):
    """Determine what actions are needed based on the email content and extracted information."""

    email_type: EmailType = dspy.InputField()
    urgency: UrgencyLevel = dspy.InputField()
    email_summary: str = dspy.InputField(desc="Brief summary of the email content")
    extracted_entities: list[ExtractedEntity] = dspy.InputField(desc="Key entities found in the email")

    action_required: bool = dspy.OutputField(desc="Whether any action is required")
    action_items: list[str] = dspy.OutputField(desc="List of specific actions needed")
    deadline: Optional[str] = dspy.OutputField(desc="Deadline for action if applicable")
    priority_score: int = dspy.OutputField(desc="Priority score from 1-10")

class SummarizeEmail(dspy.Signature):
    """Create a concise summary of the email content."""

    email_subject: str = dspy.InputField()
    email_body: str = dspy.InputField()
    key_entities: list[ExtractedEntity] = dspy.InputField()

    summary: str = dspy.OutputField(desc="A 2-3 sentence summary of the email's main points")
```

## Step 3: Build the Email Processing Module

Now let's create our main email processing module:

```python
class EmailProcessor(dspy.Module):
    """A comprehensive email processing system using DSPy."""

    def __init__(self):
        super().__init__()

        # Initialize our processing components
        self.classifier = dspy.ChainOfThought(ClassifyEmail)
        self.entity_extractor = dspy.ChainOfThought(ExtractEntities)
        self.action_generator = dspy.ChainOfThought(GenerateActionItems)
        self.summarizer = dspy.ChainOfThought(SummarizeEmail)

    def forward(self, email_subject: str, email_body: str, sender: str = ""):
        """Process an email and extract structured information."""

        # Step 1: Classify the email
        classification = self.classifier(
            email_subject=email_subject,
            email_body=email_body,
            sender=sender
        )

        # Step 2: Extract entities
        full_content = f"Subject: {email_subject}\n\nFrom: {sender}\n\n{email_body}"
        entities = self.entity_extractor(
            email_content=full_content,
            email_type=classification.email_type
        )

        # Step 3: Generate summary
        summary = self.summarizer(
            email_subject=email_subject,
            email_body=email_body,
            key_entities=entities.key_entities
        )

        # Step 4: Determine actions
        actions = self.action_generator(
            email_type=classification.email_type,
            urgency=classification.urgency,
            email_summary=summary.summary,
            extracted_entities=entities.key_entities
        )

        # Step 5: Structure the results
        return dspy.Prediction(
            email_type=classification.email_type,
            urgency=classification.urgency,
            summary=summary.summary,
            key_entities=entities.key_entities,
            financial_amount=entities.financial_amount,
            important_dates=entities.important_dates,
            action_required=actions.action_required,
            action_items=actions.action_items,
            deadline=actions.deadline,
            priority_score=actions.priority_score,
            reasoning=classification.reasoning,
            contact_info=entities.contact_info
        )
```

## Step 4: Running the Email Processing System

Let's create a simple function to test our email processing system:

```python
import os
def run_email_processing_demo():
    """Demonstration of the email processing system."""
    
    # Configure DSPy
    lm = dspy.LM(model='openai/gpt-4o-mini')
    dspy.configure(lm=lm)
    os.environ["OPENAI_API_KEY"] = "<YOUR OPENAI KEY>"
    
    # Create our email processor
    processor = EmailProcessor()
    
    # Sample emails for testing
    sample_emails = [
        {
            "subject": "Order Confirmation #12345 - Your MacBook Pro is on the way!",
            "body": """Dear John Smith,

Thank you for your order! We're excited to confirm that your order #12345 has been processed.

Order Details:
- MacBook Pro 14-inch (Space Gray)
- Order Total: $2,399.00
- Estimated Delivery: December 15, 2024
- Tracking Number: 1Z999AA1234567890

If you have any questions, please contact our support team at support@techstore.com.

Best regards,
TechStore Team""",
            "sender": "orders@techstore.com"
        },
        {
            "subject": "URGENT: Server Outage - Immediate Action Required",
            "body": """Hi DevOps Team,

We're experiencing a critical server outage affecting our production environment.

Impact: All users unable to access the platform
Started: 2:30 PM EST

Please join the emergency call immediately: +1-555-123-4567

This is our highest priority.

Thanks,
Site Reliability Team""",
            "sender": "alerts@company.com"
        },
        {
            "subject": "Meeting Invitation: Q4 Planning Session",
            "body": """Hello team,

You're invited to our Q4 planning session.

When: Friday, December 20, 2024 at 2:00 PM - 4:00 PM EST
Where: Conference Room A

Please confirm your attendance by December 18th.

Best,
Sarah Johnson""",
            "sender": "sarah.johnson@company.com"
        }
    ]
    
    # Process each email and display results
    print("🚀 Email Processing Demo")
    print("=" * 50)
    
    for i, email in enumerate(sample_emails):
        print(f"\n📧 EMAIL {i+1}: {email['subject'][:50]}...")
        
        # Process the email
        result = processor(
            email_subject=email["subject"],
            email_body=email["body"],
            sender=email["sender"]
        )
        
        # Display key results
        print(f"   📊 Type: {result.email_type}")
        print(f"   🚨 Urgency: {result.urgency}")
        print(f"   📝 Summary: {result.summary}")
        
        if result.financial_amount:
            print(f"   💰 Amount: ${result.financial_amount:,.2f}")
        
        if result.action_required:
            print(f"   ✅ Action Required: Yes")
            if result.deadline:
                print(f"   ⏰ Deadline: {result.deadline}")
        else:
            print(f"   ✅ Action Required: No")

# Run the demo
if __name__ == "__main__":
    run_email_processing_demo()
```

## Expected Output
```
🚀 Email Processing Demo
==================================================

📧 EMAIL 1: Order Confirmation #12345 - Your MacBook Pro is on...
   📊 Type: order_confirmation
   🚨 Urgency: low
   📝 Summary: The email confirms John Smith's order #12345 for a MacBook Pro 14-inch in Space Gray, totaling $2,399.00, with an estimated delivery date of December 15, 2024. It includes a tracking number and contact information for customer support.
   💰 Amount: $2,399.00
   ✅ Action Required: No

📧 EMAIL 2: URGENT: Server Outage - Immediate Action Required...
   📊 Type: other
   🚨 Urgency: critical
   📝 Summary: The Site Reliability Team has reported a critical server outage that began at 2:30 PM EST, preventing all users from accessing the platform. They have requested the DevOps Team to join an emergency call immediately to address the issue.
   ✅ Action Required: Yes
   ⏰ Deadline: Immediately

📧 EMAIL 3: Meeting Invitation: Q4 Planning Session...
   📊 Type: meeting_invitation
   🚨 Urgency: medium
   📝 Summary: Sarah Johnson has invited the team to a Q4 planning session on December 20, 2024, from 2:00 PM to 4:00 PM EST in Conference Room A. Attendees are asked to confirm their participation by December 18th.
   ✅ Action Required: Yes
   ⏰ Deadline: December 18th
```

## Next Steps

- **Add more email types** and refine classification (newsletter, promotional, etc.)
- **Add integration** with email providers (Gmail API, Outlook, IMAP)
- **Experiment with different LLMs** and optimization strategies
- **Add multilingual support** for international email processing
- **Optimization** for increasing the performance of your program

---


### Code Generation for Unfamiliar Libraries {#code-generation-for-unfamiliar-libraries}

*Source: `tutorials/sample_code_generation/index.md`*

# Automated Code Generation from Documentation with DSPy

This tutorial demonstrates how to use DSPy to automatically fetch documentation from URLs and generate working code examples for any library. The system can analyze documentation websites, extract key concepts, and produce tailored code examples.

## What You'll Build

A documentation-powered code generation system that:

- Fetches and parses documentation from multiple URLs
- Extracts API patterns, methods, and usage examples  
- Generates working code for specific use cases
- Provides explanations and best practices
- Works with any library's documentation

## Setup

```bash
pip install dspy requests beautifulsoup4 html2text
```

## Step 1: Documentation Fetching and Processing

```python
import dspy
import requests
from bs4 import BeautifulSoup
import html2text
from typing import List, Dict, Any
import json
from urllib.parse import urljoin, urlparse
import time

# Configure DSPy
lm = dspy.LM(model='openai/gpt-4o-mini')
dspy.configure(lm=lm)

class DocumentationFetcher:
    """Fetches and processes documentation from URLs."""
    
    def __init__(self, max_retries=3, delay=1):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.max_retries = max_retries
        self.delay = delay
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
    
    def fetch_url(self, url: str) -> dict[str, str]:
        """Fetch content from a single URL."""
        for attempt in range(self.max_retries):
            try:
                print(f"📡 Fetching: {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Convert to markdown for better LLM processing
                markdown_content = self.html_converter.handle(str(soup))
                
                return {
                    "url": url,
                    "title": soup.title.string if soup.title else "No title",
                    "content": markdown_content,
                    "success": True
                }
                
            except Exception as e:
                print(f"❌ Error fetching {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay)
                else:
                    return {
                        "url": url,
                        "title": "Failed to fetch",
                        "content": f"Error: {str(e)}",
                        "success": False
                    }
        
        return {"url": url, "title": "Failed", "content": "", "success": False}
    
    def fetch_documentation(self, urls: list[str]) -> list[dict[str, str]]:
        """Fetch documentation from multiple URLs."""
        results = []
        
        for url in urls:
            result = self.fetch_url(url)
            results.append(result)
            time.sleep(self.delay)  # Be respectful to servers
        
        return results

class LibraryAnalyzer(dspy.Signature):
    """Analyze library documentation to understand core concepts and patterns."""
    library_name: str = dspy.InputField(desc="Name of the library to analyze")
    documentation_content: str = dspy.InputField(desc="Combined documentation content")
    
    core_concepts: list[str] = dspy.OutputField(desc="Main concepts and components")
    common_patterns: list[str] = dspy.OutputField(desc="Common usage patterns")
    key_methods: list[str] = dspy.OutputField(desc="Important methods and functions")
    installation_info: str = dspy.OutputField(desc="Installation and setup information")
    code_examples: list[str] = dspy.OutputField(desc="Example code snippets found")

class CodeGenerator(dspy.Signature):
    """Generate code examples for specific use cases using the target library."""
    library_info: str = dspy.InputField(desc="Library concepts and patterns")
    use_case: str = dspy.InputField(desc="Specific use case to implement")
    requirements: str = dspy.InputField(desc="Additional requirements or constraints")
    
    code_example: str = dspy.OutputField(desc="Complete, working code example")
    explanation: str = dspy.OutputField(desc="Step-by-step explanation of the code")
    best_practices: list[str] = dspy.OutputField(desc="Best practices and tips")
    imports_needed: list[str] = dspy.OutputField(desc="Required imports and dependencies")

class DocumentationLearningAgent(dspy.Module):
    """Agent that learns from documentation URLs and generates code examples."""
    
    def __init__(self):
        super().__init__()
        self.fetcher = DocumentationFetcher()
        self.analyze_docs = dspy.ChainOfThought(LibraryAnalyzer)
        self.generate_code = dspy.ChainOfThought(CodeGenerator)
        self.refine_code = dspy.ChainOfThought(
            "code, feedback -> improved_code: str, changes_made: list[str]"
        )
    
    def learn_from_urls(self, library_name: str, doc_urls: list[str]) -> Dict:
        """Learn about a library from its documentation URLs."""
        
        print(f"📚 Learning about {library_name} from {len(doc_urls)} URLs...")
        
        # Fetch all documentation
        docs = self.fetcher.fetch_documentation(doc_urls)
        
        # Combine successful fetches
        combined_content = "\n\n---\n\n".join([
            f"URL: {doc['url']}\nTitle: {doc['title']}\n\n{doc['content']}"
            for doc in docs if doc['success']
        ])
        
        if not combined_content:
            raise ValueError("No documentation could be fetched successfully")
        
        # Analyze combined documentation
        analysis = self.analyze_docs(
            library_name=library_name,
            documentation_content=combined_content
        )
        
        return {
            "library": library_name,
            "source_urls": [doc['url'] for doc in docs if doc['success']],
            "core_concepts": analysis.core_concepts,
            "patterns": analysis.common_patterns,
            "methods": analysis.key_methods,
            "installation": analysis.installation_info,
            "examples": analysis.code_examples,
            "fetched_docs": docs
        }
    
    def generate_example(self, library_info: Dict, use_case: str, requirements: str = "") -> Dict:
        """Generate a code example for a specific use case."""
        
        # Format library information for the generator
        info_text = f"""
        Library: {library_info['library']}
        Core Concepts: {', '.join(library_info['core_concepts'])}
        Common Patterns: {', '.join(library_info['patterns'])}
        Key Methods: {', '.join(library_info['methods'])}
        Installation: {library_info['installation']}
        Example Code Snippets: {'; '.join(library_info['examples'][:3])}  # First 3 examples
        """
        
        code_result = self.generate_code(
            library_info=info_text,
            use_case=use_case,
            requirements=requirements
        )
        
        return {
            "code": code_result.code_example,
            "explanation": code_result.explanation,
            "best_practices": code_result.best_practices,
            "imports": code_result.imports_needed
        }

# Initialize the learning agent
agent = DocumentationLearningAgent()
```

## Step 2: Learning from Documentation URLs

```python
def learn_library_from_urls(library_name: str, documentation_urls: list[str]) -> Dict:
    """Learn about any library from its documentation URLs."""
    
    try:
        library_info = agent.learn_from_urls(library_name, documentation_urls)
        
        print(f"\n🔍 Library Analysis Results for {library_name}:")
        print(f"Sources: {len(library_info['source_urls'])} successful fetches")
        print(f"Core Concepts: {library_info['core_concepts']}")
        print(f"Common Patterns: {library_info['patterns']}")
        print(f"Key Methods: {library_info['methods']}")
        print(f"Installation: {library_info['installation']}")
        print(f"Found {len(library_info['examples'])} code examples")
        
        return library_info
        
    except Exception as e:
        print(f"❌ Error learning library: {e}")
        raise

# Example 1: Learn FastAPI from official documentation
fastapi_urls = [
    "https://fastapi.tiangolo.com/",
    "https://fastapi.tiangolo.com/tutorial/first-steps/",
    "https://fastapi.tiangolo.com/tutorial/path-params/",
    "https://fastapi.tiangolo.com/tutorial/query-params/"
]

print("🚀 Learning FastAPI from official documentation...")
fastapi_info = learn_library_from_urls("FastAPI", fastapi_urls)

# Example 2: Learn a different library (you can replace with any library)
streamlit_urls = [
    "https://docs.streamlit.io/",
    "https://docs.streamlit.io/get-started",
    "https://docs.streamlit.io/develop/api-reference"
]

print("\n\n📊 Learning Streamlit from official documentation...")
streamlit_info = learn_library_from_urls("Streamlit", streamlit_urls)
```

## Step 3: Generating Code Examples

```python
def generate_examples_for_library(library_info: Dict, library_name: str):
    """Generate code examples for any library based on its documentation."""
    
    # Define generic use cases that can apply to most libraries
    use_cases = [
        {
            "name": "Basic Setup and Hello World",
            "description": f"Create a minimal working example with {library_name}",
            "requirements": "Include installation, imports, and basic usage"
        },
        {
            "name": "Common Operations",
            "description": f"Demonstrate the most common {library_name} operations",
            "requirements": "Show typical workflow and best practices"
        },
        {
            "name": "Advanced Usage",
            "description": f"Create a more complex example showcasing {library_name} capabilities",
            "requirements": "Include error handling and optimization"
        }
    ]
    
    generated_examples = []
    
    print(f"\n🔧 Generating examples for {library_name}...")
    
    for use_case in use_cases:
        print(f"\n📝 {use_case['name']}")
        print(f"Description: {use_case['description']}")
        
        example = agent.generate_example(
            library_info=library_info,
            use_case=use_case['description'],
            requirements=use_case['requirements']
        )
        
        print("\n💻 Generated Code:")
        print("```python")
        print(example['code'])
        print("```")
        
        print("\n📦 Required Imports:")
        for imp in example['imports']:
            print(f"  • {imp}")
        
        print("\n📝 Explanation:")
        print(example['explanation'])
        
        print("\n✅ Best Practices:")
        for practice in example['best_practices']:
            print(f"  • {practice}")
        
        generated_examples.append({
            "use_case": use_case['name'],
            "code": example['code'],
            "imports": example['imports'],
            "explanation": example['explanation'],
            "best_practices": example['best_practices']
        })
        
        print("-" * 80)
    
    return generated_examples

# Generate examples for both libraries
print("🎯 Generating FastAPI Examples:")
fastapi_examples = generate_examples_for_library(fastapi_info, "FastAPI")

print("\n\n🎯 Generating Streamlit Examples:")
streamlit_examples = generate_examples_for_library(streamlit_info, "Streamlit")
```

## Step 4: Interactive Library Learning Function

```python
def learn_any_library(library_name: str, documentation_urls: list[str], use_cases: list[str] = None):
    """Learn any library from its documentation and generate examples."""
    
    if use_cases is None:
        use_cases = [
            "Basic setup and hello world example",
            "Common operations and workflows",
            "Advanced usage with best practices"
        ]
    
    print(f"🚀 Starting automated learning for {library_name}...")
    print(f"Documentation sources: {len(documentation_urls)} URLs")
    
    try:
        # Step 1: Learn from documentation
        library_info = agent.learn_from_urls(library_name, documentation_urls)
        
        # Step 2: Generate examples for each use case
        all_examples = []
        
        for i, use_case in enumerate(use_cases, 1):
            print(f"\n📝 Generating example {i}/{len(use_cases)}: {use_case}")
            
            example = agent.generate_example(
                library_info=library_info,
                use_case=use_case,
                requirements="Include error handling, comments, and follow best practices"
            )
            
            all_examples.append({
                "use_case": use_case,
                "code": example['code'],
                "imports": example['imports'],
                "explanation": example['explanation'],
                "best_practices": example['best_practices']
            })
        
        return {
            "library_info": library_info,
            "examples": all_examples
        }
    
    except Exception as e:
        print(f"❌ Error learning {library_name}: {e}")
        return None

def interactive_learning_session():
    """Interactive session for learning libraries with user input."""
    
    print("🎯 Welcome to the Interactive Library Learning System!")
    print("This system will help you learn any Python library from its documentation.\n")
    
    learned_libraries = {}
    
    while True:
        print("\n" + "="*60)
        print("🚀 LIBRARY LEARNING SESSION")
        print("="*60)
        
        # Get library name from user
        library_name = input("\n📚 Enter the library name you want to learn (or 'quit' to exit): ").strip()
        
        if library_name.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for using the Interactive Library Learning System!")
            break
        
        if not library_name:
            print("❌ Please enter a valid library name.")
            continue
        
        # Get documentation URLs
        print(f"\n🔗 Enter documentation URLs for {library_name} (one per line, empty line to finish):")
        urls = []
        while True:
            url = input("  URL: ").strip()
            if not url:
                break
            if not url.startswith(('http://', 'https://')):
                print("    ⚠️  Please enter a valid URL starting with http:// or https://")
                continue
            urls.append(url)
        
        if not urls:
            print("❌ No valid URLs provided. Skipping this library.")
            continue
        
        # Get custom use cases from user
        print(f"\n🎯 Define use cases for {library_name} (optional, press Enter for defaults):")
        print("   Default use cases will be: Basic setup, Common operations, Advanced usage")
        
        user_wants_custom = input("   Do you want to define custom use cases? (y/n): ").strip().lower()
        
        use_cases = None
        if user_wants_custom in ['y', 'yes']:
            print("   Enter your use cases (one per line, empty line to finish):")
            use_cases = []
            while True:
                use_case = input("     Use case: ").strip()
                if not use_case:
                    break
                use_cases.append(use_case)
            
            if not use_cases:
                print("   No custom use cases provided, using defaults.")
                use_cases = None
        
        # Learn the library
        print(f"\n🚀 Starting learning process for {library_name}...")
        result = learn_any_library(library_name, urls, use_cases)
        
        if result:
            learned_libraries[library_name] = result
            print(f"\n✅ Successfully learned {library_name}!")
            
            # Show summary
            print(f"\n📊 Learning Summary for {library_name}:")
            print(f"   • Core concepts: {len(result['library_info']['core_concepts'])} identified")
            print(f"   • Common patterns: {len(result['library_info']['patterns'])} found")
            print(f"   • Examples generated: {len(result['examples'])}")
            
            # Ask if user wants to see examples
            show_examples = input(f"\n👀 Do you want to see the generated examples for {library_name}? (y/n): ").strip().lower()
            
            if show_examples in ['y', 'yes']:
                for i, example in enumerate(result['examples'], 1):
                    print(f"\n{'─'*50}")
                    print(f"📝 Example {i}: {example['use_case']}")
                    print(f"{'─'*50}")
                    
                    print("\n💻 Generated Code:")
                    print("```python")
                    print(example['code'])
                    print("```")
                    
                    print(f"\n📦 Required Imports:")
                    for imp in example['imports']:
                        print(f"  • {imp}")
                    
                    print(f"\n📝 Explanation:")
                    print(example['explanation'])
                    
                    print(f"\n✅ Best Practices:")
                    for practice in example['best_practices']:
                        print(f"  • {practice}")
                    
                    # Ask if user wants to see the next example
                    if i < len(result['examples']):
                        continue_viewing = input(f"\nContinue to next example? (y/n): ").strip().lower()
                        if continue_viewing not in ['y', 'yes']:
                            break
            
            # Offer to save results
            save_results = input(f"\n💾 Save learning results for {library_name} to file? (y/n): ").strip().lower()
            
            if save_results in ['y', 'yes']:
                filename = input(f"   Enter filename (default: {library_name.lower()}_learning.json): ").strip()
                if not filename:
                    filename = f"{library_name.lower()}_learning.json"
                
                try:
                    import json
                    with open(filename, 'w') as f:
                        json.dump(result, f, indent=2, default=str)
                    print(f"   ✅ Results saved to {filename}")
                except Exception as e:
                    print(f"   ❌ Error saving file: {e}")
        
        else:
            print(f"❌ Failed to learn {library_name}")
        
        # Ask if user wants to learn another library
        print(f"\n📚 Libraries learned so far: {list(learned_libraries.keys())}")
        continue_learning = input("\n🔄 Do you want to learn another library? (y/n): ").strip().lower()
        
        if continue_learning not in ['y', 'yes']:
            break
    
    # Final summary
    if learned_libraries:
        print(f"\n🎉 Session Summary:")
        print(f"Successfully learned {len(learned_libraries)} libraries:")
        for lib_name, info in learned_libraries.items():
            print(f"  • {lib_name}: {len(info['examples'])} examples generated")
    
    return learned_libraries

# Example: Run interactive learning session
if __name__ == "__main__":
    # Run interactive session
    learned_libraries = interactive_learning_session()
```

## Example Output

When you run the interactive learning system, you'll see:

**Interactive Session Start:**
```
🎯 Welcome to the Interactive Library Learning System!
This system will help you learn any Python library from its documentation.

============================================================
🚀 LIBRARY LEARNING SESSION
============================================================

📚 Enter the library name you want to learn (or 'quit' to exit): FastAPI

🔗 Enter documentation URLs for FastAPI (one per line, empty line to finish):
  URL: https://fastapi.tiangolo.com/
  URL: https://fastapi.tiangolo.com/tutorial/first-steps/
  URL: https://fastapi.tiangolo.com/tutorial/path-params/
  URL: 

🎯 Define use cases for FastAPI (optional, press Enter for defaults):
   Default use cases will be: Basic setup, Common operations, Advanced usage
   Do you want to define custom use cases? (y/n): y
   Enter your use cases (one per line, empty line to finish):
     Use case: Create a REST API with authentication
     Use case: Build a file upload endpoint
     Use case: Add database integration with SQLAlchemy
     Use case: 
```

**Documentation Processing:**
```
🚀 Starting learning process for FastAPI...
🚀 Starting automated learning for FastAPI...
Documentation sources: 3 URLs
📡 Fetching: https://fastapi.tiangolo.com/ (attempt 1)
📡 Fetching: https://fastapi.tiangolo.com/tutorial/first-steps/ (attempt 1)
📡 Fetching: https://fastapi.tiangolo.com/tutorial/path-params/ (attempt 1)
📚 Learning about FastAPI from 3 URLs...

🔍 Library Analysis Results for FastAPI:
Sources: 3 successful fetches
Core Concepts: ['FastAPI app', 'path operations', 'dependencies', 'request/response models']
Common Patterns: ['app = FastAPI()', 'decorator-based routing', 'Pydantic models']
Key Methods: ['FastAPI()', '@app.get()', '@app.post()', 'uvicorn.run()']
Installation: pip install fastapi uvicorn
```

**Code Generation:**
```
📝 Generating example 1/3: Create a REST API with authentication

✅ Successfully learned FastAPI!

📊 Learning Summary for FastAPI:
   • Core concepts: 4 identified
   • Common patterns: 3 found
   • Examples generated: 3

👀 Do you want to see the generated examples for FastAPI? (y/n): y

──────────────────────────────────────────────────
📝 Example 1: Create a REST API with authentication
──────────────────────────────────────────────────

💻 Generated Code:
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from typing import Dict
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="Authenticated API", version="1.0.0")
security = HTTPBearer()

# Secret key for JWT (use environment variable in production)
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login")
async def login(username: str, password: str) -> dict[str, str]:
    # In production, verify against database
    if username == "admin" and password == "secret":
        token_data = {"sub": username, "exp": datetime.utcnow() + timedelta(hours=24)}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/protected")
async def protected_route(current_user: str = Depends(verify_token)) -> dict[str, str]:
    return {"message": f"Hello {current_user}! This is a protected route."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

📦 Required Imports:
  • pip install fastapi uvicorn python-jose[cryptography]
  • from fastapi import FastAPI, Depends, HTTPException, status
  • from fastapi.security import HTTPBearer
  • import jwt

📝 Explanation:
This example creates a FastAPI application with JWT-based authentication. It includes a login endpoint that returns a JWT token and a protected route that requires authentication...

✅ Best Practices:
  • Use environment variables for secret keys
  • Implement proper password hashing in production
  • Add token expiration and refresh logic
  • Include proper error handling

Continue to next example? (y/n): n

💾 Save learning results for FastAPI to file? (y/n): y
   Enter filename (default: fastapi_learning.json): 
   ✅ Results saved to fastapi_learning.json

📚 Libraries learned so far: ['FastAPI']

🔄 Do you want to learn another library? (y/n): n

🎉 Session Summary:
Successfully learned 1 libraries:
  • FastAPI: 3 examples generated
```


## Next Steps

- **GitHub Integration**: Learn from README files and example repositories
- **Video Tutorial Processing**: Extract information from video documentation
- **Community Examples**: Aggregate examples from Stack Overflow and forums
- **Version Comparison**: Track API changes across library versions
- **Testing Generation**: Automatically create unit tests for generated code
- **Page Crawling**: Automatically crawl documentation pages to actively understand the usage

This tutorial demonstrates how DSPy can automate the entire process of learning unfamiliar libraries from their documentation, making it valuable for rapid technology adoption and exploration.

---


### Building a Creative Text-Based AI Game {#building-a-creative-text-based-ai-game}

*Source: `tutorials/ai_text_game/index.md`*

# Building a Creative Text-Based AI Game with DSPy

This tutorial demonstrates how to create an interactive text-based adventure game using DSPy's modular programming approach. You'll build a dynamic game where AI handles narrative generation, character interactions, and adaptive gameplay.

## What You'll Build

An intelligent text-based adventure game featuring:

- Dynamic story generation and branching narratives
- AI-powered character interactions and dialogue
- Adaptive gameplay that responds to player choices
- Inventory and character progression systems
- Save/load game state functionality

## Setup

```bash
pip install dspy rich typer
```

## Step 1: Core Game Framework

```python
import dspy
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import random
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import typer

# Configure DSPy
lm = dspy.LM(model='openai/gpt-4o-mini')
dspy.configure(lm=lm)

console = Console()

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    INVENTORY = "inventory"
    CHARACTER = "character"
    GAME_OVER = "game_over"

@dataclass
class Player:
    name: str
    health: int = 100
    level: int = 1
    experience: int = 0
    inventory: list[str] = field(default_factory=list)
    skills: dict[str, int] = field(default_factory=lambda: {
        "strength": 10,
        "intelligence": 10,
        "charisma": 10,
        "stealth": 10
    })
    
    def add_item(self, item: str):
        self.inventory.append(item)
        console.print(f"[green]Added {item} to inventory![/green]")
    
    def remove_item(self, item: str) -> bool:
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def gain_experience(self, amount: int):
        self.experience += amount
        old_level = self.level
        self.level = 1 + (self.experience // 100)
        if self.level > old_level:
            console.print(f"[bold yellow]Level up! You are now level {self.level}![/bold yellow]")

@dataclass
class GameContext:
    current_location: str = "Village Square"
    story_progress: int = 0
    visited_locations: list[str] = field(default_factory=list)
    npcs_met: list[str] = field(default_factory=list)
    completed_quests: list[str] = field(default_factory=list)
    game_flags: dict[str, bool] = field(default_factory=dict)
    
    def add_flag(self, flag: str, value: bool = True):
        self.game_flags[flag] = value
    
    def has_flag(self, flag: str) -> bool:
        return self.game_flags.get(flag, False)

class GameEngine:
    def __init__(self):
        self.player = None
        self.context = GameContext()
        self.state = GameState.MENU
        self.running = True
        
    def save_game(self, filename: str = "savegame.json"):
        """Save current game state."""
        save_data = {
            "player": {
                "name": self.player.name,
                "health": self.player.health,
                "level": self.player.level,
                "experience": self.player.experience,
                "inventory": self.player.inventory,
                "skills": self.player.skills
            },
            "context": {
                "current_location": self.context.current_location,
                "story_progress": self.context.story_progress,
                "visited_locations": self.context.visited_locations,
                "npcs_met": self.context.npcs_met,
                "completed_quests": self.context.completed_quests,
                "game_flags": self.context.game_flags
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        console.print(f"[green]Game saved to {filename}![/green]")
    
    def load_game(self, filename: str = "savegame.json") -> bool:
        """Load game state from file."""
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            # Reconstruct player
            player_data = save_data["player"]
            self.player = Player(
                name=player_data["name"],
                health=player_data["health"],
                level=player_data["level"],
                experience=player_data["experience"],
                inventory=player_data["inventory"],
                skills=player_data["skills"]
            )
            
            # Reconstruct context
            context_data = save_data["context"]
            self.context = GameContext(
                current_location=context_data["current_location"],
                story_progress=context_data["story_progress"],
                visited_locations=context_data["visited_locations"],
                npcs_met=context_data["npcs_met"],
                completed_quests=context_data["completed_quests"],
                game_flags=context_data["game_flags"]
            )
            
            console.print(f"[green]Game loaded from {filename}![/green]")
            return True
            
        except FileNotFoundError:
            console.print(f"[red]Save file {filename} not found![/red]")
            return False
        except Exception as e:
            console.print(f"[red]Error loading game: {e}![/red]")
            return False

# Initialize game engine
game = GameEngine()
```

## Step 2: AI-Powered Story Generation

```python
class StoryGenerator(dspy.Signature):
    """Generate dynamic story content based on current game state."""
    location: str = dspy.InputField(desc="Current location")
    player_info: str = dspy.InputField(desc="Player information and stats")
    story_progress: int = dspy.InputField(desc="Current story progress level")
    recent_actions: str = dspy.InputField(desc="Player's recent actions")
    
    scene_description: str = dspy.OutputField(desc="Vivid description of current scene")
    available_actions: list[str] = dspy.OutputField(desc="List of possible player actions")
    npcs_present: list[str] = dspy.OutputField(desc="NPCs present in this location")
    items_available: list[str] = dspy.OutputField(desc="Items that can be found or interacted with")

class DialogueGenerator(dspy.Signature):
    """Generate NPC dialogue and responses."""
    npc_name: str = dspy.InputField(desc="Name and type of NPC")
    npc_personality: str = dspy.InputField(desc="NPC personality and background")
    player_input: str = dspy.InputField(desc="What the player said or did")
    context: str = dspy.InputField(desc="Current game context and history")
    
    npc_response: str = dspy.OutputField(desc="NPC's dialogue response")
    mood_change: str = dspy.OutputField(desc="How NPC's mood changed (positive/negative/neutral)")
    quest_offered: bool = dspy.OutputField(desc="Whether NPC offers a quest")
    information_revealed: str = dspy.OutputField(desc="Any important information shared")

class ActionResolver(dspy.Signature):
    """Resolve player actions and determine outcomes."""
    action: str = dspy.InputField(desc="Player's chosen action")
    player_stats: str = dspy.InputField(desc="Player's current stats and skills")
    context: str = dspy.InputField(desc="Current game context")
    difficulty: str = dspy.InputField(desc="Difficulty level of the action")
    
    success: bool = dspy.OutputField(desc="Whether the action succeeded")
    outcome_description: str = dspy.OutputField(desc="Description of what happened")
    stat_changes: dict[str, int] = dspy.OutputField(desc="Changes to player stats")
    items_gained: list[str] = dspy.OutputField(desc="Items gained from this action")
    experience_gained: int = dspy.OutputField(desc="Experience points gained")

class GameAI(dspy.Module):
    """Main AI module for game logic and narrative."""
    
    def __init__(self):
        super().__init__()
        self.story_gen = dspy.ChainOfThought(StoryGenerator)
        self.dialogue_gen = dspy.ChainOfThought(DialogueGenerator)
        self.action_resolver = dspy.ChainOfThought(ActionResolver)
    
    def generate_scene(self, player: Player, context: GameContext, recent_actions: str = "") -> Dict:
        """Generate current scene description and options."""
        
        player_info = f"Level {player.level} {player.name}, Health: {player.health}, Skills: {player.skills}"
        
        scene = self.story_gen(
            location=context.current_location,
            player_info=player_info,
            story_progress=context.story_progress,
            recent_actions=recent_actions
        )
        
        return {
            "description": scene.scene_description,
            "actions": scene.available_actions,
            "npcs": scene.npcs_present,
            "items": scene.items_available
        }
    
    def handle_dialogue(self, npc_name: str, player_input: str, context: GameContext) -> Dict:
        """Handle conversation with NPCs."""
        
        # Create NPC personality based on name and context
        personality_map = {
            "Village Elder": "Wise, knowledgeable, speaks in riddles, has ancient knowledge",
            "Merchant": "Greedy but fair, loves to bargain, knows about valuable items",
            "Guard": "Dutiful, suspicious of strangers, follows rules strictly",
            "Thief": "Sneaky, untrustworthy, has information about hidden things",
            "Wizard": "Mysterious, powerful, speaks about magic and ancient forces"
        }
        
        personality = personality_map.get(npc_name, "Friendly villager with local knowledge")
        game_context = f"Location: {context.current_location}, Story progress: {context.story_progress}"
        
        response = self.dialogue_gen(
            npc_name=npc_name,
            npc_personality=personality,
            player_input=player_input,
            context=game_context
        )
        
        return {
            "response": response.npc_response,
            "mood": response.mood_change,
            "quest": response.quest_offered,
            "info": response.information_revealed
        }
    
    def resolve_action(self, action: str, player: Player, context: GameContext) -> Dict:
        """Resolve player actions and determine outcomes."""
        
        player_stats = f"Level {player.level}, Health {player.health}, Skills: {player.skills}"
        game_context = f"Location: {context.current_location}, Progress: {context.story_progress}"
        
        # Determine difficulty based on action type
        difficulty = "medium"
        if any(word in action.lower() for word in ["fight", "battle", "attack"]):
            difficulty = "hard"
        elif any(word in action.lower() for word in ["look", "examine", "talk"]):
            difficulty = "easy"
        
        result = self.action_resolver(
            action=action,
            player_stats=player_stats,
            context=game_context,
            difficulty=difficulty
        )
        
        return {
            "success": result.success,
            "description": result.outcome_description,
            "stat_changes": result.stat_changes,
            "items": result.items_gained,
            "experience": result.experience_gained
        }

# Initialize AI
ai = GameAI()
```

## Step 3: Game Interface and Interaction

```python
def display_game_header():
    """Display the game header."""
    header = Text("🏰 MYSTIC REALM ADVENTURE 🏰", style="bold magenta")
    console.print(Panel(header, style="bright_blue"))

def display_player_status(player: Player):
    """Display player status panel."""
    status = f"""
[bold]Name:[/bold] {player.name}
[bold]Level:[/bold] {player.level} (XP: {player.experience})
[bold]Health:[/bold] {player.health}/100
[bold]Skills:[/bold]
  • Strength: {player.skills['strength']}
  • Intelligence: {player.skills['intelligence']}
  • Charisma: {player.skills['charisma']}
  • Stealth: {player.skills['stealth']}
[bold]Inventory:[/bold] {len(player.inventory)} items
    """
    console.print(Panel(status.strip(), title="Player Status", style="green"))

def display_location(context: GameContext, scene: Dict):
    """Display current location and scene."""
    location_panel = f"""
[bold yellow]{context.current_location}[/bold yellow]

{scene['description']}
    """
    
    if scene['npcs']:
        location_panel += f"\n\n[bold]NPCs present:[/bold] {', '.join(scene['npcs'])}"
    
    if scene['items']:
        location_panel += f"\n[bold]Items visible:[/bold] {', '.join(scene['items'])}"
    
    console.print(Panel(location_panel.strip(), title="Current Location", style="cyan"))

def display_actions(actions: list[str]):
    """Display available actions."""
    action_text = "\n".join([f"{i+1}. {action}" for i, action in enumerate(actions)])
    console.print(Panel(action_text, title="Available Actions", style="yellow"))

def get_player_choice(max_choices: int) -> int:
    """Get player's choice with input validation."""
    while True:
        try:
            choice = typer.prompt("Choose an action (number)")
            choice_num = int(choice)
            if 1 <= choice_num <= max_choices:
                return choice_num - 1
            else:
                console.print(f"[red]Please enter a number between 1 and {max_choices}[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")

def show_inventory(player: Player):
    """Display player inventory."""
    if not player.inventory:
        console.print(Panel("Your inventory is empty.", title="Inventory", style="red"))
    else:
        items = "\n".join([f"• {item}" for item in player.inventory])
        console.print(Panel(items, title="Inventory", style="green"))

def main_menu():
    """Display main menu and handle selection."""
    console.clear()
    display_game_header()
    
    menu_options = [
        "1. New Game",
        "2. Load Game", 
        "3. How to Play",
        "4. Exit"
    ]
    
    menu_text = "\n".join(menu_options)
    console.print(Panel(menu_text, title="Main Menu", style="bright_blue"))
    
    choice = typer.prompt("Select an option")
    return choice

def show_help():
    """Display help information."""
    help_text = """
[bold]How to Play:[/bold]

• This is a text-based adventure game powered by AI
• Make choices by selecting numbered options
• Talk to NPCs to learn about the world and get quests
• Explore different locations to find items and adventures
• Your choices affect the story and character development
• Use 'inventory' to check your items
• Use 'status' to see your character info
• Type 'save' to save your progress
• Type 'quit' to return to main menu

[bold]Tips:[/bold]
• Different skills affect your success in various actions
• NPCs remember your previous interactions
• Explore thoroughly - there are hidden secrets!
• Your reputation affects how NPCs treat you
    """
    console.print(Panel(help_text.strip(), title="Game Help", style="blue"))
    typer.prompt("Press Enter to continue")
```

## Step 4: Main Game Loop

```python
def create_new_character():
    """Create a new player character."""
    console.clear()
    display_game_header()
    
    name = typer.prompt("Enter your character's name")
    
    # Character creation with skill point allocation
    console.print("\n[bold]Character Creation[/bold]")
    console.print("You have 10 extra skill points to distribute among your skills.")
    console.print("Base skills start at 10 each.\n")
    
    skills = {"strength": 10, "intelligence": 10, "charisma": 10, "stealth": 10}
    points_remaining = 10
    
    for skill in skills.keys():
        if points_remaining > 0:
            console.print(f"Points remaining: {points_remaining}")
            while True:
                try:
                    points = int(typer.prompt(f"Points to add to {skill} (0-{points_remaining})"))
                    if 0 <= points <= points_remaining:
                        skills[skill] += points
                        points_remaining -= points
                        break
                    else:
                        console.print(f"[red]Enter a number between 0 and {points_remaining}[/red]")
                except ValueError:
                    console.print("[red]Please enter a valid number[/red]")
    
    player = Player(name=name, skills=skills)
    console.print(f"\n[green]Welcome to Mystic Realm, {name}![/green]")
    return player

def game_loop():
    """Main game loop."""
    recent_actions = ""
    
    while game.running and game.state == GameState.PLAYING:
        console.clear()
        display_game_header()
        
        # Generate current scene
        scene = ai.generate_scene(game.player, game.context, recent_actions)
        
        # Display game state
        display_player_status(game.player)
        display_location(game.context, scene)
        
        # Add standard actions
        all_actions = scene['actions'] + ["Check inventory", "Character status", "Save game", "Quit to menu"]
        display_actions(all_actions)
        
        # Get player choice
        choice_idx = get_player_choice(len(all_actions))
        chosen_action = all_actions[choice_idx]
        
        # Handle special commands
        if chosen_action == "Check inventory":
            show_inventory(game.player)
            typer.prompt("Press Enter to continue")
            continue
        elif chosen_action == "Character status":
            display_player_status(game.player)
            typer.prompt("Press Enter to continue")
            continue
        elif chosen_action == "Save game":
            game.save_game()
            typer.prompt("Press Enter to continue")
            continue
        elif chosen_action == "Quit to menu":
            game.state = GameState.MENU
            break
        
        # Handle game actions
        if chosen_action in scene['actions']:
            # Check if it's dialogue with an NPC
            npc_target = None
            for npc in scene['npcs']:
                if npc.lower() in chosen_action.lower():
                    npc_target = npc
                    break
            
            if npc_target:
                # Handle NPC interaction
                console.print(f"\n[bold]Talking to {npc_target}...[/bold]")
                dialogue = ai.handle_dialogue(npc_target, chosen_action, game.context)
                
                console.print(f"\n[italic]{npc_target}:[/italic] \"{dialogue['response']}\"")
                
                if dialogue['quest']:
                    console.print(f"[yellow]💼 Quest opportunity detected![/yellow]")
                
                if dialogue['info']:
                    console.print(f"[blue]ℹ️  {dialogue['info']}[/blue]")
                    
                # Add NPC to met list
                if npc_target not in game.context.npcs_met:
                    game.context.npcs_met.append(npc_target)
                
                recent_actions = f"Talked to {npc_target}: {chosen_action}"
            else:
                # Handle general action
                result = ai.resolve_action(chosen_action, game.player, game.context)
                
                console.print(f"\n{result['description']}")
                
                # Apply results
                if result['success']:
                    console.print("[green]✅ Success![/green]")
                    
                    # Apply stat changes
                    for stat, change in result['stat_changes'].items():
                        if stat in game.player.skills:
                            game.player.skills[stat] += change
                            if change > 0:
                                console.print(f"[green]{stat.title()} increased by {change}![/green]")
                        elif stat == "health":
                            game.player.health = max(0, min(100, game.player.health + change))
                            if change > 0:
                                console.print(f"[green]Health restored by {change}![/green]")
                            elif change < 0:
                                console.print(f"[red]Health decreased by {abs(change)}![/red]")
                    
                    # Add items
                    for item in result['items']:
                        game.player.add_item(item)
                    
                    # Give experience
                    if result['experience'] > 0:
                        game.player.gain_experience(result['experience'])
                    
                    # Update story progress
                    game.context.story_progress += 1
                else:
                    console.print("[red]❌ The action didn't go as planned...[/red]")
                
                recent_actions = f"Attempted: {chosen_action}"
            
            # Check for game over conditions
            if game.player.health <= 0:
                console.print("\n[bold red]💀 You have died! Game Over![/bold red]")
                game.state = GameState.GAME_OVER
                break
            
            typer.prompt("\nPress Enter to continue")

def main():
    """Main game function."""
    while game.running:
        if game.state == GameState.MENU:
            choice = main_menu()
            
            if choice == "1":
                game.player = create_new_character()
                game.context = GameContext()
                game.state = GameState.PLAYING
                console.print("\n[italic]Your adventure begins...[/italic]")
                typer.prompt("Press Enter to start")
                
            elif choice == "2":
                if game.load_game():
                    game.state = GameState.PLAYING
                typer.prompt("Press Enter to continue")
                
            elif choice == "3":
                show_help()
                
            elif choice == "4":
                game.running = False
                console.print("[bold]Thanks for playing! Goodbye![/bold]")
            
        elif game.state == GameState.PLAYING:
            game_loop()
            
        elif game.state == GameState.GAME_OVER:
            console.print("\n[bold]Game Over[/bold]")
            restart = typer.confirm("Would you like to return to the main menu?")
            if restart:
                game.state = GameState.MENU
            else:
                game.running = False

if __name__ == "__main__":
    main()
```

## Example Gameplay

When you run the game, you'll experience:

**Character Creation:**
```
🏰 MYSTIC REALM ADVENTURE 🏰

Enter your character's name: Aria

Character Creation
You have 10 extra skill points to distribute among your skills.
Base skills start at 10 each.

Points remaining: 10
Points to add to strength (0-10): 2
Points to add to intelligence (0-8): 4
Points to add to charisma (0-4): 3
Points to add to stealth (0-1): 1

Welcome to Mystic Realm, Aria!
```

**Dynamic Scene Generation:**
```
┌──────────── Current Location ────────────┐
│ Village Square                           │
│                                          │
│ You stand in the bustling heart of       │
│ Willowbrook Village. The ancient stone   │
│ fountain bubbles cheerfully as merchants │
│ hawk their wares and children play. A    │
│ mysterious hooded figure lurks near the  │
│ shadows of the old oak tree.             │
│                                          │
│ NPCs present: Village Elder, Merchant    │
│ Items visible: Strange Medallion, Herbs  │
└──────────────────────────────────────────┘

┌────────── Available Actions ─────────────┐
│ 1. Approach the hooded figure            │
│ 2. Talk to the Village Elder             │
│ 3. Browse the merchant's wares           │
│ 4. Examine the strange medallion         │
│ 5. Gather herbs near the fountain        │
│ 6. Head to the forest path               │
└───────────────────────────────────────────┘
```

**AI-Generated Dialogue:**
```
Talking to Village Elder...

Village Elder: "Ah, young traveler, I sense a great destiny 
surrounds you like morning mist. The ancient prophecy speaks 
of one who would come bearing the mark of courage. Tell me, 
have you noticed anything... unusual in your travels?"

💼 Quest opportunity detected!
ℹ️ The Village Elder knows about an ancient prophecy that might involve you
```

## Next Steps

- **Combat System**: Add turn-based battles with strategy
- **Magic System**: Spellcasting with resource management
- **Multiplayer**: Network support for cooperative adventures
- **Quest System**: Complex multi-step missions with branching outcomes
- **World Building**: Procedurally generated locations and characters
- **Audio**: Add sound effects and background music

This tutorial demonstrates how DSPy's modular approach enables complex, interactive systems where AI handles creative content generation while maintaining consistent game logic and player agency.

---


# DSPy in Production {#dspy-in-production}

*Source: `production/index.md`*

# Using DSPy in Production

<div class="grid cards" style="text-align: left;" markdown>

- :material-earth:{ .lg .middle } __Real-World Use Cases__

    ---

    DSPy is deployed in production by many enterprises and startups. Explore real-world case studies.

    [:octicons-arrow-right-24: Use Cases](../community/use-cases.md)

- :material-magnify-expand:{ .lg .middle } __Monitoring & Observability__

    ---

    Monitor your DSPy programs using **MLflow Tracing**, based on OpenTelemetry.

    [:octicons-arrow-right-24: Set Up Observability](../tutorials/observability/index.md#tracing)

- :material-ab-testing: __Reproducibility__

    ---

    Log programs, metrics, configs, and environments for full reproducibility with DSPy's native MLflow integration.

    [:octicons-arrow-right-24: MLflow Integration](https://mlflow.org/docs/latest/llms/dspy/index.html)

- :material-rocket-launch: __Deployment__

    ---

    When it's time to productionize, deploy your application easily with DSPy's integration with MLflow Model Serving.

    [:octicons-arrow-right-24: Deployment Guide](../tutorials/deployment/index.md)

- :material-arrow-up-right-bold: __Scalability__

    ---

    DSPy is designed with thread-safety in mind and offers native asynchronous execution support for high-throughput environments.

    [:octicons-arrow-right-24: Async Program](../api/utils/asyncify.md)

- :material-alert-rhombus: __Guardrails & Controllability__

    ---

    DSPy's **Signatures**, **Modules**, and **Optimizers** help you control and guide LM outputs.

    [:octicons-arrow-right-24: Learn Signature](../learn/programming/signatures.md)

</div>

---


## Community Resources {#community-resources}

*Source: `community/community-resources.md`*

# Resources

This is the list of tutorials and blog posts on DSPy. If you would like to add your own tutorial, please make a PR.


## A Few Blogs & Videos on using DSPy


### Blogs

| **Name** | **Link** |
|---|---|
| **Why I bet on DSPy** | [Blog](https://blog.isaacbmiller.com/posts/dspy) |
| **Not Your Average Prompt Engineering** | [Blog](https://jina.ai/news/dspy-not-your-average-prompt-engineering/) |
| **Why I'm excited about DSPy** | [Blog](https://substack.stephen.so/p/why-im-excited-about-dspy) |
| **Achieving GPT-4 Performance at Lower Cost** | [Link](https://gradient.ai/blog/achieving-gpt-4-level-performance-at-lower-cost-using-dspy) |
| **Prompt engineering is a task best left to AI models** | [Link](https://www.theregister.com/2024/02/22/prompt_engineering_ai_models/) |
| **What makes DSPy a valuable framework for developing complex language model pipelines?** | [Link](https://medium.com/@sujathamudadla1213/what-makes-dspy-a-valuable-framework-for-developing-complex-language-model-pipelines-edfa5b4bcf9b) |
| **DSPy: A new framework to program your foundation models just by prompting** | [Link](https://www.linkedin.com/pulse/dspy-new-framework-program-your-foundation-models-just-prompting-lli4c/) |
| **Intro to DSPy: Goodbye Prompting, Hello Programming** | [Link](https://medium.com/towards-data-science/intro-to-dspy-goodbye-prompting-hello-programming-4ca1c6ce3eb9) |
| **DSPyGen: Revolutionizing AI** | [Link](https://www.linkedin.com/pulse/launch-alert-dspygen-20242252-revolutionizing-ai-sean-chatman--g9f1c/) |
| **Building an AI Assistant with DSPy** | [Link](https://www.linkedin.com/pulse/building-ai-assistant-dspy-valliappa-lakshmanan-vgnsc/) |
| **Building Self-improving Agents in Production with DSPy** | [Link](https://relevanceai.com/blog/building-self-improving-agentic-systems-in-production-with-dspy) |


### Videos
| **Name** | **Link** |
|---|---|
| **DSPy Explained! (60K views)** | [Link](https://www.youtube.com/watch?v=41EfOY0Ldkc) |
| **DSPy Intro from Sephora (25K views)** | [Link](https://www.youtube.com/watch?v=D2HurSldDkE) |
| **Structured Outputs with DSPy** | [Link](https://www.youtube.com/watch?v=tVw3CwrN5-8) |
| **DSPy and ColBERT - Weaviate Podcast** | [Link](https://www.youtube.com/watch?v=CDung1LnLbY) |
| **SBTB23 DSPy** | [Link](https://www.youtube.com/watch?v=Dt3H2ninoeY) |
| **Optimization with DSPy and LangChain** | [Link](https://www.youtube.com/watch?v=4EXOmWeqXRc) |
| **Automated Prompt Engineering + Visualization** | [Link](https://www.youtube.com/watch?v=eAZ2LtJ6D5k) |
| **Transforming LM Calls into Pipelines** | [Link](https://www.youtube.com/watch?v=NoaDWKHdkHg) |
| **NeurIPS Hacker Cup: DSPy for Code Gen** | [Link](https://www.youtube.com/watch?v=gpe-rtJN8z8) |
| **MIPRO and DSPy - Weaviate Podcast** | [Link](https://www.youtube.com/watch?v=skMH3DOV_UQ) |
| **Getting Started with RAG in DSPy** | [Link](https://www.youtube.com/watch?v=CEuUG4Umfxs) |
| **Adding Depth to DSPy Programs** | [Link](https://www.youtube.com/watch?v=0c7Ksd6BG88) |
| **Programming Foundation Models with DSPy** | [Link](https://www.youtube.com/watch?v=Y94tw4eDHW0) |
| **DSPy End-to-End: SF Meetup** | [Link](https://www.youtube.com/watch?v=Y81DoFmt-2U) |
| **Monitoring & Tracing DSPy with Langtrace** | [Link](https://langtrace.ai/blog/announcing-dspy-support-in-langtrace) |
| **Teaching chat models to solve chess puzzles using DSPy + Finetuning** | [Link](https://raw.sh/posts/chess_puzzles) |
| **Build Self-Improving AI Agents with DSPy (No Code)** | [Link](https://www.youtube.com/watch?v=UY8OsMlV21Y) |
| **DSPy 3.0 and DSPy at Databricks** | [Link](https://www.youtube.com/watch?v=grIuzesOwwU) |
| **Context Engineering with DSPy** | [Link](https://www.youtube.com/watch?v=1I9PoXzvWcs) |

### Slides

| **Name** | **Link** |
|---|---|
| **Context Engineering with DSPy** | [Link](https://docs.google.com/presentation/d/1ydssF387l1LsJ14z41_HUqsJwU77tKZJNGnAWPsw-1I/edit?usp=sharing) |


### Podcasts

Weaviate has a directory of 10 amazing notebooks and 6 podcasts!
Huge shoutout to them for the massive support ❤️. See the [Weaviate DSPy directory](https://weaviate.io/developers/weaviate/more-resources/dspy).


This list represents a curated selection of DSPy resources. We continuously add new content as it becomes available in the community.

Credit: Some of these resources were originally compiled in the [Awesome DSPy](https://github.com/ganarajpr/awesome-dspy/tree/master) repo.

---


## Use Cases {#use-cases}

*Source: `community/use-cases.md`*

# Use Cases

We often get questions like “How are people using DSPy in practice?”, both in production and for research. This list was created to collect a few pointers and to encourage others in the community to add their own work below.

This list is continuously growing. We regularly add new use cases and welcome community contributions. If you would like to add your product or research to this list, please submit a PR.

## A Few Company Use Cases

| **Name** | **Use Cases** |
|---|---|
| **[JetBlue](https://www.jetblue.com/)** | Multiple chatbot use cases. [Blog](https://www.databricks.com/blog/optimizing-databricks-llm-pipelines-dspy) |
| **[Replit](https://replit.com/)** | Synthesize diffs using code LLMs using a DSPy pipeline. [Blog](https://blog.replit.com/code-repair) |
| **[Databricks](https://www.databricks.com/)** | Research, products, and customer solutions around LM Judges, RAG, classification, and other applications. [Blog](https://www.databricks.com/blog/dspy-databricks), [Blog II](https://www.databricks.com/customers/ddi) |
| **[Sephora](https://www.sephora.com/)** | Undisclosed agent usecases; perspectives shared in [DAIS Session](https://www.youtube.com/watch?v=D2HurSldDkE). |
| **[Zoro UK](https://www.zoro.co.uk/)** | E-commerce applications around structured shopping. [Portkey Session](https://www.youtube.com/watch?v=_vGKSc1tekE) |
| **[VMware](https://www.vmware.com/)** | RAG and other prompt optimization applications. [Interview in The Register.](https://www.theregister.com/2024/02/22/prompt_engineering_ai_models/) [Business Insider.](https://www.businessinsider.com/chaptgpt-large-language-model-ai-prompt-engineering-automated-optimizer-2024-3) |
| **[Haize Labs](https://www.haizelabs.com/)** | Automated red-teaming for LLMs. [Blog](https://blog.haizelabs.com/posts/dspy/) |
| **[Plastic Labs](https://www.plasticlabs.ai/)** | R&D pipelines for Honcho. [Blog](https://blog.plasticlabs.ai/blog/User-State-is-State-of-the-Art) |
| **[PingCAP](https://pingcap.com/)** | Building a knowledge graph. [Article](https://www.pingcap.com/article/building-a-graphrag-from-wikipedia-page-using-dspy-openai-and-tidb-vector-database/) |
| **[Salomatic](https://langtrace.ai/blog/case-study-how-salomatic-used-langtrace-to-build-a-reliable-medical-report-generation-system)** | Enriching medical reports using DSPy. [Blog](https://langtrace.ai/blog/case-study-how-salomatic-used-langtrace-to-build-a-reliable-medical-report-generation-system) |
| **[Truelaw](https://www.youtube.com/watch?v=O0F3RAWZNfM)** | How Truelaw builds bespoke LLM pipelines for law firms using DSPy. [Podcast](https://www.youtube.com/watch?v=O0F3RAWZNfM) |
| **[STChealth](https://stchealth.com/)** | Using DSPy for entity resolution including human-readable rationale for decisions. |
| **[Moody's](https://www.moodys.com/)** | Leveraging DSPy to optimize RAG systems, LLM-as-a-Judge, and agentic systems for financial workflows. |
| **[Normal Computing](https://www.normalcomputing.com/)** | Translate specs from chip companies from English to intermediate formal languages |
| **[Procure.FYI](https://www.procure.fyi/)** | Process messy, publicly available technology spending and pricing data via DSPy. |
| **[RadiantLogic](https://www.radiantlogic.com/)** | AI Data Assistant. DSPy is used for the agent that routes the query, the context extraction module, the text-to-sql conversion engine, and the table summarization module. |
| **[Raia](https://raiahealth.com/)** | Using DSPy for AI-powered Personal Healthcare Agents. |
| **[Hyperlint](https://hyperlint.com)** | Uses DSPy to generate technical documentation. DSPy helps to fetch relevant information and synthesize that into tutorials. |
| **[Starops](https://staropshq.com/) & [Saya](https://heysaya.ai/)** | Building research documents given a user's corpus. Generate prompts to create more articles from example articles. |
| **[Tessel AI](https://tesselai.com/)** | Enhancing human-machine interaction with data use cases. |
| **[Dicer.ai](https://dicer.ai/)** | Uses DSPy for marketing AI to get the most from their paid ads. |
| **[Howie](https://howie.ai)** | Using DSPy to automate meeting scheduling through email. |
| **[Isoform.ai](https://isoform.ai)** | Building custom integrations using DSPy. |
| **[Trampoline AI](https://trampoline.ai)** | Uses DSPy to power their data-augmentation and LM pipelines. |
| **[Pretrain](https://pretrain.com)** | Uses DSPy to automatically optimize AI performance towards user-defined tasks based on uploaded examples. |
| **[Spindle AI](https://spindle.ai)** | Turns natural-language constrained optimization problems into solvable mathematical programs whose candidate solutions are scenarios. |
| **[Infinitus](https://www.infinitus.ai/product/ai-agents/)** | Leverages DSPy to build and optimize healthcare AI agents |

This list represents companies that have publicly shared their use cases or have provided permission to be included. It reflects a selection of the many industry applications of DSPy currently in production.


## A Few Papers Using DSPy

| **Name** | **Description** |
|---|---|
| **[STORM](https://arxiv.org/abs/2402.14207)** | Writing Wikipedia-like Articles From Scratch. |
| **[PATH](https://arxiv.org/abs/2406.11706)** | Prompts as Auto-Optimized Training Hyperparameters: Training Best-in-Class IR Models from Scratch with 10 Gold Labels |
| **[WangLab @ MEDIQA](https://arxiv.org/abs/2404.14544)** | UofT's winning system at MEDIQA, outperforms the next best system by 20 points |
| **[UMD's Suicide Detection System](https://arxiv.org/abs/2406.06608)** | Outperforms 20-hour expert human prompt engineering by 40% |
| **[IReRa](https://arxiv.org/abs/2401.12178)** | Infer-Retrieve-Rank: Extreme Classification with > 10,000 Labels |
| **[Unreasonably Effective Eccentric Prompts](https://arxiv.org/abs/2402.10949v2)** | General Prompt Optimization |
| **[Palimpzest](https://arxiv.org/abs/2405.14696)** | A Declarative System for Optimizing AI Workloads |
| **[AI Agents that Matter](https://arxiv.org/abs/2407.01502v1)** | Agent Efficiency Optimization |
| **[EDEN](https://arxiv.org/abs/2406.17982v1)** | Empathetic Dialogues for English Learning: Uses adaptive empathetic feedback to improve student grit |
| **[ECG-Chat](https://arxiv.org/pdf/2408.08849)** | Uses DSPy with GraphRAG for medical report generation |
| **[DSPy Assertions](https://arxiv.org/abs/2312.13382)** | Various applications of imposing hard and soft constraints on LM outputs |
| **[DSPy Guardrails](https://boxiyu.github.io/assets/pdf/DSPy_Guardrails.pdf)** | Reduce the attack success rate of CodeAttack, decreasing from 75% to 5% |
| **[Co-STORM](https://arxiv.org/pdf/2408.15232)** | Collaborative STORM: Generate Wikipedia-like articles through collaborative discourse among users and multiple LM agents |
| **[MedVAL](https://arxiv.org/abs/2507.03152)** | Expert-level validation of AI-generated medical text with scalable language models |
| **[Neural @ ArchEHR-QA 2025](https://aclanthology.org/2025.bionlp-share.13.pdf)** | Runner up method at 2025 BioNLP Shared Task Workshop

This list is regularly updated with new research publications using DSPy.

## A Few Repositories (or other OSS examples) using DSPy

| **Name** | **Description/Link** |
|---|---|
| **Stanford CS 224U Homework** | [Github](https://github.com/cgpotts/cs224u/blob/main/hw_openqa.ipynb) |
| **STORM Report Generation (10,000 GitHub stars)** | [Github](https://github.com/stanford-oval/storm) |
| **DSPy Redteaming** | [Github](https://github.com/haizelabs/dspy-redteam) |
| **DSPy Theory of Mind** |  [Github](https://github.com/plastic-labs/dspy-opentom) |
| **Indic cross-lingual Natural Language Inference** |  [Github](https://github.com/saifulhaq95/DSPy-Indic/blob/main/indicxlni.ipynb) |
| **Optimizing LM for Text2SQL using DSPy** | [Github](https://github.com/jjovalle99/DSPy-Text2SQL) |
| **DSPy PII Masking Demo by Eric Ness** | [Colab](https://colab.research.google.com/drive/1KZR1sGTp_RLWUJPAiK1FKPKI-Qn9neUm?usp=sharing) |
| **DSPy on BIG-Bench Hard Example** |  [Github](https://drchrislevy.github.io/posts/dspy/dspy.html) |
| **Building a chess playing agent using DSPy** |  [Github](https://medium.com/thoughts-on-machine-learning/building-a-chess-playing-agent-using-dspy-9b87c868f71e) |
| **Ittia Research Fact Checking** | [Github](https://github.com/ittia-research/check) |
| **Strategic Debate via Tree-of-Thought** | [Github](https://github.com/zbambergerNLP/strategic-debate-tot) |
| **Sanskrit to English Translation App**| [Github](https://github.com/ganarajpr/sanskrit-translator-dspy) |
| **DSPy for extracting features from PDFs on arXiv**| [Github](https://github.com/S1M0N38/dspy-arxiv) |
| **DSPygen: DSPy in Ruby on Rails**| [Github](https://github.com/seanchatmangpt/dspygen) |
| **DSPy Inspector**| [Github](https://github.com/Neoxelox/dspy-inspector) |
| **DSPy with FastAPI**| [Github](https://github.com/diicellman/dspy-rag-fastapi) |
| **DSPy for Indian Languages**| [Github](https://github.com/saifulhaq95/DSPy-Indic) |
| **Hurricane: Blog Posts with Generative Feedback Loops!**| [Github](https://github.com/weaviate-tutorials/Hurricane) |
| **RAG example using DSPy, Gradio, FastAPI, and Ollama**| [Github](https://github.com/diicellman/dspy-gradio-rag) |
| **Synthetic Data Generation**| [Github](https://colab.research.google.com/drive/1CweVOu0qhTC0yOfW5QkLDRIKuAuWJKEr?usp=sharing) |
| **Self Discover**| [Github](https://colab.research.google.com/drive/1GkAQKmw1XQgg5UNzzy8OncRe79V6pADB?usp=sharing) |
| **MedVAL**| [Github](https://github.com/StanfordMIMI/MedVAL) |

This list showcases some of the open-source projects and repositories using DSPy, with many more examples available in the community.

## A Few Providers, Integrations, and related Blog Releases

| **Name** | **Link** |
|---|---|
| **Databricks** | [Link](https://www.databricks.com/blog/dspy-databricks) |
| **Zenbase** | [Link](https://zenbase.ai/) |
| **LangWatch** | [Link](https://langwatch.ai/blog/introducing-dspy-visualizer) |
| **Gradient** | [Link](https://gradient.ai/blog/achieving-gpt-4-level-performance-at-lower-cost-using-dspy) |
| **Snowflake** | [Link](https://medium.com/snowflake/dspy-snowflake-140d6d947d73) |
| **Langchain** | [Link](https://python.langchain.com/v0.2/docs/integrations/providers/dspy/) |
| **Weaviate** | [Link](https://weaviate.io/blog/dspy-optimizers) |
| **Qdrant** | [Link](https://qdrant.tech/documentation/frameworks/dspy/) |
| **Weights & Biases Weave** | [Link](https://weave-docs.wandb.ai/guides/integrations/dspy/) |
| **Milvus** | [Link](https://milvus.io/docs/integrate_with_dspy.md) |
| **Neo4j** | [Link](https://neo4j.com/labs/genai-ecosystem/dspy/) |
| **Lightning AI** | [Link](https://lightning.ai/lightning-ai/studios/dspy-programming-with-foundation-models) |
| **Haystack** | [Link](https://towardsdatascience.com/automating-prompt-engineering-with-dspy-and-haystack-926a637a3f43) |
| **Arize** | [Link](https://docs.arize.com/phoenix/tracing/integrations-tracing/dspy) |
| **LlamaIndex** | [Link](https://github.com/stanfordnlp/dspy/blob/main/examples/llamaindex/dspy_llamaindex_rag.ipynb) |
| **Langtrace** | [Link](https://docs.langtrace.ai/supported-integrations/llm-frameworks/dspy) |
| **Langfuse** | [Link](https://langfuse.com/docs/integrations/dspy) |
| **OpenLIT** | [Link](https://docs.openlit.io/latest/integrations/dspy) |
| **Relevance AI** | [Link](https://relevanceai.com/blog/dspy-programming---not-prompting---language-models) |

Credit: Some of these resources were originally compiled in the [Awesome DSPy](https://github.com/ganarajpr/awesome-dspy/tree/master) repo.

---


## Community Ports {#community-ports}

*Source: `community/community-ports.md`*

# Community Ports

DSPy has inspired implementations across many programming languages. These community-maintained ports bring DSPy's programming paradigm to different ecosystems.

If you have created a DSPy port in another language, please submit a PR to add it here!

## Language Implementations

| **Language** | **Project** | **Stars** | **Description** |
|---|---|---|---|
| **Clojure** | [DSCloj](https://github.com/unravel-team/DSCloj) | ![GitHub stars](https://img.shields.io/github/stars/unravel-team/DSCloj?style=flat) | Inspired by DSPy, adapts concepts to Clojure |
| **Elixir** | [dspy.ex](https://github.com/arthurcolle/dspy.ex) | ![GitHub stars](https://img.shields.io/github/stars/arthurcolle/dspy.ex?style=flat) | Inspired by DSPy, adapts for Elixir |
| **Go** | [dspy-go](https://github.com/XiaoConstantine/dspy-go) | ![GitHub stars](https://img.shields.io/github/stars/XiaoConstantine/dspy-go?style=flat) | Native Go implementation |
| **.NET** | [DSpyNet](https://github.com/al322se/DSpyNet) | ![GitHub stars](https://img.shields.io/github/stars/al322se/DSpyNet?style=flat) | C# .NET port |
| **R** | [dsprrr](https://github.com/jameshwade/dsprrr) | ![GitHub stars](https://img.shields.io/github/stars/jameshwade/dsprrr?style=flat) | R implementation inspired by DSPy |
| **Ruby** | [dspy.rb](https://github.com/vicentereig/dspy.rb) | ![GitHub stars](https://img.shields.io/github/stars/vicentereig/dspy.rb?style=flat) | Ruby port |
| **Rust** | [DSRs](https://github.com/krypticmouse/DSRs) | ![GitHub stars](https://img.shields.io/github/stars/krypticmouse/DSRs?style=flat) | Ground-up Rust rewrite |
| **TypeScript** | [ax](https://github.com/ax-llm/ax) | ![GitHub stars](https://img.shields.io/github/stars/ax-llm/ax?style=flat) | Inspired by DSPy for TypeScript |
| **TypeScript** | [dspy.ts](https://github.com/ruvnet/dspy.ts) | ![GitHub stars](https://img.shields.io/github/stars/ruvnet/dspy.ts?style=flat) | Complete TypeScript implementation |

## Notes

These are community-maintained projects and are not officially supported by the DSPy team. Feature availability and API compatibility may vary.

---


## Contributing {#contributing}

*Source: `community/how-to-contribute.md`*

# Contributing

DSPy is an actively growing project and community, and we welcome your contributions and involvement! Please read the
[contributing guide](https://github.com/stanfordnlp/dspy/blob/main/CONTRIBUTING.md) for how to contribute to DSPy.

---


## FAQ {#faq}

*Source: `faqs.md`*

!!! warning "This page is outdated and may not be fully accurate in DSPy 2.5 and 2.6"


# FAQs

## Is DSPy right for me? DSPy vs. other frameworks

The **DSPy** philosophy and abstraction differ significantly from other libraries and frameworks, so it's usually straightforward to decide when **DSPy** is (or isn't) the right framework for your usecase. If you're a NLP/AI researcher (or a practitioner exploring new pipelines or new tasks), the answer is generally an invariable **yes**. If you're a practitioner doing other things, please read on.

**DSPy vs. thin wrappers for prompts (OpenAI API, MiniChain, basic templating)** In other words: _Why can't I just write my prompts directly as string templates?_ Well, for extremely simple settings, this _might_ work just fine. (If you're familiar with neural networks, this is like expressing a tiny two-layer NN as a Python for-loop. It kinda works.) However, when you need higher quality (or manageable cost), then you need to iteratively explore multi-stage decomposition, improved prompting, data bootstrapping, careful finetuning, retrieval augmentation, and/or using smaller (or cheaper, or local) models. The true expressive power of building with foundation models lies in the interactions between these pieces. But every time you change one piece, you likely break (or weaken) multiple other components. **DSPy** cleanly abstracts away (_and_ powerfully optimizes) the parts of these interactions that are external to your actual system design. It lets you focus on designing the module-level interactions: the _same program_ expressed in 10 or 20 lines of **DSPy** can easily be compiled into multi-stage instructions for `GPT-4`, detailed prompts for `Llama2-13b`, or finetunes for `T5-base`. Oh, and you wouldn't need to maintain long, brittle, model-specific strings at the core of your project anymore.

**DSPy vs. application development libraries like LangChain, LlamaIndex** LangChain and LlamaIndex target high-level application development; they offer _batteries-included_, pre-built application modules that plug in with your data or configuration. If you'd be happy to use a generic, off-the-shelf prompt for question answering over PDFs or standard text-to-SQL, you will find a rich ecosystem in these libraries. **DSPy** doesn't internally contain hand-crafted prompts that target specific applications. Instead, **DSPy** introduces a small set of much more powerful and general-purpose modules _that can learn to prompt (or finetune) your LM within your pipeline on your data_. when you change your data, make tweaks to your program's control flow, or change your target LM, the **DSPy compiler** can map your program into a new set of prompts (or finetunes) that are optimized specifically for this pipeline. Because of this, you may find that **DSPy** obtains the highest quality for your task, with the least effort, provided you're willing to implement (or extend) your own short program. In short, **DSPy** is for when you need a lightweight but automatically-optimizing programming model — not a library of predefined prompts and integrations. If you're familiar with neural networks: This is like the difference between PyTorch (i.e., representing **DSPy**) and HuggingFace Transformers (i.e., representing the higher-level libraries).

**DSPy vs. generation control libraries like Guidance, LMQL, RELM, Outlines** These are all exciting new libraries for controlling the individual completions of LMs, e.g., if you want to enforce JSON output schema or constrain sampling to a particular regular expression. This is very useful in many settings, but it's generally focused on low-level, structured control of a single LM call. It doesn't help ensure the JSON (or structured output) you get is going to be correct or useful for your task. In contrast, **DSPy** automatically optimizes the prompts in your programs to align them with various task needs, which may also include producing valid structured outputs. That said, we are considering allowing **Signatures** in **DSPy** to express regex-like constraints that are implemented by these libraries.

## Basic Usage

**How should I use DSPy for my task?** We wrote a [eight-step guide](learn/index.md) on this. In short, using DSPy is an iterative process. You first define your task and the metrics you want to maximize, and prepare a few example inputs — typically without labels (or only with labels for the final outputs, if your metric requires them). Then, you build your pipeline by selecting built-in layers (`modules`) to use, giving each layer a `signature` (input/output spec), and then calling your modules freely in your Python code. Lastly, you use a DSPy `optimizer` to compile your code into high-quality instructions, automatic few-shot examples, or updated LM weights for your LM.

**How do I convert my complex prompt into a DSPy pipeline?** See the same answer above.

**What do DSPy optimizers tune?** Or, _what does compiling actually do?_ Each optimizer is different, but they all seek to maximize a metric on your program by updating prompts or LM weights. Current DSPy `optimizers` can inspect your data, simulate traces through your program to generate good/bad examples of each step, propose or refine instructions for each step based on past results, finetune the weights of your LM on self-generated examples, or combine several of these to improve quality or cut cost. We'd love to merge new optimizers that explore a richer space: most manual steps you currently go through for prompt engineering, "synthetic data" generation, or self-improvement can probably generalized into a DSPy optimizer that acts on arbitrary LM programs.

Other FAQs. We welcome PRs to add formal answers to each of these here. You will find the answer in existing issues, tutorials, or the papers for all or most of these.

- **How do I get multiple outputs?**

You can specify multiple output fields. For the short-form signature, you can list multiple outputs as comma separated values, following the "->" indicator (e.g. "inputs -> output1, output2"). For the long-form signature, you can include multiple `dspy.OutputField`s.


- **How do I define my own metrics? Can metrics return a float?**

You can define metrics as simply Python functions that process model generations and evaluate them based on user-defined requirements. Metrics can compare existent data (e.g. gold labels) to model predictions or they can be used to assess various components of an output using validation feedback from LMs (e.g. LLMs-as-Judges). Metrics can return `bool`, `int`, and `float` types scores. Check out the official [Metrics docs](learn/evaluation/metrics.md) to learn more about defining custom metrics and advanced evaluations using AI feedback and/or DSPy programs.

- **How expensive or slow is compiling??**

To reflect compiling metrics, we highlight an experiment for reference, compiling a program using the [BootstrapFewShotWithRandomSearch](api/optimizers/BootstrapFewShotWithRandomSearch.md) optimizer on the `gpt-3.5-turbo-1106` model over 7 candidate programs and 10 threads. We report that compiling this program takes around 6 minutes with 3200 API calls, 2.7 million input tokens and 156,000 output tokens, reporting a total cost of $3 USD (at the current pricing of the OpenAI model).

Compiling DSPy `optimizers` naturally will incur additional LM calls, but we substantiate this overhead with minimalistic executions with the goal of maximizing performance. This invites avenues to enhance performance of smaller models by compiling DSPy programs with larger models to learn enhanced behavior during compile-time and propagate such behavior to the tested smaller model during inference-time.  


## Deployment or Reproducibility Concerns

- **How do I save a checkpoint of my compiled program?**

Here is an example of saving/loading a compiled module:

```python
cot_compiled = teleprompter.compile(CoT(), trainset=trainset, valset=devset)

#Saving
cot_compiled.save('compiled_cot_gsm8k.json')

#Loading:
cot = CoT()
cot.load('compiled_cot_gsm8k.json')
```

- **How do I export for deployment?**

Exporting DSPy programs is simply saving them as highlighted above!

- **How do I search my own data?**

Open source libraries such as [RAGautouille](https://github.com/bclavie/ragatouille) enable you to search for your own data through advanced retrieval models like ColBERT with tools to embed and index documents. Feel free to integrate such libraries to create searchable datasets while developing your DSPy programs!

- **How do I turn off the cache? How do I export the cache?**

From v2.5, you can turn off the cache by setting `cache` parameter in `dspy.LM` to `False`:

```python
dspy.LM('openai/gpt-4o-mini',  cache=False)
```

Your local cache will be saved to the global env directory `os.environ["DSP_CACHEDIR"]` or for notebooks `os.environ["DSP_NOTEBOOK_CACHEDIR"]`. You can usually set the cachedir to `os.path.join(repo_path, 'cache')` and export this cache from here:
```python
os.environ["DSP_NOTEBOOK_CACHEDIR"] = os.path.join(os.getcwd(), 'cache')
```

!!! warning "Important"
    `DSP_CACHEDIR` is responsible for old clients (including dspy.OpenAI, dspy.ColBERTv2, etc.) and `DSPY_CACHEDIR` is responsible for the new dspy.LM client.

    In the AWS lambda deployment, you should disable both DSP_\* and DSPY_\*.


## Advanced Usage

- **How do I parallelize?**
You can parallelize DSPy programs during both compilation and evaluation by specifying multiple thread settings in the respective DSPy `optimizers` or within the `dspy.Evaluate` utility function.

- **How do freeze a module?**

Modules can be frozen by setting their `._compiled` attribute to be True, indicating the module has gone through optimizer compilation and should not have its parameters adjusted. This is handled internally in optimizers such as `dspy.BootstrapFewShot` where the student program is ensured to be frozen before the teacher propagates the gathered few-shot demonstrations in the bootstrapping process. 

- **How do I use DSPy assertions?**

    a) **How to Add Assertions to Your Program**:
    - **Define Constraints**: Use `dspy.Assert` and/or `dspy.Suggest` to define constraints within your DSPy program. These are based on boolean validation checks for the outcomes you want to enforce, which can simply be Python functions to validate the model outputs.
    - **Integrating Assertions**: Keep your Assertion statements following a model generations (hint: following a module layer)

    b) **How to Activate the Assertions**:
    1. **Using `assert_transform_module`**:
        - Wrap your DSPy module with assertions using the `assert_transform_module` function, along with a `backtrack_handler`. This function transforms your program to include internal assertions backtracking and retry logic, which can be customized as well:
        `program_with_assertions = assert_transform_module(ProgramWithAssertions(), backtrack_handler)`
    2. **Activate Assertions**:
        - Directly call `activate_assertions` on your DSPy program with assertions: `program_with_assertions = ProgramWithAssertions().activate_assertions()`

    **Note**: To use Assertions properly, you must **activate** a DSPy program that includes `dspy.Assert` or `dspy.Suggest` statements from either of the methods above. 

## Errors

- **How do I deal with "context too long" errors?**

If you're dealing with "context too long" errors in DSPy, you're likely using DSPy optimizers to include demonstrations within your prompt, and this is exceeding your current context window. Try reducing these parameters (e.g. `max_bootstrapped_demos` and `max_labeled_demos`). Additionally, you can also reduce the number of retrieved passages/docs/embeddings to ensure your prompt is fitting within your model context length.

A more general fix is simply increasing the number of `max_tokens` specified to the LM request (e.g. `lm = dspy.OpenAI(model = ..., max_tokens = ...`).

## Set Verbose Level
DSPy utilizes the [logging library](https://docs.python.org/3/library/logging.html) to print logs. If you want to debug your DSPy code, set the logging level to DEBUG with the example code below.

```python
import logging
logging.getLogger("dspy").setLevel(logging.DEBUG)
```

Alternatively, if you want to reduce the amount of logs, set the logging level to WARNING or ERROR.

```python
import logging
logging.getLogger("dspy").setLevel(logging.WARNING)
```

---


## Cheatsheet {#cheatsheet}

*Source: `cheatsheet.md`*

# DSPy Cheatsheet

This page will contain snippets for frequent usage patterns.

## DSPy Programs

### Forcing fresh LM outputs

DSPy caches LM calls. Provide a unique ``rollout_id`` and set a non-zero
``temperature`` (e.g., 1.0) to bypass an existing cache entry while still caching
the new result:

```python
predict = dspy.Predict("question -> answer")
predict(question="1+1", config={"rollout_id": 1, "temperature": 1.0})
```

### dspy.Signature

```python
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""

    question: str = dspy.InputField()
    answer: str = dspy.OutputField(desc="often between 1 and 5 words")
```

### dspy.ChainOfThought

```python
generate_answer = dspy.ChainOfThought(BasicQA)

# Call the predictor on a particular input alongside a hint.
question='What is the color of the sky?'
pred = generate_answer(question=question)
```

### dspy.ProgramOfThought

```python
pot = dspy.ProgramOfThought(BasicQA)

question = 'Sarah has 5 apples. She buys 7 more apples from the store. How many apples does Sarah have now?'
result = pot(question=question)

print(f"Question: {question}")
print(f"Final Predicted Answer (after ProgramOfThought process): {result.answer}")
```

### dspy.ReAct

```python
react_module = dspy.ReAct(BasicQA)

question = 'Sarah has 5 apples. She buys 7 more apples from the store. How many apples does Sarah have now?'
result = react_module(question=question)

print(f"Question: {question}")
print(f"Final Predicted Answer (after ReAct process): {result.answer}")
```

### dspy.Retrieve

```python
colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
dspy.configure(rm=colbertv2_wiki17_abstracts)

#Define Retrieve Module
retriever = dspy.Retrieve(k=3)

query='When was the first FIFA World Cup held?'

# Call the retriever on a particular query.
topK_passages = retriever(query).passages

for idx, passage in enumerate(topK_passages):
    print(f'{idx+1}]', passage, '\n')
```

### dspy.CodeAct

```python
from dspy import CodeAct

def factorial(n):
    """Calculate factorial of n"""
    if n == 1:
        return 1
    return n * factorial(n-1)

act = CodeAct("n->factorial", tools=[factorial])
result = act(n=5)
result # Returns 120
```

### dspy.Parallel

```python
import dspy

parallel = dspy.Parallel(num_threads=2)
predict = dspy.Predict("question -> answer")
result = parallel(
    [
        (predict, dspy.Example(question="1+1").with_inputs("question")),
        (predict, dspy.Example(question="2+2").with_inputs("question"))
    ]
)
result
```

## DSPy Metrics

### Function as Metric

To create a custom metric you can create a function that returns either a number or a boolean value:

```python
def parse_integer_answer(answer, only_first_line=True):
    try:
        if only_first_line:
            answer = answer.strip().split('\n')[0]

        # find the last token that has a number in it
        answer = [token for token in answer.split() if any(c.isdigit() for c in token)][-1]
        answer = answer.split('.')[0]
        answer = ''.join([c for c in answer if c.isdigit()])
        answer = int(answer)

    except (ValueError, IndexError):
        # print(answer)
        answer = 0

    return answer

# Metric Function
def gsm8k_metric(gold, pred, trace=None) -> int:
    return int(parse_integer_answer(str(gold.answer))) == int(parse_integer_answer(str(pred.answer)))
```

### LLM as Judge

```python
class FactJudge(dspy.Signature):
    """Judge if the answer is factually correct based on the context."""

    context = dspy.InputField(desc="Context for the prediction")
    question = dspy.InputField(desc="Question to be answered")
    answer = dspy.InputField(desc="Answer for the question")
    factually_correct: bool = dspy.OutputField(desc="Is the answer factually correct based on the context?")

judge = dspy.ChainOfThought(FactJudge)

def factuality_metric(example, pred):
    factual = judge(context=example.context, question=example.question, answer=pred.answer)
    return factual.factually_correct
```

## DSPy Evaluation

```python
from dspy.evaluate import Evaluate

evaluate_program = Evaluate(devset=devset, metric=your_defined_metric, num_threads=NUM_THREADS, display_progress=True, display_table=num_rows_to_display)

evaluate_program(your_dspy_program)
```

## DSPy Optimizers

### LabeledFewShot

```python
from dspy.teleprompt import LabeledFewShot

labeled_fewshot_optimizer = LabeledFewShot(k=8)
your_dspy_program_compiled = labeled_fewshot_optimizer.compile(student = your_dspy_program, trainset=trainset)
```

### BootstrapFewShot

```python
from dspy.teleprompt import BootstrapFewShot

fewshot_optimizer = BootstrapFewShot(metric=your_defined_metric, max_bootstrapped_demos=4, max_labeled_demos=16, max_rounds=1, max_errors=10)

your_dspy_program_compiled = fewshot_optimizer.compile(student = your_dspy_program, trainset=trainset)
```

#### Using another LM for compilation, specifying in teacher_settings

```python
from dspy.teleprompt import BootstrapFewShot

fewshot_optimizer = BootstrapFewShot(metric=your_defined_metric, max_bootstrapped_demos=4, max_labeled_demos=16, max_rounds=1, max_errors=10, teacher_settings=dict(lm=gpt4))

your_dspy_program_compiled = fewshot_optimizer.compile(student = your_dspy_program, trainset=trainset)
```

#### Compiling a compiled program - bootstrapping a bootstrapped program

```python
your_dspy_program_compiledx2 = teleprompter.compile(
    your_dspy_program,
    teacher=your_dspy_program_compiled,
    trainset=trainset,
)
```

#### Saving/loading a compiled program

```python
save_path = './v1.json'
your_dspy_program_compiledx2.save(save_path)
```

```python
loaded_program = YourProgramClass()
loaded_program.load(path=save_path)
```

### BootstrapFewShotWithRandomSearch

Detailed documentation on BootstrapFewShotWithRandomSearch can be found [here](api/optimizers/BootstrapFewShot.md).

```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

fewshot_optimizer = BootstrapFewShotWithRandomSearch(metric=your_defined_metric, max_bootstrapped_demos=2, num_candidate_programs=8, num_threads=NUM_THREADS)

your_dspy_program_compiled = fewshot_optimizer.compile(student = your_dspy_program, trainset=trainset, valset=devset)

```

Other custom configurations are similar to customizing the `BootstrapFewShot` optimizer.

### Ensemble

```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch
from dspy.teleprompt.ensemble import Ensemble

fewshot_optimizer = BootstrapFewShotWithRandomSearch(metric=your_defined_metric, max_bootstrapped_demos=2, num_candidate_programs=8, num_threads=NUM_THREADS)
your_dspy_program_compiled = fewshot_optimizer.compile(student = your_dspy_program, trainset=trainset, valset=devset)

ensemble_optimizer = Ensemble(reduce_fn=dspy.majority)
programs = [x[-1] for x in your_dspy_program_compiled.candidate_programs]
your_dspy_program_compiled_ensemble = ensemble_optimizer.compile(programs[:3])
```

### BootstrapFinetune

```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch, BootstrapFinetune

#Compile program on current dspy.settings.lm
fewshot_optimizer = BootstrapFewShotWithRandomSearch(metric=your_defined_metric, max_bootstrapped_demos=2, num_threads=NUM_THREADS)
your_dspy_program_compiled = tp.compile(your_dspy_program, trainset=trainset[:some_num], valset=trainset[some_num:])

#Configure model to finetune
config = dict(target=model_to_finetune, epochs=2, bf16=True, bsize=6, accumsteps=2, lr=5e-5)

#Compile program on BootstrapFinetune
finetune_optimizer = BootstrapFinetune(metric=your_defined_metric)
finetune_program = finetune_optimizer.compile(your_dspy_program, trainset=some_new_dataset_for_finetuning_model, **config)

finetune_program = your_dspy_program

#Load program and activate model's parameters in program before evaluation
ckpt_path = "saved_checkpoint_path_from_finetuning"
LM = dspy.HFModel(checkpoint=ckpt_path, model=model_to_finetune)

for p in finetune_program.predictors():
    p.lm = LM
    p.activated = False
```

### COPRO

Detailed documentation on COPRO can be found [here](api/optimizers/COPRO.md).

```python
from dspy.teleprompt import COPRO

eval_kwargs = dict(num_threads=16, display_progress=True, display_table=0)

copro_teleprompter = COPRO(prompt_model=model_to_generate_prompts, metric=your_defined_metric, breadth=num_new_prompts_generated, depth=times_to_generate_prompts, init_temperature=prompt_generation_temperature, verbose=False)

compiled_program_optimized_signature = copro_teleprompter.compile(your_dspy_program, trainset=trainset, eval_kwargs=eval_kwargs)
```

### MIPROv2

Note: detailed documentation can be found [here](api/optimizers/MIPROv2.md). `MIPROv2` is the latest extension of `MIPRO` which includes updates such as (1) improvements to instruction proposal and (2) more efficient search with minibatching.

#### Optimizing with MIPROv2

This shows how to perform an easy out-of-the box run with `auto=light`, which configures many hyperparameters for you and performs a light optimization run. You can alternatively set `auto=medium` or `auto=heavy` to perform longer optimization runs. The more detailed `MIPROv2` documentation [here](api/optimizers/MIPROv2.md) also provides more information about how to set hyperparameters by hand.

```python
# Import the optimizer
from dspy.teleprompt import MIPROv2

# Initialize optimizer
teleprompter = MIPROv2(
    metric=gsm8k_metric,
    auto="light", # Can choose between light, medium, and heavy optimization runs
)

# Optimize program
print(f"Optimizing program with MIPRO...")
optimized_program = teleprompter.compile(
    program.deepcopy(),
    trainset=trainset,
    max_bootstrapped_demos=3,
    max_labeled_demos=4,
)

# Save optimize program for future use
optimized_program.save(f"mipro_optimized")

# Evaluate optimized program
print(f"Evaluate optimized program...")
evaluate(optimized_program, devset=devset[:])
```

#### Optimizing instructions only with MIPROv2 (0-Shot)

```python
# Import the optimizer
from dspy.teleprompt import MIPROv2

# Initialize optimizer
teleprompter = MIPROv2(
    metric=gsm8k_metric,
    auto="light", # Can choose between light, medium, and heavy optimization runs
)

# Optimize program
print(f"Optimizing program with MIPRO...")
optimized_program = teleprompter.compile(
    program.deepcopy(),
    trainset=trainset,
    max_bootstrapped_demos=0,
    max_labeled_demos=0,
)

# Save optimize program for future use
optimized_program.save(f"mipro_optimized")

# Evaluate optimized program
print(f"Evaluate optimized program...")
evaluate(optimized_program, devset=devset[:])
```

### KNNFewShot

```python
from sentence_transformers import SentenceTransformer
from dspy import Embedder
from dspy.teleprompt import KNNFewShot
from dspy import ChainOfThought

knn_optimizer = KNNFewShot(k=3, trainset=trainset, vectorizer=Embedder(SentenceTransformer("all-MiniLM-L6-v2").encode))

qa_compiled = knn_optimizer.compile(student=ChainOfThought("question -> answer"))
```

### BootstrapFewShotWithOptuna

```python
from dspy.teleprompt import BootstrapFewShotWithOptuna

fewshot_optuna_optimizer = BootstrapFewShotWithOptuna(metric=your_defined_metric, max_bootstrapped_demos=2, num_candidate_programs=8, num_threads=NUM_THREADS)

your_dspy_program_compiled = fewshot_optuna_optimizer.compile(student=your_dspy_program, trainset=trainset, valset=devset)
```

Other custom configurations are similar to customizing the `dspy.BootstrapFewShot` optimizer.


### SIMBA

SIMBA, which stands for Stochastic Introspective Mini-Batch Ascent, is a prompt optimizer that accepts arbitrary DSPy programs and proceeds in a sequence of mini-batches seeking to make incremental improvements to the prompt instructions or few-shot examples.

```python
from dspy.teleprompt import SIMBA

simba = SIMBA(metric=your_defined_metric, max_steps=12, max_demos=10)

optimized_program = simba.compile(student=your_dspy_program, trainset=trainset)
```


## DSPy Tools and Utilities

### dspy.Tool

```python
import dspy

def search_web(query: str) -> str:
    """Search the web for information"""
    return f"Search results for: {query}"

tool = dspy.Tool(search_web)
result = tool(query="Python programming")
```

### dspy.streamify

```python
import dspy
import asyncio

predict = dspy.Predict("question->answer")

stream_predict = dspy.streamify(
    predict,
    stream_listeners=[dspy.streaming.StreamListener(signature_field_name="answer")],
)

async def read_output_stream():
    output_stream = stream_predict(question="Why did a chicken cross the kitchen?")

    async for chunk in output_stream:
        print(chunk)

asyncio.run(read_output_stream())
```


### dspy.asyncify

```python
import dspy

dspy_program = dspy.ChainOfThought("question -> answer")
dspy_program = dspy.asyncify(dspy_program)

asyncio.run(dspy_program(question="What is DSPy"))
```


### Track Usage

```python
import dspy
dspy.configure(track_usage=True)

result = dspy.ChainOfThought(BasicQA)(question="What is 2+2?")
print(f"Token usage: {result.get_lm_usage()}")
```

### dspy.configure_cache

```python
import dspy

# Configure cache settings
dspy.configure_cache(
    enable_disk_cache=False,
    enable_memory_cache=False,
)
```

## DSPy `Refine` and `BestofN`

>`dspy.Suggest` and `dspy.Assert` are replaced by `dspy.Refine` and `dspy.BestofN` in DSPy 2.6.

### BestofN

Runs a module up to `N` times with different rollout IDs (bypassing cache) and returns the best prediction, as defined by the `reward_fn`, or the first prediction that passes the `threshold`.

```python
import dspy

qa = dspy.ChainOfThought("question -> answer")
def one_word_answer(args, pred):
    return 1.0 if len(pred.answer) == 1 else 0.0
best_of_3 = dspy.BestOfN(module=qa, N=3, reward_fn=one_word_answer, threshold=1.0)
best_of_3(question="What is the capital of Belgium?").answer
# Brussels
```

### Refine

Refines a module by running it up to `N` times with different rollout IDs (bypassing cache) and returns the best prediction, as defined by the `reward_fn`, or the first prediction that passes the `threshold`. After each attempt (except the final one), `Refine` automatically generates detailed feedback about the module's performance and uses this feedback as hints for subsequent runs, creating an iterative refinement process.

```python
import dspy

qa = dspy.ChainOfThought("question -> answer")
def one_word_answer(args, pred):
    return 1.0 if len(pred.answer) == 1 else 0.0
best_of_3 = dspy.Refine(module=qa, N=3, reward_fn=one_word_answer, threshold=1.0)
best_of_3(question="What is the capital of Belgium?").answer
# Brussels
```

#### Error Handling

By default, `Refine` will try to run the module up to N times until the threshold is met. If the module encounters an error, it will keep going up to N failed attempts. You can change this behavior by setting `fail_count` to a smaller number than `N`.

```python
refine = dspy.Refine(module=qa, N=3, reward_fn=one_word_answer, threshold=1.0, fail_count=1)
...
refine(question="What is the capital of Belgium?")
# If we encounter just one failed attempt, the module will raise an error.
```

If you want to run the module up to N times without any error handling, you can set `fail_count` to `N`. This is the default behavior.

```python
refine = dspy.Refine(module=qa, N=3, reward_fn=one_word_answer, threshold=1.0, fail_count=3)
...
refine(question="What is the capital of Belgium?")
```

---


## API Reference {#api-reference}

*Source: `api/index.md`*

# API Reference

Welcome to the DSPy API reference documentation. This section provides detailed information about DSPy's classes, modules, and functions.

---


### Adapter {#adapter}

*Source: `api/adapters/Adapter.md`*

# dspy.Adapter

<!-- START_API_REF -->
::: dspy.Adapter
    handler: python
    options:
        members:
            - __call__
            - acall
            - format
            - format_assistant_message_content
            - format_conversation_history
            - format_demos
            - format_field_description
            - format_field_structure
            - format_system_message
            - format_task_description
            - format_user_message_content
            - parse
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### ChatAdapter {#chatadapter}

*Source: `api/adapters/ChatAdapter.md`*

# dspy.ChatAdapter

<!-- START_API_REF -->
::: dspy.ChatAdapter
    handler: python
    options:
        members:
            - __call__
            - acall
            - format
            - format_assistant_message_content
            - format_conversation_history
            - format_demos
            - format_field_description
            - format_field_structure
            - format_field_with_value
            - format_finetune_data
            - format_system_message
            - format_task_description
            - format_user_message_content
            - parse
            - user_message_output_requirements
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### JSONAdapter {#jsonadapter}

*Source: `api/adapters/JSONAdapter.md`*

# dspy.JSONAdapter

<!-- START_API_REF -->
::: dspy.JSONAdapter
    handler: python
    options:
        members:
            - __call__
            - acall
            - format
            - format_assistant_message_content
            - format_conversation_history
            - format_demos
            - format_field_description
            - format_field_structure
            - format_field_with_value
            - format_finetune_data
            - format_system_message
            - format_task_description
            - format_user_message_content
            - parse
            - user_message_output_requirements
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### TwoStepAdapter {#twostepadapter}

*Source: `api/adapters/TwoStepAdapter.md`*

# dspy.TwoStepAdapter

<!-- START_API_REF -->
::: dspy.TwoStepAdapter
    handler: python
    options:
        members:
            - __call__
            - acall
            - format
            - format_assistant_message_content
            - format_conversation_history
            - format_demos
            - format_field_description
            - format_field_structure
            - format_system_message
            - format_task_description
            - format_user_message_content
            - parse
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### CompleteAndGrounded {#completeandgrounded}

*Source: `api/evaluation/CompleteAndGrounded.md`*

# dspy.evaluate.CompleteAndGrounded

<!-- START_API_REF -->
::: dspy.evaluate.CompleteAndGrounded
    handler: python
    options:
        members:
            - __call__
            - acall
            - batch
            - deepcopy
            - dump_state
            - forward
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Evaluate {#evaluate}

*Source: `api/evaluation/Evaluate.md`*

# dspy.Evaluate

<!-- START_API_REF -->
::: dspy.Evaluate
    handler: python
    options:
        members:
            - __call__
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### EvaluationResult {#evaluationresult}

*Source: `api/evaluation/EvaluationResult.md`*

# dspy.evaluate.EvaluationResult

<!-- START_API_REF -->
::: dspy.evaluate.EvaluationResult
    handler: python
    options:
        members:
            - copy
            - from_completions
            - get
            - get_lm_usage
            - inputs
            - items
            - keys
            - labels
            - set_lm_usage
            - toDict
            - values
            - with_inputs
            - without
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### SemanticF1 {#semanticf1}

*Source: `api/evaluation/SemanticF1.md`*

# dspy.evaluate.SemanticF1

<!-- START_API_REF -->
::: dspy.evaluate.SemanticF1
    handler: python
    options:
        members:
            - __call__
            - acall
            - batch
            - deepcopy
            - dump_state
            - forward
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### answer_exact_match {#answerexactmatch}

*Source: `api/evaluation/answer_exact_match.md`*

# dspy.evaluate.answer_exact_match

<!-- START_API_REF -->
::: dspy.evaluate.answer_exact_match
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### answer_passage_match {#answerpassagematch}

*Source: `api/evaluation/answer_passage_match.md`*

# dspy.evaluate.answer_passage_match

<!-- START_API_REF -->
::: dspy.evaluate.answer_passage_match
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Citations {#citations}

*Source: `api/experimental/Citations.md`*

# dspy.experimental.Citations

<!-- START_API_REF -->
::: dspy.experimental.Citations
    handler: python
    options:
        members:
            - adapt_to_native_lm_feature
            - description
            - extract_custom_type_from_annotation
            - format
            - from_dict_list
            - is_streamable
            - parse_lm_response
            - parse_stream_chunk
            - serialize_model
            - validate_input
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Document {#document}

*Source: `api/experimental/Document.md`*

# dspy.experimental.Document

<!-- START_API_REF -->
::: dspy.experimental.Document
    handler: python
    options:
        members:
            - adapt_to_native_lm_feature
            - description
            - extract_custom_type_from_annotation
            - format
            - is_streamable
            - parse_lm_response
            - parse_stream_chunk
            - serialize_model
            - validate_input
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Embedder {#embedder}

*Source: `api/models/Embedder.md`*

# dspy.Embedder

<!-- START_API_REF -->
::: dspy.Embedder
    handler: python
    options:
        members:
            - __call__
            - acall
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### LM {#lm}

*Source: `api/models/LM.md`*

# dspy.LM

<!-- START_API_REF -->
::: dspy.LM
    handler: python
    options:
        members:
            - __call__
            - acall
            - aforward
            - copy
            - dump_state
            - finetune
            - forward
            - infer_provider
            - inspect_history
            - kill
            - launch
            - reinforce
            - update_history
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### BestOfN {#bestofn}

*Source: `api/modules/BestOfN.md`*

# dspy.BestOfN

<!-- START_API_REF -->
::: dspy.BestOfN
    handler: python
    options:
        members:
            - __call__
            - acall
            - batch
            - deepcopy
            - dump_state
            - forward
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### ChainOfThought {#chainofthought}

*Source: `api/modules/ChainOfThought.md`*

# dspy.ChainOfThought

<!-- START_API_REF -->
::: dspy.ChainOfThought
    handler: python
    options:
        members:
            - __call__
            - acall
            - aforward
            - batch
            - deepcopy
            - dump_state
            - forward
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### CodeAct {#codeact}

*Source: `api/modules/CodeAct.md`*

# dspy.CodeAct

<!-- START_API_REF -->
::: dspy.CodeAct
    handler: python
    options:
        members:
            - __call__
            - batch
            - deepcopy
            - dump_state
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

# CodeAct

CodeAct is a DSPy module that combines code generation with tool execution to solve problems. It generates Python code snippets that use provided tools and the Python standard library to accomplish tasks.

## Basic Usage

Here's a simple example of using CodeAct:

```python
import dspy
from dspy.predict import CodeAct

# Define a simple tool function
def factorial(n: int) -> int:
    """Calculate the factorial of a number."""
    if n == 1:
        return 1
    return n * factorial(n-1)

# Create a CodeAct instance
act = CodeAct("n->factorial_result", tools=[factorial])

# Use the CodeAct instance
result = act(n=5)
print(result) # Will calculate factorial(5) = 120
```

## How It Works

CodeAct operates in an iterative manner:

1. Takes input parameters and available tools
2. Generates Python code snippets that use these tools
3. Executes the code using a Python sandbox
4. Collects the output and determines if the task is complete
5. Answer the original question based on the collected information

## ⚠️ Limitations

### Only accepts pure functions as tools (no callable objects)

The following example does not work due to the usage of a callable object.

```python
# ❌ NG
class Add():
    def __call__(self, a: int, b: int):
        return a + b

dspy.CodeAct("question -> answer", tools=[Add()])
```

### External libraries cannot be used

The following example does not work due to the usage of the external library `numpy`.

```python
# ❌ NG
import numpy as np

def exp(i: int):
    return np.exp(i)

dspy.CodeAct("question -> answer", tools=[exp])
```

### All dependent functions need to be passed to `CodeAct`

Functions that depend on other functions or classes not passed to `CodeAct` cannot be used. The following example does not work because the tool functions depend on other functions or classes that are not passed to `CodeAct`, such as `Profile` or `secret_function`.

```python
# ❌ NG
from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    age: int
    
def age(profile: Profile):
    return 

def parent_function():
    print("Hi!")

def child_function():
    parent_function()

dspy.CodeAct("question -> answer", tools=[age, child_function])
```

Instead, the following example works since all necessary tool functions are passed to `CodeAct`:

```python
# ✅ OK

def parent_function():
    print("Hi!")

def child_function():
    parent_function()

dspy.CodeAct("question -> answer", tools=[parent_function, child_function])
```

---


### Module {#module}

*Source: `api/modules/Module.md`*

# dspy.Module

<!-- START_API_REF -->
::: dspy.Module
    handler: python
    options:
        members:
            - __call__
            - acall
            - batch
            - deepcopy
            - dump_state
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### MultiChainComparison {#multichaincomparison}

*Source: `api/modules/MultiChainComparison.md`*

# dspy.MultiChainComparison

<!-- START_API_REF -->
::: dspy.MultiChainComparison
    handler: python
    options:
        members:
            - __call__
            - acall
            - batch
            - deepcopy
            - dump_state
            - forward
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Parallel {#parallel}

*Source: `api/modules/Parallel.md`*

# dspy.Parallel

<!-- START_API_REF -->
::: dspy.Parallel
    handler: python
    options:
        members:
            - __call__
            - forward
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Predict {#predict}

*Source: `api/modules/Predict.md`*

# dspy.Predict

<!-- START_API_REF -->
::: dspy.Predict
    handler: python
    options:
        members:
            - __call__
            - acall
            - aforward
            - batch
            - deepcopy
            - dump_state
            - forward
            - get_config
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset
            - reset_copy
            - save
            - set_lm
            - update_config
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### ProgramOfThought {#programofthought}

*Source: `api/modules/ProgramOfThought.md`*

# dspy.ProgramOfThought

<!-- START_API_REF -->
::: dspy.ProgramOfThought
    handler: python
    options:
        members:
            - __call__
            - acall
            - batch
            - deepcopy
            - dump_state
            - forward
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### ReAct {#react}

*Source: `api/modules/ReAct.md`*

# dspy.ReAct

<!-- START_API_REF -->
::: dspy.ReAct
    handler: python
    options:
        members:
            - __call__
            - acall
            - aforward
            - batch
            - deepcopy
            - dump_state
            - forward
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
            - truncate_trajectory
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Refine {#refine}

*Source: `api/modules/Refine.md`*

# dspy.Refine

<!-- START_API_REF -->
::: dspy.Refine
    handler: python
    options:
        members:
            - __call__
            - acall
            - batch
            - deepcopy
            - dump_state
            - forward
            - get_lm
            - inspect_history
            - load
            - load_state
            - map_named_predictors
            - named_parameters
            - named_predictors
            - named_sub_modules
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### RLM {#rlm}

*Source: `api/modules/RLM.md`*

# dspy.RLM

`RLM` (Recursive Language Model) is a DSPy module that lets LLMs programmatically explore large contexts through a sandboxed Python REPL. Instead of feeding huge contexts directly into the prompt, RLM treats context as external data that the LLM examines via code execution and recursive sub-LLM calls.

This implements the approach described in ["Recursive Language Models" (Zhang, Kraska, Khattab, 2025)](https://arxiv.org/abs/2512.24601).

## When to Use RLM

As contexts grow, LLM performance degrades — a phenomenon known as [context rot](https://research.trychroma.com/context-rot). RLMs address this by separating the _variable space_ (information stored in the REPL) from the _token space_ (what the LLM actually processes). The LLM dynamically loads only the context it needs, when it needs it.

Use RLM when:

- Your context is **too large** to fit in the LLM's context window effectively
- The task benefits from **programmatic exploration** (searching, filtering, aggregating, chunking)
- You need the LLM to decide **how to decompose** the problem, not you

## Basic Usage

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-5"))

# Create an RLM module
rlm = dspy.RLM("context, query -> answer")

# Call it like any other module
result = rlm(
    context="...very long document or data...",
    query="What is the total revenue mentioned?"
)
print(result.answer)
```

## Deno Installation

RLM relies on [Deno](https://deno.land/) and [Pyodide](https://pyodide.org/) to create a local WASM sandbox for secure Python execution.

You can install Deno with: `curl -fsSL https://deno.land/install.sh | sh` on macOS and Linux. See the [Deno Installation Docs](https://docs.deno.com/runtime/getting_started/installation/) for more details. Make sure to accept the prompt when it asks to add it to your shell profile. 

After you have installed Deno, **Make sure to restart your shell.**

Then you can run `dspy.RLM`.

Users have reported issues with the Deno cache not being found by DSPy. We are actively investigating these issues, and your feedback is greatly appreciated.

You can also work with an external sandbox provider. We are still working on creating an example of using external sandbox providers.


## How It Works

RLM operates in an iterative REPL loop:

1. The LLM receives **metadata** about the context (type, length, preview) but not the full context
2. The LLM writes **Python code** to explore the data (print samples, search, filter)
3. Code executes in a **sandboxed interpreter**, and the LLM sees the output
4. The LLM can call `llm_query(prompt)` to run **sub-LLM calls** for semantic analysis on snippets
5. When done, the LLM calls `SUBMIT(output)` to return the final answer

#### What the LLM sees (step-by-step trace):

##### Step 1: Initial Metadata (no direct access to full context)
```python
# Step 1: Peek at the data
print(context[:2000])
```
_Output shown to the LLM:_
```
[Preview of the first 2000 characters of the document]
```

##### Step 2: Write Code to Explore Context
```python
# Step 2: Search for relevant sections
import re
matches = re.findall(r'revenue.*?\$[\d,]+', context, re.IGNORECASE)
print(matches)
```
_Output shown to the LLM:_
```
['Revenue in Q4: $5,000,000', 'Total revenue: $20,000,000']
```

##### Step 3: Trigger Sub-LLM Calls
```python
# Step 3: Use sub-LLM for semantic extraction
result = llm_query(f"Extract the total revenue from: {matches[1]}")
print(result)
```
_Output shown to the LLM:_
```
$20,000,000
```

##### Step 4: Submit Final Answer
```python
# Step 4: Return final answer
SUBMIT(result)
```
_Output shown to the user:_
```
$20,000,000
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `signature` | `str \| Signature` | required | Defines inputs and outputs (e.g., `"context, query -> answer"`) |
| `max_iterations` | `int` | `20` | Maximum REPL interaction loops before fallback extraction |
| `max_llm_calls` | `int` | `50` | Maximum `llm_query`/`llm_query_batched` calls per execution |
| `max_output_chars` | `int` | `10_000` | Maximum characters to include from REPL output |
| `verbose` | `bool` | `False` | Log detailed execution info |
| `tools` | `list[Union[Callable, dspy.Tool]]` | `None` | Additional tool functions callable from interpreter code |
| `sub_lm` | `dspy.LM` | `None` | LM for sub-queries. Defaults to `dspy.settings.lm`. Use a cheaper model here. |
| `interpreter` | `CodeInterpreter` | `None` | Custom interpreter. Defaults to `PythonInterpreter` (Deno/Pyodide WASM). |

## Built-in Tools

Inside the REPL, the LLM has access to:

| Tool | Description |
|------|-------------|
| `llm_query(prompt)` | Query a sub-LLM for semantic analysis (~500K char capacity) |
| `llm_query_batched(prompts)` | Query multiple prompts concurrently (faster for batch operations) |
| `print()` | Print output (required to see results) |
| `SUBMIT(...)` | Submit final output and end execution |
| Standard library | `re`, `json`, `collections`, `math`, etc. |

## Examples

### Long Document Q&A

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-5"))

rlm = dspy.RLM("document, question -> answer", max_iterations=10)

with open("large_report.txt") as f:
    document = f.read()  # 500K+ characters

result = rlm(
    document=document,
    question="What were the key findings from Q3?"
)
print(result.answer)
```

### Using a Cheaper Sub-LM

```python
import dspy

main_lm = dspy.LM("openai/gpt-5")
cheap_lm = dspy.LM("openai/gpt-5-nano")

dspy.configure(lm=main_lm)

# Root LM (gpt-5) decides strategy; sub-LM (gpt-5-nano) handles extraction
rlm = dspy.RLM("data, query -> summary", sub_lm=cheap_lm)
```

### Multiple Typed Outputs

```python
rlm = dspy.RLM("logs -> error_count: int, critical_errors: list[str]")

result = rlm(logs=server_logs)
print(f"Found {result.error_count} errors")
print(f"Critical: {result.critical_errors}")
```

### Custom Tools

```python
def fetch_metadata(doc_id: str) -> str:
    """Fetch metadata for a document ID."""
    return database.get_metadata(doc_id)

rlm = dspy.RLM(
    "documents, query -> answer",
    tools=[fetch_metadata]
)
```

### Async Execution

```python
import asyncio

rlm = dspy.RLM("context, query -> answer")

async def process():
    result = await rlm.aforward(context=data, query="Summarize this")
    return result.answer

answer = asyncio.run(process())
```

### Inspecting the Trajectory

```python
result = rlm(context=data, query="Find the magic number")

# See what code the LLM executed
for step in result.trajectory:
    print(f"Code:\n{step['code']}")
    print(f"Output:\n{step['output']}\n")
```

## Output

RLM returns a `Prediction` with:

- **Output fields** from your signature (e.g., `result.answer`)
- **`trajectory`**: List of dicts with `reasoning`, `code`, `output` for each step
- **`final_reasoning`**: The LLM's reasoning on the final step

## Notes

!!! warning "Experimental"
    RLM is marked as experimental. The API may change in future releases.

!!! note "Thread Safety"
    RLM instances are not thread-safe when using a custom interpreter. Create separate instances for concurrent use, or use the default `PythonInterpreter` which creates a fresh instance per `forward()` call.

!!! note "Interpreter Requirements"
    The default `PythonInterpreter` requires [Deno](https://deno.land/) to be installed for the Pyodide WASM sandbox.

## API Reference

<!-- START_API_REF -->
::: dspy.RLM
    handler: python
    options:
        members:
            - __init__
            - __call__
            - forward
            - aforward
            - tools
            - batch
            - deepcopy
            - dump_state
            - get_lm
            - load
            - load_state
            - named_parameters
            - named_predictors
            - parameters
            - predictors
            - reset_copy
            - save
            - set_lm
        show_source: true
        show_root_heading: true
        heading_level: 3
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


#### 1. GEPA Overview {#1-gepa-overview}

*Source: `api/optimizers/GEPA/overview.md`*

# dspy.GEPA: Reflective Prompt Optimizer

**GEPA** (Genetic-Pareto) is a reflective optimizer proposed in "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning" (Agrawal et al., 2025, [arxiv:2507.19457](https://arxiv.org/abs/2507.19457)), that adaptively evolves _textual components_ (such as prompts) of arbitrary systems. In addition to scalar scores returned by metrics, users can also provide GEPA with a text feedback to guide the optimization process. Such textual feedback provides GEPA more visibility into why the system got the score that it did, and then GEPA can introspect to identify how to improve the score. This allows GEPA to propose high performing prompts in very few rollouts.

<!-- START_API_REF -->
::: dspy.GEPA
    handler: python
    options:
        members:
            - auto_budget
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

One of the key insights behind GEPA is its ability to leverage domain-specific textual feedback. Users should provide a feedback function as the GEPA metric, which has the following call signature:
<!-- START_API_REF -->
::: dspy.teleprompt.gepa.gepa.GEPAFeedbackMetric
    handler: python
    options:
        members:
            - __call__
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

When `track_stats=True`, GEPA returns detailed results about all of the proposed candidates, and metadata about the optimization run. The results are available in the `detailed_results` attribute of the optimized program returned by GEPA, and has the following type:
<!-- START_API_REF -->
::: dspy.teleprompt.gepa.gepa.DspyGEPAResult
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

## Usage Examples

See GEPA usage tutorials in [GEPA Tutorials](../../../tutorials/gepa_ai_program/index.md).

### Inference-Time Search

GEPA can act as a test-time/inference search mechanism. By setting your `valset` to your _evaluation batch_ and using `track_best_outputs=True`, GEPA produces for each batch element the highest-scoring outputs found during the evolutionary search.

```python
gepa = dspy.GEPA(metric=metric, track_stats=True, ...)
new_prog = gepa.compile(student, trainset=my_tasks, valset=my_tasks)
highest_score_achieved_per_task = new_prog.detailed_results.highest_score_achieved_per_val_task
best_outputs = new_prog.detailed_results.best_outputs_valset
```

## How Does GEPA Work?

### 1. **Reflective Prompt Mutation**

GEPA uses LLMs to _reflect_ on structured execution traces (inputs, outputs, failures, feedback), targeting a chosen module and proposing a new instruction/program text tailored to real observed failures and rich textual/environmental feedback.

### 2. **Rich Textual Feedback as Optimization Signal**

GEPA can leverage _any_ textual feedback available—not just scalar rewards. This includes evaluation logs, code traces, failed parses, constraint violations, error message strings, or even isolated submodule-specific feedback. This allows actionable, domain-aware optimization. 

### 3. **Pareto-based Candidate Selection**

Rather than evolving just the _best_ global candidate (which leads to local optima or stagnation), GEPA maintains a Pareto frontier: the set of candidates which achieve the highest score on at least one evaluation instance. In each iteration, the next candidate to mutate is sampled (with probability proportional to coverage) from this frontier, guaranteeing both exploration and robust retention of complementary strategies.

### Algorithm Summary

1. **Initialize** the candidate pool with the the unoptimized program.
2. **Iterate**:
   - **Sample a candidate** (from Pareto frontier).
   - **Sample a minibatch** from the train set.
   - **Collect execution traces + feedbacks** for module rollout on minibatch.
   - **Select a module** of the candidate for targeted improvement.
   - **LLM Reflection:** Propose a new instruction/prompt for the targeted module using reflective meta-prompting and the gathered feedback.
   - **Roll out the new candidate** on the minibatch; **if improved, evaluate on Pareto validation set**.
   - **Update the candidate pool/Pareto frontier.**
   - **[Optionally] System-aware merge/crossover**: Combine best-performing modules from distinct lineages.
3. **Continue** until rollout or metric budget is exhausted. 
4. **Return** candidate with best aggregate performance on validation.

## Implementing Feedback Metrics

A well-designed metric is central to GEPA's sample efficiency and learning signal richness. GEPA expects the metric to returns a `dspy.Prediction(score=..., feedback=...)`. GEPA leverages natural language traces from LLM-based workflows for optimization, preserving intermediate trajectories and errors in plain text rather than reducing them to numerical rewards. This mirrors human diagnostic processes, enabling clearer identification of system behaviors and bottlenecks.

Practical Recipe for GEPA-Friendly Feedback:

- **Leverage Existing Artifacts**: Use logs, unit tests, evaluation scripts, and profiler outputs; surfacing these often suffices.
- **Decompose Outcomes**: Break scores into per-objective components (e.g., correctness, latency, cost, safety) and attribute errors to steps.
- **Expose Trajectories**: Label pipeline stages, reporting pass/fail with salient errors (e.g., in code generation pipelines).
- **Ground in Checks**: Employ automatic validators (unit tests, schemas, simulators) or LLM-as-a-judge for non-verifiable tasks (as in PUPA).
- **Prioritize Clarity**: Focus on error coverage and decision points over technical complexity.

### Examples

- **Document Retrieval** (e.g., HotpotQA): List correctly retrieved, incorrect, or missed documents, beyond mere Recall/F1 scores.
- **Multi-Objective Tasks** (e.g., PUPA): Decompose aggregate scores to reveal contributions from each objective, highlighting tradeoffs (e.g., quality vs. privacy).
- **Stacked Pipelines** (e.g., code generation: parse → compile → run → profile → evaluate): Expose stage-specific failures; natural-language traces often suffice for LLM self-correction.

## Custom Instruction Proposal

For advanced customization of GEPA's instruction proposal mechanism, including custom instruction proposers and component selectors, see [Advanced Features](GEPA_Advanced.md).

## Further Reading

- [GEPA Paper: arxiv:2507.19457](https://arxiv.org/abs/2507.19457)
- [GEPA Github](https://github.com/gepa-ai/gepa) - This repository provides the core GEPA evolution pipeline used by `dspy.GEPA` optimizer.
- [DSPy Tutorials](../../../tutorials/gepa_ai_program/index.md)

---


#### 2. GEPA Advanced {#2-gepa-advanced}

*Source: `api/optimizers/GEPA/GEPA_Advanced.md`*

# dspy.GEPA - Advanced Features

## Custom Instruction Proposers

### What is instruction_proposer?

The `instruction_proposer` is the component responsible for invoking the `reflection_lm` and proposing new prompts during GEPA optimization. When GEPA identifies underperforming components in your DSPy program, the instruction proposer analyzes execution traces, feedback, and failures to generate improved instructions tailored to the observed issues.

### Default Implementation

By default, GEPA uses the built-in instruction proposer from the [GEPA library](https://github.com/gepa-ai/gepa), which implements the [`ProposalFn`](https://github.com/gepa-ai/gepa/blob/main/src/gepa/core/adapter.py). The [default proposer](https://github.com/gepa-ai/gepa/blob/main/src/gepa/proposer/reflective_mutation/reflective_mutation.py#L53-L75) uses this prompt template:

````
I provided an assistant with the following instructions to perform a task for me:
```
<curr_instructions>
```

The following are examples of different task inputs provided to the assistant along with the assistant's response for each of them, and some feedback on how the assistant's response could be better:
```
<inputs_outputs_feedback>
```

Your task is to write a new instruction for the assistant.

Read the inputs carefully and identify the input format and infer detailed task description about the task I wish to solve with the assistant.

Read all the assistant responses and the corresponding feedback. Identify all niche and domain specific factual information about the task and include it in the instruction, as a lot of it may not be available to the assistant in the future. The assistant may have utilized a generalizable strategy to solve the task, if so, include that in the instruction as well.

Provide the new instructions within ``` blocks.
````

This template is automatically filled with:

- `<curr_instructions>`: The current instruction being optimized
- `<inputs_outputs_feedback>`: Structured markdown containing predictor inputs, generated outputs, and evaluation feedback

Example of default behavior:

```python
# Default instruction proposer is used automatically
gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=dspy.LM(model="gpt-5", temperature=1.0, max_tokens=32000, api_key=api_key),
    auto="medium"
)
optimized_program = gepa.compile(student, trainset=examples)
```

### When to Use Custom instruction_proposer

**Note:** Custom instruction proposers are an advanced feature. Most users should start with the default proposer, which works well for most text-based optimization tasks.

Consider implementing a custom instruction proposer when you need:

- **Multi-modal handling**: Process images (dspy.Image) alongside textual information in your inputs
- **Nuanced control on limits and length constraints**: Have more fine-grained control over instruction length, format, and structural requirements
- **Domain-specific information**: Inject specialized knowledge, terminology, or context that the default proposer lacks and cannot be provided via feedback_func. This is an advanced feature, and most users should not need to use this.
- **Provider-specific prompting guides**: Optimize instructions for specific LLM providers (OpenAI, Anthropic, etc.) with their unique formatting preferences
- **Coupled component updates**: Handle situations where 2 or more components need to be updated together in a coordinated manner, rather than optimizing each component independently (refer to component_selector parameter, in [Custom Component Selection](#custom-component-selection) section, for related functionality)
- **External knowledge integration**: Connect to databases, APIs, or knowledge bases during instruction generation

### Available Options

**Built-in Options:**

- **Default Proposer**: The standard GEPA instruction proposer (used when `instruction_proposer=None`). The default instruction proposer IS an instruction proposer as well! It is the most general one, that was used for the diverse experiments reported in the GEPA paper and tutorials.
- **MultiModalInstructionProposer**: Handles `dspy.Image` inputs and structured multimodal content.

```python
from dspy.teleprompt.gepa.instruction_proposal import MultiModalInstructionProposer

# For tasks involving images or multimodal inputs
gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=dspy.LM(model="gpt-5", temperature=1.0, max_tokens=32000, api_key=api_key),
    instruction_proposer=MultiModalInstructionProposer(),
    auto="medium"
)
```

We invite community contributions of new instruction proposers for specialized domains as the [GEPA library](https://github.com/gepa-ai/gepa) continues to grow.

### How to Implement Custom Instruction Proposers

Custom instruction proposers must implement the `ProposalFn` protocol by defining a callable class or function. GEPA will call your proposer during optimization:

```python
from dspy.teleprompt.gepa.gepa_utils import ReflectiveExample

class CustomInstructionProposer:
    def __call__(
        self,
        candidate: dict[str, str],                          # Candidate component name -> instruction mapping to be updated in this round
        reflective_dataset: dict[str, list[ReflectiveExample]],  # Component -> examples with structure: {"Inputs": ..., "Generated Outputs": ..., "Feedback": ...}
        components_to_update: list[str]                     # Which components to improve
    ) -> dict[str, str]:                                    # Return new instruction mapping only for components being updated
        # Your custom instruction generation logic here
        return updated_instructions

# Or as a function:
def custom_instruction_proposer(candidate, reflective_dataset, components_to_update):
    # Your custom instruction generation logic here
    return updated_instructions
```

**Reflective Dataset Structure:**

- `dict[str, list[ReflectiveExample]]` - Maps component names to lists of examples
- `ReflectiveExample` TypedDict contains:
  - `Inputs: dict[str, Any]` - Predictor inputs (may include dspy.Image objects)
  - `Generated_Outputs: dict[str, Any] | str` - Success: output fields dict, Failure: error message
  - `Feedback: str` - Always a string from metric function or auto-generated by GEPA

#### Basic Example: Word Limit Proposer

```python
import dspy
from gepa.core.adapter import ProposalFn
from dspy.teleprompt.gepa.gepa_utils import ReflectiveExample

class GenerateWordLimitedInstruction(dspy.Signature):
    """Given a current instruction and feedback examples, generate an improved instruction with word limit constraints."""

    current_instruction = dspy.InputField(desc="The current instruction that needs improvement")
    feedback_summary = dspy.InputField(desc="Feedback from examples that might include both positive and negative cases")
    max_words = dspy.InputField(desc="Maximum number of words allowed in the new instruction")

    improved_instruction = dspy.OutputField(desc="A new instruction that fixes the issues while staying under the max_words limit")

class WordLimitProposer(ProposalFn):
    def __init__(self, max_words: int = 1000):
        self.max_words = max_words
        self.instruction_improver = dspy.ChainOfThought(GenerateWordLimitedInstruction)

    def __call__(self, candidate: dict[str, str], reflective_dataset: dict[str, list[ReflectiveExample]], components_to_update: list[str]) -> dict[str, str]:
        updated_components = {}

        for component_name in components_to_update:
            if component_name not in candidate or component_name not in reflective_dataset:
                continue

            current_instruction = candidate[component_name]
            component_examples = reflective_dataset[component_name]

            # Create feedback summary
            feedback_text = "\n".join([
                f"Example {i+1}: {ex.get('Feedback', 'No feedback')}"
                for i, ex in enumerate(component_examples)  # Limit examples to prevent context overflow
            ])

            # Use the module to improve the instruction
            result = self.instruction_improver(
                current_instruction=current_instruction,
                feedback_summary=feedback_text,
                max_words=self.max_words
            )

            updated_components[component_name] = result.improved_instruction

        return updated_components

# Usage
gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=dspy.LM(model="gpt-5", temperature=1.0, max_tokens=32000, api_key=api_key),
    instruction_proposer=WordLimitProposer(max_words=700),
    auto="medium"
)
```

#### Advanced Example: RAG-Enhanced Instruction Proposer

```python
import dspy
from gepa.core.adapter import ProposalFn
from dspy.teleprompt.gepa.gepa_utils import ReflectiveExample

class GenerateDocumentationQuery(dspy.Signature):
    """Analyze examples with feedback to identify common issue patterns and generate targeted database queries for retrieving relevant documentation.

    Your goal is to search a document database for guidelines that address the problematic patterns found in the examples. Look for recurring issues, error types, or failure modes in the feedback, then craft specific search queries that will find documentation to help resolve these patterns."""

    current_instruction = dspy.InputField(desc="The current instruction that needs improvement")
    examples_with_feedback = dspy.InputField(desc="Examples with their feedback showing what issues occurred and any recurring patterns")

    failure_patterns: str = dspy.OutputField(desc="Summarize the common failure patterns identified in the examples")

    retrieval_queries: list[str] = dspy.OutputField(desc="Specific search queries to find relevant documentation in the database that addresses the common issue patterns identified in the problematic examples")

class GenerateRAGEnhancedInstruction(dspy.Signature):
    """Generate improved instructions using retrieved documentation and examples analysis."""

    current_instruction = dspy.InputField(desc="The current instruction that needs improvement")
    relevant_documentation = dspy.InputField(desc="Retrieved guidelines and best practices from specialized documentation")
    examples_with_feedback = dspy.InputField(desc="Examples showing what issues occurred with the current instruction")

    improved_instruction: str = dspy.OutputField(desc="Enhanced instruction that incorporates retrieved guidelines and addresses the issues shown in the examples")

class RAGInstructionImprover(dspy.Module):
    """Module that uses RAG to improve instructions with specialized documentation."""

    def __init__(self, retrieval_model):
        super().__init__()
        self.retrieve = retrieval_model  # Could be dspy.Retrieve or custom retriever
        self.query_generator = dspy.ChainOfThought(GenerateDocumentationQuery)
        self.generate_answer = dspy.ChainOfThought(GenerateRAGEnhancedInstruction)

    def forward(self, current_instruction: str, component_examples: list):
        """Improve instruction using retrieved documentation."""

        # Let LM analyze examples and generate targeted retrieval queries
        query_result = self.query_generator(
            current_instruction=current_instruction,
            examples_with_feedback=component_examples
        )

        results = self.retrieve.query(
            query_texts=query_result.retrieval_queries,
            n_results=3
        )

        relevant_docs_parts = []
        for i, (query, query_docs) in enumerate(zip(query_result.retrieval_queries, results['documents'])):
            if query_docs:
                docs_formatted = "\n".join([f"  - {doc}" for doc in query_docs])
                relevant_docs_parts.append(
                    f"**Search Query #{i+1}**: {query}\n"
                    f"**Retrieved Guidelines**:\n{docs_formatted}"
                )

        relevant_docs = "\n\n" + "="*60 + "\n\n".join(relevant_docs_parts) + "\n" + "="*60

        # Generate improved instruction with retrieved context
        result = self.generate_answer(
            current_instruction=current_instruction,
            relevant_documentation=relevant_docs,
            examples_with_feedback=component_examples
        )

        return result

class DocumentationEnhancedProposer(ProposalFn):
    """Instruction proposer that accesses specialized documentation via RAG."""

    def __init__(self, documentation_retriever):
        """
        Args:
            documentation_retriever: A retrieval model that can search your specialized docs
                                   Could be dspy.Retrieve, ChromadbRM, or custom retriever
        """
        self.instruction_improver = RAGInstructionImprover(documentation_retriever)

    def __call__(self, candidate: dict[str, str], reflective_dataset: dict[str, list[ReflectiveExample]], components_to_update: list[str]) -> dict[str, str]:
        updated_components = {}

        for component_name in components_to_update:
            if component_name not in candidate or component_name not in reflective_dataset:
                continue

            current_instruction = candidate[component_name]
            component_examples = reflective_dataset[component_name]

            result = self.instruction_improver(
                current_instruction=current_instruction,
                component_examples=component_examples
            )

            updated_components[component_name] = result.improved_instruction

        return updated_components

import chromadb

client = chromadb.Client()
collection = client.get_collection("instruction_guidelines")

gepa = dspy.GEPA(
    metric=task_specific_metric,
    reflection_lm=dspy.LM(model="gpt-5", temperature=1.0, max_tokens=32000, api_key=api_key),
    instruction_proposer=DocumentationEnhancedProposer(collection),
    auto="medium"
)
```

#### Integration Patterns

**Using Custom Proposer with External LM:**

```python
class ExternalLMProposer(ProposalFn):
    def __init__(self):
        # Manage your own LM instance
        self.external_lm = dspy.LM('gemini/gemini-2.5-pro')

    def __call__(self, candidate, reflective_dataset, components_to_update):
        updated_components = {}

        with dspy.context(lm=self.external_lm):
            # Your custom logic here using self.external_lm
            for component_name in components_to_update:
                # ... implementation
                pass

        return updated_components

gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=None,  # Optional when using custom proposer
    instruction_proposer=ExternalLMProposer(),
    auto="medium"
)
```

**Best Practices:**

- **Use the full power of DSPy**: Leverage DSPy components like `dspy.Module`, `dspy.Signature`, and `dspy.Predict` to create your instruction proposer rather than direct LM calls. Consider `dspy.Refine` for constraint satisfaction, `dspy.ChainOfThought` for complex reasoning tasks, and compose multiple modules for sophisticated instruction improvement workflows
- **Enable holistic feedback analysis**: While dspy.GEPA's `GEPAFeedbackMetric` processes one (gold, prediction) pair at a time, instruction proposers receive all examples for a component in batch, enabling cross-example pattern detection and systematic issue identification.
- **Mind data serialization**: Serializing everything to strings might not be ideal - handle complex input types (like `dspy.Image`) by maintaining their structure for better LM processing
- **Test thoroughly**: Test your custom proposer with representative failure cases

## Custom Component Selection

### What is component_selector?

The `component_selector` parameter controls which components (predictors) in your DSPy program are selected for optimization at each GEPA iteration. Instead of the default round-robin approach that updates one component at a time, you can implement custom selection strategies that choose single or multiple components based on optimization state, performance trajectories, and other contextual information.

### Default Behavior

By default, GEPA uses a **round-robin strategy** (`RoundRobinReflectionComponentSelector`) that cycles through components sequentially, optimizing one component per iteration:

```python
# Default round-robin component selection
gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=dspy.LM(model="gpt-5", temperature=1.0, max_tokens=32000, api_key=api_key),
    # component_selector="round_robin"  # This is the default
    auto="medium"
)
```

### Built-in Selection Strategies

**String-based selectors:**

- `"round_robin"` (default): Cycles through components one at a time
- `"all"`: Selects all components for simultaneous optimization

```python
# Optimize all components simultaneously
gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=reflection_lm,
    component_selector="all",  # Update all components together
    auto="medium"
)

# Explicit round-robin selection
gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=reflection_lm,
    component_selector="round_robin",  # One component per iteration
    auto="medium"
)
```

### When to Use Custom Component Selection

Consider implementing custom component selection when you need:

- **Dependency-aware optimization**: Update related components together (e.g., a classifier and its input formatter)
- **LLM-driven selection**: Let an LLM analyze trajectories and decide which components need attention
- **Resource-conscious optimization**: Balance optimization thoroughness with computational budget

### Custom Component Selector Protocol

Custom component selectors must implement the [`ReflectionComponentSelector`](https://github.com/gepa-ai/gepa/blob/main/src/gepa/proposer/reflective_mutation/base.py) protocol by defining a callable class or function. GEPA will call your selector during optimization:

```python
from dspy.teleprompt.gepa.gepa_utils import GEPAState, Trajectory

class CustomComponentSelector:
    def __call__(
        self,
        state: GEPAState,                    # Complete optimization state with history
        trajectories: list[Trajectory],      # Execution traces from the current minibatch
        subsample_scores: list[float],       # Scores for each example in the current minibatch
        candidate_idx: int,                  # Index of the current program candidate being optimized
        candidate: dict[str, str],           # Component name -> instruction mapping
    ) -> list[str]:                          # Return list of component names to optimize
        # Your custom component selection logic here
        return selected_components

# Or as a function:
def custom_component_selector(state, trajectories, subsample_scores, candidate_idx, candidate):
    # Your custom component selection logic here
    return selected_components
```

### Custom Implementation Example

Here's a simple function that alternates between optimizing different halves of your components:

```python
def alternating_half_selector(state, trajectories, subsample_scores, candidate_idx, candidate):
    """Optimize half the components on even iterations, half on odd iterations."""
    components = list(candidate.keys())

    # If there's only one component, always optimize it
    if len(components) <= 1:
        return components

    mid_point = len(components) // 2

    # Use state.i (iteration counter) to alternate between halves
    if state.i % 2 == 0:
        # Even iteration: optimize first half
        return components[:mid_point]
    else:
        # Odd iteration: optimize second half
        return components[mid_point:]

# Usage
gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=reflection_lm,
    component_selector=alternating_half_selector,
    auto="medium"
)
```

### Integration with Custom Instruction Proposers

Component selectors work seamlessly with custom instruction proposers. The selector determines which components to update, then the instruction proposer generates new instructions for those components:

```python
# Combined custom selector + custom proposer
gepa = dspy.GEPA(
    metric=my_metric,
    reflection_lm=reflection_lm,
    component_selector=alternating_half_selector,
    instruction_proposer=WordLimitProposer(max_words=500),
    auto="medium"
)
```

---


### BetterTogether {#bettertogether}

*Source: `api/optimizers/BetterTogether.md`*

# dspy.BetterTogether

**BetterTogether** is a meta-optimizer proposed in the paper [Fine-Tuning and Prompt Optimization: Two Great Steps that Work Better Together](https://arxiv.org/abs/2407.10930) by Dilara Soylu, Christopher Potts, and Omar Khattab. It combines prompt optimization and weight optimization (fine-tuning) by applying them in a configurable sequence, allowing a student program to iteratively improve both its prompts and model parameters. The core insight is that prompt and weight optimization can complement each other: prompt optimization can potentially discover effective task decompositions and reasoning strategies, while weight optimization can specialize the model to execute these patterns more efficiently. Using these approaches together in sequences (e.g., prompt optimization then weight optimization) may allow each to build on the improvements made by the other.

<!-- START_API_REF -->
::: dspy.BetterTogether
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

## Usage Examples

See BetterTogether usage tutorials in [BetterTogether Tutorials](../../../tutorials/bettertogether/index.md).

## How BetterTogether Works

BetterTogether executes optimizers in a configurable sequence, evaluating each intermediate result and returning the best performing program. Here's how it works:

### 1. **Initialization with Custom Optimizers**

When initialized, BetterTogether accepts any DSPy optimizers (Teleprompters) as keyword arguments. The keys become the optimizer names used in the strategy string:

```python
optimizer = BetterTogether(
    metric=metric,
    p=GEPA(...),           # 'p' can be used in strategy
    w=BootstrapFinetune(...) # 'w' can be used in strategy
)
```

If no optimizers are provided, BetterTogether defaults to `BootstrapFewShotWithRandomSearch` (key: 'p') and `BootstrapFinetune` (key: 'w').

### 2. **Strategy Execution**

The strategy string defines the sequence of optimizers to apply. For example:

```python
compiled = optimizer.compile(
    student,
    trainset=trainset,
    valset=valset,
    strategy="p -> w -> p"
)
```

This strategy `"p -> w -> p"` means:

1. Run prompt optimizer ('p')
2. Run weight optimizer ('w') on the result
3. Run prompt optimizer ('p') again on the result

At each step:
- The trainset is shuffled (if `shuffle_trainset_between_steps=True`)
- The optimizer is run on the current student program
- The result is evaluated on the validation set
- The candidate program and score are recorded

Since BetterTogether is a meta-optimizer, any sequence of optimizers can be combined. The optimizer names in the strategy string correspond to the keyword arguments from initialization. For example, you can sequence different prompt optimizers (note: this illustrates BetterTogether's flexibility, not necessarily a recommended configuration):

```python
optimizer = BetterTogether(
    metric=metric,
    mipro=MIPROv2(metric=metric, auto="light"),
    gepa=GEPA(metric=metric, auto="light")
)

compiled = optimizer.compile(
    student,
    trainset=trainset,
    valset=valset,
    strategy="mipro -> gepa -> mipro"
)
```

### 3. **Validation and Program Selection**

BetterTogether can use a validation set in three ways:

- **Explicit valset**: If `valset` is provided, it's used for evaluation
- **Auto-split**: If `valset_ratio > 0`, a portion of trainset is held out for validation
- **No validation**: If both `valset` and `valset_ratio` are None/0, no validation occurs

After all optimization steps complete, the best program is selected based on validation set availability:

- **With validation**: The program with the **best score** is returned (with earlier programs winning ties)
- **Without validation**: The **latest program** is returned

If an optimization step fails:
- The error is logged with full traceback
- Optimization stops early
- The best program found so far is returned
- `flag_compilation_error_occurred` is set to `True`

The returned program includes two additional attributes:

- `candidate_programs`: List of all evaluated programs with their scores and strategies, sorted by score (best first). When an error occurs, this contains all successfully evaluated programs up to the point of failure.
- `flag_compilation_error_occurred`: Boolean indicating if any optimization step failed during compilation.

### 4. **Further Details**

**Model Lifecycle Management**: For local models (like LocalLM), BetterTogether automatically launches models before first use, kills them after optimization completes, and relaunches them after fine-tuning when model names change. These operations are no-ops for API-based LMs but needed for local model serving.

**Custom Compile Arguments**: You can pass custom compile arguments to specific optimizers using the `optimizer_compile_args` parameter:

- **Override default arguments**: Pass custom trainset/valset/teacher to specific optimizers
- **Customize per optimizer**: Each optimizer can have different compile arguments (e.g., `num_trials`, `max_bootstrapped_demos`)

Note: The `student` argument cannot be included in `optimizer_compile_args` - BetterTogether manages the student program for all optimizers. See the `compile()` method docstring for detailed argument documentation.

## Best Practices

### When to Use BetterTogether

BetterTogether is the right optimizer when:

- **You want to squeeze every bit of performance**: Prompt optimization is often the best bang for buck, quickly discovering high-level strategies. When opportunity allows, adding weight optimization on top compounds these gains, yielding benefits that exceed either approach alone.
- **You have fine-tuning capabilities**: Weight optimizers like `BootstrapFinetune` require LMs with a fine-tuning interface. Currently supported: `LocalProvider`, `DatabricksProvider`, and `OpenAIProvider`. You can extend the `Provider` class for custom use cases, or use BetterTogether to combine prompt optimizers only.

The [Databricks case study](https://www.databricks.com/blog/building-state-art-enterprise-agents-90x-cheaper-automated-prompt-optimization) demonstrates this effectiveness. They evaluated on IE Bench—a comprehensive suite spanning enterprise domains (finance, legal, commerce, healthcare) with complex challenges: 100+ page documents, 70+ extraction fields, and hierarchical schemas. Using GPT-4.1:

- **SFT alone**: +1.9 points over baseline
- **GEPA alone**: +2.1 points over baseline (slightly exceeding SFT)
- **GEPA + SFT (BetterTogether)**: +4.8 points over baseline

This demonstrates that prompt optimization can match or surpass supervised fine-tuning, and combining these techniques yields strong compounding benefits.

### Common Strategies and Optimizers

Common strategies:

- `"p -> w"`: Optimize prompts first, then fine-tune (simple and often effective)
- `"p -> w -> p"`: Optimize prompts, fine-tune, then optimize prompts again (can build on fine-tuning improvements)
- `"w -> p"`: Fine-tune first, then optimize prompts

Example optimizer combinations:

- **GEPA + BootstrapFinetune**: Prompt optimization with fine-tuning
- **MIPROv2 + BootstrapFinetune**: Prompt optimization with fine-tuning
- **Multiple prompt optimizers**: Alternate between different prompt optimization approaches (experimental)

## Further Reading

- [BetterTogether Paper: arxiv:2407.10930](https://arxiv.org/abs/2407.10930)
- [Databricks Case Study](https://www.databricks.com/blog/building-state-art-enterprise-agents-90x-cheaper-automated-prompt-optimization) - Real-world application combining BetterTogether with GEPA
- [DSPy Optimizers Overview](../../../learn/programming/optimizers.md)

---


### BootstrapFewShot {#bootstrapfewshot}

*Source: `api/optimizers/BootstrapFewShot.md`*

# dspy.BootstrapFewShot

<!-- START_API_REF -->
::: dspy.BootstrapFewShot
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### BootstrapFewShotWithRandomSearch {#bootstrapfewshotwithrandomsearch}

*Source: `api/optimizers/BootstrapFewShotWithRandomSearch.md`*

# dspy.BootstrapFewShotWithRandomSearch

<!-- START_API_REF -->
::: dspy.BootstrapFewShotWithRandomSearch
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### BootstrapFinetune {#bootstrapfinetune}

*Source: `api/optimizers/BootstrapFinetune.md`*

# dspy.BootstrapFinetune

<!-- START_API_REF -->
::: dspy.BootstrapFinetune
    handler: python
    options:
        members:
            - compile
            - convert_to_lm_dict
            - finetune_lms
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### BootstrapRS {#bootstraprs}

*Source: `api/optimizers/BootstrapRS.md`*

# dspy.BootstrapRS

<!-- START_API_REF -->
::: dspy.BootstrapRS
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### COPRO {#copro}

*Source: `api/optimizers/COPRO.md`*

# dspy.COPRO

<!-- START_API_REF -->
::: dspy.COPRO
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Ensemble {#ensemble}

*Source: `api/optimizers/Ensemble.md`*

# dspy.Ensemble

<!-- START_API_REF -->
::: dspy.Ensemble
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### InferRules {#inferrules}

*Source: `api/optimizers/InferRules.md`*

# dspy.InferRules

<!-- START_API_REF -->
::: dspy.InferRules
    handler: python
    options:
        members:
            - compile
            - evaluate_program
            - format_examples
            - get_params
            - get_predictor_demos
            - induce_natural_language_rules
            - update_program_instructions
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### KNN {#knn}

*Source: `api/optimizers/KNN.md`*

# dspy.KNN

<!-- START_API_REF -->
::: dspy.KNN
    handler: python
    options:
        members:
            - __call__
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### KNNFewShot {#knnfewshot}

*Source: `api/optimizers/KNNFewShot.md`*

# dspy.KNNFewShot

<!-- START_API_REF -->
::: dspy.KNNFewShot
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### LabeledFewShot {#labeledfewshot}

*Source: `api/optimizers/LabeledFewShot.md`*

# dspy.LabeledFewShot

<!-- START_API_REF -->
::: dspy.LabeledFewShot
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### MIPROv2 {#miprov2}

*Source: `api/optimizers/MIPROv2.md`*

# dspy.MIPROv2

`MIPROv2` (<u>M</u>ultiprompt <u>I</u>nstruction <u>PR</u>oposal <u>O</u>ptimizer Version 2) is an prompt optimizer capable of optimizing both instructions and few-shot examples jointly. It does this by bootstrapping few-shot example candidates, proposing instructions grounded in different dynamics of the task, and finding an optimized combination of these options using Bayesian Optimization. It can be used for optimizing few-shot examples & instructions jointly, or just instructions for 0-shot optimization.

<!-- START_API_REF -->
::: dspy.MIPROv2
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

## Example Usage

The program below shows optimizing a math program with MIPROv2

```python
import dspy
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric

# Import the optimizer
from dspy.teleprompt import MIPROv2

# Initialize the LM
lm = dspy.LM('openai/gpt-4o-mini', api_key='YOUR_OPENAI_API_KEY')
dspy.configure(lm=lm)

# Initialize optimizer
teleprompter = MIPROv2(
    metric=gsm8k_metric,
    auto="medium", # Can choose between light, medium, and heavy optimization runs
)

# Optimize program
print(f"Optimizing program with MIPROv2...")
gsm8k = GSM8K()
optimized_program = teleprompter.compile(
    dspy.ChainOfThought("question -> answer"),
    trainset=gsm8k.train,
)

# Save optimize program for future use
optimized_program.save(f"optimized.json")
```

## How `MIPROv2` works

At a high level, `MIPROv2` works by creating both few-shot examples and new instructions for each predictor in your LM program, and then searching over these using Bayesian Optimization to find the best combination of these variables for your program.  If you want a visual explanation check out this [twitter thread](https://x.com/michaelryan207/status/1804189184988713065).

These steps are broken down in more detail below:

1) **Bootstrap Few-Shot Examples**: Randomly samples examples from your training set, and run them through your LM program. If the output from the program is correct for this example, it is kept as a valid few-shot example candidate. Otherwise, we try another example until we've curated the specified amount of few-shot example candidates. This step creates `num_candidates` sets of `max_bootstrapped_demos` bootstrapped examples and `max_labeled_demos` basic examples sampled from the training set.

2) **Propose Instruction Candidates**. The instruction proposer includes (1) a generated summary of properties of the training dataset, (2) a generated summary of your LM program's code and the specific predictor that an instruction is being generated for, (3) the previously bootstrapped few-shot examples to show reference inputs / outputs for a given predictor and (4) a randomly sampled tip for generation (i.e. "be creative", "be concise", etc.) to help explore the feature space of potential instructions.  This context is provided to a `prompt_model` which writes high quality instruction candidates.

3) **Find an Optimized Combination of Few-Shot Examples & Instructions**. Finally, we use Bayesian Optimization to choose which combinations of instructions and demonstrations work best for each predictor in our program. This works by running a series of `num_trials` trials, where a new set of prompts are evaluated over our validation set at each trial. The new set of prompts are only evaluated on a minibatch of size `minibatch_size` at each trial (when `minibatch`=`True`). The best averaging set of prompts is then evaluated on the full validation set every `minibatch_full_eval_steps`. At the end of the optimization process, the LM program with the set of prompts that performed best on the full validation set is returned.

For those interested in more details, more information on `MIPROv2` along with a study on `MIPROv2` compared with other DSPy optimizers can be found in [this paper](https://arxiv.org/abs/2406.11695).

---


### SIMBA {#simba}

*Source: `api/optimizers/SIMBA.md`*

# dspy.SIMBA

<!-- START_API_REF -->
::: dspy.SIMBA
    handler: python
    options:
        members:
            - compile
            - get_params
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

## Example Usage

```python
optimizer = dspy.SIMBA(metric=your_metric)
optimized_program = optimizer.compile(your_program, trainset=your_trainset)

# Save optimize program for future use
optimized_program.save(f"optimized.json")
```

## How `SIMBA` works
SIMBA (Stochastic Introspective Mini-Batch Ascent) is a DSPy optimizer that uses the LLM to analyze its own performance and generate improvement rules. It samples mini-batches, identifies challenging examples with high output variability, then either creates self-reflective rules or adds successful examples as demonstrations. See [this great blog post](https://blog.mariusvach.com/posts/dspy-simba) from [Marius](https://x.com/rasmus1610) for more details.

---


### Audio {#audio}

*Source: `api/primitives/Audio.md`*

# dspy.Audio

<!-- START_API_REF -->
::: dspy.Audio
    handler: python
    options:
        members:
            - adapt_to_native_lm_feature
            - description
            - extract_custom_type_from_annotation
            - format
            - from_array
            - from_file
            - from_url
            - is_streamable
            - parse_lm_response
            - parse_stream_chunk
            - serialize_model
            - validate_input
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Code {#code}

*Source: `api/primitives/Code.md`*

# dspy.Code

<!-- START_API_REF -->
::: dspy.Code
    handler: python
    options:
        members:
            - adapt_to_native_lm_feature
            - description
            - extract_custom_type_from_annotation
            - format
            - is_streamable
            - parse_lm_response
            - parse_stream_chunk
            - serialize_model
            - validate_input
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Example {#example}

*Source: `api/primitives/Example.md`*

# dspy.Example

<!-- START_API_REF -->
::: dspy.Example
    handler: python
    options:
        members:
            - copy
            - get
            - inputs
            - items
            - keys
            - labels
            - toDict
            - values
            - with_inputs
            - without
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### History {#history}

*Source: `api/primitives/History.md`*

# dspy.History

<!-- START_API_REF -->
::: dspy.History
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Image {#image}

*Source: `api/primitives/Image.md`*

# dspy.Image

<!-- START_API_REF -->
::: dspy.Image
    handler: python
    options:
        members:
            - adapt_to_native_lm_feature
            - description
            - extract_custom_type_from_annotation
            - format
            - from_PIL
            - from_file
            - from_url
            - is_streamable
            - parse_lm_response
            - parse_stream_chunk
            - serialize_model
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Prediction {#prediction}

*Source: `api/primitives/Prediction.md`*

# dspy.Prediction

<!-- START_API_REF -->
::: dspy.Prediction
    handler: python
    options:
        members:
            - copy
            - from_completions
            - get
            - get_lm_usage
            - inputs
            - items
            - keys
            - labels
            - set_lm_usage
            - toDict
            - values
            - with_inputs
            - without
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Tool {#tool}

*Source: `api/primitives/Tool.md`*

# dspy.Tool

<!-- START_API_REF -->
::: dspy.Tool
    handler: python
    options:
        members:
            - __call__
            - acall
            - adapt_to_native_lm_feature
            - description
            - extract_custom_type_from_annotation
            - format
            - format_as_litellm_function_call
            - from_langchain
            - from_mcp_tool
            - is_streamable
            - parse_lm_response
            - parse_stream_chunk
            - serialize_model
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### ToolCalls {#toolcalls}

*Source: `api/primitives/ToolCalls.md`*

# dspy.ToolCalls

<!-- START_API_REF -->
::: dspy.ToolCalls
    handler: python
    options:
        members:
            - adapt_to_native_lm_feature
            - description
            - extract_custom_type_from_annotation
            - format
            - from_dict_list
            - is_streamable
            - parse_lm_response
            - parse_stream_chunk
            - serialize_model
            - validate_input
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### InputField {#inputfield}

*Source: `api/signatures/InputField.md`*

# dspy.InputField

<!-- START_API_REF -->
::: dspy.InputField
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### OutputField {#outputfield}

*Source: `api/signatures/OutputField.md`*

# dspy.OutputField

<!-- START_API_REF -->
::: dspy.OutputField
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Signature {#signature}

*Source: `api/signatures/Signature.md`*

# dspy.Signature

<!-- START_API_REF -->
::: dspy.Signature
    handler: python
    options:
        members:
            - append
            - delete
            - dump_state
            - equals
            - insert
            - load_state
            - prepend
            - with_instructions
            - with_updated_fields
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### ColBERTv2 {#colbertv2}

*Source: `api/tools/ColBERTv2.md`*

# dspy.ColBERTv2

<!-- START_API_REF -->
::: dspy.ColBERTv2
    handler: python
    options:
        members:
            - __call__
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### Embeddings {#embeddings}

*Source: `api/tools/Embeddings.md`*

# dspy.retrievers.Embeddings

<!-- START_API_REF -->
::: dspy.Embeddings
    handler: python
    options:
        members:
            - __call__
            - forward
            - from_saved
            - load
            - save
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### PythonInterpreter {#pythoninterpreter}

*Source: `api/tools/PythonInterpreter.md`*

# dspy.PythonInterpreter

<!-- START_API_REF -->
::: dspy.PythonInterpreter
    handler: python
    options:
        members:
            - __call__
            - execute
            - shutdown
            - start
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### StatusMessage {#statusmessage}

*Source: `api/utils/StatusMessage.md`*

# dspy.streaming.StatusMessage

<!-- START_API_REF -->
::: dspy.streaming.StatusMessage
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### StatusMessageProvider {#statusmessageprovider}

*Source: `api/utils/StatusMessageProvider.md`*

# dspy.streaming.StatusMessageProvider

<!-- START_API_REF -->
::: dspy.streaming.StatusMessageProvider
    handler: python
    options:
        members:
            - lm_end_status_message
            - lm_start_status_message
            - module_end_status_message
            - module_start_status_message
            - tool_end_status_message
            - tool_start_status_message
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### StreamListener {#streamlistener}

*Source: `api/utils/StreamListener.md`*

# dspy.streaming.StreamListener

<!-- START_API_REF -->
::: dspy.streaming.StreamListener
    handler: python
    options:
        members:
            - finalize
            - flush
            - receive
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### asyncify {#asyncify}

*Source: `api/utils/asyncify.md`*

# dspy.asyncify

<!-- START_API_REF -->
::: dspy.asyncify
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### configure_cache {#configurecache}

*Source: `api/utils/configure_cache.md`*

# dspy.configure_cache

<!-- START_API_REF -->
::: dspy.configure_cache
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### disable_litellm_logging {#disablelitellmlogging}

*Source: `api/utils/disable_litellm_logging.md`*

# dspy.disable_litellm_logging

<!-- START_API_REF -->
::: dspy.disable_litellm_logging
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### disable_logging {#disablelogging}

*Source: `api/utils/disable_logging.md`*

# dspy.disable_logging

<!-- START_API_REF -->
::: dspy.disable_logging
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### enable_litellm_logging {#enablelitellmlogging}

*Source: `api/utils/enable_litellm_logging.md`*

# dspy.enable_litellm_logging

<!-- START_API_REF -->
::: dspy.enable_litellm_logging
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### enable_logging {#enablelogging}

*Source: `api/utils/enable_logging.md`*

# dspy.enable_logging

<!-- START_API_REF -->
::: dspy.enable_logging
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### inspect_history {#inspecthistory}

*Source: `api/utils/inspect_history.md`*

# dspy.inspect_history

<!-- START_API_REF -->
::: dspy.inspect_history
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### load {#load}

*Source: `api/utils/load.md`*

# dspy.load

<!-- START_API_REF -->
::: dspy.load
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


### streamify {#streamify}

*Source: `api/utils/streamify.md`*

# dspy.streamify

<!-- START_API_REF -->
::: dspy.streamify
    handler: python
    options:
        show_source: true
        show_root_heading: true
        heading_level: 2
        docstring_style: google
        show_root_full_path: true
        show_object_full_path: false
        separate_signature: false
        inherited_members: true
<!-- END_API_REF -->

---


## Additional Reference Pages


### deep-dive/data-handling/built-in-datasets.md

!!! warning "This page is outdated and may not be fully accurate in DSPy 2.5"

# Utilizing Built-in Datasets

It's easy to use your own data in DSPy: a dataset is just a list of `Example` objects. Using DSPy well involves being able to find and re-purpose existing datasets for your own pipelines in new ways; DSPy makes this a particularly powerful strategy.

For convenience, DSPy currently also provides support for the following dataset out of the box:

* **HotPotQA** (multi-hop question answering)
* **GSM8k** (math questions)
* **Color** (basic dataset of colors)


## Loading HotPotQA

HotPotQA is which is a collection of question-answer pairs.

```python
from dspy.datasets import HotPotQA

dataset = HotPotQA(train_seed=1, train_size=5, eval_seed=2023, dev_size=50, test_size=0)

print(dataset.train)
```
**Output:**
```text
[Example({'question': 'At My Window was released by which American singer-songwriter?', 'answer': 'John Townes Van Zandt'}) (input_keys=None),
 Example({'question': 'which  American actor was Candace Kita  guest starred with ', 'answer': 'Bill Murray'}) (input_keys=None),
 Example({'question': 'Which of these publications was most recently published, Who Put the Bomp or Self?', 'answer': 'Self'}) (input_keys=None),
 Example({'question': 'The Victorians - Their Story In Pictures is a documentary series written by an author born in what year?', 'answer': '1950'}) (input_keys=None),
 Example({'question': 'Which magazine has published articles by Scott Shaw, Tae Kwon Do Times or Southwest Art?', 'answer': 'Tae Kwon Do Times'}) (input_keys=None)]
```

We just loaded trainset (5 examples) and devset (50 examples). Each example in our training set contains just a question and its (human-annotated) answer. As you can see, it is loaded as a list of `Example` objects. However, one thing to note is that it doesn't set the input keys implicitly, so that is something that we'll need to do!!

```python
trainset = [x.with_inputs('question') for x in dataset.train]
devset = [x.with_inputs('question') for x in dataset.dev]

print(trainset)
```
**Output:**
```text
[Example({'question': 'At My Window was released by which American singer-songwriter?', 'answer': 'John Townes Van Zandt'}) (input_keys={'question'}),
 Example({'question': 'which  American actor was Candace Kita  guest starred with ', 'answer': 'Bill Murray'}) (input_keys={'question'}),
 Example({'question': 'Which of these publications was most recently published, Who Put the Bomp or Self?', 'answer': 'Self'}) (input_keys={'question'}),
 Example({'question': 'The Victorians - Their Story In Pictures is a documentary series written by an author born in what year?', 'answer': '1950'}) (input_keys={'question'}),
 Example({'question': 'Which magazine has published articles by Scott Shaw, Tae Kwon Do Times or Southwest Art?', 'answer': 'Tae Kwon Do Times'}) (input_keys={'question'})]
```

DSPy typically requires very minimal labeling. Whereas your pipeline may involve six or seven complex steps, you only need labels for the initial question and the final answer. DSPy will bootstrap any intermediate labels needed to support your pipeline. If you change your pipeline in any way, the data bootstrapped will change accordingly!


## Advanced: Inside DSPy's `Dataset` class (Optional)

We've seen how you can use `HotPotQA` dataset class and load the HotPotQA dataset, but how does it actually work? The `HotPotQA` class inherits from the `Dataset` class, which takes care of the conversion of the data loaded from a source into train-test-dev split, all of which are *list of examples*. In the `HotPotQA` class, you only implement the `__init__` method, where you populate the splits from HuggingFace into the variables `_train`, `_test` and `_dev`. The rest of the process is handled by methods in the `Dataset` class.

![Dataset Loading Process in HotPotQA Class](./img/data-loading.png)

But how do the methods of the `Dataset` class convert the data from HuggingFace? Let's take a deep breath and think step by step...pun intended. In example above, we can see the splits accessed by `.train`, `.dev` and `.test` methods, so let's take a look at the implementation of the `train()` method:

```python
@property
def train(self):
    if not hasattr(self, '_train_'):
        self._train_ = self._shuffle_and_sample('train', self._train, self.train_size, self.train_seed)

    return self._train_
```

As you can see, the `train()` method serves as a property, not a regular method. Within this property, it first checks if the `_train_` attribute exists. If not, it calls the `_shuffle_and_sample()` method to process the `self._train` where the HuggingFace dataset is loaded. Let's see the  `_shuffle_and_sample()` method:

```python
def _shuffle_and_sample(self, split, data, size, seed=0):
    data = list(data)
    base_rng = random.Random(seed)

    if self.do_shuffle:
        base_rng.shuffle(data)

    data = data[:size]
    output = []

    for example in data:
        output.append(Example(**example, dspy_uuid=str(uuid.uuid4()), dspy_split=split))
    
        return output
```

The `_shuffle_and_sample()` method does two things:

* It shuffles the data if `self.do_shuffle` is True.
* It then takes a sample of size `size` from the shuffled data.
* It then loops through the sampled data and converts each element in `data` into an `Example` object. The `Example` along with example data also contains a unique ID, and the split name.

Converting the raw examples into `Example` objects allows the Dataset class to process them in a standardized way later. For example, the collate method, which is used by the PyTorch DataLoader, expects each item to be an `Example`.

To summarize, the `Dataset` class handles all the necessary data processing and provides a simple API to access the different splits. This differentiates from the dataset classes like HotpotQA which require only definitions on how to load the raw data.

---


### deep-dive/data-handling/examples.md

!!! warning "This page is outdated and may not be fully accurate in DSPy 2.5"

# Examples in DSPy

Working in DSPy involves training sets, development sets, and test sets. This is like traditional ML, but you usually need far fewer labels (or zero labels) to use DSPy effectively.

The core data type for data in DSPy is `Example`. You will use **Examples** to represent items in your training set and test set. 

DSPy **Examples** are similar to Python `dict`s but have a few useful utilities. Your DSPy modules will return values of the type `Prediction`, which is a special sub-class of `Example`.

## Creating an `Example`

When you use DSPy, you will do a lot of evaluation and optimization runs. Your individual datapoints will be of type `Example`:

```python
qa_pair = dspy.Example(question="This is a question?", answer="This is an answer.")

print(qa_pair)
print(qa_pair.question)
print(qa_pair.answer)
```
**Output:**
```text
Example({'question': 'This is a question?', 'answer': 'This is an answer.'}) (input_keys=None)
This is a question?
This is an answer.
```

Examples can have any field keys and any value types, though usually values are strings.

```text
object = Example(field1=value1, field2=value2, field3=value3, ...)
```

## Specifying Input Keys

In traditional ML, there are separated "inputs" and "labels".

In DSPy, the `Example` objects have a `with_inputs()` method, which can mark specific fields as inputs. (The rest are just metadata or labels.)

```python
# Single Input.
print(qa_pair.with_inputs("question"))

# Multiple Inputs; be careful about marking your labels as inputs unless you mean it.
print(qa_pair.with_inputs("question", "answer"))
```

This flexibility allows for customized tailoring of the `Example` object for different DSPy scenarios.

When you call `with_inputs()`, you get a new copy of the example. The original object is kept unchanged.


## Element Access and Updation

Values can be accessed using the `.`(dot) operator. You can access the value of key `name` in defined object `Example(name="John Doe", job="sleep")` through `object.name`. 

To access or exclude certain keys, use `inputs()` and `labels()` methods to return new Example objects containing only input or non-input keys, respectively.

```python
article_summary = dspy.Example(article= "This is an article.", summary= "This is a summary.").with_inputs("article")

input_key_only = article_summary.inputs()
non_input_key_only = article_summary.labels()

print("Example object with Input fields only:", input_key_only)
print("Example object with Non-Input fields only:", non_input_key_only)
```

**Output**
```
Example object with Input fields only: Example({'article': 'This is an article.'}) (input_keys=None)
Example object with Non-Input fields only: Example({'summary': 'This is a summary.'}) (input_keys=None)
```

To exclude keys, use `without()`:

```python
article_summary = dspy.Example(context="This is an article.", question="This is a question?", answer="This is an answer.", rationale= "This is a rationale.").with_inputs("context", "question")

print("Example object without answer & rationale keys:", article_summary.without("answer", "rationale"))
```

**Output**
```
Example object without answer & rationale keys: Example({'context': 'This is an article.', 'question': 'This is a question?'}) (input_keys=None)
```

Updating values is simply assigning a new value using the `.` operator.

```python
article_summary.context = "new context"
```

## Iterating over Example

Iteration in the `Example` class also functions like a dictionary, supporting methods like `keys()`, `values()`, etc: 

```python
for k, v in article_summary.items():
    print(f"{k} = {v}")
```

**Output**

```text
context = This is an article.
question = This is a question?
answer = This is an answer.
rationale = This is a rationale.
```

---


### deep-dive/data-handling/loading-custom-data.md

!!! warning "This page is outdated and may not be fully accurate in DSPy 2.5"

# Creating a Custom Dataset

We've seen how to work with with `Example` objects and use the `HotPotQA` class to load the HuggingFace HotPotQA dataset as a list of `Example` objects. But in production, such structured datasets are rare. Instead, you'll find yourself working on a custom dataset and might question: how do I create my own dataset or what format should it be?

In DSPy, your dataset is a list of `Examples`, which we can accomplish in two ways:

* **Recommended: The Pythonic Way:** Using native python utility and logic.
* **Advanced: Using DSPy's `Dataset` class**

## Recommended: The Pythonic Way

To create a list of `Example` objects, we can simply load data from the source and formulate it into a Python list. Let's load an example CSV `sample.csv` that contains 3 fields: (**context**, **question** and **summary**) via Pandas. From there, we can construct our data list.

```python
import pandas as pd

df = pd.read_csv("sample.csv")
print(df.shape)
```
**Output:**
```text
(1000, 3)
```
```python
dataset = []

for context, question, answer in df.values:
    dataset.append(dspy.Example(context=context, question=question, answer=answer).with_inputs("context", "question"))

print(dataset[:3])
```
**Output:**
```python
[Example({'context': nan, 'question': 'Which is a species of fish? Tope or Rope', 'answer': 'Tope'}) (input_keys={'question', 'context'}),
 Example({'context': nan, 'question': 'Why can camels survive for long without water?', 'answer': 'Camels use the fat in their humps to keep them filled with energy and hydration for long periods of time.'}) (input_keys={'question', 'context'}),
 Example({'context': nan, 'question': "Alice's parents have three daughters: Amy, Jessy, and what’s the name of the third daughter?", 'answer': 'The name of the third daughter is Alice'}) (input_keys={'question', 'context'})]
```

While this is fairly simple, let's take a look at how loading datasets would look in DSPy - via the DSPythonic way!

## Advanced: Using DSPy's `Dataset` class (Optional)

Let's take advantage of the `Dataset` class we defined in the previous article to accomplish the preprocessing: 

* Load data from CSV to a dataframe.
* Split the data to train, dev and test splits.
* Populate `_train`, `_dev` and `_test` class attributes. Note that these attributes should be a list of dictionary, or an iterator over mapping like HuggingFace Dataset, to make it work.

This is all done through the `__init__` method, which is the only method we have to implement.

```python
import pandas as pd
from dspy.datasets.dataset import Dataset

class CSVDataset(Dataset):
    def __init__(self, file_path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        df = pd.read_csv(file_path)
        self._train = df.iloc[0:700].to_dict(orient='records')

        self._dev = df.iloc[700:].to_dict(orient='records')

dataset = CSVDataset("sample.csv")
print(dataset.train[:3])
```
**Output:**
```text
[Example({'context': nan, 'question': 'Which is a species of fish? Tope or Rope', 'answer': 'Tope'}) (input_keys={'question', 'context'}),
 Example({'context': nan, 'question': 'Why can camels survive for long without water?', 'answer': 'Camels use the fat in their humps to keep them filled with energy and hydration for long periods of time.'}) (input_keys={'question', 'context'}),
 Example({'context': nan, 'question': "Alice's parents have three daughters: Amy, Jessy, and what’s the name of the third daughter?", 'answer': 'The name of the third daughter is Alice'}) (input_keys={'question', 'context'})]
```

Let's understand the code step by step:

* It inherits the base `Dataset` class from DSPy. This inherits all the useful data loading/processing functionality.
* We load the data in CSV into a DataFrame.
* We get the **train** split i.e first 700 rows in the DataFrame and convert it to lists of dicts using `to_dict(orient='records')` method and is then assigned to `self._train`.
* We get the **dev** split i.e first 300 rows in the DataFrame and convert it to lists of dicts using `to_dict(orient='records')` method and is then assigned to `self._dev`.

Using the Dataset base class now makes loading custom datasets incredibly easy and avoids having to write all that boilerplate code ourselves for every new dataset.

!!! caution

    We did not populate `_test` attribute in the above code, which is fine and won't cause any unnecessary error as such. However it'll give you an error if you try to access the test split.

    ```python
    dataset.test[:5]
    ```
    ****
    ```text
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    <ipython-input-59-5202f6de3c7b> in <cell line: 1>()
    ----> 1 dataset.test[:5]

    /usr/local/lib/python3.10/dist-packages/dspy/datasets/dataset.py in test(self)
        51     def test(self):
        52         if not hasattr(self, '_test_'):
    ---> 53             self._test_ = self._shuffle_and_sample('test', self._test, self.test_size, self.test_seed)
        54 
        55         return self._test_

    AttributeError: 'CSVDataset' object has no attribute '_test'
    ```

    To prevent that you'll just need to make sure `_test` is not `None` and populated with the appropriate data.

You can override the methods in `Dataset` class to customize your class even more. 

In summary, the Dataset base class provides a simplistic way to load and preprocess custom datasets with minimal code!

---


### learn/programming/7-assertions.md

# DSPy Assertions 

!!! warning "Assertions are deprecated and NOT supported. Please use the `dspy.Refine` module instead. (or dspy.Suggest)."

The content below is deprecated, and is scheduled to be removed.

## Introduction

Language models (LMs) have transformed how we interact with machine learning, offering vast capabilities in natural language understanding and generation. However, ensuring these models adhere to domain-specific constraints remains a challenge. Despite the growth of techniques like fine-tuning or “prompt engineering”, these approaches are extremely tedious and rely on heavy, manual hand-waving to guide the LMs in adhering to specific constraints. Even DSPy's modularity of programming prompting pipelines lacks mechanisms to effectively and automatically enforce these constraints. 

To address this, we introduce DSPy Assertions, a feature within the DSPy framework designed to automate the enforcement of computational constraints on LMs. DSPy Assertions empower developers to guide LMs towards desired outcomes with minimal manual intervention, enhancing the reliability, predictability, and correctness of LM outputs.

### dspy.Assert and dspy.Suggest API    

We introduce two primary constructs within DSPy Assertions:

- **`dspy.Assert`**:
  - **Parameters**: 
    - `constraint (bool)`: Outcome of Python-defined boolean validation check.
    - `msg (Optional[str])`: User-defined error message providing feedback or correction guidance.
    - `backtrack (Optional[module])`: Specifies target module for retry attempts upon constraint failure. The default backtracking module is the last module before the assertion.
  - **Behavior**: Initiates retry  upon failure, dynamically adjusting the pipeline's execution. If failures persist, it halts execution and raises a `dspy.AssertionError`.

- **`dspy.Suggest`**:
  - **Parameters**: Similar to `dspy.Assert`.
  - **Behavior**: Encourages self-refinement through retries without enforcing hard stops. Logs failures after maximum backtracking attempts and continues execution.

- **dspy.Assert vs. Python Assertions**: Unlike conventional Python `assert` statements that terminate the program upon failure, `dspy.Assert` conducts a sophisticated retry mechanism, allowing the pipeline to adjust. 

Specifically, when a constraint is not met:

- Backtracking Mechanism: An under-the-hood backtracking is initiated, offering the model a chance to self-refine and proceed, which is done through signature modification.
- Dynamic Signature Modification: internally modifying your DSPy program’s Signature by adding the following fields:
    - Past Output: your model's past output that did not pass the validation_fn
    - Instruction: your user-defined feedback message on what went wrong and what possibly to fix

If the error continues past the `max_backtracking_attempts`, then `dspy.Assert` will halt the pipeline execution, alerting you with an `dspy.AssertionError`. This ensures your program doesn't continue executing with “bad” LM behavior and immediately highlights sample failure outputs for user assessment.

- **dspy.Suggest vs. dspy.Assert**: `dspy.Suggest` on the other hand offers a softer approach. It maintains the same retry backtracking as `dspy.Assert` but instead serves as a gentle nudger. If the model outputs cannot pass the model constraints after the `max_backtracking_attempts`, `dspy.Suggest` will log the persistent failure and continue execution of the program on the rest of the data. This ensures the LM pipeline works in a "best-effort" manner without halting execution. 

- **`dspy.Suggest`** statements are best utilized as "helpers" during the evaluation phase, offering guidance and potential corrections without halting the pipeline.
- **`dspy.Assert`** statements are recommended during the development stage as "checkers" to ensure the LM behaves as expected, providing a robust mechanism for identifying and addressing errors early in the development cycle.


## Use Case: Including Assertions in DSPy Programs

We start with using an example of a multi-hop QA SimplifiedBaleen pipeline as defined in the intro walkthrough. 

```python
class SimplifiedBaleen(dspy.Module):
    def __init__(self, passages_per_hop=2, max_hops=2):
        super().__init__()

        self.generate_query = [dspy.ChainOfThought(GenerateSearchQuery) for _ in range(max_hops)]
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
        self.max_hops = max_hops

    def forward(self, question):
        context = []
        prev_queries = [question]

        for hop in range(self.max_hops):
            query = self.generate_query[hop](context=context, question=question).query
            prev_queries.append(query)
            passages = self.retrieve(query).passages
            context = deduplicate(context + passages)
        
        pred = self.generate_answer(context=context, question=question)
        pred = dspy.Prediction(context=context, answer=pred.answer)
        return pred

baleen = SimplifiedBaleen()

baleen(question = "Which award did Gary Zukav's first book receive?")
```

To include DSPy Assertions, we simply define our validation functions and declare our assertions following the respective model generation. 

For this use case, suppose we want to impose the following constraints:
    1. Length - each query should be less than 100 characters
    2. Uniqueness - each generated query should differ from previously-generated queries. 
    
We can define these validation checks as boolean functions:

```python
#simplistic boolean check for query length
len(query) <= 100

#Python function for validating distinct queries
def validate_query_distinction_local(previous_queries, query):
    """check if query is distinct from previous queries"""
    if previous_queries == []:
        return True
    if dspy.evaluate.answer_exact_match_str(query, previous_queries, frac=0.8):
        return False
    return True
```

We can declare these validation checks through `dspy.Suggest` statements (as we want to test the program in a best-effort demonstration). We want to keep these after the query generation `query = self.generate_query[hop](context=context, question=question).query`.

```python
dspy.Suggest(
    len(query) <= 100,
    "Query should be short and less than 100 characters",
    target_module=self.generate_query
)

dspy.Suggest(
    validate_query_distinction_local(prev_queries, query),
    "Query should be distinct from: "
    + "; ".join(f"{i+1}) {q}" for i, q in enumerate(prev_queries)),
    target_module=self.generate_query
)
```

It is recommended to define a program with assertions separately than your original program if you are doing comparative evaluation for the effect of assertions. If not, feel free to set Assertions away!

Let's take a look at how the SimplifiedBaleen program will look with Assertions included:

```python
class SimplifiedBaleenAssertions(dspy.Module):
    def __init__(self, passages_per_hop=2, max_hops=2):
        super().__init__()
        self.generate_query = [dspy.ChainOfThought(GenerateSearchQuery) for _ in range(max_hops)]
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
        self.max_hops = max_hops

    def forward(self, question):
        context = []
        prev_queries = [question]

        for hop in range(self.max_hops):
            query = self.generate_query[hop](context=context, question=question).query

            dspy.Suggest(
                len(query) <= 100,
                "Query should be short and less than 100 characters",
                target_module=self.generate_query
            )

            dspy.Suggest(
                validate_query_distinction_local(prev_queries, query),
                "Query should be distinct from: "
                + "; ".join(f"{i+1}) {q}" for i, q in enumerate(prev_queries)),
                target_module=self.generate_query
            )

            prev_queries.append(query)
            passages = self.retrieve(query).passages
            context = deduplicate(context + passages)
        
        if all_queries_distinct(prev_queries):
            self.passed_suggestions += 1

        pred = self.generate_answer(context=context, question=question)
        pred = dspy.Prediction(context=context, answer=pred.answer)
        return pred
```

Now calling programs with DSPy Assertions requires one last step, and that is transforming the program to wrap it with internal assertions backtracking and Retry logic. 

```python
from dspy.primitives.assertions import assert_transform_module, backtrack_handler

baleen_with_assertions = assert_transform_module(SimplifiedBaleenAssertions(), backtrack_handler)

# backtrack_handler is parameterized over a few settings for the backtracking mechanism
# To change the number of max retry attempts, you can do
baleen_with_assertions_retry_once = assert_transform_module(SimplifiedBaleenAssertions(), 
    functools.partial(backtrack_handler, max_backtracks=1))
```

Alternatively, you can also directly call `activate_assertions` on the program with `dspy.Assert/Suggest` statements using the default backtracking mechanism (`max_backtracks=2`):

```python
baleen_with_assertions = SimplifiedBaleenAssertions().activate_assertions()
```

Now let's take a look at the internal LM backtracking by inspecting the history of the LM query generations. Here we see that when a query fails to pass the validation check of being less than 100 characters, its internal `GenerateSearchQuery` signature is dynamically modified during the backtracking+Retry process to include the past query and the corresponding user-defined instruction: `"Query should be short and less than 100 characters"`.


```text
Write a simple search query that will help answer a complex question.

---

Follow the following format.

Context: may contain relevant facts

Question: ${question}

Reasoning: Let's think step by step in order to ${produce the query}. We ...

Query: ${query}

---

Context:
[1] «Kerry Condon | Kerry Condon (born 4 January 1983) is [...]»
[2] «Corona Riccardo | Corona Riccardo (c. 1878October 15, 1917) was [...]»

Question: Who acted in the shot film The Shore and is also the youngest actress ever to play Ophelia in a Royal Shakespeare Company production of "Hamlet." ?

Reasoning: Let's think step by step in order to find the answer to this question. First, we need to identify the actress who played Ophelia in a Royal Shakespeare Company production of "Hamlet." Then, we need to find out if this actress also acted in the short film "The Shore."

Query: "actress who played Ophelia in Royal Shakespeare Company production of Hamlet" + "actress in short film The Shore"


Write a simple search query that will help answer a complex question.

---

Follow the following format.

Context: may contain relevant facts

Question: ${question}

Past Query: past output with errors

Instructions: Some instructions you must satisfy

Query: ${query}

---

Context:
[1] «Kerry Condon | Kerry Condon (born 4 January 1983) is an Irish television and film actress, best known for her role as Octavia of the Julii in the HBO/BBC series "Rome," as Stacey Ehrmantraut in AMC's "Better Call Saul" and as the voice of F.R.I.D.A.Y. in various films in the Marvel Cinematic Universe. She is also the youngest actress ever to play Ophelia in a Royal Shakespeare Company production of "Hamlet."»
[2] «Corona Riccardo | Corona Riccardo (c. 1878October 15, 1917) was an Italian born American actress who had a brief Broadway stage career before leaving to become a wife and mother. Born in Naples she came to acting in 1894 playing a Mexican girl in a play at the Empire Theatre. Wilson Barrett engaged her for a role in his play "The Sign of the Cross" which he took on tour of the United States. Riccardo played the role of Ancaria and later played Berenice in the same play. Robert B. Mantell in 1898 who struck by her beauty also cast her in two Shakespeare plays, "Romeo and Juliet" and "Othello". Author Lewis Strang writing in 1899 said Riccardo was the most promising actress in America at the time. Towards the end of 1898 Mantell chose her for another Shakespeare part, Ophelia im Hamlet. Afterwards she was due to join Augustin Daly's Theatre Company but Daly died in 1899. In 1899 she gained her biggest fame by playing Iras in the first stage production of Ben-Hur.»

Question: Who acted in the shot film The Shore and is also the youngest actress ever to play Ophelia in a Royal Shakespeare Company production of "Hamlet." ?

Past Query: "actress who played Ophelia in Royal Shakespeare Company production of Hamlet" + "actress in short film The Shore"

Instructions: Query should be short and less than 100 characters

Query: "actress Ophelia RSC Hamlet" + "actress The Shore"

```


## Assertion-Driven Optimizations

DSPy Assertions work with optimizations that DSPy offers, particularly with `BootstrapFewShotWithRandomSearch`, including the following settings:

- Compilation with Assertions
    This includes assertion-driven example bootstrapping and counterexample bootstrapping during compilation. The teacher model for bootstrapping few-shot demonstrations can make use of DSPy Assertions to offer robust bootstrapped examples for the student model to learn from during inference. In this setting, the student model does not perform assertion aware optimizations (backtracking and retry) during inference.
- Compilation + Inference with Assertions
    -This includes assertion-driven optimizations in both compilation and inference. Now the teacher model offers assertion-driven examples but the student can further optimize with assertions of its own during inference time. 
```python
teleprompter = BootstrapFewShotWithRandomSearch(
    metric=validate_context_and_answer_and_hops,
    max_bootstrapped_demos=max_bootstrapped_demos,
    num_candidate_programs=6,
)

#Compilation with Assertions
compiled_with_assertions_baleen = teleprompter.compile(student = baleen, teacher = baleen_with_assertions, trainset = trainset, valset = devset)

#Compilation + Inference with Assertions
compiled_baleen_with_assertions = teleprompter.compile(student=baleen_with_assertions, teacher = baleen_with_assertions, trainset=trainset, valset=devset)

```

---


### roadmap.md

!!! warning "This document is from Aug 2024. Since then, DSPy 2.5 and 2.6 were released, DSPy has grown considerably, and 3.0 is approaching! Content below is highly outdated."


# Roadmap Sketch: DSPy 2.5+

It’s been a year since DSPy evolved out of Demonstrate–Search–Predict (DSP), whose research started at Stanford NLP all the way back in February 2022. Thanks to 200 wonderful contributors, DSPy has introduced tens of thousands of people to building modular LM programs and optimizing their prompts and weights automatically. In this time, DSPy has grown to 160,000 monthly downloads and 16,000 stars on GitHub, becoming synonymous with prompt optimization in many circles and inspiring at least a half-dozen cool new libraries.

This document is an initial sketch of DSPy’s public roadmap for the next few weeks and months, as we work on DSPy 2.5 and plan for DSPy 3.0. Suggestions and open-source contributors are more than welcome: just open an issue or submit a pull request regarding the roadmap.


## Technical Objectives

The thesis of DSPy is that for LMs to be useful, we have to shift from ad-hoc prompting to new notions of programming LMs. Instead of relying on LMs gaining much more general or more compositional capabilities, we need to enable developers to iteratively explore their problems and build modular software that invokes LMs for well-scoped tasks. We need to enable that through modules and optimizers that isolate how they decompose their problems and describe their system's objectives from how their LMs are invoked or fine-tuned to maximize their objectives. DSPy's goal has been to develop (and to build the community and shared infrastructure for the collective development of) the abstractions, programming patterns, and optimizers toward this thesis.

To a first approximation, DSPy’s current user-facing language has the minimum number of appropriate abstractions that address the goals above: declarative signatures, define-by-run modules, and optimizers that can be composed quite powerfully. But there are several things we need to do better to realize our goals. The upcoming DSPy releases will have the following objectives.

1. Polishing the core functionality.
2. Developing more accurate, lower-cost optimizers.
3. Building end-to-end tutorials from DSPy’s ML workflow to deployment.
4. Shifting towards more interactive optimization & tracking.


## Team & Organization

DSPy is fairly unusual in its technical objectives, contributors, and audience. Though DSPy takes inspiration from PyTorch, a library for building and optimizing DNNs, there is one major difference: PyTorch was introduced well after DNNs were mature ML concepts, but DSPy seeks to establish and advance core LM Programs research: the framework is propelled by constant academic research from programming abstractions (like the original **Demonstrate–Search–Predict** concepts, DSPy **Signatures**, or **LM Assertions**) to NLP systems (like **STORM**, **PATH**, and **IReRa**) to prompt optimizers (like **MIPRO**) and RL (like **BetterTogether**), among many other related directions.

This research all composes into a concrete, practical library, thanks to dozens of industry contributors, many of whom are deploying apps in production using DSPy. Because of this, DSPy reaches not only of grad students and ML engineers, but also many non-ML engineers, from early adopter SWEs to hobbyists exploring new ways of using LMs. The following team, with help from many folks in the OSS community, is working towards the objectives in this Roadmap.

**Project Lead:** Omar Khattab (Stanford & Databricks)

**Project Mentors:** Chris Potts (Stanford), Matei Zaharia (UC Berkeley & Databricks), Heather Miller (CMU & Two Sigma)

**Core Library:** Arnav Singhvi (Databricks & Stanford), Herumb Shandilya (Stanford), Hanna Moazam (Databricks), Sri Vardhamanan (Dashworks), Cyrus Nouroozi (Zenbase), Amir Mehr (Zenbase), Kyle Caverly (Modular), with special thanks to Keshav Santhanam (Stanford), Thomas Ahle (Normal Computing), Connor Shorten (Weaviate)

**Prompt Optimization:** Krista Opsahl-Ong (Stanford), Michael Ryan (Stanford), Josh Purtell (Basis), with special thanks to Eric Zhang (Stanford)

**Finetuning & RL:** Dilara Soylu (Stanford), Isaac Miller (Anyscale), Karel D'Oosterlinck (Ghent), with special thanks to Paridhi Masehswari (Stanford)

**PL Abstractions:** Shangyin Tan (UC Berkeley), Manish Shetty (UC Berkeley), Peter Zhong (CMU)

**Applications:** Jasper Xian (Waterloo), Saron Samuel (Stanford), Alberto Mancarella (Stanford), Faraz Khoubsirat (Waterloo), Saiful Haq (IIT-B), Ashutosh Sharma (UIUC)


## 1) Polishing the core functionality.

Over the next month, polishing is the main objective and likely the one to have the highest ROI on the experience of the average user. Conceptually, DSPy has an extremely small core. It’s nothing but (1) LMs, (2) Signatures & Modules, (3) Optimizers, and (4) Assertions. These concepts and their implementations evolved organically over the past couple of years. We are working now to consolidate what we’ve learned and refactor internally so that things “just work” out of the box for new users, who may not know all the tips-and-tricks just yet.

More concretely:

1. We want to increase the quality of zero-shot, off-the-shelf DSPy programs, i.e. those not yet compiled on custom data.
2. Wherever possible, DSPy should delegate lower-level internal complexity (like managing LMs and structured generation) to emerging lower-level libraries. When required, we may fork smaller libraries out of DSPy to support infrastructure pieces as their own projects.
3. DSPy should internally be more modular and we need higher compatibility between internal components. Specifically, we need more deeper and more native investment in (i) typed multi-field constraints, (ii) assertions, (iii) observability and experimental tracking, (iv) deployment of artifacts and related concerns like streaming and async, and (v) fine-tuning and serving open models.


### On LMs

As of DSPy 2.4, the library has approximately 20,000 lines of code and roughly another 10,000 lines of code for tests, examples, and documentation. Some of these are clearly necessary (e.g., DSPy optimizers) but others exist only because the LM space lacks the building blocks we need under the hood. Luckily, for LM interfaces, a very strong library now exists: LiteLLM, a library that unifies interfaces to various LM and embedding providers. We expect to reduce around 6000 LoCs of support for custom LMs and retrieval models by shifting a lot of that to LiteLLM.

Objectives in this space include improved caching, saving/loading of LMs, support for streaming and async LM requests. Work here is currently led by Hanna Moazam and Sri Vardhamanan, building on a foundation by Cyrus Nouroozi, Amir Mehr, Kyle Caverly, and others.


### On Signatures & Modules

Traditionally, LMs offer text-in-text-out interfaces. Toward modular programming, DSPy introduced signatures for the first time (as DSP Templates in Jan 2023) as a way to structure the inputs and outputs of LM interactions. Standard prompts conflate interface (“what should the LM do?”) with implementation (“how do we tell it to do that?”). DSPy signatures isolate the former so we can infer and learn the latter from data — in the context of a bigger program. Today in the LM landscape, notions of "structured outputs" have evolved dramatically, thanks to constrained decoding and other improvements, and have become mainstream. What may be called "structured inputs" remains is yet to become mainstream outside of DSPy, but is as crucial.

Objectives in this space include refining the abstractions and implementations first-class notion of LM Adapters in DSPy, as translators that sits between signatures and LM interfaces. While Optimizers adjust prompts through interactions with a user-supplied metric and data, Adapters are more concerned with building up interactions with LMs to account for, e.g. (i) non-plaintext LM interfaces like chat APIs, structured outputs, function calling, and multi-modal APIs, (ii) languages beyond English or other forms of higher-level specialization. This has been explored in DSPy on and off in various forms, but we have started working on more fundamental approaches to this problem that will offer tangible improvements to most use-cases. Work here is currently led by Omar Khattab.


### On Finetuning & Serving

In February 2023, DSPy introduced the notion of compiling to optimize the weights of an LM program. (To understand just how long ago that was in AI terms, this was before the Alpaca training project at Stanford had even started and a month before the first GPT-4 was released.) Since then, we have shown in October 2023 and, much more expansively, in July 2024, that the fine-tuning flavor of DSPy can deliver large gains for small LMs, especially when composed with prompt optimization.

Overall, though, most DSPy users in practice explore prompt optimization and not weight optimization and most of our examples do the same. The primary reason for a lot of this is infrastructure. Fine-tuning in the DSPy flavor is more than just training a model: ultimately, we need to bootstrap training data for several different modules in a program, train multiple models and handle model selection, and then load and plug in those models into the program's modules. Doing this robustly at the level of abstraction DSPy offers requires a level of resource management that is not generally supported by external existing tools. Major efforts in this regard are currently led by Dilara Soylu and Isaac Miller.


### On Optimizers & Assertions

This is a naturally major direction in the course of polishing. We will share more thoughts here after making more progress on the three angles above.


## 2) Developing more accurate, lower-cost optimizers.

A very large fraction of the research in DSPy focuses on optimizing the prompts and the weights of LM programs. In December 2022, we introduced the algorithm and abstractions behind BootstrapFewShot (as Demonstrate in DSP) and several of its variants. In February 2023, we introduced the core version of what later became BootstrapFinetune. In August 2023, we introduced new variations of both of these. In December 2023, we introduced the first couple of instruction optimizers into DSPy, CA-OPRO and early versions of MIPRO. These were again upgraded in March 2024. Fast forward to June and July 2024, we released MIPROv2 for prompt optimization and BetterTogether for fine-tuning the weights of LM programs.

We have been working towards a number of stronger optimizers. While we cannot share the internal details of research on new optimizers yet, we can outline the goals. A DSPy optimizer can be characterized via three angles:

1. Quality: How much quality can it deliver from various LMs? How effective does it need the zero-shot program to be in order to work well?
2. Cost: How many labeled (and unlabeled) inputs does it need? How many invocations of the program does it need? How expensive is the resulting optimized program at inference time?
3. Robustness: How well can it generalize to different unseen data points or distributions? How sensitive is it to mistakes of the metric or labels?

Over the next six months, our goal is to dramatically improve each angle of these _when the other two are held constant_.  Concretely, there are three directions here.

- Benchmarking: A key prerequisite here is work on benchmarking. On the team, Michael Ryan and Shangyin Tan are leading these efforts. More soon.

- Quality: The goal here is optimizers that extract, on average, 20% more on representative tasks than MIPROv2 and BetterTogether, under the usual conditions — like a few hundred inputs with labels and a good metric starting from a decent zero-shot program. Various efforts here are led by Dilara Soylu, Michael Ryan, Josh Purtell, Krista Opsahl-Ong, and Isaac Miller.

- Efficiency: The goal here is optimizers that match the current best scores from MIPROv2 and BetterTogether but under 1-2 challenges like: (i) starting from only 10-20 inputs with labels, (ii) starting with a weak zero-shot program that scores 0%, (iii) where significant misalignment exists between train/validation and test, or (iii) where the user supplies no metric but provides a very small number of output judgments.


## 3) Building end-to-end tutorials from DSPy’s ML workflow to deployment.

Using DSPy well for solving a new task is just doing good machine learning with LMs, but teaching this is hard. On the one hand, it's an iterative process: you make some initial choices, which will be sub-optimal, and then you refine them incrementally. It's highly exploratory: it's often the case that no one knows yet how to best solve a problem in a DSPy-esque way. One the other hand, DSPy offers many emerging lessons from several years of building LM systems, in which the design space, the data regime, and many other factors are new both to ML experts and to the very large fraction of users that have no ML experience.

Though current docs do address [a bunch of this](learn/index.md) in isolated ways, one thing we've learned is that we should separate teaching the core DSPy language (which is ultimately pretty small) from teaching the emerging ML workflow that works well in a DSPy-esque setting. As a natural extension of this, we need to place more emphasis on steps prior and after to the explicit coding in DSPy, from data collection to deployment that serves and monitors the optimized DSPy program in practice. This is just starting but efforts will be ramping up led by Omar Khattab, Isaac Miller, and Herumb Shandilya.


## 4) Shifting towards more interactive optimization & tracking.

Right now, a DSPy user has a few ways to observe and tweak the process of optimization. They can study the prompts before, during, and after optimization methods like `inspect_history`, built-in logging, and/or the metadata returned by optimizers. Similarly, they can rely on `program.save` and `program.load` to potentially adjust the optimized prompts by hand. Alternatively, they can use one of the many powerful observability integrations — like from Phoenix Arize, LangWatch, or Weights & Biases Weave — to observe _in real time_ the process of optimization (e.g., scores, stack traces, successful & failed traces, and candidate prompts). DSPy encourages iterative engineering by adjusting the program, data, or metrics across optimization runs. For example, some optimizers allow “checkpointing” — e.g., if you optimize with BootstrapFewShotWithRandomSearch for 10 iterations then increase to 15 iterations, the first 10 will be loaded from cache.

While these can accomplish a lot of goals, there are two limitations that future versions of DSPy will seek to address.

1. In general, DSPy’s (i) observability, (ii) experimental tracking, (iii) cost management, and (iii) deployment of programs should become first-class concerns via integration with tools like MLFlow. We will share more plans addressing this for DSPy 2.6 in the next 1-2 months.

2. DSPy 3.0 will introduce new optimizers that prioritize ad-hoc, human-in-the-loop feedback. This is perhaps the only substantial paradigm shift we see as necessary in the foreseeable future in DSPy. It involves various research questions at the level of the abstractions, UI/HCI, and ML, so it is a longer-term goal that we will share more about in the next 3-4 month.

---

