# BRUMMI v2 – Blender-Skript ausführen

Datei: `brummi_drohne.py` (vollständiges, direkt ausführbares Skript)
Getestet: Blender 5.3 (headless). Geschrieben für Blender 4.2 LTS und neuer.

## Variante A – in der Blender-Oberfläche

1. Blender öffnen, **Datei > Neu > Allgemein** (das Skript leert die aktuelle Szene).
2. Oben auf den Arbeitsbereich **Scripting** wechseln.
3. Im Texteditor **Text > Öffnen…** und `brummi_drohne.py` wählen.
4. **Run Script** klicken (oder `Alt+P` mit der Maus über dem Texteditor).
5. Nach ca. 2 Sekunden steht die Drohne in der Szene (90 Bauteile).
6. Ansicht: Im 3D-Fenster `Z` > **Material-Vorschau** oder **Rendered**. Kamera wählen: Kamera-Objekt anklicken, `Strg+Num0`.
7. Rendern: **F12** (Cycles; mit Grafikkarte schneller, siehe Einstellungen > System > Cycles Render Devices).

## Variante B – Kommandozeile (rendert alle 7 Ansichten automatisch)

```bash
blender -b -P brummi_drohne.py -- --render ./renders --samples 128 --save ./brummi.blend --bom ./stueckliste.csv --stl ./stl
```

| Option | Bedeutung |
|---|---|
| `--render ORDNER` | rendert alle 7 Ansichten als PNG |
| `--samples N` | Cycles-Samples (64 = Vorschau, 128–256 = Präsentation) |
| `--res-pct P` | Auflösung in % von 1920×1200 |
| `--engine EEVEE` | schnellere Echtzeit-Engine statt Cycles |
| `--save DATEI.blend` | speichert die Szene |
| `--bom DATEI.csv` | schreibt die Stückliste (Semikolon-CSV, öffnet in Excel) |
| `--stl ORDNER` | exportiert alle 26 Druckteile einzeln als STL in mm (plus 00_Druckteile.csv mit Anzahl und Material) |

Windows-Beispiel: `"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" -b -P brummi_drohne.py -- --render renders`

## Die 7 Darstellungen

| Nr | Ansicht | Kamera | Reglerstellung |
|---|---|---|---|
| 1 | Produkt-Rendering | Kamera_01_Produkt | montiert |
| 2 | Perspektive von vorne | Kamera_02_Front | montiert |
| 3 | Draufsicht (orthografisch) | Kamera_03_Draufsicht | montiert |
| 4 | Seitenansicht (orthografisch, 4° erhöht) | Kamera_04_Seite | montiert |
| 5 | Explosionsdarstellung | Kamera_05_Explosion | Explosion = 1 |
| 6 | Baugruppen | Kamera_06_Baugruppen | Baugruppen = 1 |
| 7 | Zusammenbau | Kamera_07_Montage | Montage ≈ 0,7 |

## Explosion, Montage und Baugruppen steuern

Objekt **Steuerung_Explosion** (Collection `00_Studio_Kamera_Licht`) auswählen > Eigenschaften-Editor > **Objekt** > **Benutzerdefinierte Eigenschaften**:

- **Explosion** 0…1: alle Teile fahren auseinander.
- **Montage** 0…1: Teile fliegen in der Bau-Reihenfolge (Schritte 0–10) an ihren Platz. Die Zeitleiste ist von Bild 20 bis 200 animiert. **Leertaste** spielt den Zusammenbau als Animation ab. Um den Regler von Hand zu ziehen, vorher die Keyframes löschen (Rechtsklick auf den Regler > Keyframes löschen).
- **Baugruppen** 0…1: Rumpf, vier Ausleger und Landegestell werden getrennt, bleiben aber jeweils montiert.

Die Bewegung läuft über Treiber auf der **Delta-Position**. Die normale Position, Rotation und Geometrie jedes Teils bleibt frei bearbeitbar.
Falls Blender beim Öffnen einer gespeicherten Datei „Auto-Run disabled“ meldet: Die Treiber sind einfache Ausdrücke und laufen trotzdem. Wenn nicht, einmal **Reload Trusted** klicken.

## Ordnung in der Szene

```
BRUMMI_Bausatz_Drohne
├── 10_Rumpf
├── 21_Ausleger_1_vorne_rechts … 24_Ausleger_4_vorne_links
├── 30_Landegestell
├── 40_Verbindungselemente_orange   ← alle Verbindungen ein-/ausblendbar
└── 50_Deko_Abdeckungen_Licht
00_Studio_Kamera_Licht (Kameras, Lichter, Hohlkehle, Steuerung)
```

Jedes Bauteil hat benutzerdefinierte Eigenschaften: `Bauteil_Nr`, `Baugruppe`, `Verbindung`, `Funktion` (mechanisch/optisch), `Fertigung`, `Material`. Diese bilden die Grundlage für den Export nach Fusion 360 (Phase 4).

## Hinweise

- Die mitgelieferte `.blend`-Datei wurde mit Blender 5.3 gespeichert. Mit älteren Versionen bitte das Skript ausführen statt die Datei zu öffnen.
- Maße im Modell: Meter, Anzeige in Millimetern. Das Modell ist ein **visuelles Designmodell**, kein fertiges CAD-Modell. Rastgeometrien, Toleranzen und Wandstärken entstehen in Fusion 360.
- Hauptmaße und Farben lassen sich oben im Skript ändern (`HUB_R`, `R_MOTOR`, `ARMS`, Materialien in `build_materials()`).

## Was ist neu in v2

Gewichts- und schuboptimiert nach der Flugprüfung vom 22.11.2026; das Aussehen bleibt gleich.

- Käfigring 1,2 mm statt 2,5 mm Wand, Spalt zur Propellerspitze 2 mm, gerundete Einlauflippe oben (Höhe 22 mm bleibt, damit das obere Gitter weit genug vom Propeller weg ist)
- Gitter oben und unten mit hochkant stehenden Lamellen 1,6 × 3 mm, Käfigstreben 3 × 4,5 mm
- Stoßfänger 4 mm, Motorgondel als Topf, dünnere Motorabdeckung, Kanzel 0,8 mm, Landekufen 5 mm
- Wabentaschen auf der Rumpf-Unterseite
- Akku-Schacht 34 × 70 × 15 mm für 2S 850 mAh, Akku-Schublade als Wanne
- Neue Option `--stl` für den Export der Druckteile (siehe Druckanleitung)

Die Version 1 liegt unverändert in `drohne/blender/`.
