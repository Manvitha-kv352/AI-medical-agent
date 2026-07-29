import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None


ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"

if ENV_FILE.exists() and load_dotenv is not None:
    load_dotenv(ENV_FILE, override=False)


def _resolve_groq_model(model_name):
    model_name = str(model_name or "").strip().lower()
    if not model_name:
        return "llama-3.1-8b-instant"
    if model_name in {"llama3", "llama3.1", "llama3:latest", "llama3.1:latest"}:
        return "llama-3.1-8b-instant"
    if model_name in {"llama3.2", "llama3.3"}:
        return "llama-3.3-70b-versatile"
    return model_name


class GroqCompatLLM:
    def __init__(self, model="llama3", *args, **kwargs):
        api_key = kwargs.pop("api_key", None) or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set")

        from langchain_groq import ChatGroq

        self._client = ChatGroq(
            model=_resolve_groq_model(model),
            api_key=api_key,
            temperature=kwargs.pop("temperature", 0),
            **kwargs,
        )

    def invoke(self, prompt, *args, **kwargs):
        result = self._client.invoke(prompt, *args, **kwargs)
        return getattr(result, "content", str(result))

    async def ainvoke(self, prompt, *args, **kwargs):
        result = await self._client.ainvoke(prompt, *args, **kwargs)
        return getattr(result, "content", str(result))


try:
    import langchain_ollama as _ollama_mod

    if os.getenv("GROQ_API_KEY") and not getattr(_ollama_mod, "_groq_patched", False):
        _ollama_mod.OllamaLLM = GroqCompatLLM
        _ollama_mod._groq_patched = True
except Exception:
    pass
