from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Callable
from llms.client import Client

# from google.genai import genai
import google.genai as genai
import os
from config.config import API_KEY, MODEL_NAME


class BaseAgent(ABC):
    @abstractmethod
    def act(self, state):
        pass


class Agent(BaseAgent):
    def __init__(
        self, name: str, system_instruction: str, tools: Optional[List[Callable]] = None
    ) -> None:
        self.name = name
        self.system_instruction = system_instruction
        self.tools = tools or []

        self.client = Client(
            config={"ADAPTER": MODEL_NAME, "API_KEY": API_KEY},
            tools=self.tools,
            system_instruction=self.system_instruction,
        )

    def act(self, msg: str) -> Any:
        return self.client.get_adapter.generate(msg)
