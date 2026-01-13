# https://github.com/MaartenGr/BERTopic
# https://www.williampnicholson.com/2024-02-07-topic-modelling/



import os
import pandas as pd

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer

from umap import UMAP
from hdbscan import HDBSCAN

from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer

NUM_TOPIC = 10
NUM_WORD = 5

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def try_write_png(fig, out_png: str) -> None:
    try:
        fig.write_image(out_png, scale=2)
        print(f"[OK] Saved PNG: {out_png}")
    except Exception as e:
        print(f"[SKIP] PNG export failed (install kaleido?): {out_png}\n  Reason: {e}")


def main():
    out_dir = "outputs"
    ensure_dir(out_dir)

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
        min_df=1,
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

    topics, probs = topic_model.fit_transform(docs)
    print("Done fitting BERTopic.")

    # version 0
    # rows = []
    # for topic_id in sorted(set(topics)):
    #     if topic_id == -1:
    #         continue  # -1 is outliers
    #     words = topic_model.get_topic(topic_id) or []
    #     top_words = [w for (w, _) in words[:15]]
    #     rows.append(
    #         {
    #             "topic_id": topic_id,
    #             "top_keywords": ", ".join(top_words),
    #             "doc_count": int((pd.Series(topics) == topic_id).sum()),
    #         }
    #     )

    # df_kw = pd.DataFrame(rows).sort_values(["doc_count"], ascending=False)
    # out_csv = os.path.join(out_dir, "topic_keywords.csv")
    # df_kw.to_csv(out_csv, index=False, encoding="utf-8-sig")
    # print(f"[OK] Saved keyword table: {out_csv}")

    # version 1
    # output_dict = dict()

    # for topic_id in sorted(set(topics)):
    #     if topic_id == -1:
    #         continue  # -1 is outliers
    #     words = topic_model.get_topic(topic_id) or []

    #     top_words = [w for (w, _) in words[:15]]
    #     output_dict[topic_id] = top_words

    # new_columns = [
    #     ".".join(output_dict[i][:3])
    #     for i in range(len(output_dict))
    # ]

    # df = pd.get_dummies(topics, prefix="topic")
    # max_topic = max(topics)
    # all_columns = [f"topic_{i}" for i in range(max_topic + 1)]
    # df = df.reindex(columns=all_columns, fill_value=0)
    # df = df.astype(int)
    # df.columns = new_columns
    # df.insert(0, "docs", docs)

    # df['docs'] = df['docs'].str.split('.')
    # df = df.explode("docs")
    # out_csv = os.path.join(out_dir, "topic_keywords.csv")
    # df.to_csv(out_csv, index=False, encoding="utf-8-sig")



    # version 2
    # th = 0.3
    # binary_arr = (probs >= th).astype(int)
    # df = pd.DataFrame(binary_arr)

    # number_of_keywords = 2

    # output_dict = dict()

    # for topic_id in sorted(set(topics)):
    #     if topic_id == -1:
    #         continue  # -1 is outliers
    #     words = topic_model.get_topic(topic_id) or []

    #     top_words = [w for (w, _) in words[:15]]

    #     output_dict[topic_id] = top_words

    # new_columns = [
    #     ".".join(output_dict[i][:number_of_keywords])
    #     for i in range(len(output_dict))
    # ]

    # df.columns = new_columns
    # df.insert(0, "docs", docs)

    # df['docs'] = df['docs'].str.split('.')
    # df = df.explode("docs")
    # df = df[df["docs"].notna() & df["docs"].str.strip().ne("")]

    # out_csv = os.path.join(out_dir, f"topic_keywords_{th}.csv")
    # df.to_csv(out_csv, index=False, encoding="utf-8-sig")


    # version 3
    th = 0.05
    binary_arr = (probs >= th).astype(int)
    df = pd.DataFrame(binary_arr)

    number_of_keywords = 2

    output_dict = dict()

    for topic_id in sorted(set(topics)):
        if topic_id == -1:
            continue  # -1 is outliers
        words = topic_model.get_topic(topic_id) or []
        top_words = [w for (w, _) in words[:15]]
        output_dict[topic_id] = top_words

    new_columns = [
        ".".join(output_dict[i][:number_of_keywords])
        for i in range(len(output_dict))
    ]

    df.columns = new_columns
    df.insert(0, "text", docs)

    import numpy as np

    df["UserName"] = np.random.choice(
        ["Alice", "Bob", "Cindy"],
        size=len(df)
    )

    df["Condition"] = np.random.choice(
        ["LDSE", "HDSE"],
        size=len(df)
    )

    df = df.reset_index().rename(columns={"index": "ActivityNumber"})

    df["text"] = df["text"].str.split(".")
    df = df.explode("text")

    df["text"] = df["text"].str.strip()
    df = df[df["text"] != ""]

    df = df[df["text"].notna() & df["text"].str.strip().ne("")]

    out_csv = os.path.join(out_dir, f"topic_keywords_{th}.csv")
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")





    # (A) Topic overview
    fig_topics = topic_model.visualize_topics()
    out_html = os.path.join(out_dir, "fig_topics_overview.html")
    fig_topics.write_html(out_html)
    print(f"[OK] Saved HTML: {out_html}")
    try_write_png(fig_topics, os.path.join(out_dir, "fig_topics_overview.png"))

    # (B) Keywords
    fig_barchart = topic_model.visualize_barchart(top_n_topics=NUM_TOPIC, n_words=NUM_WORD)
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
