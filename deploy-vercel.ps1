$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
$tok = (Get-ItemProperty -Path 'HKCU:\Environment').VERCEL_TOKEN
$env:VERCEL_TOKEN = $tok
npx vercel@latest deploy --prod --yes 2>&1 | Select-Object -Last 2
