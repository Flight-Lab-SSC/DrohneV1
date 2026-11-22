# BRUMMI – Flugfähigkeit und Effizienz

Nov 22, 2026 · @Leon

Kurz: So wie gezeichnet hebt BRUMMI nicht sinnvoll ab. Mit leichterem Käfig, dünneren Wänden und einem größeren Akku fliegt er gut, ohne dass sich das Aussehen ändert.

## Gewicht

Das Modell wiegt gedruckt rund **390 g ohne Akku**, fast das Doppelte des Ziels von 200 bis 250 g. Allein die vier Propellerschutz-Käfige wiegen mit Stoßfänger rund 150 g, das ist der größte Einzelposten.

| Baugruppe | Ist (g) | Optimiert (g) | Hauptursache |
| --- | --- | --- | --- |
| 4 Käfige A-07 | 121 | 60 | Ring mit 2,5 mm Wand und 22 mm Höhe massiv (allein 19 g je Käfig) |
| 4 Stoßfänger A-08 (TPU) | 30 | 17 | Vollprofil Ø 5,2 mm |
| Rest der 4 Ausleger (Träger, Drehring, Gondel, Motor, Abdeckung, Propeller) | 127 | 106 | Gondel und Kragen massiv; Motoren je ca. 9 g |
| Rumpf ohne Akku | 91 | 95 | Schale 1,6 mm, Kanzel 1 mm |
| Landegestell | 22 | 16 | Rohr Ø 6,4 mm |
| **Summe ohne Akku** | **391** | **294** |  |

Gerechnet mit PETG (1,27 g/cm³), TPU (1,21 g/cm³), dünne Teile voll, dicke Teile mit 3–4 Perimetern und 30 % Füllung. Elektronik, Kabel und Bajonett-Kontakte sind geschätzt. Die echte Zahl kann ±15 % abweichen.

## Schub, Schub-Gewichts-Verhältnis und Flugzeit

Mit dem Akku aus der Stückliste (20 × 46 × 6,5 mm, also etwa 1S 450 mAh) hebt BRUMMI **nicht ab**: das Schub-Gewichts-Verhältnis liegt unter 1. Für eine kindgerechte, ruhige Drohne braucht es mindestens 1,8, und die Flugzeit sollte 3 Minuten oder mehr betragen.

| Variante | Abfluggewicht | Schub/Gewicht | Schwebeleistung | Flugzeit Schweben (Mischflug) |
| --- | --- | --- | --- | --- |
| Ist + Akku laut Stückliste (1S 450 mAh) | 403 g | 0,9 | 125 W (34 A) | hebt nicht ab |
| Ist + 2S 500 mAh (füllt den Schacht) | 419 g | 1,3 | 132 W | ca. 1,3 min (1,1) |
| Optimiert + 2S 500 mAh | 305 g | 1,9 | 72 W | ca. 2,5 min (2,0) |
| **Optimiert + 2S 850 mAh (Schacht etwas größer, nachgerechnet am v2-Modell)** | **340 g** | **1,7** | **87 W** | **ca. 3,5 min (2,8)** |
| Optimiert + 3S 650 mAh | 332 g | 2,5 | 82 W | ca. 4,2 min (3,4) |

Empfehlung: optimierte Teile plus **2S 850 mAh** und Motoren der Klasse 1404 mit ca. 4500–5500 KV. Das gibt einen ruhigen Anfängerflieger mit Reserve. Wer 5 Minuten und mehr will, braucht 3S oder einen noch größeren Akku.

Der Grund für die kurzen Zeiten: Vier Propeller mit 78 mm tragen über 300 g nur mit viel Leistung (kleine Rotorfläche). Größere Propeller wären effizienter, bräuchten aber größere Käfige und würden das Design verändern.

## Schutzkäfig: kostet er Leistung?

Ja, aber weniger über den Luftstrom als über das Gewicht. Der Käfig, wie er jetzt ist, kostet etwa **12–16 % Schub**. Optimiert sind es etwa **5–7 %**, mit gerundeter Einlaufkante vielleicht nahezu null.

| Käfigteil | Schubverlust Ist | Optimiert | Warum |
| --- | --- | --- | --- |
| Gitter unten (6 Streben + Ring, 7 mm unter dem Propeller) | ca. 8 % | ca. 4 % | sitzt im schnellen Abwind, dort schadet jede Fläche am meisten |
| 3 Streben + Kragen (35 mm darunter) | ca. 3 % | ca. 1 % | stehen im Strahl; flache 4 × 4 mm Balken bremsen stark |
| Gitter oben (8 Streben + Ring, 13 mm über dem Propeller) | ca. 3 % | ca. 1 % | auf der Ansaugseite ist die Luft langsamer, daher weniger schlimm |
| Ring als Duct (Spalt 3,5 mm zur Propellerspitze) | 0 bis –2 % | 0 bis +5 % | Spalt zu groß für echten Duct-Effekt; mit 2 mm Spalt und runder Lippe hilft er etwas |

Zum Vergleich: Ausleger und Motorgondel im Abwind kosten noch einmal etwa 4 %, das hat jede Quadrocopter-Drohne.

Der größere Effekt ist das Gewicht: Die Käfige machen rund 150 g aus. Jedes Gramm mehr braucht Schwebeleistung, deshalb bringt ein leichterer Käfig mehr als ein aerodynamisch besserer.

## Luftwiderstand

Der Luftwiderstand ist für BRUMMI unkritisch. Bei rund 0,009 m² Stirnfläche und c\<sub>w\</sub> ≈ 1 beträgt er bei 5 m/s (typisches Kindertempo) nur etwa 14 g, bei 10 m/s etwa 56 g. Das kostet kaum Leistung. Die großen Ringe machen ihn aber windempfindlich: über etwa Windstärke 3 driftet er spürbar. Für Kinder ist das eher ein Hinweis für die Anleitung (bei Wind drinnen oder nicht fliegen) als ein Grund für Änderungen.

## Kleine Änderungen (Design bleibt)

Alle Punkte ändern nur Wandstärken, Querschnitte oder Innenleben. Form, Farben, Wabe, Käfig oben und unten und die Verbindungen bleiben. Zusammen sparen sie rund 115 g und halbieren den Käfigverlust.

| Nr. | Teil | Änderung | Ersparnis |
| --- | --- | --- | --- |
| 1 | Käfigring A-07 | Wand 2,5 → 1,2 mm, Höhe 22 → 16 mm (deckt die Propellerebene weiter ab). Innenradius 42,5 → 41 mm, damit der Spalt zur Propellerspitze 2 mm statt 3,5 mm ist | ca. 10 g je Käfig, Schub +1–3 % |
| 2 | Käfigring A-07 | Obere Innenkante mit ca. R3 abrunden (Einlauflippe wie bei einem Mantelpropeller) | Schub bis +3 % |
| 3 | Gitter unten | Streben flach 2,4 × 2 mm → hochkant 1,6 × 3 mm (gleich steif), Ring 1,2 mm breit | Schub ca. +4 % |
| 4 | Gitter oben | 8 Streben bleiben (Fingerschutz), aber ebenfalls hochkant 1,6 × 3 mm | Schub ca. +1,5 % |
| 5 | 3 Käfigstreben | Querschnitt 4 × 4 → 3 × 4,5 mm oval, hochkant. Muster um 60° drehen, damit eine Strebe unter dem Ausleger liegt und dessen Windschatten nutzt; untere Gitterstreben über die Streben legen | Schub ca. +2 % |
| 6 | Stoßfänger A-08 | TPU-Profil Ø 5,2 → 4 mm (oder hohl) | ca. 3 g je Stück |
| 7 | Motorgondel A-04 + Käfigkragen | als Topf mit 1,6 mm Wand statt massiv, Kragen 2 mm Wand | ca. 5 g je Arm |
| 8 | Rumpfschale R01 | Wand 1,6 → 1,2 mm, auf der Unterseite (unsichtbar) Wabenausschnitte | ca. 9 g |
| 9 | Kanzel R07 | 0,8 mm tiefgezogenes PETG statt 1 mm | ca. 2 g |
| 10 | Landekufen L01/L02 | Rohr Ø 6,4 → 5 mm, federt weiterhin | ca. 6 g |
| 11 | Akku R05 / Schacht | Schacht von 26 × 70 × 11 auf ca. 32 × 66 × 14 mm innen vergrößern, für 2S 850 mAh | +17 g Akku, dafür ca. 4 min Flug |

Die Punkte 1, 3 und 5 bringen am meisten. Punkt 11 ist nötig, damit BRUMMI überhaupt sinnvoll fliegt.

## Annahmen und offene Punkte

- **Motor:** im Modell Ø 21 mm, also Klasse 1303/1404 (ca. 9 g). Maximalschub angenommen ca. 160 g je Motor auf 2S und 230 g auf 3S mit 78-mm-2-Blatt-Propeller. Ein konkretes Motormodell fehlt noch.
- **Leistung:** Impulstheorie mit Gütegrad 0,55 und Antriebswirkungsgrad 0,72, 80 % nutzbare Akkukapazität. Das entspricht etwa 3,5–4 g Schub pro Watt, typisch für 3-Zoll-Propeller.
- **Käfigverlust:** Abschätzung aus verdeckter Fläche, Luftgeschwindigkeit an der Stelle und Widerstandsbeiwert. Genau misst man das am besten auf einer Schubwaage mit und ohne gedruckten Käfig.
- **250-g-Grenze:** Auch optimiert liegt BRUMMI bei ca. 320 g. Unter 250 g kommt man nur mit kleinerer Spannweite (ca. 22 cm, siehe offener Punkt 2 im Konzept) oder Spritzguss-Teilen. Über 250 g gelten strengere EU-Drohnenregeln (Klasse C1 statt C0).
- **Fingersicherheit:** Die Gitteröffnungen sind schon jetzt ca. 15–20 mm groß. Die vorgeschlagenen Änderungen machen sie nicht größer; die Prüfung nach EN 71 bleibt für die Fusion-Phase offen.
