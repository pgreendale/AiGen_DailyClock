# Zeitliche Dichte von Wechselereignissen – Datenstand 17.10.2026

## Status
Ausgewertet: öffentliche TfL-NUMBAT-2024-Tabellen Station_Entries und Station_Exits, Montag/Dienstag–Donnerstag/Freitag, 96 Viertelstunden. Ergänzend NTS0502a 2024, England, Fahrtbeginn nach Fahrtzweck, stündlich.
Nicht ausgewertet: individuelle HETUS-Tagebuchfolgen (kein Datenzugang). Kein Ausschluss von Dreischichtbetrieb und keine Selektion auf Erwerbstätige möglich. Die Daten sind ein europäischer regionaler Verkehrsindikator, kein europäischer Bevölkerungsdurchschnitt.

## Methode
Stationssumme je Viertelstunde; Wochentagsmittel (MON+3*TWT+FRI)/5.
Verkehrsereignisse = Bahnhofseintritte + Bahnhofsaustritte. Kein Fahrgastbestand, keine Zahl verschiedener Personen; eine Reise kann zwei Ereignisse beitragen. Interne Umstiege werden nicht vollständig erfasst. Typische Herbsttage, voller fahrplanmäßiger Betrieb, keine Jahresmittelwerte. Verkehrszeit 05:00–04:59 in lokale Uhrzeit umsortiert; die Nacht gehört zum vorher beginnenden Verkehrstag. Es handelt sich nicht um ein separat exakt nach Kalender-Mo–Fr rekonstruiertes Nachtprofil.
Normierung: Anteil jedes Fensters an der Summe der 96 Fenster.
Tagessumme: 9.861.998,87 Ein-/Ausgangsereignisse. Viertelstundensummen stimmen für alle sechs Eingangstabellen mit den jeweiligen Total-Spalten bis unter 0,000001 Ereignisse überein.

## Erwerbsgewichtung – Szenarien, keine erhobenen Schadenswerte
c_h = NTS-Anteil Commuting, b_h = NTS-Anteil Business unter allen Fahrtanfängen einer Stunde (2024).
Basisszenario: Faktor 1 + 2*c_h + 2*b_h für 05:00–11:59; sonst 1 + 0,5*c_h + 2*b_h.
Starkes Szenario: Faktor 1 + 4*c_h + 4*b_h für 05:00–11:59; sonst 1 + c_h + 4*b_h.
Damit erhalten Pendelfahrten modellhaft morgens Gewicht 3 bzw. 5, außerhalb dieses Fensters 1,5 bzw. 2; Geschäftsfahrten Gewicht 3 bzw. 5; andere Fahrten Gewicht 1.
Die Richtung des Arbeitswegs ist nicht bekannt. Die morgendliche Hinwegannahme ist ein Proxy und kann bei Schichtarbeit, Teilzeit und geteilten Arbeitstagen falsch sein.
NTS bezieht sich auf England, alle Verkehrsarten und alle Personen, nicht spezifisch auf TfL-Fahrgäste. Die Übertragung der stündlichen Zweckanteile auf Londoner Ein-/Ausgänge und alle Viertelstunden ist eine Modellannahme. Sprünge an vollen Stunden können allein daraus entstehen.
Beide Scores werden separat auf 100 Prozent normiert. Es sind relative Gestaltungsindizes, keine Wechselraten pro Erwerbstätigem und keine Verspätungswahrscheinlichkeiten.
Frühstück, Schlaf und Körperpflege werden durch Verkehrsereignisse nicht erfasst; geringe Verkehrswerte belegen dort keine geringe Tätigkeitswechseldichte.
Indirekt erwerbsnotwendige Betreuung und Begleitwege sind in den aggregierten Kategorien nicht eindeutig identifizierbar und deshalb nicht pauschal hochgewichtet.

## Quellen
- TfL NUMBAT-Verzeichnis: https://crowding.data.tfl.gov.uk/
- https://crowding.data.tfl.gov.uk/NUMBAT/NUMBAT%202024/NBT24MON_outputs.xlsx
- https://crowding.data.tfl.gov.uk/NUMBAT/NUMBAT%202024/NBT24TWT_outputs.xlsx
- https://crowding.data.tfl.gov.uk/NUMBAT/NUMBAT%202024/NBT24FRI_outputs.xlsx
- NTS0502: https://www.gov.uk/government/statistical-data-sets/nts05-trips
- https://assets.publishing.service.gov.uk/media/6a9ecdd5474b8101ece46434/nts0502.ods
- HETUS: https://ec.europa.eu/eurostat/en/web/microdata/collections-research/harmonised-european-time-use-surveys
- HETUS SUF-Variablen: https://ec.europa.eu/eurostat/documents/203647/10397147/HETUS_variables%2Bdescription.pdf/54efe947-767f-2e46-09ee-fc13688f04ac

## Noch erforderlich für das eigentliche HETUS-Ergebnis
Zugelassene individuelle Daten; Erwerbstätigkeitsmarker; expliziter Marker für Dreischichtbetrieb aus nationalen Zusatzdaten, da im geprüften harmonisierten Verzeichnis kein eindeutiger Marker gefunden wurde. Kein Ersatz dieses Markers durch Ausschluss bloß nächtlicher Tage.
Wechsel an 10-Minuten-Grenzen nicht naiv in 15-Minuten-Fenster zählen: Das erzeugt abwechselnd ein/zwei mögliche Grenzen und künstliche Spitzen. Stattdessen Grenzunsicherheit modellieren, z.B. Ereignismasse gleichmäßig über das 10-Minuten-Unsicherheitsfenster verteilen, mit Sensitivität gegenüber der Phasenlage. Keine minutenpräzisen Aussagen zu kurzen Umstiegen aus HETUS allein.
Keine künstliche Verbindung von Ende und Anfang desselben Tagebuchs als aufeinanderfolgende reale Tage.

## Ergebnisse je Viertelstunde
Die drei Anteilsspalten summieren jeweils auf 100 %. JSON enthält ungerundete Rechenwerte.

| Beginn | Eintritte | Austritte | Anteil Verkehr % | Erwerb Basis % | Erwerb stark % |
|---|---:|---:|---:|---:|---:|
| 00:00 | 11.375 | 17.686 | 0,295 | 0,280 | 0,271 |
| 00:15 | 7.939 | 13.900 | 0,221 | 0,211 | 0,203 |
| 00:30 | 5.191 | 10.286 | 0,157 | 0,149 | 0,144 |
| 00:45 | 2.832 | 7.145 | 0,101 | 0,096 | 0,093 |
| 01:00 | 1.382 | 4.491 | 0,060 | 0,063 | 0,065 |
| 01:15 | 875 | 2.405 | 0,033 | 0,035 | 0,036 |
| 01:30 | 677 | 1.195 | 0,019 | 0,020 | 0,021 |
| 01:45 | 606 | 753 | 0,014 | 0,015 | 0,015 |
| 02:00 | 540 | 629 | 0,012 | 0,013 | 0,014 |
| 02:15 | 497 | 566 | 0,011 | 0,012 | 0,013 |
| 02:30 | 470 | 514 | 0,010 | 0,011 | 0,012 |
| 02:45 | 445 | 479 | 0,009 | 0,010 | 0,011 |
| 03:00 | 410 | 450 | 0,009 | 0,010 | 0,011 |
| 03:15 | 380 | 422 | 0,008 | 0,009 | 0,010 |
| 03:30 | 358 | 393 | 0,008 | 0,009 | 0,009 |
| 03:45 | 331 | 367 | 0,007 | 0,008 | 0,009 |
| 04:00 | 284 | 331 | 0,006 | 0,007 | 0,007 |
| 04:15 | 356 | 294 | 0,007 | 0,007 | 0,008 |
| 04:30 | 293 | 220 | 0,005 | 0,006 | 0,006 |
| 04:45 | 231 | 152 | 0,004 | 0,004 | 0,005 |
| 05:00 | 4.564 | 1.000 | 0,056 | 0,106 | 0,139 |
| 05:15 | 8.809 | 2.431 | 0,114 | 0,215 | 0,281 |
| 05:30 | 15.363 | 4.784 | 0,204 | 0,385 | 0,504 |
| 05:45 | 23.724 | 9.116 | 0,333 | 0,628 | 0,822 |
| 06:00 | 32.425 | 15.966 | 0,491 | 0,902 | 1,172 |
| 06:15 | 41.835 | 24.337 | 0,671 | 1,234 | 1,603 |
| 06:30 | 52.342 | 34.036 | 0,876 | 1,610 | 2,092 |
| 06:45 | 62.569 | 45.135 | 1,092 | 2,008 | 2,609 |
| 07:00 | 73.103 | 57.562 | 1,325 | 1,974 | 2,400 |
| 07:15 | 85.537 | 69.566 | 1,573 | 2,343 | 2,849 |
| 07:30 | 99.278 | 81.835 | 1,836 | 2,736 | 3,326 |
| 07:45 | 111.050 | 95.442 | 2,094 | 3,119 | 3,793 |
| 08:00 | 118.423 | 109.727 | 2,313 | 2,530 | 2,672 |
| 08:15 | 119.904 | 119.477 | 2,427 | 2,655 | 2,804 |
| 08:30 | 116.165 | 122.334 | 2,418 | 2,645 | 2,793 |
| 08:45 | 106.117 | 120.003 | 2,293 | 2,507 | 2,648 |
| 09:00 | 93.615 | 112.755 | 2,093 | 2,123 | 2,142 |
| 09:15 | 80.601 | 100.050 | 1,832 | 1,858 | 1,875 |
| 09:30 | 70.692 | 85.483 | 1,584 | 1,606 | 1,621 |
| 09:45 | 62.574 | 74.422 | 1,389 | 1,409 | 1,422 |
| 10:00 | 57.052 | 66.456 | 1,252 | 1,151 | 1,085 |
| 10:15 | 52.528 | 59.535 | 1,136 | 1,045 | 0,984 |
| 10:30 | 51.224 | 54.062 | 1,068 | 0,981 | 0,925 |
| 10:45 | 50.481 | 51.529 | 1,034 | 0,951 | 0,896 |
| 11:00 | 49.594 | 50.840 | 1,018 | 0,936 | 0,882 |
| 11:15 | 49.212 | 49.986 | 1,006 | 0,925 | 0,871 |
| 11:30 | 50.348 | 49.223 | 1,010 | 0,928 | 0,875 |
| 11:45 | 51.393 | 49.865 | 1,027 | 0,944 | 0,889 |
| 12:00 | 51.845 | 51.253 | 1,045 | 0,899 | 0,803 |
| 12:15 | 51.877 | 51.766 | 1,051 | 0,904 | 0,807 |
| 12:30 | 53.019 | 51.588 | 1,061 | 0,912 | 0,814 |
| 12:45 | 53.451 | 52.210 | 1,071 | 0,921 | 0,823 |
| 13:00 | 53.344 | 52.989 | 1,078 | 0,957 | 0,877 |
| 13:15 | 53.220 | 52.990 | 1,077 | 0,956 | 0,876 |
| 13:30 | 54.712 | 52.726 | 1,089 | 0,967 | 0,887 |
| 13:45 | 55.367 | 53.595 | 1,105 | 0,981 | 0,899 |
| 14:00 | 55.930 | 54.767 | 1,122 | 0,978 | 0,884 |
| 14:15 | 56.929 | 55.573 | 1,141 | 0,994 | 0,898 |
| 14:30 | 60.278 | 56.367 | 1,183 | 1,031 | 0,931 |
| 14:45 | 63.528 | 58.889 | 1,241 | 1,082 | 0,978 |
| 15:00 | 67.622 | 62.501 | 1,319 | 1,124 | 0,996 |
| 15:15 | 72.363 | 66.234 | 1,405 | 1,197 | 1,061 |
| 15:30 | 80.046 | 70.032 | 1,522 | 1,296 | 1,149 |
| 15:45 | 85.686 | 75.676 | 1,636 | 1,394 | 1,235 |
| 16:00 | 91.598 | 81.853 | 1,759 | 1,638 | 1,558 |
| 16:15 | 97.081 | 87.385 | 1,870 | 1,742 | 1,657 |
| 16:30 | 107.979 | 93.134 | 2,039 | 1,899 | 1,807 |
| 16:45 | 114.841 | 101.305 | 2,192 | 2,041 | 1,942 |
| 17:00 | 122.484 | 110.270 | 2,360 | 2,216 | 2,122 |
| 17:15 | 126.820 | 117.832 | 2,481 | 2,330 | 2,230 |
| 17:30 | 131.379 | 124.061 | 2,590 | 2,432 | 2,329 |
| 17:45 | 126.259 | 128.050 | 2,579 | 2,422 | 2,318 |
| 18:00 | 119.036 | 127.938 | 2,504 | 2,213 | 2,022 |
| 18:15 | 108.280 | 122.633 | 2,341 | 2,069 | 1,890 |
| 18:30 | 98.745 | 113.963 | 2,157 | 1,906 | 1,741 |
| 18:45 | 85.701 | 103.334 | 1,917 | 1,694 | 1,547 |
| 19:00 | 74.529 | 92.108 | 1,690 | 1,453 | 1,297 |
| 19:15 | 65.139 | 80.513 | 1,477 | 1,270 | 1,134 |
| 19:30 | 58.565 | 69.960 | 1,303 | 1,121 | 1,001 |
| 19:45 | 52.040 | 61.660 | 1,153 | 0,991 | 0,885 |
| 20:00 | 47.514 | 55.349 | 1,043 | 0,905 | 0,815 |
| 20:15 | 44.136 | 50.131 | 0,956 | 0,829 | 0,746 |
| 20:30 | 42.500 | 46.207 | 0,899 | 0,781 | 0,702 |
| 20:45 | 40.269 | 43.668 | 0,851 | 0,739 | 0,665 |
| 21:00 | 38.734 | 41.710 | 0,816 | 0,708 | 0,637 |
| 21:15 | 37.759 | 39.991 | 0,788 | 0,684 | 0,616 |
| 21:30 | 38.394 | 38.884 | 0,784 | 0,680 | 0,612 |
| 21:45 | 38.262 | 38.686 | 0,780 | 0,677 | 0,609 |
| 22:00 | 37.936 | 38.828 | 0,778 | 0,703 | 0,654 |
| 22:15 | 36.694 | 38.598 | 0,763 | 0,690 | 0,641 |
| 22:30 | 35.498 | 37.705 | 0,742 | 0,671 | 0,624 |
| 22:45 | 31.934 | 36.143 | 0,690 | 0,624 | 0,580 |
| 23:00 | 27.737 | 33.333 | 0,619 | 0,577 | 0,549 |
| 23:15 | 23.463 | 29.455 | 0,537 | 0,500 | 0,475 |
| 23:30 | 19.868 | 25.291 | 0,458 | 0,426 | 0,406 |
| 23:45 | 15.425 | 21.417 | 0,374 | 0,348 | 0,331 |
