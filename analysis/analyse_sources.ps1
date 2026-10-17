$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$base=Join-Path $PSScriptRoot 'data'
function ReadXml($z,$p){$r=[IO.StreamReader]::new($z.GetEntry($p).Open());try{return ,([xml]$r.ReadToEnd())}finally{$r.Dispose()}}
$all=@{}
foreach($day in @('MON','TWT','FRI')){
$z=[IO.Compression.ZipFile]::OpenRead($base+'/NBT24'+$day+'_outputs.xlsx')
$ss=ReadXml $z 'xl/sharedStrings.xml'
$strings=@($ss.sst.si|ForEach-Object{$_.InnerText})
foreach($sheet in @(1,7,8)){
$x=ReadXml $z "xl/worksheets/sheet$sheet.xml"
$rows=@($x.worksheet.sheetData.row)
if($day -eq 'MON'){Write-Output "SHEET $sheet";$rows|Select-Object -First 4|ForEach-Object{(@($_.c)|ForEach-Object{$v=$_.v;if($_.t -eq 's'){$v=$strings[[int]$v]};"$($_.r)=$v"}) -join ' | '}}
if($sheet -in @(7,8)){$sums=@{};foreach($row in $rows|Select-Object -Skip 3){foreach($c in $row.c){$col=$c.r -replace '\d','';if($c.t -ne 's' -and $null -ne $c.v){$sums[$col]+=[double]$c.v}}};$all[($day+'_'+$sheet)]=$sums}
}
$z.Dispose()
}
$all|ConvertTo-Json -Depth 5|Set-Content "$base/sums.json" -Encoding UTF8
$z=[IO.Compression.ZipFile]::OpenRead("$base/nts0502.ods")
$x=ReadXml $z 'content.xml'
$ns=[Xml.XmlNamespaceManager]::new($x.NameTable)
$ns.AddNamespace('t','urn:oasis:names:tc:opendocument:xmlns:table:1.0')
foreach($tab in $x.SelectNodes('//t:table',$ns)){if($tab.GetAttribute('name','urn:oasis:names:tc:opendocument:xmlns:table:1.0') -match '^NTS0502'){Write-Output $tab.GetAttribute('name','urn:oasis:names:tc:opendocument:xmlns:table:1.0');foreach($row in $tab.SelectNodes('t:table-row',$ns)){$cells=@($row.SelectNodes('t:table-cell',$ns)|ForEach-Object{$_.InnerText});if($cells[0] -eq '2025'){Write-Output ($cells -join ' | ')}}}}
$z.Dispose()
