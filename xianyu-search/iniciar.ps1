Set-Location -LiteralPath $PSScriptRoot
if (Test-Path -LiteralPath '.venv\Scripts\python.exe') {
    & '.\.venv\Scripts\python.exe' server.py
} else {
    Write-Host 'Siga a instalação no GUIA.md antes de iniciar.'
}
