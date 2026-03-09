from app.config.settings import settings


GREETING_TRIGGERS = {
    "hi",
    "hello",
    "hey",
    "hii",
    "good morning",
    "good afternoon",
    "good evening",
    "good night",
}


def _is_greeting(query: str) -> bool:
    text = (query or "").strip().lower()
    if not text:
        return False
    if text in GREETING_TRIGGERS:
        return True
    return any(phrase in text for phrase in GREETING_TRIGGERS)


def _fallback_answer(query: str, contexts: list[str]) -> str:
    if _is_greeting(query):
        return (
            "Hello! I can help with jobs in Tamil Nadu, required skills, salary guidance, "
            "and career paths. Try: 'software developer jobs in chennai'."
        )

    if not contexts:
        return "I could not find strong matches. Try role, city, or skill keywords."

    return "Results for '{}':\n{}".format(query, "\n".join(contexts[:5]))


def _openai_answer(query: str, contexts: list[str]) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    context_block = "\n".join(f"- {item}" for item in contexts[:8]) if contexts else "No context found."

    prompt = (
        "You are a job and career guidance assistant for Tamil Nadu. "
        "Answer clearly and concisely using provided job context. "
        "If context is limited, suggest better search queries.\n\n"
        f"User query: {query}\n"
        f"Retrieved jobs:\n{context_block}"
    )

    response = client.responses.create(
        model=settings.openai_model,
        input=prompt,
        temperature=0.3,
    )
    return (response.output_text or "").strip()


def generate_response(query: str, contexts: list[str]) -> str:
    if not settings.openai_api_key:
        return _fallback_answer(query, contexts)

    try:
        if _is_greeting(query):
            return _fallback_answer(query, contexts)
        answer = _openai_answer(query, contexts)
        return answer if answer else _fallback_answer(query, contexts)
    except Exception:
        return _fallback_answer(query, contexts)
