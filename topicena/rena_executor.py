from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RENAConfig:
    window_size_back: int = 20
    ena_input: str = ""  
    ena_output: str = ""


def _validate_config(cfg: RENAConfig) -> None:
    if cfg.window_size_back <= 0:
        raise ValueError("window_size_back must be > 0")
    
    # ena_input must exist (file)
    if not cfg.ena_input:
        raise ValueError("ena_input is required")
    ena_input_path = Path(cfg.ena_input)
    if not ena_input_path.exists():
        raise FileNotFoundError(f"ena_input file not found: {ena_input_path}")
    if not ena_input_path.is_file():
        raise ValueError(f"ena_input must be a file path, got: {ena_input_path}")

    # ena_output must be a directory (create if not exists)
    if not cfg.ena_output:
        raise ValueError("ena_output is required")
    ena_output_path = Path(cfg.ena_output)
    ena_output_path.mkdir(parents=True, exist_ok=True)
    if not ena_output_path.is_dir():
        raise ValueError(f"ena_output must be a directory path, got: {ena_output_path}")



def find_rscript() -> str:
    """
    Locate Rscript in PATH. Raise a clear error if not found.
    """
    rscript = shutil.which("Rscript")
    if not rscript:
        raise RuntimeError(
            "Rscript not found in PATH. Please install R and ensure Rscript is available."
        )
    return rscript


def run_rena_rscript(
    cfg: RENAConfig,
    extra_args: Optional[List[str]] = None,
    cwd: Optional[str] = None,
) -> subprocess.CompletedProcess:
    """
    Execute an R script via Rscript, passing window_size_back as a CLI argument.

    Example command:
        Rscript path/to/ena_runner.R --window_size_back 20

    Returns:
        subprocess.CompletedProcess (includes returncode, stdout, stderr)
    """
    _validate_config(cfg)

    rscript = find_rscript()
    # if not os.path.exists(r_script_path):
    #     raise FileNotFoundError(f"R script not found: {r_script_path}")


    # ena_r_script = "./topicena/ena_script.R" 
    ena_r_script = Path(__file__).resolve().parent / "ena_script.R"

    # r_script_path = str(root / "r" / "example.R")

    cmd = [
        rscript,
        ena_r_script,
        cfg.ena_input,
        cfg.ena_output,
    ]

    # cmd = [
    #     rscript,
    #     r_script_path,
    #     "--window_size_back",
    #     str(cfg.window_size_back),
    # ]

    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "rENA execution failed.\n"
            f"Command: {' '.join(cmd)}\n"
            f"Return code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}\n"
        )

    return result
