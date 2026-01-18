import kagglehub

# https://www.kaggle.com/datasets/lburleigh/asap-2-0

# Download latest version
path = kagglehub.dataset_download("lburleigh/asap-2-0")

print("Path to dataset files:", path)



import os
import pandas as pd
import numpy as np

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
    out_dir = "./"
    ensure_dir(out_dir)



    asap_pd = pd.read_csv(path + "/ASAP2_train_sourcetexts.csv")
    assignment = asap_pd["assignment"].unique()[0]
    asap_assignment_pd = asap_pd[asap_pd["assignment"] == assignment]
    asap_assignment_pd['group'] = np.where(asap_assignment_pd['score'] <= 3, 'low', 'high')
    reflection_df = pd.DataFrame()

    reflection_df["reflection"] = asap_assignment_pd["full_text"]
    reflection_df["group"] = asap_assignment_pd["group"]
    reflection_df["id"] = asap_assignment_pd["essay_id"]

    docs = reflection_df["reflection"].astype("str").to_list()





    print(f"Loaded docs: {len(docs)}")

    # Embeddings
    embedding_model = SentenceTransformer("all-mpnet-base-v2")

    # Dimensionality reduction (UMAP)
    umap_model = UMAP(
        n_neighbors=10,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
        random_state=42,
    )

    # Clustering (HDBSCAN)
    hdbscan_model = HDBSCAN(
        min_cluster_size=20,
        min_samples=5,
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
        min_topic_size=5
    )

    topics, probs = topic_model.fit_transform(docs)

    print("Done fitting BERTopic.")








    th = 0.01

    binary_arr = (probs >= th).astype(int)
    df = pd.DataFrame(binary_arr)

    number_of_keywords = 7

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

    # df.columns = new_columns
    df.columns = ['.'.join(col.split('.')[-3:]) for col in new_columns]

    print(new_columns)
    df.insert(0, "text", docs)

    df["UserName"] = reflection_df["id"].values
    df["Condition"] = reflection_df["group"].values

    df = df.reset_index().rename(columns={"index": "ActivityNumber"})

    df["text"] = df["text"].str.split(".")
    df = df.explode("text")

    df["text"] = df["text"].str.strip()
    df = df[df["text"] != ""]

    df['text'] = df['text'].str.split('.')
    df = df.explode("text")

    out_csv = os.path.join(out_dir, f"topic_keywords_asap_{th}_reflection.csv")
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