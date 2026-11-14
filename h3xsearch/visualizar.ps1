Set-Location -LiteralPath $PSScriptRoot
Write-Host 'Abra http://127.0.0.1:8080/ - Ctrl+C para encerrar.'
python -m http.server 8080 --bind 127.0.0.1 --directory site
