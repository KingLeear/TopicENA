# TopicENA
TopicENA is a lightweight, open-source pipeline that integrates neural topic modeling with Epistemic Network Analysis (ENA) to support scalable discourse structure analysis.



## Project Structure

```text
TopicENA/
├─ data/
│  └─ sample/
│     └─ sample_students.csv
├─ src/
│  └─ topicena/
│     ├─ cli.py
│     ├─ pipeline.py
│     ├─ bertopic_step.py
│     ├─ semantic_coding.py
│     └─ ena_bridge.py
├─ r/
│  └─ ena_run.R
├─ outputs/
├─ docker/
└─ README.md
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
