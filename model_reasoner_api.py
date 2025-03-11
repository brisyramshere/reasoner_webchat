from typing import AsyncGenerator
import os
from openai import OpenAI

def get_reasoner_response(prompt: str) -> AsyncGenerator[str, None]:
    """
    使用OpenAI API直接调用推理模型并实现流式输出，包括思考过程和最终回复
    Args:
        prompt: 用户输入的提示文本
    Yields:
        模型的思考过程和最终回复的文本片段
    """

    # 创建系统提示
    system_prompt = """
    你是一个专业的推理助手。请先思考问题，然后给出详细的推理过程和最终答案。
    """
    
    # 初始化 Anthropic 客户端
    client = OpenAI(
        api_key="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",
        base_url="https://openrouter.ai/api/v1/"
        )
    
    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",  # 请替换为实际的模型名称
        messages=[
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": prompt}],
        stream=True
    )

    reasoning_content = ""
    answer_content = ""
    is_thinking = False
    is_answering = False

    # 处理流式响应
    for chunk in completion:
         if not chunk.choices:           
             print("\nUsage:"+str(chunk.usage))            
         else: 
            delta = chunk.choices[0].delta
            # print(chunk)
            if hasattr(delta, 'reasoning') and delta.reasoning is not None:
                if is_thinking is False:
                    is_thinking = True
                    yield "<think_start>"
                reasoning_content += delta.reasoning
                yield delta.reasoning
            else:
                if delta.content != "" and is_answering is False:
                    is_answering = True
                    yield "<think_end>"
                answer_content += delta.content
                yield delta.content

    # 将完整的回复添加到消息历史记录
    # messages.append({"role": "assistant", "content": answer_content})
