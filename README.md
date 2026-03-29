<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=40&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&height=80&lines=⚡+JARVIS+AI+Shell;Your+Personal+AI+OS+Controller" alt="Jarvis AI" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-00d4ff?style=for-the-badge)](https://ollama.ai)
[![Mistral](https://img.shields.io/badge/LLM-Mistral%207B-purple?style=for-the-badge)](https://mistral.ai)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)](https://github.com/aryxn1233/JARVIS)

<br/>

> **"Just A Rather Very Intelligent System"**  
> A locally-running, voice-activated AI OS assistant powered by Mistral 7B and CodeLlama — no cloud, no subscriptions, pure local intelligence.

<br/>

[✨ Features](#-features) • [🚀 Quick Start](#-quick-start) • [🏗️ Architecture](#️-architecture) • [💻 Usage](#-usage) • [⚙️ Configuration](#️-configuration)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🧠 AI-Powered Routing
- **Mistral 7B** understands natural language commands
- **CodeLlama 7B** generates executable Python scripts on-the-fly
- **Keyword fallback** — works even without Ollama running

</td>
<td width="50%">

### 🗣️ Voice-First Interface
- **Google Speech Recognition** (online)
- **OpenAI Whisper** (fully offline)
- Hybrid mode: voice first, text fallback

</td>
</tr>
<tr>
<td width="50%">

### 🖥️ Full GUI
- Dark-theme **tkinter chat interface**
- Real-time status indicator
- 🎤 voice button, 🗑️ clear, timestamps

</td>
<td width="50%">

### 🔍 Web Search
- **DuckDuckGo** Instant Answer API
- No API key required
- Returns abstracts, answers & related topics

</td>
</tr>
<tr>
<td width="50%">

### 🚀 App Launcher
- Open **30+ apps** by name
- `open chrome`, `launch vscode`, `start spotify`
- Fully customizable app map

</td>
<td width="50%">

### 🔒 Permission System
- Critical actions always require confirmation
- SAFE_MODE for non-critical actions
- Hardened regex-based script safety filter

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python 3.9+
# Install Ollama
winget install Ollama.Ollama          # Windows
curl -fsSL https://ollama.ai/install.sh | sh   # Linux
```

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/aryxn1233/JARVIS.git
cd JARVIS/jarvis-ai

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Pull the AI models (one-time setup)
ollama pull mistral:7b-instruct-q4_K_M
ollama pull codellama:7b-instruct-q4_K_M

# 4. Start Ollama server
ollama serve
```

### Launch

```bash
# CLI mode (text + hybrid voice)
python main.py

# GUI mode (tkinter chat interface)
python main.py --gui
```

---

## 🏗️ Architecture

### System Architecture

```mermaid
graph TB
    subgraph INPUT["🎙️ Input Layer"]
        TXT[Text Input]
        VOICE[Voice Input<br/>Google SR / Whisper]
    end

    subgraph CORE["🧠 Core Engine"]
        ROUTER[Router<br/>route_command]
        FALLBACK[Keyword Fallback<br/>Router]
        MEM[Memory<br/>Context Injector]
    end

    subgraph LLM["🤖 LLM Layer"]
        MISTRAL[Mistral 7B<br/>Intent Reasoning]
        CODELLAMA[CodeLlama 7B<br/>Code Generation]
        OLLAMA[Ollama Client<br/>HTTP API]
    end

    subgraph PERMISSION["🔒 Permission Layer"]
        PERM[Permission Manager]
        PROMPT[User Confirmation<br/>Prompt]
    end

    subgraph EXEC["⚙️ Execution Layer"]
        EXECUTOR[Command Executor]
        DIRECT[Direct Intent<br/>Handler]
        SCRIPT[Script Runner<br/>Python Temp File]
        SANDBOX[Safety Filter<br/>Regex Blocklist]
    end

    subgraph OS["🖥️ OS Layer"]
        SYS[System Control<br/>shutdown / restart]
        PROC[Process Manager]
        NET[Network Control<br/>WiFi on/off]
        FILE[File Manager]
        WEB[Web Search<br/>DuckDuckGo]
        APPS[App Launcher<br/>30+ apps]
        MON[System Monitor<br/>CPU/RAM/Disk]
    end

    subgraph OUTPUT["🔊 Output Layer"]
        TTS[Text-to-Speech<br/>pyttsx3]
        CLI_OUT[CLI Print]
        GUI_OUT[GUI Chat Bubble]
    end

    TXT & VOICE --> ROUTER
    MEM --> ROUTER
    ROUTER -->|LLM available| OLLAMA
    ROUTER -->|LLM unavailable| FALLBACK
    OLLAMA --> MISTRAL
    MISTRAL -->|requires_code=true| CODELLAMA
    ROUTER --> PERM --> PROMPT
    PERM --> EXECUTOR
    EXECUTOR --> DIRECT & SCRIPT
    SCRIPT --> SANDBOX
    DIRECT --> SYS & PROC & NET & FILE & WEB & APPS
    MON -->|alerts| ROUTER
    EXECUTOR --> TTS & CLI_OUT & GUI_OUT

    style INPUT fill:#1f3a5f,stroke:#00d4ff,color:#e6edf3
    style CORE fill:#1a2332,stroke:#00d4ff,color:#e6edf3
    style LLM fill:#2d1b69,stroke:#9f7aea,color:#e6edf3
    style PERMISSION fill:#3f1515,stroke:#f85149,color:#e6edf3
    style EXEC fill:#1a3322,stroke:#3fb950,color:#e6edf3
    style OS fill:#1a2a3a,stroke:#58a6ff,color:#e6edf3
    style OUTPUT fill:#2a1f3f,stroke:#d29922,color:#e6edf3
```

---

### Command Flow Diagram

```mermaid
sequenceDiagram
    actor User
    participant Input as 🎙️ CLI/GUI
    participant Router as 🧠 Router
    participant LLM as 🤖 Ollama LLM
    participant Fallback as 🔑 Keyword Fallback
    participant Perm as 🔒 Permission
    participant Exec as ⚙️ Executor
    participant OS as 🖥️ OS Layer

    User->>Input: "open chrome" / voice
    Input->>Router: user_input + context (last 5 commands)

    Router->>LLM: Reasoning prompt (Mistral 7B)
    alt LLM Available
        LLM-->>Router: { intent, requires_code, parameters }
    else LLM Offline
        Router->>Fallback: keyword match
        Fallback-->>Router: { intent: "open_app", app_name: "chrome" }
    end

    alt Critical Intent (shutdown, format, etc.)
        Router->>Perm: check_permission(action_plan)
        Perm->>User: "Approve this action? (yes/no)"
        User-->>Perm: yes / no
        Perm-->>Router: approved / denied
    end

    Router->>Exec: execute_command(action_plan)

    alt Direct Intent
        Exec->>OS: subprocess / psutil call
        OS-->>Exec: result
    else AI-Generated Script
        Exec->>Exec: safety filter (regex)
        Exec->>Exec: write temp .py file
        Exec->>OS: python temp_script.py
        OS-->>Exec: stdout (30s timeout)
        Exec->>Exec: cleanup temp file (finally)
    end

    Exec-->>Input: result string
    Input->>User: 🔊 TTS + 💬 display
    Router->>Router: save to memory (timestamped)
```

---

### Class Diagram

```mermaid
classDiagram
    class OllamaClient {
        +str base_url
        +str generate_endpoint
        +generate(model, prompt, temperature) str
        +generate_json(model, prompt) dict
        +health_check() bool
    }

    class Router {
        +route_command(user_input) dict
        +fallback_route(user_input) dict
        +build_reasoning_prompt(input, recent) str
        +build_coding_prompt(input, reasoning) str
        -_FALLBACK_RULES list
    }

    class CommandExecutor {
        +execute_command(action_plan) str
        +handle_direct_intent(intent, parameters) str
        +open_application(app_name) str
        +execute_generated_script(code) str
        +is_dangerous(code) bool
        -DANGEROUS_PATTERNS list
    }

    class PermissionManager {
        +CRITICAL_INTENTS list
        +check_permission(action_plan) bool
    }

    class Memory {
        +load_memory()
        +save_memory()
        +update_memory(key, value)
        +add_recent_command(command)
        +get_memory(key) any
        -memory_data dict
        -DATA_DIR str
    }

    class StateManager {
        +update_system_state()
        +add_active_task(task_name)
        +remove_active_task(task_name)
        +get_system_state() dict
        -system_state dict
    }

    class Monitor {
        +start_monitoring()
        +stop_monitoring()
        +get_system_snapshot() dict
        +analyze_snapshot(snapshot) dict
        +get_pending_alerts() list
        -monitoring_active bool
        -CPU_THRESHOLD int
        -RAM_THRESHOLD int
        -DISK_THRESHOLD int
    }

    class TTSOutput {
        +speak(text)
        -_get_engine() Engine
        -_engine Engine
    }

    class SpeechInput {
        +get_voice_input(timeout, engine) str
        -_get_voice_google(timeout) str
        -_get_voice_whisper() str
    }

    class CLIInterface {
        +get_user_input() str
        -_get_text_input() str
        -_get_voice() str
    }

    class JarvisGUI {
        +launch_gui()
        -_build_ui()
        -_on_send()
        -_on_voice()
        -_jarvis_thread(user_input)
        -_append_user(text)
        -_append_jarvis(text)
        -BG str
        -ACCENT str
    }

    class WebSearch {
        +search_web(query, max_results) str
        -DDGO_API str
    }

    class Logger {
        +setup_logger()
        +log_event(message, level)
        -LOG_DIR str
    }

    Router --> OllamaClient : uses
    Router --> Memory : reads context
    CommandExecutor --> WebSearch : delegates web_search
    CommandExecutor --> Logger : logs events
    PermissionManager --> CLIInterface : prompts user
    Monitor --> Memory : persists state
    JarvisGUI --> Router : route_command()
    JarvisGUI --> CommandExecutor : execute_command()
    JarvisGUI --> SpeechInput : voice input
    JarvisGUI --> TTSOutput : speaks result
    CLIInterface --> SpeechInput : voice fallback
    StateManager --> Memory : update_memory()
```

---

### Module Dependency Graph

```mermaid
graph LR
    MAIN[main.py] --> ROUTER[core/router.py]
    MAIN --> MEMORY[core/memory.py]
    MAIN --> LOGGER[core/logger.py]
    MAIN --> EXECUTOR[executor/command_executor.py]
    MAIN --> PERM[permission/permission_manager.py]
    MAIN --> CLI[interface/cli_interface.py]
    MAIN --> TTS[interface/tts_output.py]
    MAIN --> GUI[interface/gui.py]
    MAIN --> MON[os_layer/monitor.py]

    ROUTER --> OLLAMA[llm/ollama_client.py]
    ROUTER --> MEMORY
    ROUTER --> LOGGER
    ROUTER --> SETTINGS[config/settings.py]

    EXECUTOR --> APPMAP[config/app_map.py]
    EXECUTOR --> WEB[os_layer/web_search.py]
    EXECUTOR --> NET[os_layer/network_control.py]
    EXECUTOR --> LOGGER

    PERM --> CLI
    CLI --> SPEECH[interface/speech_input.py]
    CLI --> SETTINGS

    GUI --> ROUTER
    GUI --> EXECUTOR
    GUI --> PERM
    GUI --> MEMORY
    GUI --> TTS
    GUI --> SPEECH

    MON --> LOGGER
    MEMORY --> LOGGER

    OLLAMA --> SETTINGS

    style MAIN fill:#00d4ff,stroke:#005f73,color:#000
    style ROUTER fill:#9f7aea,stroke:#6b46c1,color:#fff
    style EXECUTOR fill:#3fb950,stroke:#238636,color:#fff
    style GUI fill:#d29922,stroke:#b08800,color:#fff
```

---

### Input Mode State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle : App starts

    Idle --> ListeningVoice : INPUT_MODE = voice/hybrid
    Idle --> WaitingText : INPUT_MODE = text

    ListeningVoice --> VoiceDetected : Speech recognized
    ListeningVoice --> NoSpeech : Timeout / silence

    NoSpeech --> WaitingText : hybrid mode fallback
    NoSpeech --> ListeningVoice : voice-only mode retry

    VoiceDetected --> Routing : send to router
    WaitingText --> Routing : user hits Enter

    Routing --> LLMRouting : Ollama is online
    Routing --> KeywordRouting : Ollama is offline

    LLMRouting --> PermCheck : intent resolved
    KeywordRouting --> PermCheck : keyword matched
    KeywordRouting --> Idle : no match found

    PermCheck --> Executing : approved / not critical
    PermCheck --> Idle : denied

    Executing --> Speaking : result ready
    Speaking --> Idle : done

    state Executing {
        [*] --> DirectIntent
        [*] --> ScriptGen
        ScriptGen --> SafetyFilter
        SafetyFilter --> RunScript : safe
        SafetyFilter --> Blocked : dangerous
    }
```

---

## 💻 Usage

### CLI / Voice Commands

```
You: check cpu                      → CPU Usage: 12% overall | Cores: [8, 5, ...]
You: how much RAM do I have         → RAM Usage: 61% | Used: 9.8 GB / Total: 16 GB
You: open chrome                    → Opening chrome.
You: search Python async tutorials  → 📖 Asyncio is a library...
You: clean temp files               → Cleanup complete. Freed 1.2 GB
You: shutdown                       → Approve? → System shutting down.
```

### GUI

```bash
python main.py --gui
```

| Button | Action |
|--------|--------|
| `Send ➤` or `Enter` | Send text command |
| `🎤` | Record voice command |
| `🗑️` | Clear chat history |

---

## ⚙️ Configuration

Edit `config/settings.py`:

```python
OLLAMA_URL        = "http://localhost:11434"   # Ollama server
REASONING_MODEL   = "mistral:7b-instruct-q4_K_M"
CODING_MODEL      = "codellama:7b-instruct-q4_K_M"

SAFE_MODE         = True     # Gate non-critical actions
INPUT_MODE        = "hybrid" # "text" | "voice" | "hybrid"
VOICE_ENGINE      = "google" # "google" | "whisper"
MEMORY_CONTEXT_SIZE = 5      # Commands injected into LLM context
GUI_MODE          = False    # True = launch GUI on startup
```

### Add Your Own Apps (`config/app_map.py`)

```python
APP_MAP = {
    "myapp": {"win": "myapp.exe", "linux": "myapp"},
    ...
}
```

### Enable Whisper (Offline Voice)

```bash
pip install openai-whisper sounddevice soundfile numpy
# then set VOICE_ENGINE = "whisper" in config/settings.py
```

---

## 📁 Project Structure

```
jarvis-ai/
├── main.py                    ← Entry point (CLI + GUI)
├── requirements.txt
│
├── config/
│   ├── settings.py            ← All configuration
│   ├── app_map.py             ← App name → executable map
│   └── permissions.yaml       ← Critical intents list
│
├── core/
│   ├── router.py              ← LLM routing + keyword fallback
│   ├── memory.py              ← Persistent JSON memory
│   ├── state_manager.py       ← Live system state
│   └── logger.py              ← Centralized logging
│
├── llm/
│   ├── ollama_client.py       ← HTTP client for Ollama
│   ├── reasoning_model.py     ← Mistral 7B wrapper
│   └── coding_model.py        ← CodeLlama 7B wrapper
│
├── executor/
│   ├── command_executor.py    ← Intent dispatch + script runner
│   ├── sandbox_runner.py      ← Safety validation
│   └── script_runner.py       ← Script execution helper
│
├── interface/
│   ├── cli_interface.py       ← Hybrid text/voice input
│   ├── tts_output.py          ← pyttsx3 text-to-speech
│   ├── speech_input.py        ← Google SR + Whisper
│   ├── gui.py                 ← Tkinter dark-theme GUI ✨
│   └── permission_prompt.py   ← User confirmation prompts
│
├── os_layer/
│   ├── monitor.py             ← Background resource monitor
│   ├── file_manager.py        ← File operations
│   ├── process_manager.py     ← Process listing
│   ├── network_control.py     ← WiFi toggle
│   ├── system_control.py      ← Shutdown / restart
│   └── web_search.py          ← DuckDuckGo search ✨
│
├── permission/
│   ├── permission_manager.py  ← Critical intent gating
│   └── privilege_escalation.py
│
├── workflows/
│   ├── automation_engine.py   ← Dynamic workflow dispatcher
│   ├── cleanup.py             ← Temp file cleanup
│   └── optimizer.py           ← Process optimizer
│
├── tests/
│   ├── test_executor.py       ← 10 executor tests
│   ├── test_permissions.py    ← 4 permission tests
│   └── test_router.py         ← 5 router tests
│
├── data/
│   └── memory.json            ← Persistent session memory
└── logs/
    └── jarvis.log             ← Full event log
```

---

## 🧪 Running Tests

```bash
python -m unittest discover -s tests -v
# Ran 19 tests in ~1s: OK
```

---

## 🛠️ Built With

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| AI Runtime | [Ollama](https://ollama.ai) |
| Reasoning LLM | Mistral 7B Instruct Q4 |
| Coding LLM | CodeLlama 7B Instruct Q4 |
| TTS | pyttsx3 (offline) |
| Voice Input | Google SR / OpenAI Whisper |
| GUI | tkinter (stdlib) |
| System Monitoring | psutil |
| Web Search | DuckDuckGo Instant Answer API |

---

## 🔮 Roadmap

- [ ] Plugin system for custom intent handlers
- [ ] GUI settings panel
- [ ] Multi-language TTS
- [ ] Home Assistant integration
- [ ] Conversation history export

---

## 👤 Author

**Aryan Thakur**  
GitHub: [@aryxn1233](https://github.com/aryxn1233)

---

<div align="center">

Made with ❤️ and ⚡ by Aryan Thakur

</div>
