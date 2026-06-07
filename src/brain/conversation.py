# In-memory conversation history (per session)
_conversation = []  # list of {role, content}
MAX_HISTORY = 6  # keep last 3 exchanges (user+assistant = 2 messages each)

def add_exchange(user_msg: str, assistant_msg: str):
    _conversation.append({"role": "user", "content": user_msg})
    _conversation.append({"role": "assistant", "content": assistant_msg})
    # Trim to MAX_HISTORY
    while len(_conversation) > MAX_HISTORY:
        _conversation.pop(0)

def get_conversation_history():
    return _conversation.copy()

def reset_conversation():
    global _conversation
    _conversation = []