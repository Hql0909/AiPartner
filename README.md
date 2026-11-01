# AiPartner 🤖

> 一个基于 **Streamlit + DeepSeek** 的 AI 伴侣聊天应用 —— 自定义角色名称与性格,支持流式回复、多会话存档与历史回溯。

**中文** | [English](README.en.md)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-4D6BFE)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 项目简介

AiPartner 是一个用 **Python** 写成的 Web 聊天应用。它通过 **OpenAI 兼容接口**调用 **DeepSeek** 大模型,
让你可以给自己设定一个"AI 伴侣":给它起名字、写性格,然后像聊天软件一样与它连续对话。

整个项目只有 **200 行左右**的代码,却覆盖了一个完整聊天应用需要的核心能力:
会话状态管理、流式输出、本地持久化、多会话切换、侧边栏控制面板。

适合作为 **Streamlit 入门 / 大模型 API 调用** 的实践案例。

---

## ✨ 功能特性

| 特性 | 说明 |
| :--- | :--- |
| 💬 **流式对话** | `stream=True` 逐字接收,回复像打字一样实时显示,不用等整段返回 |
| 🎭 **自定义人设** | 侧边栏填写「Partner 名称」与「Partner 性格」,自动拼进 System Prompt |
| 🗂️ **多会话管理** | 一键开启新对话,历史会话列表可随时加载、删除 |
| 💾 **自动存档** | 每条消息自动保存为 `sessions/<会话名>.json`,关掉浏览器再打开也不丢 |
| 🎨 **聊天界面** | 复用 Streamlit 原生 `st.chat_message` / `st.chat_input`,带宽屏布局与侧边栏 |
| 🔄 **状态持久化** | 基于 `st.session_state`,页面重跑(rerun)期间对话不丢失 |

---

## 🖼️ 界面预览

```
┌──────────────────────────┬──────────────────────────────────────────┐
│  Ai控制面板               │  会话名称:2026-10-29_14-32-13             │
│                          │                                          │
│  [🗞️ 开启新对话]          │  🙃 好想睡觉呀                            │
│                          │  👾 那就别硬撑啦~困意来了是身体在提醒你…   │
│  历史会话                 │                                          │
│  [2026-10-29_14-32-13]   │  🙃 讲小故事                              │
│  [2026-10-29_14-23-01]   │  👾 好呀,给你讲一个很轻很轻的小故事——     │
│                          │                                          │
│  Partner信息              │                                          │
│  Partner名称 [奇犽      ] │                                          │
│  Partner性格 [冷静、毒舌 ] │                                          │
│                          │                                          │
│                          │  ┌──────────────────────────┬─────────┐  │
│                          │  │ 请输入你要问的问题…       │         │  │
└──────────────────────────┴──────────────────────────────────────────┘
```

> 想放真实截图?运行应用后截图,保存到项目根目录 `screenshot.png`,
> 再把上面的代码块替换成 `![界面预览](screenshot.png)` 即可。

---

## 🚀 快速开始

### 1. 获取代码

```bash
git clone https://github.com/Hql0909/AiPartner.git
cd AiPartner
```

### 2. 创建虚拟环境并安装依赖

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. 配置 API Key

本项目通过环境变量 `DEEPSEEK_API_KEY` 读取密钥,**不会把密钥写进代码**。
请先在 [DeepSeek 开放平台](https://platform.deepseek.com/api_keys) 申请一个 API Key。

**Windows PowerShell(当前窗口有效)**

```powershell
$env:DEEPSEEK_API_KEY = "sk-你的密钥"
```

**永久生效(可选)**

```powershell
setx DEEPSEEK_API_KEY "sk-你的密钥"
```

**macOS / Linux**

```bash
export DEEPSEEK_API_KEY="sk-你的密钥"
```

### 4. 启动应用

```bash
streamlit run AiPartner.py
```

浏览器会自动打开 `http://localhost:8501`,左侧填写 Partner 名称与性格,就可以开始聊天了。

---

## 📁 项目结构

```
AiPartner/
├── AiPartner.py          # ⭐ 主程序:聊天界面 + DeepSeek 调用 + 会话管理
├── requirements.txt      # 依赖清单
├── README.md             # 中文说明
├── README.en.md          # English README
├── LICENSE               # MIT 许可证
└── .gitignore            # Git 忽略规则
```

运行时会在本地生成 `sessions/<会话名>.json` 保存聊天记录(不入库)。

---

## 🔧 核心实现

### 调用大模型

DeepSeek 提供 **OpenAI 兼容接口**,所以直接复用官方 `openai` SDK,只需把 `base_url` 指向 DeepSeek:

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

> 模型名 `deepseek-flash` 可在 `AiPartner.py` 中随时替换,例如 `deepseek-chat`、`deepseek-reasoner`。

### 人设注入

用户填写的名称与性格被拼成 System Prompt,模型的每一次回复都会带上这个设定:

```python
system_prompt = f"你是{st.session_state.partner_name},性格为{st.session_state.partner_character}"
```

### 流式渲染

逐块接收 `chunk`,不断刷新同一个占位容器,实现"打字机"效果:

```python
response_container = st.empty()
full_response = ""
for chunk in response:
    if chunk.choices[0].delta.content:
        full_response += chunk.choices[0].delta.content
        response_container.chat_message("👾").write(full_response)
```

### 会话持久化

每条消息保存为独立 JSON 文件,文件名即会话名(时间戳):

```
sessions/
├── 2026-10-29_14-32-13.json
└── 2026-10-29_14-23-01.json
```

结构为 `{session_name, partner_name, partner_character, messages[]}`,加载时整体回填到 `st.session_state`。

---

## 🔐 数据与隐私

- **API Key** 只从环境变量读取,仓库中不存在任何明文密钥。
- **聊天记录** 保存在本地 `sessions/` 目录,已加入 `.gitignore`,不会被推送到 GitHub。
- 所有请求直接发往 `https://api.deepseek.com`,不经过任何第三方中转。

---

## ❓ 常见问题

<details>
<summary><b>报错 <code>AuthenticationError</code> / 401</b></summary>

环境变量没生效。注意 Windows 下 `setx` 需要**新开一个终端**才生效;
也可以先在当前窗口用 `$env:DEEPSEEK_API_KEY = "sk-..."` 临时设置。

</details>

<details>
<summary><b>报错 <code>'streamlit' 不是内部或外部命令</code></b></summary>

虚拟环境没有激活,或依赖没装好。先执行 `.\.venv\Scripts\Activate.ps1`,
再 `pip install -r requirements.txt`。也可以用 `python -m streamlit run AiPartner.py`。

</details>

<details>
<summary><b>PowerShell 提示"禁止运行脚本"</b></summary>

执行策略限制,运行一次即可:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

</details>

<details>
<summary><b>端口 8501 被占用</b></summary>

```bash
streamlit run AiPartner.py --server.port 8502
```

</details>

<details>
<summary><b>回复是乱码 / 中文显示异常</b></summary>

确认终端与文件编码为 UTF-8。`.json` 存档已使用 `ensure_ascii=False`,
Windows 记事本打开也正常。

</details>

---

## 🗺️ 后续计划

- [ ] 支持 Markdown / 代码块高亮渲染
- [ ] 导出会话为 Markdown 文件
- [ ] 流式输出时显示 token 用量
- [ ] 支持多模型切换(deepseek-chat / deepseek-reasoner)

---

## 📄 License

本项目基于 [MIT License](LICENSE) 开源,欢迎自由使用与修改。
