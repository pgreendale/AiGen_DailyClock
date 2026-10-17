# Quellen und genaue Verwendung

[Übersicht](../README.md) · Stand der Quellenprüfung: 17.10.2026.

Die folgenden Angaben unterscheiden tatsächliche Recheneingänge, Methodenrecherche, technische Referenzen und übernommene Daten. Rohdatendateien werden nicht als eigene Erhebung ausgegeben.

## TfL NUMBAT 2024 – numerischer Eingang

- [MON](https://crowding.data.tfl.gov.uk/NUMBAT/NUMBAT%202024/NBT24MON_outputs.xlsx), [TWT](https://crowding.data.tfl.gov.uk/NUMBAT/NUMBAT%202024/NBT24TWT_outputs.xlsx), [FRI](https://crowding.data.tfl.gov.uk/NUMBAT/NUMBAT%202024/NBT24FRI_outputs.xlsx)
- [Methodeneinführung](https://crowding.data.tfl.gov.uk/NUMBAT/Intro_to_NUMBAT.pdf)
- [TfL Open Data – Beschreibung von NUMBAT](https://tfl.gov.uk/info-for/open-data-users/our-open-data)
- [Nutzungsbedingungen Transport Data Service](https://tfl.gov.uk/corporate/terms-and-conditions/transport-data-service)

**Verwendet:** Stations-Eintritte und -Austritte, 96 Viertelstunden je Betriebstag, summiert über Stationen; typische Wochentage mit 1:3:1 gewichtet. Introduction/Open-Data-Seite dienen zur Einordnung als modellierte typische Nachfrage, nicht als zusätzliche Daten.

**Ergebnisdateien:** analysis/data/sums.json und profile_15min.json. Die Originaldateien sind wegen Größe und Lizenzierung nicht mitgeliefert; Downloadadressen sind in analysis/sources.json einsehbar.

**Attribution:** Die vollständigen verpflichtenden TfL-Lizenzhinweise stehen in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Für Weiterverwendung der Daten gelten die verlinkten TfL-Bedingungen, nicht die auf den Code bezogene Lizensierung des Projektes. 

## DfT National Travel Survey – numerischer Eingang

- [Tabellen zu Fahrtstartzeiten / NTS05](https://www.gov.uk/government/statistical-data-sets/nts05-trips)
- [NTS0502-ODS, konkret gespeicherte Veröffentlichung](https://assets.publishing.service.gov.uk/media/6a9ecdd5474b8101ece46434/nts0502.ods)
- [NTS 2024 – Definitionen](https://www.gov.uk/government/statistics/national-travel-survey-2024/nts-2024-notes-and-definitions)
- [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)

**Verwendet:** Blatt NTS0502a_start_time_by_purpose, Jahr 2024, stündliche Commuting- und Business-Prozentanteile für Mo–Fr in England. Die All-day-Zeile wird ausgelassen; Stundenanteile werden durch 100 geteilt und auf vier Viertelstunden übertragen.

**Nicht verwendet:** jüngere Jahreszeilen derselben fortgeschriebenen Datei, Individualdaten, Erwerbsstatusfilter oder Verkehrsmittel-Auswahl. Der Downloadname allein fixiert das Datenjahr nicht; Jahrfilter und Prüfsumme tun dies.

**Attribution:** Source: Department for Transport, National Travel Survey. Contains public sector information licensed under the Open Government Licence v3.0, soweit die Quelle keine gesonderten Rechte ausweist. Die Zweckanteile aller Verkehrsarten werden als ausdrückliche Annahme auf den Londoner Bahnverkehr übertragen.

## Eurostat HETUS

- [Beschreibung und Mikrodatenverfügbarkeit](https://ec.europa.eu/eurostat/en/web/microdata/collections-research/harmonised-european-time-use-surveys)
- [Variablenbeschreibung](https://ec.europa.eu/eurostat/documents/203647/10397147/HETUS_variables%2Bdescription.pdf/54efe947-767f-2e46-09ee-fc13688f04ac)
- [HETUS 2018 Guidelines](https://ec.europa.eu/eurostat/documents/3859598/11597606/KS-GQ-20-011-EN-N.pdf)

**Verwendet:** ausschließlich Methoden-/Verfügbarkeitsrecherche: 10-Minuten-Tagebuchraster, mögliche Erwerbsmerkmale und Zugangsbeschränkungen. Die aktuelle Eurostat-Seite nennt 17 SUF-Länder für 2010 und eine Freigabe der Welle 2020 nicht vor 2027.

**Nicht verwendet:** keine individuellen Tagebuchfolgen, keine HETUS-Zahlen zur Berechnung der Kurve. 

## Ergänzende Zeitverwendungsrecherche

- [ONS, Time use in the UK, March 2023](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/bulletins/timeuseintheuk/march2023/pdf)
- [INSEE, Zeitverwendung](https://www.insee.fr/fr/statistiques/1281016)

**Verwendet:** qualitative Orientierung von Schlaf, Arbeit und Tagesrhythmen. **Keine** Werte aus diesen Veröffentlichungen gingen in profile_15min.json, Kubikkoeffizienten oder Firmware ein.

## Waveshare – Hardware und übernommene Initialisierungsdaten

- [RP2040-LCD-1.28 Wiki](https://www.waveshare.com/wiki/RP2040-LCD-1.28)
- [RP2040-LCD-1.28 Herstellerschaltplan, S. 1–2](https://files.waveshare.com/upload/6/60/RP2040-LCD-1.28-sch.pdf)
- [Demoarchiv RP2350-LCD-1.28](https://files.waveshare.com/wiki/RP2350-LCD-1.28/RP2350-LCD-1.28.zip)
- [CircuitPython-Boarddefinition als zusätzliche Pinreferenz](https://github.com/adafruit/circuitpython/blob/main/ports/raspberrypi/boards/waveshare_rp2040_lcd_1_28/pins.c)

**Verwendet:** Wiki und RP2040-Schaltplan für Boardtyp, Displayauflösung, SPI- und Steuerpins. CircuitPython diente als Gegenprüfung der Pinbelegung, nicht als Firmwarebasis.

**Übernommen:** GC9A01-Registerinitialisierung aus C/lib/LCD/LCD_1in28.c des Waveshare-RP2350-Demoarchivs, weil dieses gemeinsame Displayinitialisierung enthält. Daraus wurde firmware/generated/gc9a01_init.h erzeugt. Der Lizenzhinweis aus dem Demo (DEV_Config.h) ist in licenses/Waveshare.txt erhalten. Eigene Ergänzungen: RP2040-SDK-Anbindung, Bilddarstellung, PWM und 180°-Montagekorrektur. Das getestete Gerät ist trotz Herkunft dieser Registerfolge ein RP2040.

**Nicht übernommen:** vollständige Waveshare-Anwendungssoftware oder Touch-/IMU-Funktionen.

## Raspberry Pi Pico SDK und Extension

- [Pico SDK 2.2.0](https://github.com/raspberrypi/pico-sdk/tree/2.2.0)
- [Pico SDK Runtime / USB-stdio](https://www.raspberrypi.com/documentation/pico-sdk/runtime.html#pico_stdio_usb)
- [Offizielle Pico-VS-Code-Erweiterung](https://github.com/raspberrypi/pico-vscode)

**Verwendet:** CMake-/Boardstruktur, Hardware-SPI/PWM, Timer und USB-CDC über stdio. Die neuen Konfigurationsskripte erkennen vorhandene Extension-Werkzeuge oder nehmen explizite Pfade. SDK, TinyUSB, Compiler und Extension werden nicht mitgeliefert; ihre eigenen Lizenztexte bleiben in den Installationen maßgeblich.

## Farbskala und Plotwerkzeuge

- [Matplotlib Colormap-Referenz](https://matplotlib.org/stable/gallery/color/colormap_reference.html)
- [Matplotlib YlGnBu-Definition](https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/_cm.py)

**Verwendet:** YlGnBu_r, beschnitten auf 0–0,75 und mit 256 Werten neu abgetastet, für den blau-grünen Ring und den Stundenzeiger. Matplotlib/Pillow/NumPy erzeugen die Abbildungen und Flashassets. Die Änderung der Farbskala sowie die Normierung auf g/max(g) sind projektspezifisch. Bibliotheken sind nicht im Repository enthalten.

Die Lizenzrechtliche Einordnung einschließlich ColorBrewer/Apache, Schriftkonturen und offener TfL-/Waveshare-Fragen steht im [Lizenzbericht](06-lizenzpruefung.md).


### Lizenzhinweis zur LCD-Initialisierung

Die LCD-Initialisierungsfolge wurde aus dem offiziellen Waveshare-Demo RP2350-LCD-1.28, Datei C/lib/LCD/LCD_1in28.c, übernommen und in eine Registertabelle überführt. Waveshare ist die unmittelbare Quelle, nicht als alleiniger ursprünglicher Urheber nachgewiesen. Der im Demo enthaltene Freigabe- und Haftungstext bleibt unverändert in licenses/Waveshare.txt erhalten. Soweit übernommene Bestandteile Rechten oder Lizenzbedingungen Dritter unterliegen, gelten diese für die betreffenden Bestandteile weiter; die Projektlizenz ersetzt sie nicht. Dieser Hinweis behauptet keine Umlizenzierung und ersetzt keine gegebenenfalls konkret erforderlichen Copyright- oder Lizenzangaben.
