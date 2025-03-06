from typing import Generator, AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
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
        model_name="google/gemini-2.0-flash-lite-001",
        streaming=True
    )
    
    # 创建消息
    messages = [HumanMessage(content=prompt)]
    
    # 获取流式响应
    async for chunk in model.astream(messages):
        if chunk.content:
            yield chunk.content


from typing import Generator
def get_model_response_test(prompt: str) -> Generator[str, None, None]:
    """
    模拟大模型的流式响应
    实际使用时替换为真实的API调用
    """
    # 这里替换为实际的API调用
    # 例如使用 Anthropic Claude API:
    # from anthropic import Anthropic
    # client = Anthropic(api_key="your-api-key")
    
    # 示例响应
    response = "This is a simulated streaming response from Claude 3.5 Sonnet. Replace this with actual API calls."
    
    # 模拟流式输出
    for word in response.split():
        yield word + " "