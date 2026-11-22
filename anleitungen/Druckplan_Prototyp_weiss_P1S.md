# BRUMMI v3 – Druckplan Prototyp (alles weiß) · Bambu Lab P1S

Alle Teile werden für den ersten Prototyp **in Weiß** gedruckt. Kein AMS-Farbwechsel nötig, dadurch kein Purge-Abfall und deutlich kürzere Druckzeit. Die STL-Dateien liegen in `v3/stl/`, Anzahl und Material in `v3/stl/00_Druckteile.csv`.

## Filament

| Material | Menge (inkl. 20 % Reserve) | Wofür |
|---|---|---|
| **PETG weiß** (z. B. Bambu PETG HF) | ca. **300-320 g** → 1 Rolle 1 kg reicht für 3 Prototypen | alle festen Teile, auch Kanzel und LED-Visier |
| **TPU 95A weiß** | ca. **25 g** | 4 Stoßfänger, 4 Kufengummis |

Hinweise zum weißen Prototyp:
- Die Kanzel ist in Weiß **blickdicht**. Für den Test egal. Die Status-LED auf der FC schimmert durch 0,8 mm weißes PETG noch durch.
- Ziffern und Nummernschilder: weiß drucken und die Zahlen mit Edding nachmalen (1 + 3 = CW gelb, 2 + 4 = CCW violett). Drehrichtung beim Zusammenbau trotzdem prüfen.
- Sobald das Design passt, kommen die Farben über das AMS (Skriptoption `--farbe voll`).

## Grundeinstellungen

Wie bei v2: Profil „0.20mm Standard @BBL P1P/P1S“, Düse 0,4 mm, Textured PEI, Filament „Bambu PETG HF“ bzw. „Generic PETG“. Vordere Tür leicht offen. TPU über die externe Spule (nicht AMS), „Generic TPU“, max. 3,5 mm³/s.
Wo nichts anderes steht: 3 Wandlinien, 4 Deck- und Bodenschichten, 15 % Gyroid, keine Stützen.

## Teile und Einstellungen (alle weiß)

| Datei | Anz. | Material | Liegt auf | Besondere Einstellungen | ca. g |
|---|---|---|---|---|---|
| R01_Rumpfschale | 1 | PETG weiß | Unterseite | 3 Wandlinien, **Blitz-Füllung (Lightning) 10 %**, Baumstützen nur auf der Platte für Akku-Schacht, XT30-Tasche und Bajonett-Öffnungen. Tunnel und Kanäle druckt er als Brücke. | 55-80 |
| R04_Akku_Schublade | 1 | PETG weiß | Boden | 2 Wandlinien, Endkappe steht senkrecht, ok ohne Stütze | 10 |
| A_07_Propellerschutz | 4 | PETG weiß | oberes Gitter (kopfüber) | Baumstützen nur für unteres Gitter und Streben; 2 Wandlinien | 17-19 |
| A_01_Auslegertraeger | 4 | PETG weiß | Unterseite (Waben-Taschen oben) | 4 Wandlinien, 25 % Gyroid; Kanal 4 × 4 mm wird überbrückt. Einsatz-Löcher unten zeigen nach unten: ok | 6 |
| A_04_Motorgondel | 4 | PETG weiß | Motorplatte unten | 4 Wandlinien; Baumstütze nur unter der Lasche | 6,5 |
| A_06_Motorabdeckung | 4 | PETG weiß | flach | – | 1 |
| V05_Drehring, V01_Bajonett_Buchse | je 4 | PETG weiß | Stirnfläche | 100 % Füllung | 1,6 / 0,8 |
| V09 / V17 Rastpins | 8 / 4 | PETG weiß | Kopf unten | 100 %, 0,12 mm | 0,5 / 0,7 |
| R06_Kanzelring_mit_Clips | 1 | PETG weiß | flach | einfarbig | 5 |
| R07_Kanzel | 1 | PETG weiß | Rand unten | 2 Wandlinien, Baumstützen innen für die flache Spitze | 5 |
| R08 Seitenblenden (3) | je 1 | PETG weiß | Rückseite | – | 1,2 |
| R09_LED_Visier | 1 | PETG weiß | flach | 100 % | 0,1 |
| L01 / L02 Landekufen | je 1 | PETG weiß | seitlich | Baumstützen für Pfosten | 4,4 |
| Nummernschilder R11/R12/A_02 | je 2 | PETG weiß | flach | Zahl mit Edding farbig nachmalen | 0,1 |
| V25_Akku_Riegel | 1 | PETG weiß | flach | 100 % | 0,1 |
| A_08_Stossfaenger | 4 | TPU 95A weiß | flach | 100 %, langsam, Retraction max. 0,8 mm | 4 |
| L03_Kufengummi | 4 | TPU 95A weiß | Stirnseite | 100 % | 0,8 |

## Druckplatten (256 × 256 mm)

Weil alles weiß ist, kann alles PETG ohne Farbwechsel durchlaufen.

| Platte | Inhalt | ca. Zeit |
|---|---|---|
| 0 (Test) | 1 × Motorgondel + 1 × Träger: Lochbild, Einsätze und Kanal prüfen, bevor alles gedruckt wird | 1 h |
| 1 | Rumpfschale + Akku-Schublade | 5,5 h |
| 2 | 4 Käfige | 7 h |
| 3 | restliche 3 Gondeln + 3 Träger, 2 Landekufen, Kanzelring, Kanzel | 5 h |
| 4 | alle Kleinteile (Ringe, Buchsen, Rastpins, Abdeckungen, Blenden, Schilder, Riegel, Visier) | 2,5 h |
| 5 | 4 Stoßfänger + 4 Kufengummis (TPU, externe Spule) | 3 h |

**Gesamt ca. 24 h** (ohne AMS-Wechsel gut 2 h kürzer als v2).

## Nach dem Druck

1. Stützen entfernen, Bohrungen Ø 3,2 mm mit einem 3,2-mm-Bohrer nachdrehen (von Hand).
2. **13 Gewindeeinsätze M2 × 3 einschmelzen:** 4 in die Dome, 1 hinten in den Rumpf, je 2 in die Träger-Unterseite. Lötkolben ca. 230 °C, senkrecht ansetzen, ohne Druck einsinken lassen, kurz mit etwas Flachem bündig drücken.
3. Langlöcher der Motorplatte: M2-Schraube probeweise einsetzen. Klemmt sie, mit 2,2-mm-Bohrer nacharbeiten.
4. Akku-Schublade ohne Akku in den Rumpf schieben: Sie muss leicht laufen. Wenn sie klemmt, Seiten leicht schleifen.
5. Teile wiegen und in die Kostentabelle (Blatt „Filament“, Spalte „Gewicht je Teil“) eintragen. Damit stimmt die Gewichts- und Schubrechnung auf dem Blatt „Übersicht“.
