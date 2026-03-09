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

    for phrase in GREETING_TRIGGERS:
        if phrase in text:
            return True
    return False


def generate_response(query: str, contexts: list[str]) -> str:
    if _is_greeting(query):
        return (
            "Hello! Good to see you. I can help with job search, career paths, skills, "
            "salary insights, and interview preparation. Try asking: 'engineering jobs in chennai'."
        )

    if not contexts:
        return "I could not find exact matches. Try role, city, or skill keywords."

    top_contexts = "\n".join(contexts[:5])
    return f"Results for '{query}':\n{top_contexts}"
