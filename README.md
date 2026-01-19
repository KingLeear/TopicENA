# TopicENA
TopicENA is a lightweight, open-source pipeline that integrates neural topic modeling with Epistemic Network Analysis (ENA) to support scalable discourse structure analysis.



## Project Structure

```text
TopicENA/
├─ data/
│  └─ sample/
│     └─ sample_students.csv
├── topicena/
│   ├── __init__.py
│   └── cli.py
├─ r/
│  └─ ena_run.R
├─ outputs/
├─ docker/
└─ README.md
```


## Installation (Local / Development Mode)

Clone this repository and install TopicENA in **editable mode**:

```bash
git clone https://github.com/owen198/topicena.git
cd topicena
python -m pip install -e .
```

Check whether TopicENA is installed and where it is loaded from:

```bash
python -m pip show topicena
```


## Removing TopicENA

To remove TopicENA from your environment:

```bash
python -m pip uninstall topicena
```

## Executing TopicENA

```bash
topicena \
  --prob_th 0.01 \
  --n_neighbors 10 \
  --n_components 5 \
  --min_dist 0.0 \
  --min_cluster_size 20 \
  --min_samples 5 \
  --min_topic_size 5 \
  --window_size_back 20
```






## Installation

```bash

python -m venv .venv

source .venv/bin/activate

pip install -e .

Rscript r/requirements.R
```





## Execution

BERTopic Test

```bash
(venv) python BERTopic.py
```

```bash
(venv) python calling_r.py
```

```bash
topicena run \
  --input data/sample/sample_students.csv \
  --text-col text \
  --id-col student_id \
  --group-col group \
  --n-topics 10 \
  --outdir outputs
```


## Output

```text
outputs/
└─ <run_id>/
   ├─ bertopic/
   │  ├─ doc_topics.csv
   │  └─ topic_info.csv
   ├─ viz/
   │  └─ topic_visualizations.png
   ├─ ena_input/
   │  └─ codes_long.csv
   └─ ena/
      ├─ ena_network.png
      ├─ ena_difference.png
      └─ ena_stats.csv
```

---

## Python–R Integration

TopicENA uses **Python as the main pipeline controller** and **R for Epistemic Network Analysis (ENA)**.

The interaction between Python and R follows a simple file-based workflow:

1. **Python stage**
   - Python performs topic modeling using BERTopic.
   - Topic assignments are automatically transformed into semantic codes.
   - Intermediate ENA input files (e.g., `codes_long.csv`, `metadata.csv`) are written to disk.

2. **R stage**
   - Python invokes the R script (`r/ena_run.R`) via `Rscript`.
   - The R script reads the generated CSV files and runs ENA.
   - ENA network visualizations and statistical outputs are saved to the output directory.

This loose coupling design keeps the system lightweight, transparent, and easy to reproduce, while allowing researchers to modify or extend the Python and R components independently.
