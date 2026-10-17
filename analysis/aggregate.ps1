$ErrorActionPreference='Stop'
$base=Join-Path $PSScriptRoot 'data'
$s=Get-Content "$base/sums.json" -Raw|ConvertFrom-Json
function Col($n){$v='';while($n -gt 0){$n--;$v=[char][int](65+$n%26)+$v;$n=[math]::Floor($n/26)};return $v}
Add-Type -AssemblyName System.IO.Compression.FileSystem
$z=[IO.Compression.ZipFile]::OpenRead("$base/nts0502.ods")
$r=[IO.StreamReader]::new($z.GetEntry('content.xml').Open());[xml]$x=$r.ReadToEnd();$r.Dispose();$z.Dispose()
$ns=[Xml.XmlNamespaceManager]::new($x.NameTable);$ns.AddNamespace('t','urn:oasis:names:tc:opendocument:xmlns:table:1.0')
$shares=@{}
foreach($tab in $x.SelectNodes('//t:table',$ns)){if($tab.GetAttribute('name','urn:oasis:names:tc:opendocument:xmlns:table:1.0') -eq 'NTS0502a_start_time_by_purpose'){foreach($row in $tab.SelectNodes('t:table-row',$ns)){$c=@($row.SelectNodes('t:table-cell',$ns)|ForEach-Object{$_.InnerText});if($c[0] -eq '2024' -and $c[1] -ne 'All day'){$h=[int]$c[1].Substring(0,2);$shares[$h]=@([double]$c[2],[double]$c[3])}}}}
$rows=@(for($i=0;$i -lt 96;$i++){
$col=Col ($i+12);$hour=([math]::Floor($i/4)+5)%24;$minute=($i%4)*15
$en=($s.MON_7.$col+3*$s.TWT_7.$col+$s.FRI_7.$col)/5
$ex=($s.MON_8.$col+3*$s.TWT_8.$col+$s.FRI_8.$col)/5
$comm=$shares[[int]$hour][0]/100;$bus=$shares[[int]$hour][1]/100
[pscustomobject]@{time=('{0:00}:{1:00}' -f $hour,$minute);hour=$hour;entries=$en;exits=$ex;events=($en+$ex);commuting_share_england=$comm;business_share_england=$bus;score_3x=($en+$ex)*(1+$(if($hour -ge 5 -and $hour -lt 12){2}else{0.5})*$comm+2*$bus);score_5x=($en+$ex)*(1+$(if($hour -ge 5 -and $hour -lt 12){4}else{1})*$comm+4*$bus)}
})
$total=($rows|Measure-Object events -Sum).Sum;$t3=($rows|Measure-Object score_3x -Sum).Sum;$t5=($rows|Measure-Object score_5x -Sum).Sum
foreach($row in $rows){$row|Add-Member share_pct (100*$row.events/$total);$row|Add-Member weighted3_pct (100*$row.score_3x/$t3);$row|Add-Member weighted5_pct (100*$row.score_5x/$t5)}
$rows=@($rows|Sort-Object time)
$rows|ConvertTo-Json -Depth 4|Set-Content "$base/profile_15min.json" -Encoding UTF8
"TOTAL events=$total"
"TOP RAW";$rows|Sort-Object events -Descending|Select-Object -First 5 time,events,share_pct|Format-Table
"TOP weighted3";$rows|Sort-Object score_3x -Descending|Select-Object -First 5 time,weighted3_pct,commuting_share_england|Format-Table
"HOURLY"
$rows|Group-Object hour|ForEach-Object{[pscustomobject]@{hour=[int]$_.Name;share=[math]::Round(($_.Group|Measure-Object share_pct -Sum).Sum,2);weighted3=[math]::Round(($_.Group|Measure-Object weighted3_pct -Sum).Sum,2);weighted5=[math]::Round(($_.Group|Measure-Object weighted5_pct -Sum).Sum,2)}}|Sort-Object hour|Format-Table
"VALIDATION"
foreach($day in @('MON','TWT','FRI')){foreach($n in @(7,8)){$obj=$s.($day+'_'+$n);$q=0;for($i=12;$i -le 107;$i++){$q+=$obj.(Col $i)};"$day sheet$n totalDifference=$($q-$obj.E)"}}
$rows|ConvertTo-Json -Depth 4|Set-Content "$base/profile_15min.json" -Encoding UTF8
