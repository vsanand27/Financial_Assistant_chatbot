"""Streamlit UI: sidebar parameter controls, chat history, and the chat loop."""

import streamlit as st

from backend import MissingAPIKeyError, generate_answer
from config import (
    DEFAULT_TEMPERATURE,
    DISCLAIMER,
    MODEL_NAME,
    PAGE_ICON,
    PAGE_TITLE,
)
from prompt_template import (
    CURRENCIES,
    DETAIL_LEVELS,
    GOALS,
    HORIZONS,
    KNOWLEDGE_LEVELS,
    LIFE_STAGES,
    RISK_LEVELS,
    TONES,
    build_prompt_params,
    render_system_prompt,
)


def render_sidebar() -> tuple[dict, float]:
    """Draw the parameter controls. Returns (prompt_params, temperature)."""
    with st.sidebar:
        st.header(f"{PAGE_ICON} {PAGE_TITLE}")
        st.caption(f"Model: `{MODEL_NAME}`")

        st.subheader("Your profile")
        life_stage = st.selectbox("Life stage", LIFE_STAGES, index=1)
        goal = st.selectbox("Primary goal", GOALS, index=0)
        risk = st.select_slider("Risk tolerance", RISK_LEVELS, value="Moderate")
        horizon = st.select_slider("Time horizon", HORIZONS, value="3-7 years")
        knowledge = st.radio(
            "Financial knowledge", KNOWLEDGE_LEVELS, index=0, horizontal=True
        )
        currency_label = st.selectbox("Currency / region", list(CURRENCIES))

        st.subheader("Answer style")
        tone = st.selectbox("Tone", list(TONES))
        detail = st.select_slider(
            "Detail level", list(DETAIL_LEVELS), value="Balanced"
        )
        temperature = st.slider(
            "Creativity (temperature)", 0.0, 1.0, DEFAULT_TEMPERATURE, 0.1
        )

        st.markdown("---")
        if st.button("🗑️ Clear conversation"):
            st.session_state.messages = []
            st.rerun()
        st.caption(DISCLAIMER)
        st.caption(
            "⚠️ Limitation: this tool uses an older language model whose "
            "knowledge has not been updated since 2023, so it may be unaware "
            "of recent products, rules, rates or events."
        )

    params = build_prompt_params(
        life_stage=life_stage,
        goal=goal,
        risk=risk,
        horizon=horizon,
        knowledge=knowledge,
        currency_label=currency_label,
        tone=tone,
        detail=detail,
    )
    return params, temperature


def render_header(params: dict) -> None:
    st.title(f"{PAGE_ICON} {PAGE_TITLE}")
    st.caption("This Financial Assistant application is built by Vick Anand")
    st.caption(
        f"Advising a **{params['life_stage'].lower()}** profile · "
        f"goal: **{params['goal'].lower()}** · "
        f"**{params['risk'].lower()}** risk · "
        f"**{params['horizon'].lower()}** horizon"
    )
    with st.expander("🔍 See the prompt these settings produce"):
        st.code(render_system_prompt(params), language="text")


def render_history() -> None:
    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(content)


def handle_question(question: str, params: dict, temperature: float) -> None:
    """Answer one question and append both turns to the history."""
    history = list(st.session_state.messages)  # prior turns only

    st.session_state.messages.append(("user", question))
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = generate_answer(question, history, params, temperature)
            except MissingAPIKeyError as exc:
                st.error(str(exc))
                st.stop()
        st.markdown(answer)

    st.session_state.messages.append(("assistant", answer))


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

    if "messages" not in st.session_state:
        st.session_state.messages = []  # list of (role, content) tuples

    params, temperature = render_sidebar()
    render_header(params)
    render_history()

    question = st.chat_input("Ask me anything about your finances...")
    if question:
        handle_question(question, params, temperature)
