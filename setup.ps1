$ErrorActionPreference = "Stop"
Write-Host "PocketSmart AI - Python 3.15 setup" -ForegroundColor Cyan
py -3.15 --version
if (-not (Test-Path ".venv")) { py -3.15 -m venv .venv }
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path ".env")) { Copy-Item .env.example .env }
Write-Host "Setup complete. Edit .env, then run: .\.venv\Scripts\python.exe run.py" -ForegroundColor Green
