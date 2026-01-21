## Demo: ASAP 2.0 – Automated Student Assessment Prize

This demo shows how to preprocess the ASAP 2.0 dataset and run TopicENA for analysis.

### 0. Pre-requirement
Make sure **TopicENA** is already installed in your environment.

---

### 1. Preprocess the dataset
Run the following command:
```bash
python asap20_preprocess.py
```

This command will generate a file named `asap20.csv` in the local folder.
The original dataset comes from Kaggle:
https://www.kaggle.com/datasets/lburleigh/asap-2-0

### 2. Run TopicENA analysis

```bash
topicena \
  --input ./demo/asap20.csv \
  --n_neighbors 60 \
  --min_dist 0.2 \
  --min_cluster_size 60 \
  --min_topic_size 20 \
  --number_of_keywords 5 \
  --prob_th 0.01
```

The analysis results will be automatically saved to the default `output` folder


### 3. Batch Execution Script

This script runs multiple `topicena` jobs sequentially with different BERTopic configurations, from fine-grained to coarse-grained settings. Each job prints progress messages to the console, continues even if a single run fails, and records failed runs in a log file.

```bash
chmod +x run_topicena_10.sh
./run_topicena.sh
```