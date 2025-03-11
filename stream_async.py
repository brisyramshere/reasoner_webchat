import streamlit as st
# from model_api import get_model_response
from model_reasoner_api import get_reasoner_response
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
import asyncio

st.set_page_config(page_title="ICH Copilot", page_icon="🦜")
st.title("🦜 ICH Copilot")

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

async def main():    
    init_session_state()
    display_chat_history()
    
    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            async for chunk in get_reasoner_response(prompt):
                full_response += chunk
                # 使用空格确保 Markdown 正确渲染
                message_placeholder.markdown(full_response + "▌ ")
                await asyncio.sleep(0.01)  # 减少延迟时间提高响应速度
            message_placeholder.markdown(full_response)
            
        if full_response:  # 只在成功获得响应时添加到历史记录
            st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    asyncio.run(main())