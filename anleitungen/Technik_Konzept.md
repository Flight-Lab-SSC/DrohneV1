# BRUMMI – Technik: Motoren, Platine, Kabel, Sensorik

Nov 22, 2026 · @Leon

Empfehlung: vier bürstenlose Motoren der Klasse 1404 an 2S, eine eigene Flugsteuer-Platine mit selbst aufgelöteten Sensor-Chips im Power-Core und Motorstrom über Federkontakte im Bajonett. Die Sensoren selbst (IMU, Barometer, Magnetometer) kann man nicht im Bastelkeller herstellen, aber man kann sie als nackte Chips auf eine eigene Platine setzen statt fertige Module zu kaufen.

## Aufbau im Überblick

Der Strom fließt vom Akku in der Schublade über Kontakte in den Power-Core, dort zum Motorregler (ESC) und von dort durch die vier Bajonette in die Ausleger zu den Motoren.

| Block | Ort | Selbst bauen oder kaufen | Gewicht |
| --- | --- | --- | --- |
| Akku 2S 850 mAh, mind. 40C, mit Schutzschaltung | Akku-Schublade R04 | kaufen (Sicherheit) | ca. 45 g |
| Flugsteuerung (Prozessor + IMU + Barometer + Magnetometer) | Power-Core R02, untere Platine | **selbst entwerfen und bestücken** | ca. 4 g |
| Magnetometer-Tochterplatine | oben unter der Kanzel | **selbst** | ca. 1 g |
| 4-in-1-Motorregler (ESC), 2S, ca. 12 A je Kanal | Power-Core, obere Platine | anfangs kaufen (20 × 20 mm), später selbst möglich | ca. 4 g |
| Funkempfänger (ExpressLRS 2,4 GHz) | Power-Core | kaufen oder Chip auf eigene Platine | ca. 1 g |
| 4 Motoren 1404 + Propeller 78 mm | Motorgondeln | kaufen | 4 × 9 g |
| Kabel und Federkontakte | Rumpf, Bajonette, Ausleger | selbst konfektionieren | ca. 8 g |

Der Power-Core (36 × 28 × 15 mm) reicht für zwei gestapelte Platinen: unten die Flugsteuerung, darüber der ESC.

## Motoren und Propeller

Empfehlung: **bürstenloser Außenläufer 1404 mit ca. 4800–5500 KV** für 2S, mit weichem 2-Blatt-Propeller 3 Zoll (78 mm). Der Motor passt genau in das Modell (Ø 21 mm Glocke, ca. 9 g).

- **Warum bürstenlos:** Bürstenmotoren (coreless) schaffen nur Drohnen bis ca. 50 g. BRUMMI wiegt rund 340 g.
- **Warum diese KV-Zahl:** Ein 3-Zoll-Propeller braucht für vollen Schub ca. 27.000 U/min. Mit 7,4 V und Lastverlust ergibt das etwa 5000 KV. Schweben braucht dann nur ca. 40 % Gas, es bleibt viel Reserve.
- **Strom:** schwebend ca. 2,7 A je Motor, maximal ca. 8 A. Der ESC sollte 12 A je Kanal können.
- **Alternative 3S:** 1404 mit ca. 3500 KV. Mehr Schub (Schub-Gewichts-Verhältnis ca. 2,5), aber ein größerer Akku.
- **Montage:** Motor mit 4 Schrauben M2 auf der Gondel-Motorplatte (Lochkreis bei 1404 meist 9–12 mm, im Fusion-Modell an den gewählten Motor anpassen). Schraubensicherung mittelfest.
- **Propeller:** weiches Material (z. B. PC-TPU-Mischung), mit Wellenmutter oder Klemmkappe A-10. Gelb = rechtsdrehend (CW) an Arm 1 und 3, Violett = linksdrehend (CCW) an Arm 2 und 4.

## Platine im Power-Core

Die Flugsteuerung wird eine eigene 4-lagige Platine von ca. 34 × 26 mm, entworfen in KiCad (kostenlos) und bei einem Platinenhersteller gefertigt. Die winzigen Sensor-Chips lässt man am besten gleich vom Hersteller bestücken (Bestückungsservice), den Rest kann man selbst löten.

| Baustein | Vorschlag | Aufgabe |
| --- | --- | --- |
| Prozessor | STM32F405 (oder STM32H743 für mehr Reserve) | rechnet die Lageregelung 1000–8000 Mal pro Sekunde |
| IMU | TDK ICM-42688-P oder Bosch BMI270 | Lage und Drehung (siehe Sensorik) |
| Barometer | Infineon DPS310 oder Bosch BMP390 | Höhe |
| Magnetometer | auf Tochterplatine (siehe Sensorik) | Himmelsrichtung |
| Spannungsversorgung | Schaltregler 5 V, 2 A + getrennter rauscharmer 3,3-V-Regler nur für die IMU | sauberer Strom für Sensoren |
| Akkumessung | Spannungsteiler + Messwiderstand (Shunt) 0,5 mΩ | Akkustand, Strom, Notlandung |
| Speicher | Flash 16 MB | Fluglog für Fehlersuche und Lernen |
| Anschlüsse | USB-C, UART für Empfänger, 4 Motorsignale (DShot), LED-Ausgang | Programmieren, Funk, ESC, LED-Augen |

Tipps für das Layout:

1. IMU genau in die Mitte der Drohne (Schwerpunkt) und weit weg von Spannungsreglern und Motorstromleitungen.
2. Die Platine über 4 weiche Gummitüllen (M2) im Power-Core lagern, damit Motorvibrationen nicht in die IMU gehen.
3. Große Massefläche auf einer Innenlage, Motorstrom und Sensorleitungen auf getrennten Seiten.
4. Als Vorlage lohnt ein quelloffenes Flugsteuer-Design (z. B. aus der Betaflight- oder ArduPilot-Community): Schaltplan anschauen, verstehen, dann selbst zeichnen.

## Sensorik selbst gebaut

Die Messzellen von IMU, Barometer und Magnetometer sind MEMS-Chips: winzige bewegliche Strukturen aus Silizium, die nur im Reinraum gefertigt werden können. Selbst bauen heißt deshalb: **keine fertigen Sensor-Module oder Breakout-Boards, sondern die nackten Chips auf der eigenen Platine**, mit eigener Schaltung, eigener Verdrahtung und eigener Kalibrierung. Das ist genau der Teil, bei dem man am meisten lernt.

| Sensor | Chip-Vorschlag | Was er misst | Worauf achten |
| --- | --- | --- | --- |
| IMU (Beschleunigung + Drehrate, 3 Achsen) | TDK ICM-42688-P (2,5 × 3 mm) oder Bosch BMI270 | Neigung und Drehung, Grundlage jeder Lageregelung | über SPI anbinden (schnell), eigene 3,3-V-Versorgung, mittig und entkoppelt montieren |
| Barometer | Infineon DPS310 oder Bosch BMP390 | Luftdruck, daraus Höhe auf ca. 10 cm genau | mit offenporigem Schaumstoff abdecken (gegen Propellerwind und Licht), kleine Belüftungsöffnung in der Kanzel |
| Magnetometer (Kompass) | ST LIS3MDL, MEMSIC MMC5983MA oder QST QMC5883P | Erdmagnetfeld, daraus Himmelsrichtung | so weit wie möglich weg von Strom: Tochterplatine oben unter der Kanzel, ca. 15 mm über der Hauptplatine; Akkukabel verdrillen; vor jedem Flugtag kalibrieren |

Zwei ehrliche Hinweise:

- **Magnetometer:** In Innenräumen und neben Stahl stört alles das Magnetfeld. Für einen Kinder-Flieger ist der Kompass nicht nötig; er lohnt sich erst mit GPS oder für „Kopf zeigt immer nach Norden“-Spiele. Ich würde ihn einbauen, aber in der Firmware zunächst nur mitloggen.
- **Sehr empfehlenswert für Kinder:** ein optischer Bodensensor (z. B. PixArt PMW3901) plus Laser-Abstandssensor (z. B. ST VL53L1X) auf der Unterseite. Damit hält BRUMMI drinnen von allein seine Position. Auch die gibt es als nackte Chips.

Für die Kinder-Bauanleitung lässt sich das Prinzip anschaulich nachbauen, ohne dass es fliegen muss: ein Pendel mit Winkelmesser zeigt, was ein Beschleunigungssensor spürt, und ein Kreisel auf einer Drehscheibe, was ein Gyroskop misst.

## Kabelführung

Kinder sehen und berühren keine Kabel und keine Stecker: Alle Verbindungen laufen über Kontakte, die sich beim Zusammenbauen von selbst schließen.

1. **Akku → Rumpf:** Die Schublade hat vorne zwei vergoldete Federkontakte (Hochstrom-Pogo-Pins, mind. 10 A je Pin, oder Kontaktfedern aus Messingblech). Der Akku wird werkseitig mit seiner Schutzschaltung in die Schublade gesteckt. Leitung im Rumpf: Silikonkabel 0,5 mm² (AWG 20), Plus und Minus verdrillt (wegen Magnetometer).
2. **Rumpf → Power-Core:** Federkontakte im Schacht unter dem Power-Core: 2 × Akku, dazu 4 × 3 Motorphasen nach außen zu den Bajonett-Buchsen.
3. **Bajonett (Typ A):** Pro Arm 3 Kontakte für die drei Motorphasen plus 1 Erkennungskontakt. Die Kontakte sitzen als Ringe oder Blätter in der Buchse und als Federn am Auslegerhals; sie schließen erst im verriegelten Zustand. Belastung: max. ca. 8 A je Phase, also Kontakte für mind. 5 A Dauerstrom wählen.
4. **Erkennung:** Ein kleiner Magnet im orangen Drehring und ein Hallsensor (oder der vierte Kontakt) in der Buchse melden „Arm eingerastet“. Die Firmware startet die Motoren nur, wenn alle vier Arme gemeldet sind.
5. **Ausleger:** 3 Silikonlitzen 0,25 mm² (AWG 24) im Träger. Dafür braucht der Auslegerträger in Fusion einen inneren Kabelkanal von ca. 5 × 4 mm, der an den Wabenlöchern vorbeiführt.
6. **Gondel:** Kabel durch ein Loch in der Motorplatte direkt an die Motorlitzen, gelötet und mit Schrumpfschlauch isoliert (werkseitig, nicht für Kinder).
7. **LED-Augen und Status-LED:** über zwei weitere Federkontakte vom Power-Core zur vorderen Blende; adressierbare RGB-LEDs (eine Datenleitung).

Für Fusion vormerken: Kabelkanal im Träger, Kontakttaschen in Buchse und Hals, Durchführung in der Gondel, Kontaktfläche in Schublade und Schacht.

## Firmware und Sicherheitsfunktionen

Am Anfang läuft eine fertige, quelloffene Flugsoftware auf der eigenen Platine: **INAV** oder **ArduPilot**. Beide können Höhe halten mit dem Barometer, nutzen den Kompass und unterstützen optischen Bodensensor und Abstandssensor. Damit man sie nutzen kann, muss die eigene Platine als neues „Board“ beschrieben werden (eine Konfigurationsdatei mit Pins und Sensoren), das ist ein gutes Lernprojekt für sich. Eine komplett eigene Software geht später auch, ist aber ein großes Projekt.

Sicherheitsfunktionen, die für BRUMMI eingestellt werden sollten:

- [ ] Motoren starten nur, wenn alle 4 Arme eingerastet sind (Erkennungskontakt)
- [ ] Anfängermodus: selbststabilisierend, max. 25° Neigung, Höhe gehalten, max. 3 m Höhe
- [ ] Motorstopp bei Absturz oder Anstoßen (starker Stoß an der IMU erkannt)
- [ ] Automatisch landen bei schwachem Akku oder Funkverlust
- [ ] Drehzahlbegrenzung im Kindermodus, voller Schub nur im Erwachsenenmodus
- [ ] LED-Augen zeigen Zustand: blau = bereit, grün = fliegt, rot blinkend = Akku leer

Nächster Schritt: Motor und Akku konkret auswählen, dann Schaltplan in KiCad und parallel Kabelkanal und Kontakte in Fusion konstruieren.
