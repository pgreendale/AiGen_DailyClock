# Lizenzprüfung für eine Veröffentlichung unter MIT

Stand: 17.10.2026. Geprüft wurde der konkrete Inhalt dieses Repositorys, nicht beliebige zusätzliche Dateien einer späteren Veröffentlichung. Dies ist eine technische Quellen- und Lizenzprüfung mit benannten Unsicherheiten, keine verbindliche rechtliche Freigabe.

## Ergebnis

**Eigener Code kann unter MIT veröffentlicht werden; ein pauschales „sämtlicher Inhalt ausschließlich MIT“ wäre falsch.** Es wurde kein eindeutiges Copyleft-Hindernis für eigenen Code festgestellt. Daten, Farbdefinitionen und externer Code behalten ihre Bedingungen. Die Prüfung benennt Unsicherheiten bei TfL-Aktualitätsvorgaben und der Reichweite der Waveshare-Erlaubnis.

## Einzelprüfung

| Bestandteil | Befund | Folge |
|---|---|---|
| eigener C-/Python-/PowerShell-Code, eigene Texte und Funktionszeichnungen | kein bewusst übernommener Fremdcode außer ausgewiesenen Teilen | MIT für bestehende eigene Rechte möglich |
| TfL NUMBAT und abgeleitete Zahlen | TfL-spezifische, auf OGL 2.0 basierende Bedingungen, keine MIT-Lizenz | Quellenhinweise und Bedingungen erhalten; Aktualitätsfrage offen |
| NTS0502a / DfT | OGL v3.0 laut Veröffentlichungsseite, sofern nicht anders ausgewiesen | kommerzielle Nutzung und Bearbeitung erlaubt; Quelle und Lizenzlink erhalten |
| ColorBrewer YlGnBu | Apache-2.0 laut Matplotlib-Lizenzsammlung | mit MIT-Projekt kombinierbar; Apache-Hinweise und Änderungsvermerk erhalten |
| Matplotlib-Ableitungen | BSD-kompatible Matplotlib-Lizenz | mit MIT kombinierbar; Originalhinweise erhalten |
| DejaVu Sans | Bitstream-Vera-Lizenz, DejaVu-Änderungen Public Domain | keine ausschließliche MIT-Umlizenzierung; Lizenzhinweise für enthaltene Konturen vorsorglich beigefügt |
| Waveshare LCD-Registerfolge | MIT-ähnlicher Freigabetext in eingebundener DEV_Config.h, kein übergreifendes LICENSE im Demoarchiv | Waveshare als unmittelbare Quelle nennen, Originaltext erhalten und Drittbedingungen vorbehalten; Reichweite bleibt nicht abschließend nachgewiesen |
| Pico SDK 2.2.0 | BSD-3-Clause, zusätzlich dateibezogene Hinweise möglich | MIT-Projekt zulässig; bei Binärdistribution Hinweise beilegen |
| TinyUSB | MIT | Original-Copyright und Lizenz beilegen |
| newlib / libm / libgcc in UF2 | Linkermap bestätigt Einbindung, mehrere Laufzeitlizenzen | separates Firmware-Release braucht versionspassende Laufzeitnotices |
| Hersteller-PDFs und HETUS-Mikrodaten | nicht im Repository enthalten | keine Umlizenzierung beanspruchen; externe Links beibehalten |

### TfL: erlaubt, aber nicht bedingungslos

Die [Transport-Data-Service-Lizenz](https://tfl.gov.uk/corporate/terms-and-conditions/transport-data-service) erlaubt Vervielfältigung, Bearbeitung und kommerzielle Nutzung unter Bedingungen. Sie verlangt konkrete Quellenangaben und verbietet den Eindruck einer offiziellen Unterstützung. Die vorgeschriebenen Attributionen stehen jetzt vollständig in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

Die [NUMBAT-Beschreibung](https://tfl.gov.uk/info-for/open-data-users/our-open-data) nennt zusätzlich maximal neun Monate zwischen Erfassung und Anzeige sowie ein Jahr Anzeigezeit bis zur Aktualisierung. Ob diese Feed-/Anzeigevorgaben auch die dauerhafte Publikation einer klar datierten historischen Analyse und einer daraus abgeleiteten künstlerischen Uhrenskala betreffen, ist aus den Seiten nicht eindeutig ersichtlich. Die allgemeine Lizenz beschreibt zugleich eine dauerhafte Nutzungserlaubnis. Diese Spannung lässt sich durch bloße Namensnennung nicht abschließend lösen.

Daher: Das Modell wird ausdruecklich als historische Ableitung aus 2024 bezeichnet; Originale Datensaetze werden nicht mitveroeffentlicht

### DfT

Die [NTS-Veröffentlichungsseite](https://www.gov.uk/government/statistical-data-sets/nts05-trips) verweist auf OGL v3.0. Diese erlaubt nach [Lizenztext](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) Weitergabe und Bearbeitung auch kommerziell, bei Attribution und Lizenzverweis. Keine Anforderung gefunden, den eigenen Programmcode unter OGL zu stellen.

### Farben und Schrift: bisher fehlende Hinweise ergänzt

Die [Matplotlib-Lizenzsammlung](https://matplotlib.org/stable/project/license.html#colormaps-and-themes) führt ColorBrewer ausdrücklich als Apache-2.0. Das betrifft hier die YlGnBu-Ableitung in Palette und Farbring. Änderung: umgekehrt, auf 75 % beschnitten und in 256 RGB565-Farben abgetastet. Die eigene Projektlizenz hebt Apache-Bedingungen nicht auf.

DejaVu Sans wurde für Ziffern und Diagramme verwendet. Die [DejaVu-Lizenz](https://dejavu-fonts.github.io/License.html) erlaubt breite Nutzung mit eigenen Bedingungen. SVG-Pfade enthalten Schriftkonturen; daher wird der vollständige Originalhinweis beigefügt, obwohl keine Fontdateien verteilt werden. Schrift und Farbpalette müssen nicht aus dem Projekt entfernt werden, um eigenen Code unter MIT zu stellen.

### Waveshare: tatsächlicher Archivbefund

Geprüftes Archiv: RP2350-LCD-1.28.zip, SHA-256 36a996bb548e44e02c73adfc5001ebf3915fa22e969c180799c46f68da10581d. Es gibt kein zentrales LICENSE/LICENCE. Der MIT-ähnliche Text steht unter C/lib/Config/DEV_Config.h; die übernommene Registerfolge kommt aus C/lib/LCD/LCD_1in28.c. Diese Datei bindet die Headerdatei ein, enthält aber selbst nur einen Waveshare-Autorenhinweis.

Die Projektentscheidung ist, die funktionsgeprüfte Registerfolge beizubehalten, Waveshare als unmittelbare Quelle zu nennen und den vorhandenen Freigabetext zusammen mit einem ausdrücklichen Vorbehalt von Drittbedingungen zu erhalten. Der konkrete Hinweis steht in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

Ein Include und ein allgemeiner Drittbedingungenvorbehalt weisen für sich keine zusätzliche Lizenzgewährung nach. Unbekannte Drittlizenzen werden damit weder identifiziert noch gegebenenfalls erforderliche Einzelhinweise ersetzt. Diese verbleibende Grenze wird dokumentiert; es wurde keine Bestätigung von Waveshare eingeholt und keine Ersatzinitialisierung eingebaut.

Der [Adafruit-GC9A01A-Treiber](https://github.com/adafruit/Adafruit_GC9A01A/blob/main/Adafruit_GC9A01A.cpp) enthält eine weitgehend ähnliche Folge und nennt frühen Herstellercode als deren Quelle, ohne den Hersteller zu benennen. Unterschiede bestehen unter anderem bei 0xB6 und dem dort deaktivierten Befehl 0x70. Daraus folgt kein Beleg, dass Waveshare von Adafruit übernommen hat. Unsere unmittelbare Quelle bleibt das Waveshare-Archiv.

### Quellrepository und Firmware-Release unterscheiden

SDK-Source, Compiler und Python-Bibliotheken werden nicht mitgeliefert. Die UF2 steht in einem ignorierten Buildordner und wird nicht durch git add übernommen. In der UF2 sind dennoch Pico SDK, TinyUSB und Laufzeitbibliotheken enthalten.

Die Linkermap zeigt libm, newlib/libg und libgcc. Pico-/TinyUSB-Lizenztexte sind beigefügt. Für ein fertiges Binärrelease müssen zusätzlich die konkreten notices der verwendeten Arm-Toolchain und newlib-Version zusammengestellt werden. Das ist noch kein abgeschlossener Audit aller Runtime-Objektdateien. Der [GCC Runtime Library Exception](https://www.gnu.org/licenses/gcc-exception-3.1.en.html) zufolge ist gewöhnliche Verlinkung unabhängiger Module nicht gleichbedeutend mit einer GPL-Pflicht für die Anwendung; trotzdem werden die Bibliotheken nicht selbst unter MIT umlizenziert.

## Empfohlene Lizenzabgrenzung

MIT für die eigenen Programm- und Dokumentationsanteile, soweit daran Rechte bestehen. Fremddaten, abgeleitete Inhalte und ausgewiesene Bestandteile sind nach THIRD_PARTY_NOTICES.md ausgenommen. Eine kurze README-Angabe „Code: MIT; third-party material under its respective licenses“ ist zutreffender als ein uneingeschränktes MIT-Label für alle Dateien.

Der überwiegend KI-gestützte Entstehungsprozess bleibt offengelegt. Die Schutzfähigkeit rein KI-erzeugter Anteile wird dadurch nicht als gesichert behauptet; ein MIT-Hinweis kann nur Rechte einräumen, die der Lizenzgeber tatsächlich hat.

## Projektentscheidung und verbleibende Punkte

pgreendale hat entschieden, die starke historische Abstraktion aus TfL-Daten mit Quellenhinweisen sowie die Waveshare-Initialisierung mit Originaltext und Drittbedingungenvorbehalt beizubehalten. Die oben beschriebenen Unsicherheiten bleiben als Befund des Audits sichtbar.

MIT wird für eigene Anteile als Lizenzmodell gewählt. Falls eine UF2 als Release hochgeladen wird, sind die versionspassenden Runtime-Lizenzhinweise zusätzlich zu berücksichtigen. Die geprüften Quellen zeigen kein eindeutiges Copyleft-Hindernis für ein MIT-Hauptprojekt mit erhaltenen Fremdlizenzen; eine pauschale ausschließliche MIT-Lizenz für sämtliche Inhalte wird nicht behauptet.
