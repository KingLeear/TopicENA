# calling_r.py
import subprocess
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent  
    
    input_data = root / "r" / "RS.data.rda"
    output_dir = root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "Rscript",
        str(root / "r" / "example.R"),
        str(input_data),
        str(output_dir),
    ]

    # cwd 設成根目錄，讓 R 端 getwd() 就是根目錄
    subprocess.run(cmd, check=True, cwd=str(root))

if __name__ == "__main__":
    main()
