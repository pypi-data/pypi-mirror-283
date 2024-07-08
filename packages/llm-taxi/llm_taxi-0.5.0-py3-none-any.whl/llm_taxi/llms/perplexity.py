from typing import ClassVar

from llm_taxi.clients.perplexity import Perplexity as PerplexityClient
from llm_taxi.llms.openai import OpenAI
from llm_taxi.types import NotSupportedOr


class Perplexity(PerplexityClient, OpenAI):
    param_mapping: ClassVar[dict[str, NotSupportedOr[str]]] = {}
