import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    llm_provider: str
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    embedding_provider: str
    embedding_base_url: str
    embedding_api_key: str
    embedding_model: str
    embedding_dim: int


def get_settings() -> Settings:
    return Settings(
        llm_provider=os.getenv("LLM_PROVIDER", "groq"),
        llm_base_url=os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1"),
        llm_api_key=os.getenv("LLM_API_KEY", ""),
        llm_model=os.getenv("LLM_MODEL", "openai/gpt-oss-20b"),
        embedding_provider=os.getenv("EMBEDDING_PROVIDER", "local"),
        embedding_base_url=os.getenv("EMBEDDING_BASE_URL", "https://api.openai.com/v1"),
        embedding_api_key=os.getenv("EMBEDDING_API_KEY", ""),
        embedding_model=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
        embedding_dim=int(os.getenv("EMBEDDING_DIM", "384")),
    )
