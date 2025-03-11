import streamlit as st
from model_reasoner_api import get_reasoner_response
import time
import re

st.set_page_config(page_title="ICH Copilot with Reasoning", page_icon="🦜")
st.title("🧠 ICH Copilot with Reasoning 🔍✅📝📄")

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def format_response(response: str):
    """将响应文本分割成思考过程和最终答案"""
    think_pattern = r'<think_start>(.*?)<think_end>'
    think_parts = re.findall(think_pattern, response, re.DOTALL)
    final_response = re.sub(think_pattern, '', response).strip()
    return think_parts, final_response

def stream_display(placeholder, response, thinking_placeholder=None):
    """处理流式输出的显示"""
    think_parts, final_response = format_response(response)
    
    # 更新思考过程
    if think_parts and thinking_placeholder is not None:
        think_text = ""
        for i, think in enumerate(think_parts, 1):
            think_text += f"**思考步骤 {i}:**\n{think.strip()}\n\n"
        thinking_placeholder.markdown(think_text)
    
    # 更新最终答案
    if final_response:
        placeholder.markdown(final_response + "▌ ")

def display_message(message):
    """显示历史消息"""
    think_parts, final_response = format_response(message)
    
    # 如果有思考过程，显示在可折叠区域
    if think_parts:
        with st.expander("💭 查看思考过程", expanded=False):
            for i, think in enumerate(think_parts, 1):
                st.markdown(f"**思考步骤 {i}:**")
                st.markdown(think.strip())
    
    # 显示最终答案
    if final_response:
        st.markdown(final_response)

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            display_message(message["content"])

def main():    
    init_session_state()
    display_chat_history()
    
    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # 创建两个占位符：一个用于思考过程，一个用于最终答案
            thinking_placeholder = st.empty()
            answer_placeholder = st.empty()
            
            full_response = ""
            
            # 流式输出处理
            for chunk in get_reasoner_response(prompt):
                full_response += chunk
                stream_display(answer_placeholder, full_response, thinking_placeholder)
                time.sleep(0.05)
            
            # 清理流式输出的痕迹，重新显示完整响应
            thinking_placeholder.empty()
            answer_placeholder.empty()
            display_message(full_response)
            
        if full_response:
            st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()