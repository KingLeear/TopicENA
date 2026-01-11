# https://github.com/MaartenGr/BERTopic

# berTopic_demo.py
# Reference style: https://www.williampnicholson.com/2024-02-07-topic-modelling/  (modular BERTopic pipeline + visualizations)
# - Auto-download dataset (20 Newsgroups)
# - Export multiple figures, including topic keyword barcharts

import os
import pandas as pd

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer

from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN

from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def try_write_png(fig, out_png: str) -> None:
    """
    BERTopic visualizations are Plotly figures.
    Writing PNG needs kaleido: pip install -U kaleido
    """
    try:
        fig.write_image(out_png, scale=2)
        print(f"[OK] Saved PNG: {out_png}")
    except Exception as e:
        print(f"[SKIP] PNG export failed (install kaleido?): {out_png}\n  Reason: {e}")


def main():
    out_dir = "outputs"
    ensure_dir(out_dir)

    # 1) Download a sample dataset automatically
    #    (You can limit categories to make it faster/smaller.)
    categories = [
        "comp.graphics",
        "comp.sys.mac.hardware",
        "sci.space",
        "rec.sport.baseball",
        "talk.politics.mideast",
    ]
    data = fetch_20newsgroups(
        subset="train",
        categories=categories,
        remove=("headers", "footers", "quotes"),
    )
    docs = [d.strip().replace("\n", " ") for d in data.data if d and d.strip()]

    print(f"Loaded docs: {len(docs)}")

    # 2) Build a Nicholson-style modular BERTopic pipeline
    # Embeddings
    embedding_model = SentenceTransformer("all-mpnet-base-v2")

    # Dimensionality reduction (UMAP)
    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
        random_state=42,
    )

    # Clustering (HDBSCAN)
    hdbscan_model = HDBSCAN(
        min_cluster_size=20,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )

    # Vectorizer + c-TF-IDF
    vectorizer_model = CountVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=5,
    )
    ctfidf_model = ClassTfidfTransformer()

    topic_model = BERTopic(
        language="english",
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        ctfidf_model=ctfidf_model,
        calculate_probabilities=True,
        verbose=True,
    )

    # 3) Fit
    topics, probs = topic_model.fit_transform(docs)
    print("Done fitting BERTopic.")

    # 4) Export "keywords per topic" table (核心需求：各群關鍵字)
    #    topic_model.get_topic(topic_id) returns list[(word, weight), ...]
    rows = []
    for topic_id in sorted(set(topics)):
        if topic_id == -1:
            continue  # -1 is outliers
        words = topic_model.get_topic(topic_id) or []
        top_words = [w for (w, _) in words[:15]]
        rows.append(
            {
                "topic_id": topic_id,
                "top_keywords": ", ".join(top_words),
                "doc_count": int((pd.Series(topics) == topic_id).sum()),
            }
        )

    df_kw = pd.DataFrame(rows).sort_values(["doc_count"], ascending=False)
    out_csv = os.path.join(out_dir, "topic_keywords.csv")
    df_kw.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"[OK] Saved keyword table: {out_csv}")

    # 5) Visualizations (Plotly HTML + optional PNG)
    # (A) Topic overview
    fig_topics = topic_model.visualize_topics()
    out_html = os.path.join(out_dir, "fig_topics_overview.html")
    fig_topics.write_html(out_html)
    print(f"[OK] Saved HTML: {out_html}")
    try_write_png(fig_topics, os.path.join(out_dir, "fig_topics_overview.png"))

    # (B) "各群關鍵字" barchart (most important for your requirement)
    fig_barchart = topic_model.visualize_barchart(top_n_topics=12, n_words=10)
    out_html = os.path.join(out_dir, "fig_topic_keywords_barchart.html")
    fig_barchart.write_html(out_html)
    print(f"[OK] Saved HTML: {out_html}")
    try_write_png(fig_barchart, os.path.join(out_dir, "fig_topic_keywords_barchart.png"))

    # (C) Topic similarity heatmap
    fig_heatmap = topic_model.visualize_heatmap()
    out_html = os.path.join(out_dir, "fig_topic_heatmap.html")
    fig_heatmap.write_html(out_html)
    print(f"[OK] Saved HTML: {out_html}")
    try_write_png(fig_heatmap, os.path.join(out_dir, "fig_topic_heatmap.png"))

    # (D) Hierarchical topics
    fig_hier = topic_model.visualize_hierarchy()
    out_html = os.path.join(out_dir, "fig_topic_hierarchy.html")
    fig_hier.write_html(out_html)
    print(f"[OK] Saved HTML: {out_html}")
    try_write_png(fig_hier, os.path.join(out_dir, "fig_topic_hierarchy.png"))

    # (E) Documents scatter (2D) — might take a bit longer
    fig_docs = topic_model.visualize_documents(docs)
    out_html = os.path.join(out_dir, "fig_documents_scatter.html")
    fig_docs.write_html(out_html)
    print(f"[OK] Saved HTML: {out_html}")
    try_write_png(fig_docs, os.path.join(out_dir, "fig_documents_scatter.png"))

    print("\nAll outputs are in ./outputs")
    print("Tip: open the .html files in your browser for interactive exploration.")


if __name__ == "__main__":
    main()
