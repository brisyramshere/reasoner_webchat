import streamlit as st
from model_reasoner_api import get_reasoner_response
import time
# import asyncio

st.set_page_config(page_title="ICH Copilot with Reasoning", page_icon="🦜")
st.title("🦜 ICH Copilot with Reasoning")

# 在侧边栏添加配置选项  
with st.sidebar:  
    with st.expander("LLM模型API设置", expanded=False):
        # 提供一个文本输入框让用户可以手动输入API Key（可选）  
        st.markdown('<span style="font-size: 14px;">内置deepseek模型为免费模型，如果存在卡顿或者超时问题，建议接入自己的Deepseek API</span>', unsafe_allow_html=True)
        api_base = st.text_input("Base Url", key="chatbot_api_base", type="default", 
                                 placeholder="https://api.deepseek.com/v1")  
        api_key = st.text_input("API Key", key="chatbot_api_key", type="password", 
                                placeholder="sk-9ee206fef1134798a880a7e328c77dd7")  
        model = st.text_input("Model",key="chatbot_model", type="default",
                              placeholder="deepseek-reasoner")
        "[获取 DeepSeek API key](https://platform.deepseek.com/api_keys)"  

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():    
    init_session_state()
    display_chat_history()
    
    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # 创建一个expander显示思考过程，reason_container用来放置思考过程的文本
            with st.expander("思考中...", expanded=True):
                reason_container = st.empty()
            answer_container = st.empty()

            answer_content = ""
            reasoning_content = ""
            stream_phase = "notstart"
            print("model: ", model)
            print("api_base: ", api_base)
            print("api_key: ", api_key)
            for chunk in get_reasoner_response(prompt,model, api_base, api_key):
                chunk_cleaned  = chunk\
                    .replace("<think_start>", "")\
                    .replace("<think_end>", "")
                
                if(chunk.find("<think_start>") != -1):
                    stream_phase = "thinking"
                    continue

                if(chunk.find("<think_end>") != -1):
                    stream_phase = "answering"
                    continue

                if stream_phase == "thinking":
                    reasoning_content += chunk_cleaned
                    with st.expander("思考中...", expanded=True):
                        reason_container.markdown(reasoning_content+"▌")

                if stream_phase == "answering":
                    answer_content += chunk_cleaned
                    answer_container.markdown(answer_content+"▌")
                time.sleep(0.05)
            answer_container.markdown(answer_content)

            
        if answer_content != "":  # 只在成功获得响应时添加到历史记录
            st.session_state.messages.append({"role": "assistant", "content": answer_content})

if __name__ == "__main__":
    main()