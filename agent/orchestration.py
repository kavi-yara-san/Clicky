from agent.core import Agent
from tools.tools import ToolRegistry
import asyncio


class Orchestration:
    """Agent orchestration"""

    def __init__(self, agent: Agent, tool_registry: ToolRegistry):
        self.max_steps = 10
        self.agent = agent
        self.tool_registry = tool_registry

    async def run(self, prompt: str):
        messages = [{"role": "user", "content": prompt}]

        for _ in range(self.max_steps):
            print("intiating model inference...")
            response = self.agent.act(messages)
            accumulated_text = ""
            function_calls_made = []

            # stream processing / chunk aggregation
            async for chunk in response:
                if chunk.text:
                    accumulated_text += chunk.text
                if chunk.function_calls:
                    function_calls_made.extend(chunk.function_calls)

            # conversation history
            model_parts = []
            if accumulated_text:
                model_parts.append(accumulated_text)
            for call in function_calls_made:
                model_parts.append(
                    {
                        "type": "function_call",
                        "name": call["name"],
                        "args": call["args"],
                    }
                )

            messages.append({"role": "assistant", "content": model_parts})

            # if no function calls were requested than task is complete
            if not function_calls_made:
                print("\n[Final Response]:", accumulated_text)
                break


            #conc exe
            tool_response_parts = await asyncio.gather(                            
                *[
                    asyncio.to_thread(self._exe_tool, call)
                    for call in function_calls_made
                ]
            )

            messages.append({"role": "user", "content": tool_response_parts})

    def _exe_tool(self, call):
        tool_name = call["name"]
        tool_args = call["args"]
        # print(f"\n[Tool Call]: {tool_name} ({tool_args})")
        result = self.tool_registry.execute(tool_name, **tool_args)
        return {
            "type": "function_response",
            "name": tool_name,
            "response": {"result": result},
        }
