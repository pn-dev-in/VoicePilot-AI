# src/tools/new_tools.py
import requests
import webbrowser
import urllib.parse
from datetime import datetime
import re
import subprocess
import os

# ------------------------------------------------------------
# 1. WEATHER – using wttr.in (no API key)
# ------------------------------------------------------------
def get_weather(city_name: str) -> dict:
    """Fetch weather from wttr.in. Example: city_name = "London" """
    try:
        url = f"https://wttr.in/{city_name}?format=%l:+%c+%t,+feels+like+%f,+humidity+%h,+wind+%w"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            text = response.text.strip()
            return {"weather_summary": text}
        else:
            return {"error": f"Weather not found for {city_name}"}
    except Exception as e:
        return {"error": f"Could not fetch weather: {str(e)}"}


# ------------------------------------------------------------
# 2. NEWS – using DuckDuckGo RSS (no API key)
# ------------------------------------------------------------
def get_news(topic: str = "latest") -> dict:
    """Fetch news headlines for a given topic using DuckDuckGo RSS."""
    try:
        search_query = topic if topic != "latest" else "world news"
        url = f"https://rss.app/feeds/duckduckgo.xml?q={urllib.parse.quote(search_query)}"
        # Alternative: use a simple RSS feed from a news source
        # We'll use a free RSS aggregator
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Parse XML (very basic)
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            headlines = []
            for item in items[:5]:
                title = item.find("title").text if item.find("title") is not None else ""
                headlines.append(title)
            return {"topic": topic, "headlines": headlines}
        else:
            # Fallback: use a simple text-based news API (no key)
            fallback_url = f"https://www.drudgereport.com/rss.xml"  # static
            resp2 = requests.get(fallback_url, timeout=10)
            if resp2.status_code == 200:
                root2 = ET.fromstring(resp2.content)
                items2 = root2.findall(".//item")
                headlines2 = []
                for item in items2[:5]:
                    title = item.find("title").text if item.find("title") is not None else ""
                    headlines2.append(title)
                return {"topic": topic, "headlines": headlines2}
            return {"error": "Could not fetch news."}
    except Exception as e:
        return {"error": f"News error: {str(e)}"}


# ------------------------------------------------------------
# 3. WEB SEARCH – using DuckDuckGo HTML (no API key)
# ------------------------------------------------------------
def search_web(query: str) -> dict:
    """Search the web using DuckDuckGo's HTML interface."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Extract results with regex (simple)
            results = []
            for match in re.finditer(r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>', response.text):
                link = match.group(1)
                title = match.group(2)
                results.append({"title": title, "url": link})
                if len(results) >= 3:
                    break
            return {"query": query, "results": results}
        else:
            return {"error": "Search failed."}
    except Exception as e:
        return {"error": f"Search error: {str(e)}"}


# ------------------------------------------------------------
# 4. MUSIC – play audio from YouTube (using yt-dlp + pygame)
# ------------------------------------------------------------
def play_music(song_name: str) -> dict:
    query = urllib.parse.quote_plus(f"{song_name} official audio")
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return {"message": f"Opened YouTube search for '{song_name}' in your browser."}


# ------------------------------------------------------------
# 5. STOP MUSIC
# ------------------------------------------------------------
def stop_music() -> dict:
    """Stop currently playing music."""
    try:
        import pygame
        pygame.mixer.music.stop()
        return {"status": "stopped", "message": "Music stopped."}
    except:
        return {"error": "No music playing."}
    
# ------------------------------------------------------------
# 5. TELL A JOKE (free, no API)
# ------------------------------------------------------------
def tell_joke() -> dict:
    """Fetch a random joke from icanhazdadjoke.com (free, no key)."""
    try:
        headers = {'Accept': 'application/json', 'User-Agent': 'Assistant/1.0'}
        response = requests.get('https://icanhazdadjoke.com/', headers=headers, timeout=5)
        if response.status_code == 200:
            joke = response.json().get('joke', "Why don't scientists trust atoms? Because they make up everything!")
            return {"joke": joke}
        else:
            # Fallback jokes list
            fallback_jokes = [
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call fake spaghetti? An impasta!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!"
            ]
            import random
            return {"joke": random.choice(fallback_jokes)}
    except Exception as e:
        print(f"Joke error: {e}")
        return {"joke": "Why did the computer keep freezing? It left its Windows open!"}

# ------------------------------------------------------------
# 6. RANDOM FACT (free, no API)
# ------------------------------------------------------------
def random_fact() -> dict:
    """Get a random fact from uselessfacts.jsph.pl."""
    try:
        response = requests.get('https://uselessfacts.jsph.pl/api/v2/facts/random', timeout=5)
        if response.status_code == 200:
            fact = response.json().get('text', "A group of flamingos is called a flamboyance.")
            return {"fact": fact}
        else:
            fallback_facts = [
                "Octopuses have three hearts.",
                "Bananas are berries, but strawberries aren't.",
                "Honey never spoils. Archaeologists found 3000-year-old honey in tombs."
            ]
            import random
            return {"fact": random.choice(fallback_facts)}
    except Exception as e:
        print(f"Fact error: {e}")
        return {"fact": "The Eiffel Tower can be 15 cm taller during summer due to heat expansion."}