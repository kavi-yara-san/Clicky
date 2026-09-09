from tools.registory import ToolRegistry
from typing import Any, Callable, Dict, List, Optional
import os
import webbrowser

tool_registry = ToolRegistry()

_file = {'current_file': None}
if not os.path.exists("output"):
    os.makedirs('output')
file = os.path.join("output", "ff")

@tool_registry.register
def file_write(code: str,filename: str) -> str:    
    """file_write: use for the first draft, or when >50% of the file needs to change.
    Always writes the full file — don't use it for small tweaks."""
    
    file = os.path.join("output", filename)
    with open(file, "w", encoding="utf-8") as f:
        f.write(code)
    _file["current_file"] = file
    return f"File written successful - [{file}]."


@tool_registry.register
def file_read() -> str:
    """file_read: call before editing if you're not certain of the current file content."""
    #print("agent reads..")
    file = _file["current_file"]
    if file is None:
        return "No active file."
    if not os.path.exists(file):
        return "File does not exist."
    with open(file, "r", encoding="utf-8") as f:
        return f.read()


@tool_registry.register
def file_delete() -> str:
    """file_delete: only use if the user explicitly asks to start over."""
    file = _file["current_file"]
    if file is None:
        return "No active file to delete."
    if not os.path.exists(file):
        return f"File does not exist: {file}"
    os.remove(file)
    _file["current_file"] = None
    return "File deleted successfully."

@tool_registry.register
def edit_file(old_code_snippet: str, new_code_snippet: str) -> str:
    """edit_file: use for targeted changes (adjusting a color, fixing one function, tweaking a label).
    old_code_snippet must match the file's exact current content — read the file first with file_read if unsure of exact formatting.
    """
    file = _file["current_file"]
    if not os.path.exists(file):
        return "File does not exist."
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    if old_code_snippet not in content:
        return "old_code_snippet not found in file — no changes made."
    content = content.replace(old_code_snippet, new_code_snippet)
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

    return "File edited successfully."


@tool_registry.register
def append_file(code:str,anchor: Optional[str] = None):
    """file append : used to add a new code to the active file without replacing anything
     e.g add new section m function and so ...
     if [anchor] is given the new code insert after the first occurance.
     if [anchor] is not given it add code end of the file.
     """

    file = _file["current_file"]
    if file is None:
        return "No active file. Call file_write first."
    if not os.path.exists(file):
        return f"File does not exist: {file}"

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    if anchor is None:                      # than add to eof
        content = content + "\n" + code
    else:
        count = content.count(anchor)
        if count == 0:
            return "anchor not found in file — no changes made."
        if count > 1:
            return (
                f"anchor appears {count} times in the file — "
                "make it more specific so the insertion point..."
            )
        content = content.replace(anchor, anchor + "\n" + code, 1)

    with open(file,"w",encoding="utf-8") as f:
        f.write(content)

    return f"code appended to [{file}]"


def get_file() -> str:
    return _file["current_file"] if _file["current_file"] is not None else " "