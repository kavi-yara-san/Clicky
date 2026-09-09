import asyncio
import os
from agent.core import Agent
from tools.tools import tool_registry,get_file
from agent.orchestration import Orchestration
from prompts.load import get_instruction
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()


if not os.path.exists("static"):
    os.makedirs("static")


app.mount("/static", StaticFiles(directory="static"), name="static")


class PromptRequest(BaseModel):
    """prompt data validation"""
    prompt: str


@app.get("/", response_class=HTMLResponse)
async def render_ui():
    """Serves the main sketch ui page."""
    return FileResponse("ui.html")


@app.post("/run")
async def main(request: PromptRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    agent = Agent("main", system_instruction=get_instruction(), tools=tool_registry)
    orchestration = Orchestration(agent, tool_registry)
    print(f"Received prompt: {request.prompt}")
    result = await orchestration.run(request.prompt)
    file = get_file()
    with open(file, "r", encoding="utf-8") as f:
        html_code = f.read()
    return {"html_code": html_code}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
