# TopicENA
TopicENA is a lightweight, open-source pipeline that integrates neural topic modeling with Epistemic Network Analysis (ENA) to support scalable discourse structure analysis.



## Project Structure

```text
TopicENA/
├─ demo/
│  ├── README.md
│  ├── asap20_preprocess.py
│  └── run_topicena.sh
├── topicena/
│   ├── __init__.py
│   ├── bertopic_runner.py
│   ├── ena_script.R
│   ├── cli.py
│   └── rena_executor.py
├── pyproject.toml
└─ README.md
```


## 1. Installation

Clone this repository and install TopicENA in **editable mode**:

```bash
git clone https://github.com/owen198/topicena.git
cd topicena

# create virtual environment
python -m venv .venv

# activate virtual environment
# macOS / Linux
source .venv/bin/activate

# Windows
# .venv\Scripts\activate

# install TopicENA and Python dependencies
python -m pip install -e .
```

Check whether TopicENA is installed and where it is loaded from:

```bash
python -m pip show topicena

topicena --help  
```


## 2. Executing TopicENA

```bash
topicena 
```



## 3. Removing TopicENA

To remove TopicENA from your environment:

```bash
python -m pip uninstall topicena
```



## 4. Troubleshooting

### Duplicate keyword columns detected

If you encounter the following warning during execution:
```
Duplicate keyword columns detected
This usually indicates that the topic configuration is too fine-grained.
```

This means that BERTopic has produced topics with overlapping or identical keywords**, which can lead to duplicated semantic codes in the ENA input and cause issues in downstream analysis. This situation typically occurs when the topic modeling configuration is too fine-grained, resulting in multiple topics sharing very similar top keywords.

### Recommended solutions

The simplest and most effective solution is to increase the `number_of_keywords` used to represent each topic, so that topic codes become more distinctive. By default, TopicENA uses the last `2` keywords of each topic to construct semantic codes. You may try increasing this value.

For example:

```bash
topicena
  --number_of_keywords 3
```





## BERTopic

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

