from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RENAConfig:
    window_size_back: int = 20


def _validate_config(cfg: RENAConfig) -> None:
    if cfg.window_size_back <= 0:
        raise ValueError("window_size_back must be > 0")


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
    r_script_path: str,
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
    if not os.path.exists(r_script_path):
        raise FileNotFoundError(f"R script not found: {r_script_path}")

    cmd = [
        rscript,
        r_script_path,
        "--window_size_back",
        str(cfg.window_size_back),
    ]

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
