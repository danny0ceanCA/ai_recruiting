import os
import sys
import types
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services import embeddings


def test_embed_text_uses_openai(monkeypatch):
    called = {}
    def fake_create(input, model):
        called['input'] = input
        called['model'] = model
        return {"data": [{"embedding": [1.0, 2.0, 3.0]}]}
    monkeypatch.setattr(embeddings.openai, "api_key", "test")
    monkeypatch.setattr(embeddings.openai.Embedding, "create", fake_create)
    vec = embeddings.embed_text("hello")
    assert vec == [1.0, 2.0, 3.0]
    assert called['input'] == "hello"
    assert called['model'] == "text-embedding-3-small"


def test_embed_text_without_key(monkeypatch):
    monkeypatch.setattr(embeddings.openai, "api_key", "")
    vec = embeddings.embed_text("something")
    assert vec == [0.0] * 1536
