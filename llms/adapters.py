from abc import abstractmethod
from typing import Any, List, Optional, Callable
import google.genai as genai
from dataclasses import dataclass


@dataclass
class ResponseChunk:
    """A dataclass representing a chunk of response from the model."""

    text: str
    is_final: bool = False
    function_calls: Optional[List[dict]] = None






class Adapter:
    """An abstract base class for adapters for different LLM apis."""


    @abstractmethod
    async def generate(self, msg: str) -> Any:
        """Generate content based on the input message."""
        pass

    @abstractmethod
    def _to_contents(self, msg) -> Any:
        """Convert input messages into the model-specific content format."""
        pass

    @abstractmethod
    def _from_contents(self, chunk) -> ResponseChunk:
        """Convert model-specific content format back into a ResponseChunk."""
        pass






class GeminAdapter(Adapter):
    """A adapter for interacting with the Gemini API."""


    def __init__(
        self,
        Api_key: str,
        tools: Optional[List[Callable]] = None,
        system_instruction: str = None,
    ) -> None:
        #print("Initializing GeminAdapter with API key:", Api_key)
        self.gemin_client = genai.Client(api_key=Api_key)
        self.tools = tools or []
        self.system_instruction = system_instruction

        # content cache for avoid re-execution(_to_content)
        self._content_cache : List[Any] = []
        self._cache_id: Optional[int] = None
        self._cache_len: int = 0



    async def generate(self, msg: str) -> Any:
        """model inference"""

        contents = self._to_contents(msg)
        response = await self.gemin_client.aio.models.generate_content_stream(
            model="gemini-3.6-flash",
            contents=contents,
            config=genai.types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                tools=[{"function_declarations": self.tools.schema}],
            ),
        )

        async for chunk in response:
            # print(chunk.text)
            yield self._from_contents(chunk)






    def _to_contents(self, msg) -> list:
        """convert input payload into the model-specific content format."""

        if isinstance(msg, str):
            return msg

        if id(msg) != self._cache_id:
            self._content_cache = []
            self._cache_len = 0
        self._content_cache += [
            self._convert_format(m) for m in msg[self._cache_len :]
        ]
        self._cache_id = id(msg)
        self._cache_len = len(msg)

        return list(self._content_cache)




    def _convert_format(self, msg) -> Any:
        """convert gemini compitable msg format"""

        role_map = {"assistant": "model", "tool": "user", "system": "user"}
        role = role_map.get(msg.get("role"), msg.get("role", "user"))
        content = msg.get("content", "")

        if isinstance(content, str):
            parts = [genai.types.Part.from_text(text=content)]

        elif isinstance(content, list):
            parts = []

            for p in content:
                if isinstance(p, str):
                    parts.append(genai.types.Part.from_text(text=p))

                elif isinstance(p, dict) and p.get("type") == "function_call":
                    # construct function-call + attach required thought_signature
                    fn_call = genai.types.FunctionCall(
                        name=p["name"],
                        args=dict(p.get("args", {}))
                    )
                    parts.append(
                        genai.types.Part(
                            function_call=fn_call,
                            thought_signature=b"",
                        )
                    )
                elif isinstance(p, genai.types.Part):
                    # if is type compitable
                    parts.append(p)
                else:
                    # prevent error if ....
                    parts.append(genai.types.Part.from_text(text=str(p)))
        else:
            parts = [genai.types.Part.from_text(text=str(content))]

        return genai.types.Content(role=role, parts=parts)



    

    def _from_contents(self, chunk) -> ResponseChunk:
        """convert model-specific content format back into a Response.chunk."""
        text = ""
        tool_calls = []
        is_final = False

        if hasattr(chunk, "text") and chunk.text:
            text = chunk.text

        if hasattr(chunk, "function_calls") and chunk.function_calls:
            for call in chunk.function_calls:
                tool_calls.append({"name": call.name, "args": call.args})

        is_final = False
        if hasattr(chunk, "candidates") and chunk.candidates:
            candidate = chunk.candidates[0]
            is_final = candidate.finish_reason is not None

        return ResponseChunk(text=text, is_final=is_final, function_calls=tool_calls)
