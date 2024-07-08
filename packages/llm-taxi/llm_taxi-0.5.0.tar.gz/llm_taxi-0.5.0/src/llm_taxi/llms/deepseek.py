from typing import ClassVar

from llm_taxi.clients.deepseek import DeepSeek as DeepSeekClient
from llm_taxi.llms.openai import OpenAI
from llm_taxi.types import NOT_SUPPORTED, NotSupportedOr


class DeepSeek(DeepSeekClient, OpenAI):
    param_mapping: ClassVar[dict[str, NotSupportedOr[str]]] = {
        "temperature": "temperature",
        "max_tokens": "max_tokens",
        "top_k": NOT_SUPPORTED,
        "top_p": "top_p",
        "stop": "stop",
        "seed": NOT_SUPPORTED,
    }
