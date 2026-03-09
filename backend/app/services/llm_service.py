def generate_response(query: str, contexts: list[str]) -> str:
    if not contexts:
        return "No relevant jobs were found yet. Try a broader query."

    top_contexts = "\n".join(contexts[:3])
    return f"Results for '{query}':\n{top_contexts}"
