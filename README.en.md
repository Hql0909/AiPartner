# AiPartner 🤖

> An AI companion chat app built with **Streamlit + DeepSeek** — define your partner's name and personality, chat with streaming responses, and keep every conversation saved.

[中文](README.md) | **English**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-4D6BFE)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 About

AiPartner is a lightweight web chat application written in **Python** (~200 lines).
It talks to **DeepSeek** through the **OpenAI-compatible API**, and lets you create an "AI partner"
with a custom name and personality — then chat with it like a real messaging app.

Despite its small size, it covers everything a real chat app needs:
session state management, streaming output, local persistence, multi-conversation switching,
and a sidebar control panel.

A compact reference project for learning **Streamlit** and **LLM API integration**.

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 💬 **Streaming replies** | `stream=True` renders tokens as they arrive — no waiting for the full answer |
| 🎭 **Custom persona** | Set the partner's name and personality in the sidebar; injected into the System Prompt |
| 🗂️ **Multi-session** | Start a new chat, reload or delete any previous conversation |
| 💾 **Auto-save** | Every message is written to `sessions/<session-name>.json` |
| 🎨 **Native chat UI** | Built on `st.chat_message` / `st.chat_input` with a wide layout and sidebar |
| 🔄 **Persistent state** | Powered by `st.session_state`, survives Streamlit reruns |

---

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/Hql0909/AiPartner.git
cd AiPartner
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Set your API key

Get a key from the [DeepSeek platform](https://platform.deepseek.com/api_keys), then:

```bash
export DEEPSEEK_API_KEY="sk-your-key"      # Windows PowerShell: $env:DEEPSEEK_API_KEY = "sk-your-key"
```

The key is read from the environment — **no secrets are stored in the code**.

### 4. Run

```bash
streamlit run AiPartner.py
```

Open `http://localhost:8501`, fill in the partner's name and personality, and start chatting.

---

## 📁 Project Structure

```
AiPartner/
├── AiPartner.py          # Main app: chat UI + DeepSeek calls + session management
├── requirements.txt      # Dependencies
├── README.md             # Chinese README
├── README.en.md          # English README (this file)
├── LICENSE               # MIT
└── .gitignore
```

Chat history is generated at runtime under `sessions/` and is git-ignored.

---

## 🔧 How It Works

### Calling the model

DeepSeek exposes an OpenAI-compatible endpoint, so the official `openai` SDK works out of the box:

```python
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages],
    stream=True,
)
```

Swap `deepseek-flash` for `deepseek-chat` or `deepseek-reasoner` as needed.

### Persona injection

```python
system_prompt = f"You are {name}, your personality is {personality}"
```

### Streaming render

```python
container = st.empty()
full = ""
for chunk in response:
    if chunk.choices[0].delta.content:
        full += chunk.choices[0].delta.content
        container.chat_message("👾").write(full)
```

---

## 🔐 Privacy

- The API key comes from an environment variable only.
- Chat logs stay in the local `sessions/` folder and are excluded via `.gitignore`.
- Requests go directly to `https://api.deepseek.com` — no third-party proxy.

---

## 📄 License

[MIT](LICENSE)
