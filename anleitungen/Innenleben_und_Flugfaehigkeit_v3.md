# BRUMMI v3 – Innenleben, Halterungen und Flugfähigkeit

Stand: 22.11.2026 · gehört zu `v3/brummi_drohne.py`

## 1. Fliegt die Drohne?

**Mit dem Akku aus v2 (2S) nein. Mit einem 3S-Akku ja, aber nicht sportlich.**

Die 1404-Motoren (z. B. T-Motor F1404) sind laut Hersteller für **3-4S** gebaut. Der Hersteller misst mit dem 4600-KV-Motor und einem 3-Zoll-Propeller (GF3016) auf 4S (15,6 V) **345 g Schub pro Motor**. Der Schub wächst ungefähr mit dem Quadrat der Spannung:

| Akku | Spannung unter Last | Schub je Motor | 4 Motoren (−7 % Käfig) | Gewicht | Schub/Gewicht |
|---|---|---|---|---|---|
| 2S (v2) | ca. 7 V | ca. 70 g | ca. 260 g | ca. 390 g | **0,7 → hebt nicht ab** |
| 3S 450 mAh (v3) | ca. 11 V | ca. 170 g | ca. 640 g | ca. 390 g | **≈ 1,6 → fliegt** |

Die Rechnung aus der Flugprüfung (Schub/Gewicht 1,8 mit 2S) war zu optimistisch, weil sie die Motoren nicht auf 2S umgerechnet hat. Deshalb ist der Akku-Schacht in v3 auf 3S umgestellt.

- Gewicht geschätzt aus den STL-Volumen: Druckteile ca. 255-280 g (Rumpf 55-80 g je nach Füllung, vier Käfige zusammen ca. 76 g), dazu Motoren, Elektronik und Akku → **ca. 390 g**. Die Kostentabelle rechnet das mit (Blatt „Übersicht“).
- Flugzeit mit 3S 450-550 mAh: **ca. 2,5-3 Minuten** (Schweben braucht ca. 100 W).
- Ziel für mehr Reserve: unter 360 g. Den größten Hebel haben der Rumpf (Infill 10 % statt 15 %) und die Käfige.
- **Vor dem Erstflug:** Drohne wiegen (mit Akku). Unter 400 g ist ok, darüber den Schub prüfen (siehe Abschnitt 5).

## 2. Wie sah es innen bisher aus?

In v1/v2 war das Innere **nicht** für echte Elektronik vorbereitet:

- Der Rumpf war ein massiver Block mit zwei Taschen: oben ein Schacht für einen geschlossenen Kasten („Power-Core“, nur angedeutet) und unten der Akku-Schacht.
- Es gab **keine Schraubpunkte**, keine Platinenhalter, keine Kabelwege zwischen Akku, Elektronik und Motoren.
- Die Motoren saßen nur auf einer glatten Platte, ohne Lochbild. Der Träger steckte ohne Befestigung in der Motorgondel (Teile überlappten sich).

## 3. Was ist neu in v3 (Außendesign bleibt gleich)

Ansichten: `renders/08_Innenleben.png`, `09_Schnitt_Rumpf.png`, `10_Motorhalterung.png`, Vergleich `11_Vergleich_v2_v3.jpg`.

### Rumpf (R01)
| Was | Maße |
|---|---|
| Elektronik-Schacht | 40 × 40 mm, Boden bei 21,6 mm über Rumpfunterseite |
| 4 Schraubdome | Lochbild **20 × 20 mm**, Ø 6 mm, 4 mm hoch, Bohrung Ø 3,2 mm für Gewindeeinsatz M2 × 3 |
| Akku-Schacht | 36 × 78 × 19 mm, von hinten, für 3S 450-550 mAh bis 32 × 60 × 17 mm |
| XT30-Tasche | 11 × 18 × 6,2 mm vor dem Akku-Schacht, Buchse wird eingeklebt |
| Akkukabel-Kanal | 8 × 6 mm hoch, dann 8 × 4,5 mm bis in den Elektronik-Schacht |
| 4 Motorkabel-Tunnel | 9 × 4,5 mm vom Schacht bis in jede Bajonett-Öffnung (Platz für JST-PH 3-polig) |
| Gewindeeinsatz Schublade | M2 an der Rückseite über dem Akku-Schacht |

### Elektronik-Stack (Standard 20 × 20, M2)
Von unten nach oben: Gummidämpfer → **4in1-ESC** → Nylon-Abstandshalter 5 mm → **Flugsteuerung** (eigene Platine 27 × 27 mm oder Kauf-FC) → hinten 2× M2 × 14 Schrauben, vorne 2× Abstandsbolzen M2 × 8 → **Magnetometer-Tochterplatine** 24 × 10 mm, 8 mm über der FC (weiter weg von den Motorströmen). ELRS-Empfänger mit Klebeband auf der FC. Kondensator 470 µF an den Akkupads des ESC.

Weil das Lochbild Standard ist, passt jede gekaufte 20 × 20-FC. **Empfehlung:** Zuerst mit einer gekauften FC fliegen und den Rahmen testen, dann die eigene Platine einsetzen. So weißt du bei Problemen, ob es am Rahmen oder an der eigenen Elektronik liegt.

### Akku-Schublade (R04)
- Wanne mit 32,6 mm Innenbreite, Akku liegt formschlüssig im Schacht, oben ein dünnes Schaumpad (bei 2S 850 mAh 3 mm).
- **XT30-Stecker in der Stirnwand:** Beim Einschieben steckt der Akku automatisch in die Buchse im Rumpf.
- **Endkappe mit M2 × 8-Schraube** in den Gewindeeinsatz. Der Schnapp-Riegel V25 bleibt als zweite Sicherung.

### Ausleger und Motorgondel (A01, A04)
- **Motorplatte 3 mm** mit Lochbild **9 × 9 mm, als Langloch bis 12 × 12 mm** (M2). Damit passen die üblichen 1404-Motoren. T-Motor gibt das Lochbild auf der Produktseite nicht an: beim Kauf nachmessen.
- Mittelloch Ø 6 mm für Welle und Sicherungsring, Schlitz für die Motorlitzen.
- **Motorschrauben M2 × 5** von unten (in der offenen Gondel erreichbar). Maximal 2 mm dürfen in den Motor ragen, sonst berührt die Schraube die Wicklung.
- Gondel hat eine **Lasche** unter dem Träger: 2× M2 × 6 von unten in 2 Gewindeeinsätze im Träger.
- **Kabelkanal 4 × 4 mm** durch Träger und Bajonett-Hals; Kabelfenster in der Gondelwand.
- Trägerende ist an die Gondel angepasst (vorher überlappten sich die Teile), Wabenausschnitte sind jetzt 4 mm tiefe Taschen, damit der Kanal geschlossen bleibt.

## 4. Montage-Reihenfolge

1. **Gewindeeinsätze einschmelzen** (13 Stück): 4 in die Dome, 1 hinten in den Rumpf, je 2 in jeden Träger. Lötkolben ca. 230 °C, senkrecht und langsam eindrücken.
2. Motoren auf die Gondeln schrauben (4× M2 × 5), Litzen durch den Schlitz nach unten und durch das Fenster in den Träger führen.
3. Gondel an den Träger schrauben (2× M2 × 6).
4. Motorlitzen durch Hals und Tunnel in den Elektronik-Schacht ziehen. Ausleger einsetzen und Drehring verriegeln.
5. XT30-Buchse mit Kabel in die Tasche, Kabel durch den Kanal nach oben.
6. Dämpfer auf die Dome, ESC einsetzen, Motorlitzen und Akkukabel anlöten, Kondensator anlöten.
7. Abstandshalter, FC, Schrauben und Bolzen, Magnetometer-Platine, Empfänger.
8. Akku mit XT30-Stecker in die Schublade, Stecker in die Stirnwand klemmen, Schublade einschieben, M2 × 8 festziehen.
9. Kanzelring und Kanzel aufsetzen, Käfige und Landegestell montieren.

## 5. Vor dem Erstflug

- Ohne Propeller: Drehrichtung jedes Motors prüfen (1 und 3 CW, 2 und 4 CCW, siehe Nummernschilder).
- Propeller erst montieren, wenn Firmware, Fernsteuerung und Failsafe getestet sind.
- Erster Schwebeflug draußen auf Wiese, 1 m Höhe. Braucht sie mehr als ca. 60 % Gas zum Schweben, ist sie zu schwer.
