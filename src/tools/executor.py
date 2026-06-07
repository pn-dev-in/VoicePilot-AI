from tools.tool_registry import TOOLS

def execute_tool(tool_name: str, content: str = "") -> str:
    if tool_name not in TOOLS:
        return "Tool not allowed."
    func = TOOLS[tool_name]["func"]
    return func(content) if content else func()