#!/usr/bin/env bash
set -e

echo "=== [1/5] Update system ==="
sudo apt update

echo "=== [2/5] Install system dependencies ==="
sudo apt install -y \
  build-essential pkg-config \
  curl unzip git \
  libcurl4-openssl-dev libssl-dev \
  libxml2-dev \
  libfontconfig1-dev libfreetype6-dev \
  libharfbuzz-dev libfribidi-dev \
  libpng-dev libjpeg-dev \
  libnss3 libatk-bridge2.0-0 libcups2 \
  libxcomposite1 libxdamage1 libxfixes3 \
  libxrandr2 libgbm1 libxkbcommon0 \
  libpango-1.0-0 libcairo2 libasound2

echo "=== [3/5] (Optional) Install AWS CLI v2 if not exists ==="
if ! command -v aws >/dev/null 2>&1; then
  cd /tmp
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip -q awscliv2.zip
  sudo ./aws/install
else
  echo "AWS CLI already installed"
fi

echo "=== [4/5] Install Python dependencies (current venv) ==="
python -m pip install --upgrade pip
python -m pip install -U \
  bertopic \
  kaleido \
  plotly

echo "=== [5/5] Sanity checks ==="
python - << 'PY'
import plotly.express as px
import kaleido

fig = px.scatter(x=[1,2,3], y=[4,5,6])
fig.write_image("kaleido_test.png")

print("✓ plotly version OK")
print("✓ kaleido version OK")
print("✓ PNG export successful (kaleido_test.png)")
PY

echo "=== Setup completed successfully ==="
