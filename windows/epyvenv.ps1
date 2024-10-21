$base = Get-Location
$sc = Join-Path $base "venv\Scripts\activate.ps1"
Invoke-Expression -Command $sc
