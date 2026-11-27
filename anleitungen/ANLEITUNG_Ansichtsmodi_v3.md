# BRUMMI v3 – Ansichtsmodi (Technical View & Co.)

Das bestehende v3-Modell bleibt vollständig erhalten. Das Add-on schaltet **nur die Sichtbarkeit** der Bauteile um (Auge im Outliner und Render-Sichtbarkeit). Es löscht nichts, verschiebt nichts und ändert weder Geometrie noch Materialien. Geprüft: Vor und nach dem Durchschalten aller Ansichten sind Vertex-Daten, Positionen und Materialien aller 126 Objekte identisch.

## Dateien

| Datei | Inhalt |
|---|---|
| `v3/brummi_v3_ansichten.blend` | Kopie von `brummi_v3_blender53.blend` + eingebettetes Add-on (sonst unverändert) |
| `v3/brummi_ansichten.py` | Das Add-on als einzelne Datei (für jede BRUMMI-v3-Datei nutzbar) |
| `v3/renders/12_Ansichtsmodi.jpg` | Vorschau aller Ansichten |
| `v3/brummi_v3_blender53.blend` | Original, **nicht verändert** |

## Starten

**Variante A (am einfachsten):** `brummi_v3_ansichten.blend` öffnen. Wenn Blender oben einen gelben Hinweis zu „Automatische Ausführung von Python-Skripten“ zeigt: **Erlauben** (bzw. „Allow Execution“). Falls kein Hinweis kommt und das Panel fehlt: Arbeitsbereich *Scripting* → im Texteditor `brummi_ansichten.py` auswählen → **Run Script** (Alt+P).

**Variante B (dauerhaft):** *Bearbeiten → Einstellungen → Add-ons* → Pfeil oben rechts → *Von Festplatte installieren…* → `brummi_ansichten.py` wählen → Haken setzen. Funktioniert dann auch in der Original-Datei.

Danach im 3D-Viewport **N** drücken → Reiter **BRUMMI**.

## Ansichten

| Ansicht | Sichtbar | Teile |
|---|---|---|
| **Full View** | komplettes Modell, Originalzustand | 113 |
| **Technical View** | alles außer Verkleidung/Deko | 83 |
| **Structural View** | Rahmen, Arme, Verbindungen, tragende Teile | 54 |
| **Electronics View** | Elektronik, Stromversorgung, Kabel | 12 |
| **Propulsion View** | Motoren, Propeller und Zubehör | 21 |

**Technical View blendet aus:** Kanzel, Kanzelring + 4 Kanzel-Clips (halten nur die Kanzel), 3 Seitenblenden, LED-Visier, 8 Nummernschilder + 8 Ziffern, 4 Motorabdeckungen. Propellerschutz und Stoßfänger bleiben sichtbar, weil sie tragende/schützende Funktion haben (über die Bauteil-Liste einzeln ausblendbar).

**Structural View:** Rumpfschale, Akku-Schublade, Auslegerträger, Motorgondeln, Propellerschutz, Stoßfänger, Landekufen + Kufengummis, Bajonett-Buchsen, Drehringe, Rastpins, Akku-Riegel, alle Schrauben, Gummidämpfer, Abstandshalter und Abstandsbolzen des Stacks.

**Electronics View:** 4in1-ESC, Flugsteuerung, Magnetometer-Platine, ELRS-Empfänger, Kondensator, XT30-Buchse und -Stecker, Akkukabel plus/minus, Motorkabel, Status-LED, Akku-Pack.

**Propulsion View:** 4 Motoren, 4 Propeller, 4 Propellerkappen, Motorschrauben, Motorgondeln (Motorhalter) und Motorkabel.

Einige Teile gehören zu zwei Ansichten: Motorgondel (Struktur + Antrieb), Motorkabel (Elektronik + Antrieb).

## Optionen im Panel

- **Auch beim Rendern ausblenden** (Standard an): F12-Renders zeigen dieselbe Ansicht.
- **Rumpfschale als Drahtgitter:** Rumpfschale und Akku-Schublade werden im Viewport als Drahtgitter gezeigt. So sieht man den Elektronik-Stack und den Akku in ihrer echten Einbaulage durch die Wand. Nur Darstellung, im Render unverändert.
- **Röntgen (X-Ray):** normale Blender-Röntgenansicht des Viewports.
- **In Einbauposition bringen:** erscheint nur, wenn Explosion, Baugruppen oder Montage-Animation die Teile gerade versetzt haben. Setzt die Regler zurück (Explosion 0, Baugruppen 0, Bild 200) und verschiebt selbst nichts.

## Component Isolation (Panel „Bauteile“)

- Liste aller 113 Bauteile mit Augen-Symbol zum einzelnen Ein-/Ausblenden. Suche über das Lupenfeld unter der Liste.
- Filter nach Kategorie (Verkleidung, Struktur, Elektronik, Antrieb, Innenausbau) und „nur sichtbare“.
- **Kategorie zeigen / verbergen:** die gefilterte Kategorie zusätzlich ein- oder ausblenden, z. B. Technical View + Antrieb verbergen.
- **Markiertes Bauteil isolieren:** nur das in der Liste markierte Teil zeigen.
- **Auswahl im Viewport isolieren / ausblenden:** wirkt auf die im 3D-Fenster ausgewählten Teile.
- Unter der Liste steht ein Steckbrief des markierten Teils: Nummer, Baugruppe, Funktion, Verbindung, Fertigung (aus den Daten im Modell).
- **Alles wiederherstellen (Full View)** stellt jederzeit den Originalzustand her. Rückgängig (Strg+Z) funktioniert ebenfalls.

## Was im Modell nur teilweise existiert

Das Add-on zeigt nur, was im v3-Modell tatsächlich konstruiert ist. Nichts wurde nachkonstruiert:

- **Motorkabel** sind nur im Rumpf modelliert (vom ESC bis zu den Bajonett-Öffnungen). Durch die Ausleger bis zum Motor fehlen sie. Im Propulsion View sieht man deshalb eine Lücke zwischen Kabelende und Motor.
- **Signalkabel** zwischen Flugsteuerung, ESC und Empfänger sowie das Kabel zur Magnetometer-Platine sind nicht modelliert (beim echten Stack laufen sie als kurze Steckverbinder/Lötbrücken).
- Clips und Bajonette sind wie bisher nur angedeutet (Funktionsgeometrie folgt in Fusion 360).

## Kategorien anpassen

Die Zuordnung steht oben in `brummi_ansichten.py` in der Liste `RULES` (Bauteilnummer → Kategorie). Ein neues Teil, das keiner Regel entspricht, landet automatisch in „nicht zugeordnet“ und bleibt in Full und Technical View sichtbar, damit nie etwas unbemerkt verschwindet.
