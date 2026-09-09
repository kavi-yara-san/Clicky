import inspect
from typing import Callable, Any, Dict, Optional, List


class Tool:
    """Tool class that wraps a tool function and provides metadata for schema generation."""

    def __init__(
        self, func: Callable, description: str = None, Model: str = None
    ) -> None:
        self.func = func
        self.name = func.__name__
        self.description = description or func.__doc__
        self.model = Model
        self.schema = self._get_schema()

    def _get_schema(self) -> Dict[str, Any]:
        """should return the schema of the tool in a format compatible with the model."""
        signature = inspect.signature(self.func)
        properties = {}
        required = []
        for name, param in signature.parameters.items():
            py_type = param.annotation
            type = self.type_mapping.get(py_type, "string")
            properties[name] = {"type": type}
            if param.default is inspect.Parameter.empty:
                required.append(name)

        if self.model == "gemini":
            return self._gemini_tool_schema(properties, required)
        else:
            return {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            }

    @property
    def type_mapping(self) -> Dict[type, str]:
        return {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

    def exe(self, **kwargs) -> Any:
        return self.func(**kwargs)

    def _gemini_tool_schema(
        self, properties: Dict[str, Any], required: List[str]
    ) -> Dict[str, Any]:
        """Return the tool schema in a format compatible with Gemini API."""

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "OBJECT",
                "properties": properties,
                "required": required,
            },
        }
