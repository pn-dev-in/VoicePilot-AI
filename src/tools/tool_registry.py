from tools.notes import save_note, read_notes
from tools.new_tools import get_weather, get_news, search_web, play_music, stop_music,  tell_joke, random_fact 

TOOLS = {
    "save_note": {"func": save_note, "description": "Save a note"},
    "read_notes": {"func": read_notes, "description": "Read all notes"},
    "get_weather": {"func": get_weather, "description": "Get current weather for a city"},
    "get_news": {"func": get_news, "description": "Get latest news headlines by topic"},
    "search_web": {"func": search_web, "description": "Search the internet for information"},
    "play_music": {"func": play_music, "description": "Play a song from YouTube by name"},
    "stop_music": {"func": stop_music, "description": "Stop currently playing music"},
    "tell_joke": {"func": tell_joke, "description": "Tell a joke"},
    "random_fact": {"func": random_fact, "description": "Give a random interesting fact"}
}