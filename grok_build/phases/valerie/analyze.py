"""ANALYSIS: TF-IDF, tagging, bifurcation, arc stitching."""

import re
from collections import Counter, defaultdict
from typing import Any

COVEN_TAGS = {
    "tech": {"jetson", "mcp", "letta", "tensorrt", "docker", "python", "api", "model"},
    "ingest": {"valerie", "ingest", "rag", "chunk", "jsonl", "pipeline", "harvest"},
    "swarm": {"agent", "orchestrator", "hub", "crystal", "echo", "mira", "roster"},
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z']{3,}", text.lower())


def _tfidf_keywords(texts: list[str], top_n: int = 12) -> list[str]:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer

        vec = TfidfVectorizer(max_features=500, stop_words="english")
        matrix = vec.fit_transform(texts)
        scores = matrix.sum(axis=0).A1
        terms = vec.get_feature_names_out()
        ranked = sorted(zip(terms, scores), key=lambda x: -x[1])
        return [t for t, _ in ranked[:top_n]]
    except ImportError:
        doc_tokens = [_tokenize(t) for t in texts]
        df = Counter()
        for toks in doc_tokens:
            for t in set(toks):
                df[t] += 1
        N = max(1, len(doc_tokens))
        scores: list[tuple[str, float]] = []
        for toks in doc_tokens:
            tf = Counter(toks)
            for w, c in tf.most_common():
                idf = N / (1 + df[w])
                scores.append((w, c * idf))
        scores.sort(key=lambda x: -x[1])
        seen: set[str] = set()
        out: list[str] = []
        for w, _ in scores:
            if w not in seen:
                seen.add(w)
                out.append(w)
            if len(out) >= top_n:
                break
        return out


def _vader_sentiment(text: str) -> float:
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

        return SentimentIntensityAnalyzer().polarity_scores(text)["compound"]
    except ImportError:
        emotional = sum(
            1
            for w in ("love", "feel", "great", "happy", "excited", "amazing")
            if w in text.lower()
        )
        return min(1.0, emotional * 0.2)


def analyze_text(text: str, corpus: list[str] | None = None) -> dict[str, Any]:
    corpus = corpus or [text]
    keywords = _tfidf_keywords(corpus)
    tokens = set(_tokenize(text))
    tags = []
    for category, vocab in COVEN_TAGS.items():
        if tokens & vocab:
            tags.append(category)
    if not tags:
        tags = ["general"]

    compound = _vader_sentiment(text)
    bifurcation = "emotional" if compound > 0.15 else "fact"

    return {
        "keywords": keywords[:8],
        "tags": tags,
        "bifurcation": bifurcation,
        "sentiment_compound": round(compound, 3),
    }


def build_arc_index(blocks: list[dict]) -> dict[str, list[str]]:
    """Longitudinal arc stitching: group block IDs by shared top tag."""
    arcs: dict[str, list[str]] = defaultdict(list)
    for blk in blocks:
        top_tag = (blk.get("tags") or ["general"])[0]
        arcs[top_tag].append(blk["id"])
    return dict(arcs)