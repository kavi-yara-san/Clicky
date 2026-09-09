from tools.base_tool import Tool
from typing import Any, Callable, Dict, List, Optional


class ToolRegistry:
    """Registry for managing tools and executing them."""

    def __init__(self, tools: Optional[list[Callable]] = None) -> None:
        self.tools: Dict[str, Tool] = {}
        if tools:
            for tool in tools:
                self.register(tool)

    def register(self, tool: Tool, description: str = None) -> None:
        tool = Tool(tool, description) if isinstance(tool, Callable) else tool
        self.tools[tool.name] = tool

    @property
    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        """list all registered tools and their schemas."""
        return {name: tool.schema for name, tool in self.tools.items()}

    @property
    def schema(self) -> list[Dict[str, Any]]:
        """return the schemas of all registered tools"""
        return [tool.schema for tool in self.tools.values()]

    def execute(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' is not registered.")
        tool = self.tools[tool_name]
        return tool.exe(**kwargs)
