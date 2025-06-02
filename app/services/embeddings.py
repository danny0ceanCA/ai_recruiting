"""Embedding utilities using OpenAI."""
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "")


def embed_text(text: str) -> list[float]:
    """Return embedding vector for given text using OpenAI API."""
    if not openai.api_key:
        # offline or no key – return dummy vector
        return [0.0] * 1536
    response = openai.Embedding.create(input=text, model="text-embedding-3-small")
    return response["data"][0]["embedding"]
