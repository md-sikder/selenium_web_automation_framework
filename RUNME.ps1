param(
  [switch]$Headless
)

Write-Host "=== Selenium UI Tests Runner (PowerShell) ==="

# 1) Python check
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Error "Python is not installed or not on PATH. Install from https://www.python.org/downloads/"
  exit 1
}

# 2) venv
if (-not (Test-Path ".venv")) {
  Write-Host "Creating virtual environment..."
  python -m venv .venv
}

# 3) activate
. .\.venv\Scripts\Activate.ps1

# 4) deps
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5) mode (GUI default)
if (-not $Headless.IsPresent) {
  $choice = Read-Host "Run mode: [1=GUI (default), 2=Headless]"
  if ($choice -eq "2") { $Headless = $true }
}

# 6) dirs
New-Item -ItemType Directory -Force -Path reports, logs, screenshots | Out-Null

# 7) run
$cmd = "pytest -n auto --env=test --html=reports/report.html --self-contained-html"
if ($Headless) { $cmd += " --headless" }
Write-Host "Running: $cmd"
Invoke-Expression $cmd
$code = $LASTEXITCODE

Write-Host "Report: reports/report.html"
if (Test-Path "reports/report.html") { Start-Process "reports/report.html" }
exit $code
