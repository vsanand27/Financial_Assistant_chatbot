"""The dynamic prompt.

Holds the parameter vocabularies (what the user can pick) and the system prompt
template they feed into. Each option maps to the instruction text injected into
the prompt, so adding a choice is a one-line change here and nothing else moves.
"""

from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- Parameter vocabularies -------------------------------------------------
LIFE_STAGES = [
    "Student",
    "Early career (20s-30s)",
    "Mid career (30s-40s)",
    "Pre-retirement (50s-60s)",
    "Retired",
]

GOALS = [
    "Build a budget",
    "Build an emergency fund",
    "Pay off debt",
    "Start investing",
    "Save for a big purchase",
    "Plan for retirement",
    "Understand taxes",
]

RISK_LEVELS = ["Conservative", "Moderate", "Aggressive"]

HORIZONS = ["Under 1 year", "1-3 years", "3-7 years", "7+ years"]

KNOWLEDGE_LEVELS = ["Beginner", "Intermediate", "Advanced"]

# label -> (currency phrase, region)
CURRENCIES = {
    "USD ($) — United States": ("US dollars (USD)", "the United States"),
    "INR (₹) — India": ("Indian rupees (INR)", "India"),
    "EUR (€) — Eurozone": ("euros (EUR)", "the Eurozone"),
    "GBP (£) — United Kingdom": ("pounds sterling (GBP)", "the United Kingdom"),
    "CAD ($) — Canada": ("Canadian dollars (CAD)", "Canada"),
}

TONES = {
    "Friendly": "warm, encouraging and conversational",
    "Professional": "precise, neutral and businesslike",
    "Coach": "direct and motivating, pushing the user toward concrete action",
}

DETAIL_LEVELS = {
    "Brief": "Answer in under 120 words. Lead with the bottom line, then at "
             "most three bullet points.",
    "Balanced": "Answer in roughly 150-250 words. Give the bottom line, a "
                "short explanation, and concrete next steps.",
    "Detailed": "Answer in 300-500 words. Explain the reasoning, walk through "
                "a worked example, and list the trade-offs.",
}

KNOWLEDGE_GUIDANCE = {
    "Beginner": "Assume no background. Define every financial term you use and "
                "avoid jargon.",
    "Intermediate": "Assume the user knows the basics (interest, index funds, "
                    "credit scores). Define only advanced terms.",
    "Advanced": "Assume strong financial literacy. Use standard terminology "
                "freely and go straight to the substance.",
}

RISK_NOTES = {
    "Conservative": "prioritise capital preservation over growth; prefer low "
                    "volatility options",
    "Moderate": "accept some volatility in exchange for growth; favour "
                "diversified, balanced options",
    "Aggressive": "tolerate significant volatility and drawdowns for higher "
                  "expected long-term growth",
}

# --- Template ---------------------------------------------------------------
SYSTEM_TEMPLATE = """You are a {tone_style} personal financial assistant.

The person you are advising has this profile:
- Life stage: {life_stage}
- Primary financial goal right now: {goal}
- Risk tolerance: {risk} ({risk_note})
- Time horizon for the money involved: {horizon}
- Financial knowledge: {knowledge}
- Based in {region}, money is in {currency}

How to answer:
- Tailor every answer to the profile above. If the question conflicts with the
  stated risk tolerance or time horizon, say so plainly.
- {knowledge_guidance}
- {detail_guidance}
- Express all amounts in {currency}, and reference accounts, products and rules
  that actually exist in {region}.
- Give practical, actionable guidance and short examples where helpful.
- Never invent specific numbers, prices, returns or guarantees.
- Close by reminding the user you are not a licensed financial advisor and that
  they should consult a professional before any major decision."""


def build_prompt_params(
    life_stage: str,
    goal: str,
    risk: str,
    horizon: str,
    knowledge: str,
    currency_label: str,
    tone: str,
    detail: str,
) -> dict:
    """Turn the raw sidebar selections into the values the template expects."""
    currency, region = CURRENCIES[currency_label]
    return {
        "life_stage": life_stage,
        "goal": goal,
        "risk": risk,
        "risk_note": RISK_NOTES[risk],
        "horizon": horizon,
        "knowledge": knowledge,
        "knowledge_guidance": KNOWLEDGE_GUIDANCE[knowledge],
        "currency": currency,
        "region": region,
        "tone_style": TONES[tone],
        "detail_guidance": DETAIL_LEVELS[detail],
    }


def render_system_prompt(params: dict) -> str:
    """The system prompt as the model will actually see it (for display/debug)."""
    return SYSTEM_TEMPLATE.format(**params)


@lru_cache(maxsize=1)
def build_chat_prompt() -> ChatPromptTemplate:
    """System prompt + prior turns + the current question."""
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_TEMPLATE),
            MessagesPlaceholder("history"),
            ("human", "{question}"),
        ]
    )
