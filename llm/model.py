import os
import requests
from dotenv import load_dotenv

load_dotenv()


class GroqLLM:
    def __init__(self, model="llama-3.3-70b-versatile", api_key=None, temperature=0, max_tokens=1024):
        self.model = model
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.temperature = temperature
        self.max_tokens = max_tokens

    def invoke(self, prompt, *args, **kwargs):
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is not set")

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def ainvoke(self, prompt, *args, **kwargs):
        return self.invoke(prompt, *args, **kwargs)


llm = GroqLLM()