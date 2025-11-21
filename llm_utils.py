# llm_utils.py
"""
大模型通用工具：读取 .env，封装统一的 call_llm、parse_json_from_llm

依赖:
    pip install openai python-dotenv
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_api_key = os.getenv("LLM_API_KEY")
if not _api_key:
    raise RuntimeError("缺少环境变量 LLM_API_KEY，请在 .env 中配置")

client = OpenAI(
    api_key=_api_key,
    base_url=os.getenv(
        "LLM_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",  # 默认按 Qwen 兼容地址
    ),
)

LLM_MODEL = os.getenv("LLM_MODEL_NAME", "qwen-max")


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """统一的大模型调用，只返回文本"""
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    return resp.choices[0].message.content


def parse_json_from_llm(text: str) -> dict:
    """
    处理 ```json ... ``` 这种包裹格式，并转成 dict
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json\n", "").replace("json\r\n", "")
    return json.loads(cleaned)
