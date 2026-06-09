# 🎙️ VoicePilot AI

### Private Voice-First AI Assistant with Memory, Tool Use & Conversational Intelligence

> **Talk to your computer naturally. Wake it with your voice, ask questions, retrieve information, and maintain long-term conversations through an intelligent AI assistant designed for privacy, speed, and extensibility.**

---

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com)
[![Whisper](https://img.shields.io/badge/STT-Whisper-green.svg)](https://openai.com/research/whisper)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## 🌟 Overview

VoicePilot AI is a voice-first conversational assistant that combines wake-word detection, speech recognition, large language models, memory management, and intelligent tool usage into a seamless user experience.

The assistant continuously listens for a wake word, processes spoken commands, understands user intent, retrieves information from tools and memory systems, generates intelligent responses using an LLM, and responds naturally using text-to-speech.

Unlike traditional voice assistants, VoicePilot AI focuses on privacy, modularity, extensibility, and local-first architecture, giving users full control over their personal data and interactions.

---

## ✨ Key Features

### 🎙️ Voice Interaction

* Wake-word activated assistant
* Natural voice conversations
* Real-time speech recognition
* Context-aware responses
* Adjustable speech output speed
* Follow-up conversation support

### 🧠 Long-Term Memory

* Persistent memory across sessions
* User profile management
* Fact storage and recall
* Personalized interactions
* JSON-based local memory system

### 🤖 AI Reasoning

* Groq-powered LLM integration
* Fast conversational responses
* Context retention
* Intent understanding
* Natural language processing

### 🛠️ Tool Integration

Built-in tools include:

* Weather Information
* News Summaries
* Web Search
* Random Facts
* Joke Generator
* Personal Notes
* Memory Recall

### 🔒 Privacy-Focused Design

* Local wake-word detection
* Local speech processing pipeline
* User-controlled memory storage
* No vendor lock-in
* Extensible architecture

### ⚙️ Extensible Framework

* Modular tool system
* Easy plugin integration
* Configurable components
* Swappable LLM providers
* Future local model support

---

## 🏗️ System Architecture

```text
Microphone Input
       │
       ▼
Wake Word Detection
(openWakeWord)
       │
       ▼
Speech-to-Text
(Whisper)
       │
       ▼
Intent Classification
       │
       ▼
 ┌────────────┬────────────┬────────────┐
 │            │            │
 ▼            ▼            ▼
Memory      Tools         LLM
System    Execution    Reasoning
 │            │            │
 └────────────┴────────────┘
              │
              ▼
Response Generation
              │
              ▼
Text-to-Speech
(pyttsx3)
              │
              ▼
Speaker Output
```

---

## 🚀 Core Capabilities

### Wake Word Activation

The assistant remains idle until it detects the configured wake word, reducing unnecessary processing and creating a hands-free experience.

### Speech Recognition

Voice commands are converted into text using Whisper for accurate speech-to-text processing.

### Intent Understanding

Commands are classified and routed to the most appropriate subsystem:

* Memory
* Tools
* LLM
* Safety Layer

### Long-Term Memory

The assistant can remember user-provided information such as:

```text
"My name is Alex"

"I work as a developer"

"I prefer Python"
```

and recall these details in future conversations.

### Tool Calling

The assistant can execute external tools when needed.

Examples:

```text
What's the weather today?

Tell me a joke.

Give me a random fact.

Search for Python tutorials.
```

### Conversational AI

General knowledge and reasoning are handled through Groq-powered LLM responses.

---

## 📊 Project Highlights

* Voice-first interaction model
* Wake-word activation system
* Persistent memory architecture
* Intelligent tool orchestration
* Real-time speech processing
* Modular AI agent design
* Privacy-focused implementation
* Extensible plugin ecosystem
* Production-style architecture
* Local-first user experience

---

## 🎯 Example Commands

| User Command                     | System Action                 |
| -------------------------------- | ----------------------------- |
| "What's the weather in London?"  | Retrieves weather information |
| "Tell me a joke"                 | Returns a joke                |
| "Give me a random fact"          | Fetches an interesting fact   |
| "Search for Python tutorials"    | Performs a web search         |
| "My name is Alex"                | Stores memory                 |
| "What's my name?"                | Retrieves stored memory       |
| "What is the capital of France?" | Uses LLM reasoning            |
| "Bye"                            | Ends current session          |

---

## 🛠️ Technology Stack

| Layer                | Technology           |
| -------------------- | -------------------- |
| Programming Language | Python               |
| Speech Recognition   | Whisper              |
| Wake Word Detection  | openWakeWord         |
| Language Model       | Groq (Llama 3.1)     |
| Text-to-Speech       | pyttsx3              |
| Memory Storage       | JSON                 |
| Web Search           | DuckDuckGo           |
| Weather Service      | wttr.in              |
| News Retrieval       | RSS Feeds            |
| Architecture         | Modular Agent System |

---

## 📂 Project Structure

```text
VoicePilot-AI/

├── src/
│
├── audio/
│   ├── speech_to_text.py
│   └── vad.py
│
├── brain/
│   ├── llm.py
│   └── conversation.py
│
├── memory/
│   ├── long_term.py
│   ├── profile.py
│   └── memory_store.py
│
├── tools/
│   ├── weather.py
│   ├── news.py
│   ├── jokes.py
│   ├── search.py
│   └── tool_registry.py
│
├── safety/
│   ├── intent_classifier.py
│   └── guardrails.py
│
├── voice/
│   └── tts.py
│
├── wakeword/
│   └── detector.py
│
├── modes/
│   ├── daily_briefing.py
│   └── mode_detector.py
│
├── config.py
├── main.py
│
├── user_data/
│   ├── memory.json
│   ├── profile.json
│   └── notes/
│
├── requirements.txt
├── README.md
└── .env
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/pn-dev-in/VoicePilot-AI.git

cd VoicePilot-AI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### Run Application

```bash
python src/main.py
```

---

## ⚙️ Configuration

### Change Wake Word

Modify the detector configuration:

```python
wake_word = "jarvis"
```

Supported examples:

* jarvis
* alexa
* hey_mycroft
* hey_rhasspy

---

## 🔧 Extending The Assistant

Adding a new tool is straightforward.

Create:

```python
def get_stock_price(symbol):
    return {"price": 123.45}
```

Register the tool inside:

```text
src/tools/tool_registry.py
```

Update:

```text
src/brain/llm.py
```

to expose the tool to the assistant.

---

## 🎓 Skills Demonstrated

This project demonstrates practical experience in:

✅ Artificial Intelligence

✅ Conversational AI

✅ AI Agent Development

✅ Speech Recognition

✅ Wake Word Detection

✅ Tool Calling Systems

✅ Long-Term Memory Architectures

✅ Prompt Engineering

✅ API Integration

✅ Python Development

✅ System Design

✅ Software Architecture

---

## 🚀 Future Roadmap

* Local LLM support via Ollama
* Desktop GUI interface
* Smart home integration
* Calendar and email assistant
* Retrieval-Augmented Generation (RAG)
* Document assistant
* Voice cloning
* Multi-user profiles
* Mobile companion application

---

## 📈 Why This Project Matters

Most modern assistants rely heavily on proprietary cloud ecosystems.

VoicePilot AI demonstrates how a conversational AI assistant can be built using open-source technologies, local audio processing, persistent memory, intelligent tool orchestration, and modern LLMs while maintaining user privacy and control.

The project serves as both a practical productivity tool and a showcase of modern AI engineering concepts.

---

## 👨‍💻 Author

### Pravesh Nandanwar

Computer Science & Engineering

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.

Feedback, feature requests, and contributions are always welcome.

---

### 🎙️ Speak Naturally. Think Smarter. Stay Private.
