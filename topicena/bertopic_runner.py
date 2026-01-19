from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from bertopic import BERTopic
from umap import UMAP
import hdbscan


@dataclass
class BERTopicConfig:
    # TopicENA (multi-topic assignment)
    prob_th: float = 0.01

    # UMAP
    n_neighbors: int = 10
    n_components: int = 5
    min_dist: float = 0.0

    # HDBSCAN
    min_cluster_size: int = 20
    min_samples: int = 5

    # BERTopic
    min_topic_size: int = 5


def _validate_config(cfg: BERTopicConfig) -> None:
    if not (0.0 <= cfg.prob_th <= 1.0):
        raise ValueError(f"prob_th must be in [0,1], got {cfg.prob_th}")
    if cfg.n_neighbors <= 1:
        raise ValueError("n_neighbors must be > 1")
    if cfg.n_components <= 0:
        raise ValueError("n_components must be > 0")
    if cfg.min_dist < 0.0:
        raise ValueError("min_dist must be >= 0")
    if cfg.min_cluster_size <= 1:
        raise ValueError("min_cluster_size must be > 1")
    if cfg.min_samples <= 0:
        raise ValueError("min_samples must be > 0")
    if cfg.min_topic_size <= 1:
        raise ValueError("min_topic_size must be > 1")


def build_topic_model(cfg: BERTopicConfig) -> BERTopic:
    """
    Build a BERTopic model with explicit UMAP + HDBSCAN configuration.
    """
    _validate_config(cfg)

    umap_model = UMAP(
        n_neighbors=cfg.n_neighbors,
        n_components=cfg.n_components,
        min_dist=cfg.min_dist,
        metric="cosine",
        random_state=42,
    )

    hdbscan_model = hdbscan.HDBSCAN(
        min_cluster_size=cfg.min_cluster_size,
        min_samples=cfg.min_samples,
        metric="euclidean",
        prediction_data=True,
    )

    topic_model = BERTopic(
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        min_topic_size=cfg.min_topic_size,
        calculate_probabilities=True,
        verbose=False,
    )
    return topic_model


def fit_transform_docs(
    docs: List[str],
    cfg: BERTopicConfig,
    embeddings: Optional[np.ndarray] = None,
) -> Tuple[BERTopic, List[int], Optional[np.ndarray]]:
    """
    Fit a BERTopic model and return (model, topics, probs).
    probs is an array of shape (n_docs, n_topics) when calculate_probabilities=True.
    """
    model = build_topic_model(cfg)
    topics, probs = model.fit_transform(docs, embeddings=embeddings)
    return model, topics, probs


def multi_topic_assignment(
    probs: np.ndarray,
    prob_th: float = 0.01,
) -> pd.DataFrame:
    """
    Convert topic probability matrix into a binary doc-topic membership matrix.
    This enables ENA visualization when a document can belong to multiple topics.

    Returns:
        DataFrame with columns like topic_0, topic_1, ... containing 0/1.
    """
    if probs is None:
        raise ValueError("probs is None. Make sure BERTopic calculate_probabilities=True.")
    if not (0.0 <= prob_th <= 1.0):
        raise ValueError(f"prob_th must be in [0,1], got {prob_th}")

    binary = (probs >= prob_th).astype(int)
    df = pd.DataFrame(binary)
    df.columns = [f"topic_{i}" for i in range(df.shape[1])]
    return df


def get_topic_keywords(
    model: BERTopic,
    top_n: int = 15,
) -> Dict[int, List[str]]:
    """
    Return a mapping {topic_id: [keyword1, keyword2, ...]} (excluding outlier -1).
    """
    out: Dict[int, List[str]] = {}
    for topic_id in sorted(set(model.topics_)):
        if topic_id == -1:
            continue
        words = model.get_topic(topic_id) or []
        out[topic_id] = [w for (w, _) in words[:top_n]]
    return out
