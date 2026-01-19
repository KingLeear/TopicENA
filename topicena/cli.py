# topicena/cli.py
import argparse

from topicena.bertopic_runner import BERTopicConfig
from topicena.rena_executor import RENAConfig, run_rena_rscript


def main():
    parser = argparse.ArgumentParser(prog="topicena", description="TopicENA: Topic-based Epistemic Network Analysis")

    # TopicENA
    parser.add_argument("--prob_th", type=float, default=0.01, help="Probability threshold for multi-topic assignment (default: 0.01)")

    # UMAP
    parser.add_argument("--n_neighbors", type=int, default=10, help="UMAP n_neighbors parameter (default: 10)")
    parser.add_argument("--n_components", type=int, default=5, help="UMAP n_components parameter (default: 5)")
    parser.add_argument("--min_dist", type=float, default=0.0, help="UMAP min_dist parameter (default: 0.0)")

    # HDBSCAN
    parser.add_argument("--min_cluster_size", type=int, default=20, help="HDBSCAN min_cluster_size parameter (default: 20)")
    parser.add_argument("--min_samples", type=int, default=5, help="HDBSCAN min_samples parameter (default: 5)")

    # BERTopic
    parser.add_argument("--min_topic_size", type=int, default=5, help="BERTopic min_topic_size parameter (default: 5)")

    # rENA
    parser.add_argument("--window_size_back", type=int, default=20, help="rENA window.size.back parameter (default: 20)")

    args = parser.parse_args()

    print(args)


    bertopic_cfg = BERTopicConfig(
        prob_th=args.prob_th,
        n_neighbors=args.n_neighbors,
        n_components=args.n_components,
        min_dist=args.min_dist,
        min_cluster_size=args.min_cluster_size,
        min_samples=args.min_samples,
        min_topic_size=args.min_topic_size,
    )

    rena_cfg = RENAConfig(window_size_back=args.window_size_back)

    result = run_rena_rscript(
        r_script_path=args.rena_r_script,
        cfg=rena_cfg,
        extra_args=None
    )
    print(result.stdout)

if __name__ == "__main__":
    main()
