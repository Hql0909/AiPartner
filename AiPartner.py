import os
import streamlit as st
from openai import OpenAI
import datetime
import json

def save_session():
    if st.session_state.session_name:
        # 构建当前会话对象
        session_obj = {
            "session_name": st.session_state.session_name,
            "partner_name": st.session_state.partner_name,
            "partner_character": st.session_state.partner_character,
            "messages": st.session_state.messages
        }

        # 将会话文件保存在session文件夹中
        if not os.path.exists("sessions"):
            os.makedirs("sessions")

        with open(f"sessions/{st.session_state.session_name}.json", "w", encoding="utf-8") as f:
            json.dump(session_obj, f, ensure_ascii=False, indent=4)

# 历史会话
def load_sessions():
    sessions_list = []
    if os.path.exists("sessions"):
        files_list = os.listdir("sessions")
        for session_file in files_list:
            if session_file.endswith(".json"):
                sessions_list.append(session_file[:-5])
    sessions_list = sorted(sessions_list, reverse=True)
    return sessions_list

# 加载对话
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话文件
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_obj = json.load(f)
                st.session_state.session_name = session_obj["session_name"]
                st.session_state.partner_name = session_obj["partner_name"]
                st.session_state.partner_character = session_obj["partner_character"]
                st.session_state.messages = session_obj["messages"]
    except Exception as e:
        st.error(f"加载会话出错: {e}")

# 删除会话
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
        if session_name == st.session_state.session_name:
            st.session_state.session_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            st.session_state.partner_name = ""
            st.session_state.partner_character = ""
            st.session_state.messages = []
    except Exception as e:
        st.error(f"删除会话出错: {e}")

# 创建与AI大模型交互的客户端对象
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com",
)

st.set_page_config(
    page_title="AiPartner_steam",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# 大标题
st.title("AiPartner_steam")

# logo
st.logo("💤")

# 初始化会话
if "session_name" not in st.session_state:
    st.session_state.session_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# 昵称
if "partner_name" not in st.session_state:
    st.session_state.partner_name = ""
# 性格
if "partner_character" not in st.session_state:
    st.session_state.partner_character = ""
# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []


# 左侧侧边栏
# st.sidebar.subheader("Partner信息")
# partner_name = st.sidebar.text_input("Partner名称", "奇犽")
# st.sidebar.write("这是侧边栏")
with st.sidebar: #这个with是streamlit的上下文管理器
    st.subheader("Ai控制面板")
    if st.button("开启新对话",icon="🗞️",width="stretch"):
        st.session_state.session_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if st.session_state.messages:
            # 保存当前会话
            # save_session()
            # 开启新会话
            st.session_state.messages = []
            st.session_state.partner_name = ""
            st.session_state.partner_character = ""
            # st.session_state.session_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            st.rerun()

    # 历史会话
    st.text("历史会话",)
    sessions_list = load_sessions()
    for session in sessions_list:
        col_1,col_2 = st.columns([4,1])
        # 历史会话名称
        with col_1:
            if st.button(session,width="stretch",key=f"load_{session}",type="primary" if session == st.session_state.session_name else "secondary"):
                load_session(session)
                st.rerun()
        # 删除键
        with col_2:
            if st.button("删除",icon="🗑️",width="stretch",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    # 分隔线
    st.divider()

    st.text("Partner信息")
    #输入partner名字
    partner_name = st.text_input("Partner名称",placeholder="请输入Partner名称",value=st.session_state.partner_name)
    if partner_name:
        st.session_state.partner_name = partner_name
    #输入partner性格
    partner_character = st.text_area("Partner性格",placeholder="请输入Partner性格",value=st.session_state.partner_character)
    if partner_character:
        st.session_state.partner_character = partner_character

# 系统提示词
system_prompt = f"你是{st.session_state.partner_name},性格为{st.session_state.partner_character}"

# 显示会话名称
st.text(f"会话名称:{st.session_state.session_name}")

# 显示聊天信息
for message in st.session_state.messages:#{ "role": "user", "content": prompt }
    if message["role"] == "user":
        st.chat_message("🙃").write(message["content"])
    elif message["role"] == "assistant":
        st.chat_message("👾").write(message["content"])
    # st.chat_message(message["role"]).write(message["content"])

# 输入框
prompt = st.chat_input("请输入你要问的问题")
if prompt:
    # st.write(f"用户:{prompt}")
    st.chat_message("🙃").write(prompt)
    # 添加用户消息到会话状态
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 与AI大模型进行交互
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "disabled"}},
    )

    # 输出大模型返回的结果:response.choices[0].message.content(非流式输出)
    # st.chat_message("👾").write(response.choices[0].message.content)

    # 流式输出大模型返回结果
    response_container = st.empty() # 创建一个空的容器用于显示大模型返回结果
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_container.chat_message("👾").write(full_response, unsafe_allow_html=True)

    # 开启新对话会重新加载渲染页面
    # 添加AI助手消息到会话状态
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 保存会话
if st.session_state.messages:
    save_session()
    if st.session_state.session_name not in sessions_list:
        st.rerun()

