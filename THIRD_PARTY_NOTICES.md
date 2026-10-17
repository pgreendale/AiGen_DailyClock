# Fremdmaterial und Attributionen

Die Projektlizenz ersetzt keine der folgenden Bedingungen. Das gilt auch für abgeleitete Datentabellen, Farbring, Modellkoeffizienten und generierte Flashdaten, soweit daran Rechte der Quellen fortbestehen.

## Verkehrsquellen

Powered by TfL Open Data

Contains OS data © Crown copyright and database rights 2016

Geomni UK Map data © and database rights [2019]

Quelle: TfL NUMBAT 2024, Stations-Eintritte/-Austritte, typische Wochentage. Eigenes historisches Modell; keine aktuelle Verkehrs- oder Fahrplaninformation. TfL, Ordnance Survey und Geomni unterstützen oder zertifizieren dieses Projekt nicht. Die beiden Geodatenhinweise werden vorsorglich entsprechend der allgemeinen TfL-Lizenz beibehalten; im Modell werden keine Kartenkoordinaten verwendet.

Lizenz: https://tfl.gov.uk/corporate/terms-and-conditions/transport-data-service
Zur offenen Einordnung der dortigen Aktualitätsvorgaben siehe docs/06-lizenzpruefung.md.

Source: Department for Transport, National Travel Survey, NTS0502a, England 2024.
Contains public sector information licensed under the Open Government Licence v3.0.
https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

## Software, Schrift und Farben

### LCD-Initialisierung / Waveshare

Die LCD-Initialisierungsfolge wurde aus dem offiziellen Waveshare-Demo RP2350-LCD-1.28, Datei C/lib/LCD/LCD_1in28.c, übernommen und in eine Registertabelle überführt. Waveshare ist die unmittelbare Quelle, nicht als alleiniger ursprünglicher Urheber nachgewiesen. Der im Demo enthaltene Freigabe- und Haftungstext bleibt unverändert in licenses/Waveshare.txt erhalten. Soweit übernommene Bestandteile Rechten oder Lizenzbedingungen Dritter unterliegen, gelten diese für die betreffenden Bestandteile weiter; die Projektlizenz ersetzt sie nicht. Dieser Hinweis behauptet keine pauschale MIT-Umlizenzierung des Fremdmaterials und ersetzt keine gegebenenfalls konkret erforderlichen Copyright- oder Lizenzangaben.

### Weitere Bestandteile

- ColorBrewer YlGnBu: Apache-2.0, Copyright 2002 Cynthia Brewer, Mark Harrower und The Pennsylvania State University. Änderungen und Hinweis in licenses/ColorBrewer-NOTICE.txt; Lizenztexte in licenses/Matplotlib-LICENSE.txt.
- Matplotlib-Farbdefinition: Matplotlib-Lizenz, Copyright 2012– Matplotlib Development Team. Farbdefinition abgeleitet, umgekehrt, beschnitten und neu abgetastet; Matplotlib selbst wird nicht mitgeliefert.
- DejaVu Sans / Bitstream Vera: Schriftkonturen in SVGs und gerasterte Ziffern; Hinweise vorsorglich in licenses/DejaVu-LICENSE.txt. Keine TTF-Dateien mitgeliefert.
- Pico SDK 2.2.0: BSD-3-Clause, licenses/Pico-SDK-BSD-3-Clause.txt.
- TinyUSB: MIT, licenses/TinyUSB-MIT.txt.

SDK und TinyUSB werden nicht als Source gebündelt, sind aber in der kompilierten UF2 enthalten. Für Firmware-Releases zusätzlich die zur konkreten Arm-Toolchain passenden newlib-/libm-/libgcc-Hinweise beifügen; siehe Lizenzbericht. Compiler und Python-Pakete werden nicht mitgeliefert.

## Nur verlinkte Quellen

Eurostat-/HETUS-Unterlagen und Waveshare-Herstellerschaltplan werden nur verlinkt und in eigenen Worten beschrieben. Es sind keine HETUS-Mikrodaten, Hersteller-PDFs oder deren Abbildungen im Repository enthalten. Eigene Funktionsschaltbilder sind Neuzeichnungen der sachlichen Anschlussbelegung.
