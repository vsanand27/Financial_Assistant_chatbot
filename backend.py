"""Back end: the model client and the LangChain chain that produces an answer.

Deliberately free of Streamlit imports — this module knows nothing about the UI
and can be exercised from a plain script or a test.
"""

from functools import lru_cache

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI

from config import DEFAULT_TEMPERATURE, MODEL_NAME, get_api_key
from prompt_template import build_chat_prompt


class MissingAPIKeyError(RuntimeError):
    """Raised when OPENAI_API_KEY is not set. The UI turns this into a message."""


@lru_cache(maxsize=8)
def get_llm(temperature: float = DEFAULT_TEMPERATURE) -> ChatOpenAI:
    """Chat model client, cached per temperature so we don't rebuild it per turn."""
    api_key = get_api_key()
    if not api_key:
        raise MissingAPIKeyError(
            "No OPENAI_API_KEY found. Add it to your .env file as "
            "`OPENAI_API_KEY=sk-...` and restart the app."
        )
    return ChatOpenAI(model=MODEL_NAME, temperature=temperature, api_key=api_key)


def to_lc_messages(history: list[tuple[str, str]]) -> list[BaseMessage]:
    """Convert (role, content) turns into LangChain message objects."""
    return [
        HumanMessage(content=content) if role == "user" else AIMessage(content=content)
        for role, content in history
    ]


def generate_answer(
    question: str,
    history: list[tuple[str, str]],
    prompt_params: dict,
    temperature: float = DEFAULT_TEMPERATURE,
) -> str:
    """Render the dynamic prompt with `prompt_params` and answer `question`."""
    chain = build_chat_prompt() | get_llm(temperature)
    response = chain.invoke(
        {**prompt_params, "history": to_lc_messages(history), "question": question}
    )
    return response.content
