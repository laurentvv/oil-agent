import os
import multiprocessing
import logging
from pathlib import Path
from typing import Any, List, Optional, Dict
from llama_cpp import Llama
from smolagents.models import Model, ChatMessage, MessageRole, get_clean_message_list
import dspy

log = logging.getLogger(__name__)

def detect_hardware():
    cpu_count = multiprocessing.cpu_count()
    has_gpu = False

    import llama_cpp
    try:
        has_gpu = llama_cpp.llama_supports_gpu_offload()
    except Exception:
        pass

    if not has_gpu:
        if os.path.exists("/dev/kfd") or os.path.exists("/dev/dri"):
            has_gpu = True

    return {
        "has_gpu": has_gpu,
        "cpu_count": cpu_count,
        "threads": max(cpu_count - 1, 1)
    }

class LlamaCppManager:
    _instance = None
    _model_path = None

    @classmethod
    def get_instance(cls, model_path: str = None):
        if cls._instance is None:
            if model_path is None:
                raise ValueError("Model path must be provided for the first initialization")

            cls._model_path = model_path
            hw = detect_hardware()
            log.info(f"Initializing Llama with model: {model_path}")
            log.info(f"Hardware detected: {hw}")

            cls._instance = Llama(
                model_path=model_path,
                n_gpu_layers=-1 if hw["has_gpu"] else 0,
                n_threads=hw["threads"],
                n_ctx=8192,
                verbose=False
            )
        return cls._instance

class SmolLlamaCppModel(Model):
    def __init__(self, model_path: str, **kwargs):
        super().__init__(**kwargs)
        self.llm = LlamaCppManager.get_instance(model_path)

    def generate(self, messages, stop_sequences=None, response_format=None, **kwargs):
        formatted_messages = get_clean_message_list(
            messages,
            role_conversions={"assistant": "assistant", "user": "user", "system": "system"}
        )

        params = {
            "messages": formatted_messages,
            "stop": stop_sequences,
            "max_tokens": kwargs.get("max_new_tokens", 2048),
            "temperature": kwargs.get("temperature", 0.7),
        }

        response = self.llm.create_chat_completion(**params)
        content = response["choices"][0]["message"]["content"]

        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content=content
        )

class LlamaCppDSPy(dspy.LM):
    def __init__(self, model_path: str, **kwargs):
        super().__init__(model="llama-cpp-python")
        self.llm = LlamaCppManager.get_instance(model_path)

    def forward(self, prompt: str | None = None, messages: List[Dict[str, Any]] | None = None, **kwargs):
        params = {**self.kwargs, **kwargs}

        if messages:
            response = self.llm.create_chat_completion(
                messages=messages,
                stop=params.get("stop"),
                max_tokens=params.get("max_tokens"),
                temperature=params.get("temperature")
            )
            content = response["choices"][0]["message"]["content"]
        else:
            response = self.llm.create_completion(
                prompt=prompt,
                stop=params.get("stop"),
                max_tokens=params.get("max_tokens"),
                temperature=params.get("temperature")
            )
            content = response["choices"][0]["text"]

        class Choice:
            def __init__(self, text, message=None):
                self.text = text
                self.message = message
                self.finish_reason = "stop"

        class Message:
            def __init__(self, content):
                self.content = content

        class Result:
            def __init__(self, content):
                self.choices = [Choice(content, Message(content))]
                self.usage = {"total_tokens": 0}

        return Result(content)
