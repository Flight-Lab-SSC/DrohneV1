# BRUMMI v2 – Druckanleitung Bambu Lab P1S

Nov 22, 2026 · @Leon

Alle 26 Druckteile liegen einzeln als STL im Projektordner unter drohne/blender\_v2/stl/, zusammen sind es 58 Teile auf einer Testplatte und sechs weiteren Druckplatten. Wichtig: Die Clips, Bajonette und Rastpins sind im Blender-Modell nur angedeutet. Die Drucke sind ein Design- und Gewichtsmuster zum Anschauen, Anpassen und Wiegen; einrastende Verbindungen kommen in der Fusion-Phase.

## Vorbereitung

Du brauchst Bambu Studio, die Textured-PEI-Platte und drei Materialien: PETG (weiß, graphit, orange, türkis, gelb, violett, transparent), TPU 95A schwarz und optional PLA für die kleinen Nummernschilder.

1. Alle STL-Dateien aus drohne/blender\_v2/stl/ in Bambu Studio ziehen. Die Datei 00\_Druckteile.csv sagt, wie oft jedes Teil gebraucht wird; in Bambu Studio mit Rechtsklick > „Klonen“ vervielfältigen.
2. Maße sind in mm. Wenn Bambu Studio fragt, ob in Zoll umgerechnet werden soll: Nein.
3. Jedes Teil mit „Auf Fläche legen“ (Taste F) auf die in der Tabelle genannte Seite legen.
4. Grundprofil: „0.20mm Standard @BBL P1P/P1S“, Düse 0,4 mm, Filamentprofil „Bambu PETG HF“ bzw. „Generic PETG“.
5. PETG: Platte sauber und fettfrei (Spüli, kein Kleber nötig auf Textured PEI). Vordere Tür leicht offen oder Deckel ab, damit PETG nicht zu warm wird.
6. TPU geht nicht durch das AMS: Spule hinten am externen Halter einhängen und direkt einfädeln, Profil „Generic TPU“, Geschwindigkeit max. 3,5 mm³/s.

Gewichtsziel für alle Druckteile zusammen: ca. 230 g. Wiege jeden Käfig nach dem Druck, er sollte 16–18 g haben. Das ist der beste Test, ob die Rechnung stimmt.

## Teile und Einstellungen

Wo nichts anderes steht: 3 Wandlinien, 4 Deck- und Bodenschichten, 15 % Gyroid, keine Stützen. Gewichte sind Schätzwerte für ein Stück.

| Datei | Anz. | Material | Liegt auf | Besondere Einstellungen | ca. g |
| --- | --- | --- | --- | --- | --- |
| A\_07\_Propellerschutz | 4 | PETG weiß | oberes Gitter (kopfüber) | Baumstützen (Tree), nur für unteres Gitter und Streben; 2 Wandlinien | 17 |
| A\_08\_Stossfaenger | 4 | TPU 95A | flach | 100 % Füllung, langsam, Retraction max. 0,8 mm | 4 |
| A\_01\_Auslegertraeger | 4 | PETG graphit | Seite, Wabenlöcher senkrecht zur Platte | 4 Wandlinien, 25 % Gyroid (tragendes Teil) | 6 |
| A\_04\_Motorgondel | 4 | PETG graphit | Motorplatte unten (offene Seite oben) | 4 Wandlinien | 6 |
| A\_06\_Motorabdeckung\_CW / \_CCW | je 2 | PETG gelb / violett | flach | – | 1 |
| V05\_Drehring | 4 | PETG orange | Stirnfläche | 100 % Füllung | 1,6 |
| V01\_Bajonett\_Buchse | 4 | PETG orange | Stirnfläche | 100 % Füllung | 0,8 |
| V09\_Rastpin\_Kaefig | 8 | PETG orange | Kopf unten | 100 % Füllung, 0,12 mm Schichthöhe | 0,5 |
| V17\_Rastpin\_Kufe | 4 | PETG orange | Kopf unten | wie V09 | 0,7 |
| R01\_Rumpfschale | 1 | PETG weiß | Unterseite (Wabentaschen unten) | 3 Wandlinien, Füllung „Blitz“ (Lightning) 10 %, Stützen nur auf der Platte für Bajonettöffnungen | 45 |
| R04\_Akku\_Schublade | 1 | PETG türkis | Boden | 2 Wandlinien | 7 |
| R06\_Kanzelring\_mit\_Clips | 1 | PETG graphit, Clips orange | flach | Clips im AMS orange einfärben (Malwerkzeug) oder einfarbig drucken | 5 |
| R07\_Kanzel | 1 | PETG transparent | Rand unten | Vasenmodus aus; 2 Wandlinien, Baumstützen innen für die flache Kuppel-Spitze; für Klarheit: 0,28 mm, langsam, Düse 250 °C | 5 |
| R08\_Seitenblende (rechts, links, vorne) | je 1 | PETG graphit | Rückseite | Wabenrelief oben | 1,2 |
| R09\_LED\_Visier | 1 | PETG transparent | flach | 100 % Füllung | 0,1 |
| L01 / L02\_Landekufe | je 1 | PETG weiß | seitlich (Kufe flach) | Baumstützen für die Pfosten | 4,4 |
| L03\_Kufengummi | 4 | TPU 95A | Stirnseite | 100 % Füllung | 1 |
| R11 / R12 und A\_02 Nummernschilder | je 2 | PLA oder PETG gelb / violett | flach | Ziffern als zweite Farbe per AMS-Farbwechsel ab Schicht 4 oder aufkleben | 0,1 |
| V25\_Akku\_Riegel | 1 | PETG orange | flach | 100 % Füllung | 0,1 |

Nicht drucken: Propeller (Kaufteil, weich), Propellerkappen, Motoren, Akku und das Power-Core-Gehäuse (kommt, wenn die eigene Platine fertig ist).

## Druckplatten und Reihenfolge

Die Platte des P1S ist 256 × 256 mm. So passt alles auf fünf Platten; druck zuerst einen Käfig allein als Test.

| Platte | Inhalt | Material | ca. Druckzeit |
| --- | --- | --- | --- |
| 0 (Test) | 1 × A\_07\_Propellerschutz | PETG weiß | 2,5 h |
| 1 | restliche 3 Käfige + 2 Landekufen | PETG weiß | 7 h |
| 2 | Rumpfschale + Akku-Schublade | PETG weiß / türkis (AMS) | 6 h |
| 3 | 4 Auslegerträger, 4 Gondeln, 3 Seitenblenden, Kanzelring | PETG graphit (+ orange) | 5 h |
| 4 | alle orangen Teile, Motorabdeckungen, Nummernschilder, Visier | PETG orange, gelb, violett, transparent (AMS) | 4 h |
| 5 | Kanzel | PETG transparent | 1,5 h |
| 6 | 4 Stoßfänger + 4 Kufengummis | TPU 95A (externe Spule) | 3 h |

Nach dem Druck:

1. Stützen entfernen, Kanten am Käfiggitter mit Schleifpapier 240 brechen (keine scharfen Kanten für Kinderfinger).
2. Käfige wiegen und notieren. Liegt ein Käfig über 20 g, Wandlinien oder Flächenfüllung prüfen.
3. Probe-Zusammenstecken: Passen Gondel und Kragen, sitzen Ausleger im Rumpf? Spiel notieren, das fließt in die Fusion-Konstruktion ein.
4. Nicht fliegen mit diesen Teilen: Verriegelungen und Kabelwege sind noch nicht ausgeführt.

Druckzeiten sind grobe Schätzungen; Bambu Studio zeigt nach dem Slicen die genaue Zeit und das Gewicht an.
