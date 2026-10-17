param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Options)
$ErrorActionPreference='Stop'
& python (Join-Path $PSScriptRoot 'configure.py') @Options
if($LASTEXITCODE -ne 0){throw 'configure failed'}
