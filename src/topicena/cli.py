# src/topicena/cli.py
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(add_completion=False, help="TopicENA CLI")


@dataclass
class RunConfig:
    input: str
    text_col: str
    id_col: str
    group_col: str
    n_topics: int
    outdir: str
    run_id: str
    seed: int

    ena_unit: str
    ena_conversation: str
    ena_conditions: str
    ena_window: int

    rscript: str
    ena_script: str


def _now_run_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _ensure_file(path: Path, label: str) -> None:
    if not path.exists() or not path.is_file():
        raise typer.BadParameter(f"{label} not found: {path}")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_config_json(config: RunConfig, run_root: Path) -> None:
    _ensure_dir(run_root)
    config_path = run_root / "config.json"
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(asdict(config), f, ensure_ascii=False, indent=2)


def _check_rscript_available(rscript: str) -> None:
    if shutil.which(rscript) is None:
        raise typer.BadParameter(
            f"Rscript executable not found: {rscript}. "
            f"Please install R and ensure '{rscript}' is in PATH, or pass --rscript."
        )


def _run_r_ena(rscript: str, ena_script: Path, run_root: Path) -> None:
    """
    Calls: Rscript r/ena_run.R --run-root <outputs/run_id>
    Your R script can parse args however you like. This is a simple convention.
    """
    _check_rscript_available(rscript)
    _ensure_file(ena_script, "ENA R script")

    cmd = [rscript, str(ena_script), "--run-root", str(run_root)]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise typer.Exit(code=e.returncode)


@app.command("run")
def run(
    input: Path = typer.Option(..., "--input", help="Input CSV file"),
    text_col: str = typer.Option("text", "--text-col", help="Text column name"),
    id_col: str = typer.Option("student_id", "--id-col", help="Student ID column name"),
    group_col: str = typer.Option("group", "--group-col", help="Group/condition column name"),
    n_topics: int = typer.Option(10, "--n-topics", min=1, help="Number of topics"),
    outdir: Path = typer.Option(Path("outputs"), "--outdir", help="Output directory"),
    run_id: Optional[str] = typer.Option(None, "--run-id", help="Run identifier (default: timestamp)"),
    seed: int = typer.Option(42, "--seed", help="Random seed"),
    # ENA parameters (MVP)
    ena_unit: Optional[str] = typer.Option(None, "--ena-unit", help="ENA unit column (default: same as --id-col)"),
    ena_conversation: Optional[str] = typer.Option(
        None,
        "--ena-conversation",
        help="Conversation column (default: same as --id-col). Use a session column if available.",
    ),
    ena_conditions: str = typer.Option("group", "--ena-conditions", help="Condition column for ENA comparison"),
    ena_window: int = typer.Option(1, "--ena-window", min=1, help="ENA sliding window size"),
    # R integration
    rscript: str = typer.Option("Rscript", "--rscript", help="Path/name of Rscript executable"),
    ena_script: Path = typer.Option(Path("r/ena_run.R"), "--ena-script", help="Path to ENA R script"),
) -> None:
    """
    Run the full TopicENA pipeline:
    1) BERTopic topic modeling (Python)
    2) Automated semantic coding for ENA input (Python)
    3) ENA analysis & visualization (R)
    """
    _ensure_file(input, "Input CSV")
    rid = run_id or _now_run_id()

    run_root = outdir / rid
    bertopic_dir = run_root / "bertopic"
    viz_dir = run_root / "viz"
    ena_input_dir = run_root / "ena_input"
    ena_out_dir = run_root / "ena"

    for d in [run_root, bertopic_dir, viz_dir, ena_input_dir, ena_out_dir]:
        _ensure_dir(d)

    cfg = RunConfig(
        input=str(input),
        text_col=text_col,
        id_col=id_col,
        group_col=group_col,
        n_topics=n_topics,
        outdir=str(outdir),
        run_id=rid,
        seed=seed,
        ena_unit=ena_unit or id_col,
        ena_conversation=ena_conversation or id_col,
        ena_conditions=ena_conditions,
        ena_window=ena_window,
        rscript=rscript,
        ena_script=str(ena_script),
    )
    _write_config_json(cfg, run_root)

    # Import lazily so `topicena --help` works even if heavy deps are not installed yet.
    try:
        from topicena.pipeline import run_pipeline
    except Exception as e:
        typer.echo(
            "ERROR: Failed to import topicena.pipeline.run_pipeline.\n"
            "Create src/topicena/pipeline.py with a run_pipeline(config: dict, paths: dict) function.\n"
            f"Import error: {e}"
        )
        raise typer.Exit(code=1)

    # Execute Python pipeline (BERTopic + coding + optional Python-side plots)
    run_pipeline(
        config=asdict(cfg),
        paths={
            "run_root": str(run_root),
            "bertopic_dir": str(bertopic_dir),
            "viz_dir": str(viz_dir),
            "ena_input_dir": str(ena_input_dir),
            "ena_out_dir": str(ena_out_dir),
        },
    )

    # Execute R ENA (reads from outputs/<run_id>/ena_input and writes to outputs/<run_id>/ena)
    _run_r_ena(rscript=rscript, ena_script=ena_script, run_root=run_root)

    typer.echo(f"Done. Outputs saved to: {run_root}")


if __name__ == "__main__":
    app()
