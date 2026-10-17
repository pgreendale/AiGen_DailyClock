# Nachweise und Pruefungen



[Ãœbersicht](../README.md)



## Stand vom 17.10.2026

Das Repository wurde als eigener Quellbaum mit eigenem CMake-Cache neu gebaut. Der Build verwendet ausschließlich eigene Firmwaredateien und explizit konfigurierte vorhandene SDK-/Compilerinstallationen. Getestete Umgebung: Windows, Pico SDK 2.2.0, Arm GNU 14.2.Rel1, CMake 4.4.4, Ninja 1.13.2.



- RP2040-Releasebuild erfolgreich; UF2 umfasst 679 Bloecke zu 512 Bytes, SHA-256: FD10856A5F04517D221364267183BC5B6FF9BBD106B2ADF732A64A7AE8D29A22

- Native C-Tests bestanden: gregorianischer 400-Jahres-Zyklus, Parser, logarithmische Helligkeit, Winkelmodell und Framebuffergrenzen.

- Alle sechs Python-Tests für Synchronisierung und Bootloaderbehandlung bestanden.

- Modellrekonstruktion: maximale Koeffizientenabweichung 0; Integral f=1; G(0)=0, G(12)=0,5, G(24)=1.

- Relative Verweise und Bilddateien der Dokumentation werden zusaetzlich auf Existenz geprüft.

Maschinenlesbare Ergebnisse: [Modellpruefung](evidence/model-check.json), [Repositorypruefung](evidence/package-check.json).



## Tests am realen Board

[Hardware-Testprotokoll](evidence/hardware-test.json) enthält konkrete Befehle und Antworten zu Helligkeit, ungültigen Kommandos und Kalenderübertragungen. [Validierungsbericht](evidence/hardware-validation.md) enthaelt Firmwarehash, Bildzeiten und die zeitliche Einordnung der Hardwaretests.

Die Kalender-/Protokolltests liefen vor den abschliessenden grafischen Ergaenzungen; darauffolgend wurden Firmwarestart, Status und Zeitsynchronisierung erneut geprueft.

Gemessenes Einzelintervall: 1.000.931 µs, Renderzeit 22.637 µs, LCD-Transfer 32.302 µs, Jitter und Langzeitpraezision unbekannt

## Datenherkunft und Reproduzierbarkeit

[Originaldateimanifest](../analysis/sources.json): URLs, Bytezahlen und SHA-256 der verwendeten Rohdateien. Die Dateien werden nicht mitgeliefert; download_sources.py prÃ¼ft heruntergeladene Bytes gegen diese Werte.

[Reproduktion der Datenanalyse](../analysis/README.md): Rohdaten, Stationssummen, gewichtetes Viertelstundenprofil, Dichtekoeffizienten. Die portablen Extraktions- und Aggregationsskripte wurden mit den Originaldateien erneut ausgeführt; das Profil stimmt bis auf Rundungsfehler mit dem ursprünglichen Stand überein. [Reproduktionsnachweis](evidence/source-reproduction.json). Die sechs Stationsblattsummen wurden gegen die jeweiligen Tagessummen geprueft (Abweichung unter 0,000001 Ereignissen).

Historische Entwurfsskripte sind als solche gekennzeichnet. Die aktuelle Gestaltung ist zusaetzlich als akzeptierte Bitmap und Firmwarevorschau dokumentiert. Eine vollstaendig automatisierte Wiederholung jeder gestalterischen Zwischenrevision liegt nicht vor.



## Veroeffentlichung

Repositoryinhaber und Ideengeber ist **pgreendale** ; die fast vollstaendige Erstellung durch ChatGPT Codex ist in README und Dokumentation offengelegt. 

