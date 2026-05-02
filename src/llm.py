import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_llm(model=None):
    api_key = os.getenv("OPENAI_API_KEY")
    model_llm = model or os.getenv("OPENAI_MODEL")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add a valid key to .env or your container environment.")

    if not model_llm:
        raise RuntimeError("OPENAI_MODEL is not set. Add a model name to .env, for example gpt-4o-mini.")

    return ChatOpenAI(
        model=model_llm,
        api_key=api_key,
        temperature=0,
    )
