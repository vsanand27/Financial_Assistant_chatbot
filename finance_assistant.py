"""Entry point.

    streamlit run finance_assistant.py

Layout:
    config.py           settings and .env loading
    prompt_template.py  the dynamic prompt and its parameter vocabularies
    backend.py          model client + LangChain chain (no Streamlit)
    ui.py               Streamlit widgets and chat loop
"""

from ui import main

main()
