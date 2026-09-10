from pathlib import Path

from app.retrieval import VectorRetriever


def test_retrieves_ranked_incidents_from_persistent_store(tmp_path: Path):
    corpus = tmp_path / "incidents"
    corpus.mkdir()
    (corpus / "missing.md").write_text(
        "# Missing dependency\nImportError package missing in tests", encoding="utf-8"
    )
    (corpus / "timeout.md").write_text(
        "# Flaky timeout\nTests exceeded the configured timeout", encoding="utf-8"
    )

    retriever = VectorRetriever(corpus, threshold=0.2, store_path=tmp_path / "chroma")

    matches = retriever.retrieve("ImportError package missing", top_k=2)

    assert matches
    assert matches[0].id == "missing"
    assert matches[0].title == "Missing dependency"


def test_unavailable_corpus_returns_empty_results(tmp_path: Path):
    retriever = VectorRetriever(tmp_path / "missing", store_path=tmp_path / "chroma")

    assert retriever.retrieve("anything") == []
