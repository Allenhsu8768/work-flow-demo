import os
from dotenv import load_dotenv

# Langchain imports
from langchain.chat_models import init_chat_model


# Load environment variables from .env file
load_dotenv()



# 1. LLM 初始化 (GPT)
ollama_gpt_model_20b = init_chat_model(
    model="gpt-oss:20b",
    model_provider='ollama',
    base_url=os.getenv('OLLAMA_BASE_URL'),
    temperature=0.5,
    num_ctx=8192
)

