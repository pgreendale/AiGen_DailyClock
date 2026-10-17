# Daten und Reproduktion

Die Rohdateien werden nicht mitgeliefert. Ihre exakten SHA-256-Prüfsummen und Downloadadressen stehen in sources.json. Abgeleitete Daten stehen unter data/.

    python analysis/download_sources.py
    powershell -NoProfile -ExecutionPolicy Bypass -File analysis/analyse_sources.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File analysis/aggregate.ps1
    python analysis/reconstruct.py

Die PowerShell-Skripte stammen aus der ursprünglichen Auswertung; nur das Arbeitsverzeichnis wurde portabel gemacht. Sie erwarten die ursprüngliche Blattstruktur. Eine diagnostische Ausgabe von NTS-2025-Zeilen im ersten Skript ist kein Modelleingang: aggregate.ps1 wählt ausdrücklich 2024 aus.

reconstruct.py rekonstruiert die Kubikkoeffizienten aus dem Viertelstundenprofil, prüft sie gegen die gespeicherte Dichte und erstellt die Modellabbildung. Optional benötigte Pakete:

    python -m pip install -r analysis/requirements.txt

Die Dateien unter history/ dokumentieren frühere Entwurfsstände. Sie sind keine vollständige automatische Pipeline aller späteren Layoutrevisionen. Das akzeptierte Ziffernblatt ist als firmware/assets/clockface_240.png eingefroren. Der Firmwarebuild braucht keine Rohdateien und keine Plotbibliotheken.

Ergebnis.md ist der historische Analysebericht; für die aktuelle Einordnung und Grenzen gilt docs/01-vorarbeit.md.
