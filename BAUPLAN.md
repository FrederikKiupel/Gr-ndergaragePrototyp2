# PIXEL & PROTOCOL × netzfest – Analyse, Fusion & Bauplan

Stand: 18.11.2026 · Grundlage: bestehende netzfest-Seite (Base44/React, Screenshots + Code), Recherche-Daten aus `inhalte/recherche/` (Abruf 06.11.2026)

> Der Auftrag lautete „analysieren, als HTML/CSS/JS bauen, mit mehr Infos füllen“. Deshalb läuft diese Runde ohne Zwischenstopp
> (Antwort 1 und 2 in einem Durchgang). Jede Weggabelung unten lässt sich mit `/umentscheiden` kippen.

---

## Phase 0 – Briefing-Dekodierung

🎯 **MARA:** netzfest ist eine kostenlose Plattform gegen Cybermobbing, Hass im Netz und Desinformation. Sie richtet sich an vier
sehr unterschiedliche Gruppen: Schüler:innen, Eltern, Lehrkräfte und Fachkräfte. Die bestehende Seite sieht ordentlich aus, ist aber
eine Bibliothek mit Schaufenster. Das Thema verlangt mehr: Ein Teil der Besucher:innen kommt nicht zum Stöbern, sondern weil es gerade wehtut.

**Leitfrage:** *Nach 10 Sekunden soll man fühlen: „Hier bin ich richtig, hier hilft mir jemand.“ Nach 2 Minuten soll man entweder
den nächsten konkreten Schritt kennen (akut) oder ein passendes Material geöffnet haben (Vorbereitung).*

🧭 **JONAS:**
| Hart (gesetzt) | Weich (Annahme, markiert) |
|---|---|
| Themen: Cybermobbing, Hass im Netz, Fake News | **A1** Kein CMS-Budget, Pflege durch eine Person mit HTML-Grundkenntnissen |
| Zielgruppen: 4 Rollen | **A2** Statisches Hosting (Netlify/Uberspace/eigener Webspace) |
| Kostenlos, ohne Anmeldung | **A3** Mut-Level 6/10: Vertrauen vor Spektakel, aber nicht beliebig |
| Format: HTML + CSS + JS | **A4** Ein großer Teil mobil, Kinder und Jugendliche fast nur mobil |
| Deutsch, Raum Deutschland | **A5** Materialien sind Demo-Inhalte, die Dateien fehlen noch |

**Rückfragen (beantwortet mit Annahmen):**
1. Gibt es echte Material-Dateien (PDF) und ein Logo? → *Annahme: nein. Platzhalter sind markiert.*
2. Wer betreibt die Seite (Verein, Schule, Projekt)? → *Annahme: gemeinnütziges Projekt. Impressum als Gerüst.*
3. Domain? → *Annahme: `https://www.netzfest.example`. Steht zentral in `_werkstatt/bauen.py`.*

---

## Analyse der bestehenden Seite

**Was zu sehen ist:** Zentrierter Hero mit Eyebrow-Pille, Riesen-Claim „Gemeinsam stark im Netz.“ (Buchstaben-Welle), vier
Rollenkarten, gelber CTA mit Trennstrich-Pfeil, drei KI-generierte Fotos. Materialbibliothek mit linker Filterspalte (6 Gruppen als Chips)
und Kartenraster mit Illustrationen. Palette: Navy-Tinte, Himmelblau, Amber. Schrift: geometrische Grotesk (Plus Jakarta Sans).

**Stärken, die bleiben:**
1. **Rollenwahl als Einstieg.** Vier klare Türen statt eines Mega-Menüs.
2. **Filter nach Zeitrahmen.** „Ich habe 15 Minuten“ ist die ehrlichste Frage, die eine Lehrkraft stellt. Das ist echter Nutzwert.
3. **Ruhige, vertrauenswürdige Palette** mit einem markanten CTA (Amber, dunkle Kontur, abgesetzter Pfeil).

**Größte Schwächen:**
1. **Hilfe ist versteckt.** Wer akut betroffen ist, findet die Nummern erst im vorletzten Abschnitt. Für dieses Thema ist das der schwerste Fehler.
2. **Das Versprechen „Die Seite stellt sich darauf ein“ wird nicht eingelöst.** Die Rolle setzt nur einen Filter, die Startseite bleibt gleich.
3. **Template-Detektor schlägt an:** Eyebrow + Claim + 4 Karten + Button + 3 Stockfotos. Die Fotos sind austauschbare KI-Bilder ohne Aussage.
4. **Karten sind nicht unterscheidbar.** Dieselben drei Illustrationen wiederholen sich, Titel werden abgeschnitten („Rechtlich sicher reagieren: …“).
5. **Inhalt ist dünn und unbelegt.** Wissen umfasst drei Absätze ohne Rechtslage, Quellen und Glossar. Dazu kommt Technik: Als React-SPA zeigt die Seite ohne JavaScript nichts an (SEO, Robustheit).

**Visuelle DNA (weiterverwenden / brechen / umkehren):**
- ✅ Weiterverwenden: Navy-Tinte + Amber-CTA mit Konturrahmen und Pfeilfach
- ✅ Weiterverwenden: enge, schwere Headlines (Letter-Spacing −0.04em)
- 🔁 Umkehren: Statt Stockfotos zeigt der Hero eine **Netz-Grafik**. Der Claim wird zum Bild.
- 💥 Brechen: Statt identischer Illustrationen bekommen die Karten **typografische Codes**: Materialtyp als Farbfeld, Thema als Glyphe, Dauer groß.

---

## Phase 1 – Divergenz

🧭 **JONAS – Strategie**
- **I1 Zwei Geschwindigkeiten:** Die Seite unterscheidet „Ich brauche jetzt Hilfe“ von „Ich bereite etwas vor“. Beide Wege sind ab der ersten Sekunde sichtbar.
- **I2 Die 45-Minuten-Lehrkraft:** Die Persona mit dem höchsten Wiederkehrwert. Für sie zählt „Stunde morgen früh, null Vorbereitung“, also Ablaufpläne mit Minutenangaben.
- **I3 Eltern um 23 Uhr:** Die Persona mit dem höchsten Stress. Sie braucht keine Bibliothek, sondern drei Sätze und eine Nummer mit Uhrzeit.

🗺️ **LINA – UX & IA**
- **I4 Erste-Hilfe-Navigator:** Zwei Fragen („Wer bist du?“, „Was passiert gerade?“) ergeben einen persönlichen Schritte-Plan mit passender Anlaufstelle. *(Kein Hero-Muster.)*
- **I5 Themen als eigene Seiten** statt Tabs. Jede bekommt dieselbe Gliederung: Was ist das, Formen, Woran erkennen, Was tun, Rechtslage, Quellen.
- **I6 Filter per URL:** `materialien.html?thema=fakenews&fuer=eltern`. Damit sind Auswahlen teilbar und verlinkbar.

🎨 **YUKI – Visual**
- **I7 Typografische Materialkarten:** Typ als Farbfeld, große Dauerangabe, Themen-Glyphe. Keine Illustration nötig, trotzdem unterscheidbar.
- **I8 Zwei Tonlagen in einem System:** Erwachsene in Navy/Weiß, Kinderbereich in warmem Papier-Gelb mit größerer Type. Gleiche Tokens, anderes Gewicht.
- **I9 Lesespalte mit Randnotizen** für Wissensseiten. Paragrafen und Quellen stehen am Rand wie in einem Schulbuch. *(Kein Hero-Muster.)*

✨ **NOVA – Wildcard**
- **I10 „Das Netz hält“:** Im Hero liegt ein Feld aus Punkten. Bewegt man Maus oder Finger, verbinden sich die Punkte in der Nähe zu einem Netz. Allein fällt man durch, gemeinsam hält es.
- **I11 Akut-Knopf als Puls:** Ein dauerhafter, ruhig pulsierender Punkt in der Kopfzeile. Er klingelt nicht, er ist da.
- **I12 (fast zu viel) Die Seite zerbricht:** Scrollt man in den Bereich Hass im Netz, zerkratzen Kommentare die Seite. Mit Gegenrede setzt man sie wieder zusammen.

💻 **ANTON – Frontend**
- **I13 Statisch vorgerendert, JS nur als Verstärkung:** Alle Karten stehen im HTML, JavaScript blendet beim Filtern nur aus. Ohne JS bleibt alles lesbar.
- **I14 Native `<dialog>`** für den Navigator: Fokusfalle, Esc und Hintergrund-Sperre gibt es dabei kostenlos.
- **I15 Ein Mini-Generator** (Python) baut aus JSON + Teilvorlagen alle Seiten. Kopf und Fuß stehen nur einmal da, es gibt keinen Framework-Zwang.

🗄️ **IDA – Backend/Pflege**
- **I16 Materialien als eine JSON-Datei.** Ein neues Material bedeutet einen Block kopieren und `python3 bauen.py` ausführen.
- **I17 Merkliste ohne Konto** (localStorage). Datenschutzfreundlich, kein Backend.
- **I18 Kontaktformular erst später.** Für die Startphase ein Mailto mit klarer Erwartung, kein halbes Backend.

📈 **FELIX – SEO/A11y/Recht**
- **I19 Schriften selbst hosten.** Google Fonts per CDN ist in Deutschland ein Datenschutzrisiko (keine Rechtsberatung). Mit Fallback-Metriken gibt es keinen Layout-Shift.
- **I20 Strukturierte Daten:** `FAQPage` für Hilfe, `LearningResource` für Materialien, `Organization` für die Startseite.
- **I21 Hilfenummern mit Erreichbarkeit,** belegt, mit Stand-Datum. Eine Nummer ohne Uhrzeit ist um 23 Uhr eine Enttäuschung.

😈 **VIKTOR – Kritik**
- **I22 Stockfotos raus.** KI-Teenager mit Laptop sind 2026 das neue Handshake-Foto.
- **I23 Ein Spiel reicht, wenn es gut ist.** Lieber „Fake Detektiv“ mit 6 starken Runden plus Links auf geprüfte externe Spiele als drei halbe Eigenbauten.

---

## Phase 2 – Kollision & Mutation

✨ NOVA: „I12 ist mein Herz.“ — 😈 VIKTOR: „I12 ist ein Trigger. Auf einer Seite, die Betroffene besuchen, zerkratzt du ihnen den Bildschirm mit Hass?“ — 🎯 MARA: „Viktor hat recht. I12 wird umgekehrt: Nicht der Hass zerkratzt, sondern die Hilfe verknüpft.“ → **H1**

- **H1 Netz statt Narbe (I10 + umgekehrtes I12):** Der Hero zeigt einzelne, lose Punkte (Menschen). Die Nähe der Hand verbindet sie, die Rollenwahl zieht das Netz enger. Das Bild trägt den Claim, ohne ein Foto zu brauchen.
- **H2 Akut-Navigator (I1 + I4 + I11 + I14):** Ein ruhiger Akut-Knopf in der Kopfzeile öffnet auf jeder Seite den Navigator als Dialog. Ohne JS führt er zur Hilfe-Seite, wo derselbe Navigator als Abschnitt steht. *Übertragung aus der Medizin:* das Triage-Prinzip der Notaufnahme, nicht alles auf einmal.
- **H3 Rolle verändert Inhalte, nicht nur Filter (I2 + I3 + Schwäche 2):** Elemente tragen `data-fuer="eltern"`. Die Startseite zeigt pro Rolle einen eigenen Untertitel, eine eigene Empfehlung („Für dich: …“) und eine eigene Hilfe-Priorität.
- **H4 Schulbuch-Wissen (I5 + I9 + I21):** Themenseiten mit Lesespalte, Randnotizen für Paragrafen und Quellen, „Was tun“ nach Rolle gegliedert. *Was kann das nur im Web?* Jede Randnotiz ist ein echter Link zur Quelle.

🗺️ LINA: „H2 und die Rollenkarten konkurrieren im Hero.“ — 🎯 MARA: „Nein, sie sind die zwei Geschwindigkeiten. Akut steht oben rechts und als Band direkt unter dem Hero. Die Rolle ist der Hero.“ — 💻 ANTON: „H1 läuft auf einem Canvas mit höchstens 90 Punkten, pausiert außerhalb des Bildschirms und ist bei reduzierter Bewegung ein statisches Netz. Machbar.“

---

## Phase 3 – Realitätscheck

| Idee | Machbarkeit | Pflege | Risiko | Klischee |
|---|---|---|---|---|
| H1 Netz-Hero | ✅ ~80 Zeilen JS | keine | Ablenkung, Akku → begrenzt, pausiert | mittel, wird durch die Bedeutung getragen |
| H2 Akut-Navigator | ✅ Daten in JS + Fallback-HTML | Texte in einer Datei | Falsche Empfehlung → nur Schritte und Anlaufstellen, keine Diagnose | niedrig |
| H3 Rollen-Inhalte | ✅ data-Attribute | gering | Ohne JS → neutraler Inhalt sichtbar | niedrig |
| H4 Schulbuch-Wissen | ✅ statisch | Texte pflegen | Rechtsinfos → als Überblick markiert, keine Beratung | niedrig |
| I13/I15 Generator | ✅ Python 3, keine Pakete | ein Befehl | Pflegende müssen wissen, dass sie nicht die Ausgabe bearbeiten → LIESMICH | – |
| I19 Fonts lokal | ✅ woff2 (OFL) | keine | – | – |
| I12 original | ⚠️ machbar | – | ❌ belastend für Betroffene | hoch |

---

## Phase 4 – Fusion

**Rückgrat:** **H2 „Zwei Geschwindigkeiten“**. Jede Seite beantwortet zuerst „Brauchst du jetzt Hilfe?“ und erst danach „Was willst du vorbereiten?“.
**Schichten:** H3 (Struktur), H4 (Inhalt), I7 (Unterscheidbarkeit), I13/I15/I16 (Pflege), I19–I21 (Vertrauen).
**Signature Moment:** H1 „Das Netz hält“, mit statischem Fallback.

### Fusionsmatrix

| Idee | Status | Begründung |
|---|---|---|
| I1 Zwei Geschwindigkeiten | ✅ Rückgrat | Löst die schwerste Schwäche der alten Seite. |
| I2 45-Min-Lehrkraft | ✅ übernommen | Ablaufpläne mit Minuten in jeder Unterrichtseinheit. |
| I3 Eltern um 23 Uhr | ✅ übernommen | Erreichbarkeiten stehen direkt an jeder Nummer. |
| I4 Navigator | ✅ übernommen | Kern von H2. |
| I5 Themen-Seiten | ✅ übernommen | SEO und klare Gliederung. |
| I6 Filter-URL | ✅ übernommen | Themen-Links springen direkt in die gefilterte Bibliothek. |
| I7 Typo-Karten | ✅ übernommen | Unterscheidbar ohne Bildproduktion. |
| I8 Zwei Tonlagen | 🔧 angepasst | Nur der Kinderbereich bekommt die warme Tonlage, kein eigenes System. |
| I9 Randnotizen | 🔧 angepasst | Ab Desktop als Randspalte, mobil als Kasten im Fluss. |
| I10 Netz | ✅ Signature | Siehe H1. |
| I11 Puls-Knopf | 🔧 angepasst | Puls nur einmal beim Laden, danach ruhig. Dauerpuls stresst. |
| I12 Zerbrechen | ❌ verworfen | Belastend für Betroffene, umgekehrt in H1 aufgegangen. |
| I13 Vorrendern | ✅ übernommen | Robust, SEO-fest. |
| I14 `<dialog>` | ✅ übernommen | Barrierefreiheit gibt es eingebaut. |
| I15 Generator | ✅ übernommen | Kopf und Fuß nur einmal pflegen. |
| I16 JSON-Material | ✅ übernommen | Eine Datei, ein Befehl. |
| I17 Merkliste lokal | ✅ übernommen | Kein Konto, kein Backend. |
| I18 Mailto | ✅ übernommen | Ehrlicher als ein halbes Formular. |
| I19 Fonts lokal | ✅ übernommen | Datenschutz und kein Layout-Shift. |
| I20 Strukturierte Daten | ✅ übernommen | FAQ und LearningResource. |
| I21 Nummern + Zeiten | ✅ übernommen | Aus der geprüften Recherche. |
| I22 Fotos raus | ✅ übernommen | Das Netz ersetzt sie. Echte Fotos sind nur auf „Über uns“ vorgesehen. |
| I23 Ein Spiel | ✅ übernommen | 6 Runden plus geprüfte externe Spiele. |
| H1–H4 | ✅ | siehe oben |

😈 **Frankenstein-Check (VIKTOR):** Netz, Navigator und Rollen erzählen dieselbe Geschichte: *Niemand muss allein durch.* Das hält.
Rausgeflogen sind I12, ein zweites und drittes Eigenbau-Spiel und eine animierte Zahlenleiste („10.000 Downloads“), weil sie unbelegt und
Eitelkeit wären.

### Weggabelungen

| # | Gewählt | Verworfen | Begründung |
|---|---|---|---|
| W1 | **Netz-Grafik im Hero** | Die drei Fotos behalten | Die Fotos sind generisch. Das Netz trägt den Claim und lädt keine Bilder. |
| W2 | **Mehrseitig, statisch generiert** | Eine Single-Page mit JS-Router | Funktioniert ohne JS, ist SEO-fest und auf jedem Webspace hostbar. |
| W3 | **Akut-Navigator als Dialog** | Eigene Notfall-Seite als einziger Weg | Hilfe muss ohne Seitenwechsel erreichbar sein. Die Seite bleibt als Fallback. |
| W4 | **Kein Dark Mode** | Hell/Dunkel-Umschaltung | Doppelter Testaufwand ohne Nutzen für die Kernaufgabe. Kann später kommen. |

---

## BAUPLAN der Idealversion

**Name:** netzfest · **Leitidee:** *Erst auffangen, dann stärken. Die Seite hat zwei Geschwindigkeiten und knüpft ein Netz um alle, die online allein sind.*

### Erlebnis
Die Seite lädt, Schrift und Layout stehen sofort. Im Hero verbinden sich lose Punkte, sobald sich Maus oder Finger nähern. Oben rechts
liegt ruhig der Akut-Knopf. Direkt unter dem Claim stehen vier Rollen. Wer „Eltern“ wählt, sieht einen neuen Untertitel, die Elternnummer
rückt nach vorn und die Empfehlungen wechseln. Unter dem Hero folgt das Akut-Band „Gerade passiert etwas?“, das den Navigator öffnet.
Danach kommen Themen, Empfehlungen, die vier Erste-Hilfe-Schritte, Spiel, Hilfe und Footer.

### Sitemap
```
index.html
├─ materialien.html ─ material-<id>.html (18 Detailseiten)
├─ wissen.html (Überblick + Glossar + Fakes prüfen)
│   ├─ wissen-cybermobbing.html
│   ├─ wissen-hass.html
│   └─ wissen-fakenews.html
├─ spiele.html (Fake Detektiv + externe Spiele)
├─ kinder.html
├─ hilfe.html (Navigator, Nummern, Beweise sichern, Melden, FAQ)
├─ ueber-uns.html · sammlung.html
└─ impressum.html · datenschutz.html · barrierefreiheit.html · 404.html
```
**Nutzerflüsse:**
1. Akut: beliebige Seite → Akut-Knopf → 2 Fragen → Schritte + Nummer (tel-Link)
2. Lehrkraft: Startseite → Rolle → Bibliothek vorgefiltert → Detail mit Ablauf → Merken/Download
3. Eltern: Startseite → Rolle Eltern → Elterntelefon + „Wenn dein Kind betroffen ist“ → Wissen
4. Kind: Startseite → Kinderbereich → 116 111 / Spiel

### Abschnitte (Startseite)
1. **Kopfzeile:** Logo, Nav (6 Einträge), Merkliste mit Zähler, Rollen-Wahl, **Akut-Knopf** (Amber-Punkt). Mobil: Akut bleibt sichtbar, der Rest wandert ins Menü.
2. **Hero:** Canvas-Netz (aria-hidden), Eyebrow, Claim als Buchstaben-Welle, Untertitel je Rolle, Rollenkarten (Buttons, aria-pressed), CTA „Alle Materialien entdecken“.
3. **Akut-Band:** dunkles Band, Satz plus Button „Erste-Hilfe-Navigator öffnen“ plus 116 111 direkt.
4. **Themen:** 3 Karten mit Glyphe, Teaser und 2 Links (Verstehen / Material).
5. **Für dich:** 3 Materialkarten je Rolle (ohne Rolle: Auswahl der Redaktion).
6. **Erste Hilfe in 4 Schritten:** Ruhe → Sichern → Melden & Blockieren → Reden. Nummerierte Liste, keine Karten-Optik.
7. **Spiel + Hilfe:** zweispaltig (Fake Detektiv / Nummern mit Erreichbarkeit).
8. **Footer:** Navigation, Rechtliches, Stand der Hilfeangaben.

### Signature Moment – „Das Netz hält“
Canvas hinter dem Hero mit 40–90 Punkten (abhängig von der Fläche), die langsam driften. Im Radius von 160 px um Zeiger oder Finger
verbinden sie sich mit Linien (Sky, Deckkraft nach Abstand). Ist eine Rolle gewählt, wächst der Verbindungsradius dauerhaft um 25 %
(„das Netz wird enger“). **Fallback:** Bei `prefers-reduced-motion` oder ohne JS steht ein statisches, dezent verknüpftes SVG-Netz. Der Canvas pausiert außerhalb des Bildschirms.

### Design Tokens
| Token | Wert |
|---|---|
| `--ink` | #0F172A (Text, dunkle Flächen) |
| `--ink-2` | #334155 |
| `--muted` | #526072 (Fließtext sekundär, 6,3 : 1 auf Weiß) |
| `--line` | #E2E8F0 |
| `--paper` | #F7F9FC |
| `--white` | #FFFFFF |
| `--sky` | #0EA5E9 (nur Deko/Fokus) |
| `--sky-ink` | #0B6F9C (Links/Akzenttext, 5,6 : 1) |
| `--sky-soft` | #E6F4FC |
| `--amber` | #F59E0B (CTA-Fläche, Text darauf `--ink`) |
| `--amber-soft` | #FEF3C7 · `--amber-ink` #8A3B0B |
| `--kid-paper` | #FFF8EC |
| Typ-Farben | Einheit #0B6F9C · Arbeitsblatt #334155 · Video #A24806 · Podcast #6D28D9 · Artikel #146C34 · Workshop #0369A1 · Spiel #C2410C (in der QA nachgedunkelt) |

**Typo:** Plus Jakarta Sans Variable (lokal, 400–800), Fallback mit Metrik-Anpassung. Fluid-Skala:
`--t-sm` 0.875rem · `--t-base` 1–1.0625rem · `--t-lg` 1.125–1.25rem · `--t-xl` 1.375–1.75rem · `--t-2xl` 1.75–2.5rem · `--t-3xl` 2.25–3.5rem · `--t-hero` 2.6–5.5rem.
**Abstände:** 8-px-Raster `--s-1` 0.25rem … `--s-12` 6rem. **Radien:** 10 / 16 / 24 / 999 px.
**Motion:** `--dur-1` 160 ms, `--dur-2` 320 ms, `--dur-3` 700 ms, `--ease` cubic-bezier(.22,1,.36,1). Bei `prefers-reduced-motion`: keine Transforms, nur Opacity, kein Canvas-Lauf.

### Komponenten
Kopfzeile · Rollen-Wahl (Menü) · Akut-Knopf · Navigator-Dialog · Rollenkarte · Chip-Filter · Materialkarte (typografisch) ·
Merken-Knopf · Themenkarte · Schritt-Liste · Nummern-Liste · Randnotiz · Akkordeon (FAQ/Glossar) · Quiz · Breadcrumb · Footer

### Tech-Stack
HTML + CSS + Vanilla-JS (eine Datei, ~12 KB), ein Python-3-Generator (ohne Pakete) für Kopf, Fuß, Material- und Detailseiten.
Ausgabe: reine statische Dateien, auch per Doppelklick lauffähig. Hosting überall.

### Inhalte
- **Aus dem Briefing/der Recherche:** Rollen, Themen, Hilfenummern mit Erreichbarkeit (Stand 06.11.2026), Handlungstipps (klicksafe, JUUUPORT, HateAid, Handysektor, ichbinhier), Prüftipps (so geht MEDIEN, CORRECTIV, Saferinternet.at, Mimikama), externe Spiele (SWR Fakefinder, Bad News)
- **Vom Team getextet** (markiert mit `TEXT PRÜFEN`): Materialbeschreibungen und Abläufe, Wissenstexte, Rechtsüberblick, Glossar, Kinderbereich, Über uns
- **Vom Kunden zu liefern:** Material-Dateien (PDF), Trägerangaben für Impressum, Datenschutzerklärung, Logo final, OG-Bild, Fotos für „Über uns“, Domain

### Akzeptanzkriterien
1. Akut-Hilfe ist auf jeder Seite mit höchstens einem Klick bzw. Tipp erreichbar, auch mobil und ohne JavaScript.
2. Navigation, Rollenwahl, Filter, Navigator und Quiz sind vollständig per Tastatur bedienbar, mit sichtbarem Fokus.
3. Ohne JavaScript sind alle Inhalte (inkl. aller Materialien) lesbar und verlinkt.
4. Kein horizontales Scrollen von 320 px bis 2560 px.
5. Kein Layout-Shift durch Schriften (lokale Fonts mit Fallback-Metriken, `font-display: swap`).
6. `prefers-reduced-motion` schaltet Buchstaben-Welle, Canvas und Hover-Bewegungen ab.
7. Jede Seite hat eigenen Title, Meta-Description, Open Graph und genau eine H1. Strukturierte Daten auf Start, Hilfe und Materialdetail.
8. Textkontraste ≥ 4,5 : 1 (Fließtext) bzw. ≥ 3 : 1 (große Schrift, UI-Elemente).
9. Die Rollenwahl ändert sichtbar Untertitel, Empfehlungen und Bibliotheksfilter und bleibt beim Seitenwechsel erhalten.
10. Keine externen Requests beim Laden (keine CDN-Fonts, keine Tracker).

---

## Phase 5 – Umsetzung: Abweichungen vom Bauplan

💻 **ANTON:**
- **Rollenkarten bleiben auf der Startseite**, statt wie im Original in die Bibliothek zu springen. Sonst würde man die Anpassung (H3) nie sehen. Ein Live-Hinweis unter den Karten bestätigt den Wechsel.
- **Akut-Knopf unter 416 px nur „Hilfe“**, und die Merkliste wandert ins Menü. Bei 320 px war die Kopfzeile sonst 26 px zu breit.
- **Navigator ohne JS:** Auf `hilfe.html` steht eine statische Schritte-Liste. Der Akut-Knopf ist ein echter Link dorthin.
- **Netz-Deckkraft angehoben** (Linien 0,12 → 0,20), weil das Netz im ersten Test kaum zu sehen war.

## Phase 6 – Qualitätssicherung (😈 VIKTOR + 📈 FELIX)

Geprüft im Browser bei 320 / 375 / 768 / 1024 / 1280 / 1440 / 2560 px, per Tastatur und mit automatischen Checks.

| # | Kriterium | Status | Anmerkung |
|---|---|---|---|
| 1 | Akut-Hilfe überall mit 1 Klick, auch ohne JS | ✅ erfüllt | Knopf in jeder Kopfzeile. Ohne JS ein Link zu `hilfe.html#navigator` mit statischer Liste |
| 2 | Vollständig per Tastatur bedienbar | ✅ erfüllt | Skip-Link zuerst. Rollenmenü mit Pfeiltasten und Esc. Dialog mit Fokusfalle und Esc. Quiz setzt den Fokus auf Feedback und Ergebnis |
| 3 | Ohne JS alles lesbar | ✅ erfüllt | Alle 18 Karten vorgerendert. Filter, Merken und Quiz blenden sich ohne JS aus bzw. zeigen Hinweise |
| 4 | Kein horizontales Scrollen 320–2560 px | ✅ erfüllt | **Behoben:** Kopfzeile bei 320 px und Hilfe-Box auf der Startseite (lange Nummern) |
| 5 | Kein Layout-Shift durch Schriften | 🟡 teilweise | Lokale Schrift mit Preload und angepasstem Fallback. Die Metrikwerte sind geschätzt und nicht gemessen → mit Lighthouse/CLS prüfen |
| 6 | Reduzierte Bewegung | ✅ erfüllt | Canvas startet nicht, statisches SVG-Netz, Buchstaben sofort sichtbar, Transitions aus |
| 7 | Title, Description, OG, 1 × H1, strukturierte Daten | ✅ erfüllt | Automatisch geprüft: 33 Seiten mit je genau einer H1. JSON-LD auf Start, Hilfe (FAQPage) und allen Materialseiten. OG-Bild fehlt noch (BILD) |
| 8 | Kontraste | ✅ erfüllt | **Behoben:** Fokusring (2,8 → 5,6 : 1), Typfarben Video/Artikel (4,46 → 5,3/5,7 : 1), Text im Spiel-Kasten, Rahmen aktiver Chips |
| 9 | Rolle ändert Untertitel, Empfehlungen, Filter, bleibt erhalten | ✅ erfüllt | Getestet mit „Eltern“: Untertitel, 3 Karten, Kopfzeile und Bibliotheksfilter `?fuer=eltern` |
| 10 | Keine externen Requests | ✅ erfüllt | Netzwerkprotokoll: nur eigene Dateien |

**Weitere behobene Fehler:** Die Bibliothek zeigte bei 1280 px nur 2 breite Spalten (→ 3). Neben 3 Empfehlungskarten blieb eine leere 4. Spalte. Mobil fehlte im Filter der Weg zurück zu den Ergebnissen (→ „X Ergebnisse anzeigen“). Das Netz blieb leer, wenn der Tab im Hintergrund startete (→ erstes Bild wird sofort gezeichnet).
**Automatisch geprüft:** keine doppelten IDs, keine toten internen Links oder Anker.

**Nicht geprüft:** echter Screenreader-Durchlauf (VoiceOver/NVDA), Safari/iOS, Firefox, Lighthouse-Messung.

### Stellen, an denen Inhalte oder Bilder ersetzt werden müssen
- `_werkstatt/materialien.json` – alle 18 Materialien sind Demo-Inhalte. Die PDF-Dateien fehlen (`DATEI:` auf jeder Materialseite)
- `bauen.py` → `BASE_URL` (Domain), `og:image` (`BILD:` 1200 × 630 px in `assets/img/og.jpg`)
- `ueber-uns.html` – Trägertext, Teamfoto (`BILD:` 4:3), Kontaktadresse
- `impressum.html`, `datenschutz.html`, `barrierefreiheit.html` – Gerüste mit `[Klammern]`
- `wissen*.html` – Rechtsüberblick juristisch gegenlesen lassen (`TEXT PRÜFEN`)
- `hilfe.html` – Links zu jugendschutz.net und Internet-Beschwerdestelle sind nicht in der Recherche geprüft
- `kinder.html` – Sprache mit Kindern testen

## Phase 7 – Übergabe (🎯 MARA)

**Was die Seite besonders macht:** netzfest hat jetzt zwei Geschwindigkeiten. Wer akut verletzt ist, erreicht von jeder Seite aus mit einem
Klick einen Plan mit der passenden Nummer und Uhrzeit. Wer etwas vorbereitet, filtert in Sekunden eine Stunde mit Ablaufplan heraus. Das
Netz im Hero macht aus dem Claim ein Bild, das man berühren kann, und die Rollenwahl verändert jetzt wirklich, was man sieht.

**Was du noch tun musst:**
1. Material-PDFs erstellen und `DATEI:`-Stellen verlinken
2. Träger, Impressum und Datenschutz ausfüllen und rechtlich prüfen lassen
3. Domain eintragen, OG-Bild gestalten, Teamfoto liefern
4. Hilfenummern vor dem Livegang erneut prüfen (Stand 06.11.2026)
5. Hosting wählen. Ein Formular-Backend ist nicht nötig, Kontakt läuft per Mail

**Lernchance:** **Progressive Enhancement mit `hidden` und `data-`-Attributen.** Das HTML ist vollständig, und JavaScript blendet nur
um (Rollen, Filter, Navigator). Schau dir `applyRole()` und `matches()` in `app.js` an. Das Muster trägt auch große Projekte ohne Framework.

**Ausbaustufen:**
1. **Material-Downloads mit Vorschau:** PDF-Thumbnails und eine Druckansicht der Abläufe (`@media print` ist vorbereitet)
2. **Headless CMS** (z. B. Decap CMS auf Netlify), damit Redakteur:innen Materialien ohne JSON pflegen. `bauen.py` bleibt der Generator
3. **Navigator 2.0:** Bundesland wählen → regionale Beratungsstellen und die Internetwache der passenden Landespolizei

> Am stärksten würde die Angabe **„Wer pflegt die Seite später?“** die nächste Runde verbessern. Davon hängt ab, ob JSON + Generator reicht oder ein CMS nötig ist.
