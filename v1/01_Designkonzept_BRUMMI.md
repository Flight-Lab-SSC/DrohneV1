# BRUMMI – modulare Bausatz-Drohne für Kinder

**Phase 1: Designkonzept** · **Phase 3: Verbindungs- und Sicherheitskonzept**
Stand: 21.11.2026 · Status: Designentwurf zur Abstimmung (vor Fusion-360-Phase)

---

## 1. Produktidee in einem Satz

BRUMMI ist ein Technik-Baukasten zum Fliegen: Kinder setzen eine Quadrocopter-Drohne aus wenigen großen, farbcodierten Modulen zusammen, verstehen dabei, wie Rumpf, Ausleger, Motoren und Propeller zusammenwirken, und können jedes Modul einzeln tauschen.

**Zielgruppe:** Kinder ab 10 Jahren, Montage gemeinsam mit Erwachsenen. Laden des Akkus und Propellerwechsel nur durch Erwachsene.
**Positionierung:** hochwertiges Technik-Bauset (Anmutung zwischen Technic-Modell und Designobjekt), kein Wegwerf-Spielzeug.

---

## 2. Designsprache „Wabe & Hummel“

Eine eigene Formensprache, die sich klar von LEGO Technic (Lochbalken) und Fischertechnik (Nutbausteine) abhebt:

| Merkmal | Umsetzung | Wirkung |
|---|---|---|
| **Kiesel-Achteck** | Rumpf als achteckiger „Kiesel“ mit großen Radien (R9 vertikal, R3 an Ober-/Unterkante) | robust, freundlich, technisch präzise |
| **Wabe** | sechseckige Ausschnitte in den Auslegern, Waben-Relief auf den Seitenblenden | Leichtbau sichtbar machen, Wiedererkennung |
| **Käfig statt Klinge** | jeder Propeller sitzt in einem runden Schutzkäfig mit weichem Stoßfänger | Sicherheit wird zur Gestaltung |
| **Gesicht** | zwei leuchtende LED-„Augen“ vorne | Flugrichtung sofort erkennbar, Charakter |
| **Gläserne Kanzel** | transparente Kuppel über dem Elektronikmodul | „Herz“ der Drohne sichtbar, erklärt Technik |
| **Ringe & Kreise** | alle Verbindungen sind runde, orange Ringe oder Pins | klare, wiederkehrende Geometrie |

### Farbcode (zugleich Bauanleitung)

| Farbe | Bedeutung | Bauteile |
|---|---|---|
| **Orange** | „Hier wird verbunden“ – alles, was man dreht, steckt oder klickt | Bajonett-Buchsen, Drehringe, Rastpins, Schnapp-Clips, Akku-Riegel |
| **Weiß** | tragende Struktur | Rumpfschale, Propellerschutz, Landekufen |
| **Graphit** | Ausleger und Rahmen | Auslegerträger, Motorgondeln, Blenden, Kanzelring |
| **Türkis** | Energie und Elektronik | Power-Core, Akku-Schublade, LEDs |
| **Gelb** | Rotor dreht im Uhrzeigersinn (CW) | Motorabdeckung, Propeller, Kappe an Ausleger 1 und 3 + Nummernschild am Rumpf |
| **Violett** | Rotor dreht gegen den Uhrzeigersinn (CCW) | dito an Ausleger 2 und 4 |
| **Schwarz (weich)** | Gummi/TPU, darf anstoßen | Stoßfänger, Kufengummis |

Kinderregel: **„Orange verbindet. Gelb zu Gelb, Violett zu Violett. Die Nummer am Arm passt zur Nummer am Rumpf.“**

---

## 3. Proportionen und Hauptmaße (Designmodell)

| Maß | Wert |
|---|---|
| Spannweite über Propellerschutz (diagonal) | ca. 300 mm |
| Breite/Tiefe Gesamtmodell | ca. 246 × 246 mm |
| Höhe mit Kanzel | ca. 68 mm |
| Rumpf (Achteck) | ca. 100 mm Schlüsselweite, 28 mm hoch |
| Motorabstand diagonal | 210 mm (Achsabstand 148 mm benachbart) |
| Propeller | 2-Blatt, ca. 78 mm (3″-Klasse), weich |
| Propellerschutz | Ø 90 mm innen, Käfig oben + unten |

Alle Maße sind Designwerte aus dem Blender-Modell. Die technische Auslegung (Gewicht, Schub, Wandstärken) erfolgt in Fusion 360 und muss die Maße ggf. anpassen.
**Wichtigstes technisches Risiko:** Gewicht. Ziel ist ein Abfluggewicht unter 250 g (besser < 200 g). Gedruckte Käfige sind schwer, deshalb werden dort in Fusion Wandstärken und Gitter optimiert.

---

## 4. Baugruppen und Module

```
BRUMMI
├── Rumpf (Baugruppe R)
│   ├── R01 Rumpfschale (mit 4 Bajonett-Buchsen V01–V04)
│   ├── R02 Power-Core – Elektronikmodul, werkseitig geschlossen
│   ├── R04 Akku-Schublade + R05 Akku-Pack + V25 Akku-Riegel
│   ├── R06 Kanzelring + V21–V24 Schnapp-Clips + R07 Kanzel
│   └── Deko: R08 Seitenblenden (3), R09 LED-Visier, R03 Status-LED, Nummernschilder 1–4
├── Ausleger 1–4 (Baugruppe A, 4x baugleich, Farbe je Drehrichtung)
│   ├── A-01 Auslegerträger mit Bajonett-Stecker
│   ├── V05–V08 Drehring (orange, unverlierbar)
│   ├── A-04 Motorgondel + A-05 Motor (vormontiert)
│   ├── A-06 Motorabdeckung (gelb/violett)
│   ├── A-07 Propellerschutz-Käfig + A-08 Stoßfänger + 2 Rastpins
│   └── A-09 Propeller + A-10 Propellerkappe
└── Landegestell (Baugruppe L)
    ├── L01/L02 Landekufen (federnd)
    ├── L03–L06 Kufengummis
    └── V17–V20 Rastpins
```

**Austauschbarkeit:** Alle vier Ausleger sind mechanisch identisch. Nur Motorabdeckung und Propeller unterscheiden sich in der Drehrichtung (Farbe). Ein gebrochener Arm, Käfig oder eine Kufe wird einzeln ersetzt, ohne Werkzeug.

---

## 5. Verbindungskonzept (Phase 3)

Leitidee: **Drei Verbindungstypen für Kinder, ein Typ nur für Erwachsene.** Alle kindgerechten Verbindungen sind orange, groß (Greifflächen ≥ 15 mm) und geben ein hörbares Klick-Feedback.

### Typ A – Twist-Lock-Bajonett (Ausleger ↔ Rumpf)
- Auslegerhals (Ø 13,6 mm) mit zwei Nocken in die Buchse stecken, orangen Drehring **90° drehen bis „Klick“**.
- Rastnase mit Federzunge hält die Position; Lösen durch Zurückdrehen gegen spürbaren Widerstand.
- Trägt die Hauptlasten (Schub, Landestoß). Nocken und Buchse in Fusion auf Biegung/Torsion auslegen; Buchse als Einlegeteil aus POM/PA für viele Steckzyklen.
- **Sicherheitsfunktion:** Im Hals sitzen Federkontakte für Motorstrom. Erst im verriegelten Zustand ist der Kontakt geschlossen. Ein nicht eingerasteter Arm = Motor startet nicht.
- **Verwechslungsschutz:** Nummer 1–4 und Farbe am Arm und am Rumpf.

### Typ B – Rastpin (Propellerschutz ↔ Motorgondel, Landekufe ↔ Rumpf)
- Ein einheitlicher Pin: Ø 6 mm Schaft mit geschlitztem Spreizende, Ø 9–11 mm Kopf.
- **Unverlierbar:** Pin bleibt über einen Bund im Bauteil gefangen und kann nur ein- und ausgerastet, nicht abgezogen werden (Verschluckschutz).
- Reine Steckverbindung, keine Lastspitzen im Flug, Kräfte gering.

### Typ C – Schnapp-Clip (Abdeckungen)
- Kanzelring (4 Clips), Motorabdeckungen, Seitenblenden, Akku-Riegel.
- Großzügige Biegelänge und Hinterschnitt ≤ 1 mm, damit die Clips im 3D-Druck (PETG) nicht ermüden.
- Akku-Riegel als **Schiebe-und-Drück-Verriegelung** (zwei Bewegungen = Kindersicherung).

### Typ W – werkseitig / nur Erwachsene
- Motor in Gondel, Propellerkappe (mit Werkzeug), Power-Core-Gehäuse (verklebt/verschraubt, nicht zu öffnen).

### Funktional oder nur optisch?

| Element | Mechanisch funktional | Nur optisch / Designmerkmal |
|---|---|---|
| Bajonett-Buchse, Drehring, Nocken | ✔ trägt Last + verriegelt + schaltet Strom | – |
| Rastpins Käfig/Kufe | ✔ | – |
| Schnapp-Clips Kanzel, Akku-Riegel | ✔ | – |
| Wabenausschnitte im Ausleger | teilweise (Gewicht) | ✔ Wiedererkennung |
| Waben-Relief Seitenblenden | – | ✔ (Blenden sind Wechselteile zum Personalisieren) |
| Grip-Rippen am Drehring | ✔ Griffigkeit | ✔ |
| Nummernschilder, Ziffern | – | ✔ Montagehilfe |
| LED-Visier, Status-LED | Funktion: Flugrichtung/Status | ✔ Charakter |
| Kühlrippen auf Power-Core | im Blender-Modell angedeutet, echte Kühlung in Fusion auslegen | ✔ |
| Kanzel | Staub-/Fingerschutz der Elektronik | ✔ „gläsernes Herz“ |

Im Blender-Modell sind die Verbindungen **visuell** dargestellt (Ringe, Nocken, Pins, Clips). Die exakten Rastgeometrien (Federzungen, Hinterschnitte, Spiel) werden in Fusion 360 neu konstruiert.

---

## 6. Montageabfolge für Kinder (entspricht dem Regler „Montage“ im Modell)

| Schritt | Was das Kind tut | Verbindung |
|---|---|---|
| 0 | Rumpfschale hinlegen, Buchsen 1–4 entdecken | – |
| 1 | Power-Core in den Schacht drücken bis Klick | C |
| 2 | Akku-Schublade von hinten einschieben, Riegel schließen *(Erwachsene)* | C |
| 3 | Seitenblenden und LED-Visier einclipsen | C |
| 4 | Kanzelring mit Kanzel aufclipsen | C |
| 5 | Landekufen von unten einstecken | B |
| 6 | (Kontrolle: steht der Rumpf gerade?) | – |
| 7 | Ausleger 1–4 einstecken und Drehring bis Klick drehen | A |
| 8 | Motorabdeckungen (Farbe beachten) aufclipsen | C |
| 9 | Propellerschutz-Käfige aufsetzen, Rastpins drücken | B |
| 10 | Propeller und Kappen *(vormontiert oder durch Erwachsene)* | W |

---

## 7. Sicherheitskonzept (Grundlage, nicht abschließend)

| Risiko | Gegenmaßnahme im Design |
|---|---|
| **Verletzung durch Propeller** | geschlossener Käfig oben + unten, Gitterweite in Fusion auf Fingersicherheit auslegen; weiche Propeller; Motorfreigabe nur bei verriegelten Armen; Propellerstopp bei Anstoß/Absturz (Firmware); Anfängermodus mit begrenzter Drehzahl und Höhe |
| **Verschlucken von Kleinteilen** | keine losen Kleinteile: Pins und Drehringe unverlierbar; alle losen Teile größer als der Prüfzylinder für Kleinteile; Kennzeichnung „nicht für Kinder unter 3 Jahren“ |
| **Akku: Überhitzung/Brand** | Akku nur mit Schutzschaltung (Überladung, Tiefentladung, Kurzschluss, Temperatur); Akkufach aus flammhemmendem Material (z. B. UL94 V-0); Akku-Riegel als Kindersicherung; Laden nur mit Original-Ladegerät durch Erwachsene; Akkupack als geprüftes Kaufteil (Transporttest UN 38.3) |
| **Elektronik: Überhitzung** | Power-Core geschlossen, mit Kühlfläche und Temperaturabschaltung; keine offenen Kontakte; Federkontakte im Bajonett berührungsgeschützt |
| **Scharfe Kanten** | alle Außenkanten ≥ R1, Gitterstreben gerundet, gedruckte Teile mit Entgratungs-Hinweis |
| **Mechanisches Versagen** | Lastpfade über Bajonett und Rumpfschale; Fall- und Steckzyklen-Test in der Prototypphase |

**Wichtig:** Dieses Konzept ersetzt keine Sicherheitsprüfung. Vor jedem Einsatz durch Kinder muss das Produkt fachgerecht geprüft werden, u. a. nach Spielzeugrichtlinie (EN 71-1/-2/-3), Elektrospielzeug (EN IEC 62115), Funk/EMV (RED), Batterie-/Akkuvorschriften und den geltenden Drohnenregeln (EU-Drohnenverordnung, Klasse C0 bzw. Spielzeug).

---

## 8. 3D-Druck-Leitlinien (Vorschau auf Phase 4/5)

- Strukturteile: PETG oder ASA, 3–4 Perimeter, 25–40 % Gyroid-Füllung.
- Weiche Teile: TPU 95A (Stoßfänger, Kufengummis).
- Propeller: **nicht drucken**, Kaufteil aus flexiblem Kunststoff.
- Rastpins und Bajonett-Buchsen langfristig als Spritzguss (POM/PA), im Prototyp gedruckt.
- Druckausrichtung so wählen, dass Clips und Nocken entlang der Schichten belastet werden (in Fusion festlegen).

---

## 9. Offene Punkte für dein Feedback

1. Gefällt dir die Richtung „Wabe & Hummel“ mit dem Farbcode, oder soll es technischer/dunkler wirken?
2. Größe: ca. 30 cm Spannweite ist gut zu greifen, macht aber Gewicht. Lieber kompakter (ca. 22 cm)?
3. Landegestell: Kufen (wie jetzt) oder vier einzelne Beine?
4. Die drei Streben des Propellerschutzes reichen unter die Gondel und sehen wie Beine aus. Gewollt, oder lieber versteckt?
5. Sollen Kinder die Propeller selbst wechseln dürfen (mit Werkzeug), oder bleibt das bei Erwachsenen?
