from llms.adapters import GeminAdapter, Adapter
from typing import Any, List, Optional, Callable


class ClientConfigError(Exception):
    """exception for client configuration errors."""

    pass


class Client:

    def __init__(
        self,
        config: dict,
        tools: Optional[List[Callable]] = None,
        system_instruction: str = None,
    ) -> None:
        
        self.config = config
        self.tools = tools or []
        self.system_instruction = system_instruction
        self._adapter: Optional[Adapter] = None

    @property
    def get_adapter(self) -> Adapter:
        """Return  instance of adapters based on the configuration."""
        if not self.config or "ADAPTER" not in self.config:
            raise ClientConfigError(
                "Adapter type must be specified in the configuration."
            )

        if self._adapter is None:
            if (
                self.config.get("ADAPTER") == "gemini"
            ):  # now only support gemini adapter,  add more adapters in the future
                api_key = self.config.get("API_KEY")
                self._adapter = GeminAdapter(
                    api_key, tools=self.tools, system_instruction=self.system_instruction
                )
            else:
                raise ClientConfigError(
                    f"unsupported adapters type: {self.config.get('ADAPTER')}"
                )
        return self._adapter