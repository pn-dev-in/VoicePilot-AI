# src/brain/llm.py (updated ask_llm function)
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_groq_api_key
from brain.conversation import get_conversation_history, add_exchange
from tools.executor import execute_tool
from groq import Groq

client = Groq(api_key=get_groq_api_key())
MODEL = "llama-3.1-8b-instant"

# The new, more detailed system prompt that defines the available tools
SYSTEM_PROMPT = """You are a helpful AI assistant. You can answer general questions from your knowledge, and you can also use these tools:

TOOLS:
1. get_weather – {"city_name": "city"}
2. get_news – {"topic": "topic"}
3. search_web – {"query": "search term"}
4. play_music – {"song_name": "song name"}
5. stop_music – {}
6. tell_joke – {} (no arguments)
7. random_fact – {} (no arguments)

If the user asks for a joke, tell a joke. If they want a fact, give a fact. For weather, news, search, music, use the appropriate tool.
Otherwise, answer directly in plain text.

Respond with JSON for tool requests: {"tool": "tool_name", "arguments": {...}}
Otherwise respond in natural language.

Keep answers concise.
"""

def ask_llm(user_text: str) -> str:
    # 1. Build the conversation history
    history = get_conversation_history()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_text}
    ]

    # 2. First call: Let the LLM decide if a tool is needed
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0,
            max_tokens=300
        )
        llm_output = response.choices[0].message.content.strip()
        print(f"🤖 LLM raw response: {llm_output}")
    except Exception as e:
        print(f"LLM error: {e}")
        return "Sorry, I'm having trouble connecting to my brain."

    # 3. Check if the output is a tool request (starts with "{" and ends with "}")
    if llm_output.startswith("{") and llm_output.endswith("}"):
        try:
            tool_request = json.loads(llm_output)
            tool_name = tool_request.get("tool")
            arguments = tool_request.get("arguments", {})

            if tool_name and tool_name in ["get_weather", "get_news", "search_web", "play_music"]:
                # Execute the requested tool
                tool_result = execute_tool(tool_name, arguments)
                print(f"🔧 Tool result: {tool_result}")

                # 4. Second call: Give the tool result back to the LLM to formulate the final answer
                messages.append({"role": "assistant", "content": llm_output})
                messages.append({"role": "user", "content": f"The tool returned this data: {json.dumps(tool_result)}. Please provide a helpful natural language answer based on this data."})

                final_response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=300
                )
                final_answer = final_response.choices[0].message.content.strip()
                add_exchange(user_text, final_answer)
                return final_answer
        except json.JSONDecodeError:
            # If it's not valid JSON, treat as plain text
            pass

    # 5. If no tool was used, just return the plain text answer
    add_exchange(user_text, llm_output)
    return llm_output