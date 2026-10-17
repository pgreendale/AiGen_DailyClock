Historischer Testbericht vom 17.10.2026. Gerätekennung entfernt; Dateiverweise für das Repository angepasst.

# Verifikation der Uhr-Firmware

- Zielgerät: Waveshare RP2040-LCD-1.28.
- USB CDC im Test: Produkt NonlinearClock, VID/PID 2E8A:000A.
- Finale Firmware: dist/nonlinear_clock_rp2040.uf2.
- SHA256: FD10856A5F04517D221364267183BC5B6FF9BBD106B2ADF732A64A7AE8D29A22.
- Auf dem Gerät installiert; lokale PC-Zeit und Datum wiederhergestellt; Helligkeit 6.
- 180°-Displayrotation durch Benutzer bestätigt.
- Sekundenzeiger: rot, 1,2 Pixel nominale Breite, 60 Positionen pro Minute, 1 Sekunde pro Position; alle Zeiger werden einmal pro Sekunde aktualisiert.
- Gemessenes Frameintervall nach Installation: 1000931 µs; Renderzeit 22637 µs; LCD-Transfer 32302 µs. Einzelmessung unter USB-Betrieb, kein Langzeit-Jittertest.
- Flash-Code/Daten laut arm-none-eabi-size: 177716 Byte; BSS 131524 Byte. SDK-Stack/Heap zusätzlich gemäß Linkerskript.
- Native C-Tests nach Sekundenzeigeränderung bestanden (400-Jahres-Zyklus, Grenzfälle, Parser, PWM, Winkel einschließlich aller 60 Sekundenpositionen, Framebuffer-Grenzen).
- Sechs Python-Tests bestanden.
- Hardware-Integrationstests für Kalender, USB und Helligkeit: hardware-test.json. Diese liefen vor der ausschließlich grafischen Sekundenzeiger-Ergänzung; danach wurden Boot, Zeitsynchronisation und Framezeiten erneut auf dem Gerät geprüft.
- Vorschauen in docs/images/previews wurden mit dem finalen C-Renderer aktualisiert.



- Dichtekurve: maximalnormiert 0–1, rote Linie ohne Achsen im oberen Innenkreis; aktueller roter Balken bewegt sich von 00:00 links nach 24:00 rechts. Statische Kurve als kleines Rechteck zwischengespeichert. Tests und native Vorschauen aktualisiert; finale Firmware installiert und USB-Status geprüft.
