from typing import ClassVar

from llm_taxi.clients.openrouter import OpenRouter as OpenRouterClient
from llm_taxi.llms.openai import OpenAI
from llm_taxi.types import NotSupportedOr


class OpenRouter(OpenRouterClient, OpenAI):
    param_mapping: ClassVar[dict[str, NotSupportedOr[str]]] = {}
