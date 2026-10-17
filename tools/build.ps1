param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Options)
$ErrorActionPreference='Stop'
& python (Join-Path $PSScriptRoot 'build.py') @Options
if($LASTEXITCODE -ne 0){throw 'build failed'}
