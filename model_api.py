from typing import Generator, AsyncGenerator
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def get_model_response(prompt: str) -> AsyncGenerator[str, None]:
    """
    使用 LangChain 调用模型 API 并实现流式输出
    Args:
        prompt: 用户输入的提示文本
    Yields:
        模型响应的文本片段
    """
    # 初始化模型
    model = ChatOpenAI(
        api_key="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",
        base_url="https://openrouter.ai/api/v1/",
        model_name="deepseek/deepseek-r1:free",
        streaming=True
    )
    
    # 创建消息
    system_promt = """
    请先思考在回答。
    """

    messages = [
        SystemMessage(content=system_promt),
        HumanMessage(content=prompt)]
    is_answering = False
    # 获取流式响应
    async for chunk in model.astream(messages):
        if chunk.content != "" and is_answering is False:
            yield "\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n\n"
            is_answering = True
        yield chunk.content
