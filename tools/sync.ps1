param([string]$Port,[int]$Brightness=0,[switch]$List)
$ErrorActionPreference='Stop'
$options=@((Join-Path $PSScriptRoot 'sync_clock.py'))
if($Port){$options+=@('--port',$Port)}
if($Brightness){$options+=@('--brightness',$Brightness)}
if($List){$options+='--list'}
& python @options
if($LASTEXITCODE -ne 0){throw 'Synchronisation failed'}
