from typing import ClassVar

from llm_taxi.clients.dashscope import DashScope as DashScopeClient
from llm_taxi.llms.openai import OpenAI
from llm_taxi.types import NOT_SUPPORTED, NotSupportedOr


class DashScope(DashScopeClient, OpenAI):
    param_mapping: ClassVar[dict[str, NotSupportedOr[str]]] = {
        "temperature": "temperature",
        "max_tokens": "max_tokens",
        "top_k": NOT_SUPPORTED,
        "top_p": "top_p",
        "stop": "stop",
        "seed": "seed",
    }
