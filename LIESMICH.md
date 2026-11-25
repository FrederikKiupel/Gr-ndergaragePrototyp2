# netzfest – statische Website (HTML · CSS · JS)

Konzept, Fusion und Bauplan: [BAUPLAN.md](BAUPLAN.md)

## Ansehen
- **Per Doppelklick:** `index.html` öffnen – es braucht keinen Server. Firefox und Safari geben Dateien (`file://`) keinen gemeinsamen Speicher. Darum reichen interne Links Merkliste und Ansicht dann in der Adresse weiter (`?nf=…`, wird sofort wieder entfernt). Über Links funktioniert so alles. Wer eine Adresse von Hand eintippt oder ein Lesezeichen nutzt, startet aber mit leerer Merkliste.
- **Mit lokalem Server** (empfohlen): im Ordner `Website 2/netzfest-html` ausführen
  `python3 -m http.server 8766` → http://localhost:8766

## Inhalte ändern

| Was | Wo |
|---|---|
| Materialien (Titel, Ablauf, Lernziele …) | `_werkstatt/materialien.json` |
| Texte der Seiten | `_werkstatt/seiten/*.html` (oben im Kommentar: Titel, Beschreibung, aktiver Menüpunkt) |
| Kopf, Navigation, Fuß, Hilfenummern, Domain | `_werkstatt/bauen.py` (Abschnitt „Einstellungen“ und `HILFE`) |
| Navigator-Texte, Quizfragen | `assets/js/app.js` (Abschnitte 4 und 8) |
| Farben, Schrift, Abstände (Design Tokens) | `assets/css/styles.css`, Abschnitt 2 |

Danach im Ordner `Website 2/netzfest-html` ausführen:

```
python3 _werkstatt/bauen.py
```

Das Skript erzeugt alle `*.html` im Hauptordner, `assets/js/daten.js`, `sitemap.xml` und `robots.txt` neu.
**Die erzeugten Dateien nicht direkt bearbeiten** – sonst sind die Änderungen beim nächsten Lauf weg.

### Platzhalter in Seiten
`{{ICON:name}}` fügt ein Icon ein (Namen siehe `_P` in `bauen.py`). Weitere Bausteine wie `{{BIBLIOTHEK}}`,
`{{HILFEKARTEN}}` oder `{{NUMMERN_KURZ}}` stehen in `main()` unter `snippets`.

### Rollenabhängige Inhalte
Ein Element mit `data-fuer="eltern"` (und `hidden`) erscheint nur, wenn „Eltern“ gewählt ist.
`data-fuer="alle"` ist der Inhalt ohne Rollenwahl. Mehrere Rollen mit Leerzeichen trennen.

## Material aus NETZKLAR (Website 1)
27 Materialien stammen aus Website 1: Unterrichtsstunden, Gesprächsleitfäden für Eltern, Beratungsbausteine und Selbstlern-Einheiten. Sie stehen in `_werkstatt/materialien.json` mit `"herkunft": "netzklar"` und haben zusätzlich Hintergrund, Tipps, Arbeitsmaterial (teils in Altersfassungen), Anpassung und Weiterlesen-Links.
Website 1 wird dabei nur gelesen. Hat sich dort etwas geändert, holt `python3 _werkstatt/uebernahme_netzklar.py` den neuen Stand (ersetzt nur die übernommenen Einträge), danach `python3 _werkstatt/bauen.py`. Im Wissen (Glossar, Rechtslage, Hass, Fake News) sind ergänzende Inhalte aus Website 1 direkt in den Seitenvorlagen eingearbeitet.

## Material aus der Recherche
37 weitere Materialien (`"herkunft": "recherche-2026-11"`) kommen aus `../../Recherche-2026-11/`. Jedes baut auf einem externen Angebot auf. Die Detailseite zeigt darum statt des Download-Platzhalters den Knopf „Zum Material bei …“ und den Hinweis „Grundlage: …“. Neue Typen: Gesprächsleitfaden, Beratungsbaustein, Selbstlern-Einheit. Änderungen bitte in den Recherche-Dateien machen und `einbau.py` ausführen (siehe LIESMICH im Hauptordner).

## Fotos
15 Stockfotos von Unsplash (Unsplash-Lizenz: kostenlos, auch kommerziell; Namensnennung freiwillig, steht trotzdem im Impressum). Sie liegen in `assets/img/fotos/` als `<name>-800` und `<name>-1600`, jeweils als `.webp` und `.jpg` im Format 3:2. Dazu kommt `assets/img/og.jpg` (1200 × 630) als Vorschaubild beim Teilen.

| Name | Wo | Foto |
|---|---|---|
| `cybermobbing`, `hass`, `fakenews` | Themenkarten auf der Startseite, Kopf der drei Wissensseiten | Vullnet Ademaj, Kev Costello, Houcine Ncib |
| `hilfe` | Kopf der Hilfe-Seite, Vorschaubild `og.jpg` | Priscilla Du Preez |
| `spiele` | Kopf der Spiele-Seite | Hiki App |
| `wissen` | Kopf der Wissen-Übersicht | Taylor Flowe |
| `rolle-schueler`, `rolle-eltern`, `rolle-lehrkraefte`, `rolle-fachkraefte` | Rollenkarten auf der Startseite (erst ab 576 px Breite) | Tim Mossholder, Vitaly Gariev, Vitaly Gariev, Vitaly Gariev |
| `gespraech`, `gegenrede`, `recherche` | Im Text der Wissensseiten: „Was tun?“, „Gegenrede, die wirkt“, „Die Prüfliste“ | Timur Shakerzianov, Taylor Flowe, Annie Spratt |
| `beweise` | Hilfe-Seite, Abschnitt „Beweise sichern“ | Paul Hanaoka |
| `gruppenarbeit` | Kopf der Materialien-Seite | Yegor Makarenko |

Einsetzen in einer Seitenvorlage: `{{FOTO:name}}` in Karten, `{{FOTO:name:kopf}}` im Seitenkopf, `{{FOTO:name:text}}` im Fließtext. Alle Fotos laden verzögert. Neue Fotos in `FOTOS` in `_werkstatt/bauen.py` eintragen: Alt-Text, Fotograf:in, Link. Der Bildnachweis im Impressum entsteht daraus automatisch. Im Seitenkopf erscheinen Fotos erst ab 640 px Breite, damit auf dem Handy der Inhalt zuerst kommt. Auswahlregel: Personen im Alter der Zielgruppe (Schüler:innen 10–18) und ein Umfeld, das zu Schulen und Familien im DACH-Raum passt, mit realistischer Vielfalt. Auf der Seite „Über uns“ bleibt der Platzhalter: Dort gehört ein echtes Teamfoto hin, kein Stockfoto.

## Gestaltung und Bedienung
- **Farben:** Yale Blue `#033F63`, Stormy Teal `#28666E`, Muted Teal `#7C9885`, Dry Sage `#B5B682`, Soft Peach `#FEDC97` (Tokens in `assets/css/styles.css`, Abschnitt 1). Text nur in Yale Blue, Stormy Teal und Dunkelgrau; Muted Teal und Dry Sage nur für Flächen und Linien.
- **Raster:** alle Abstände, Höhen und Zeilenhöhen in Schritten von 8 px. Prüfen: eine Seite mit `?raster` öffnen, z. B. `index.html?raster`.
- **Typografie:** eine Grotesk aus dem System (Helvetica Neue, sonst Arial), linksbündig, sechs feste Größen. Keine Eyebrows über Überschriften – jede Seite hat eine H1, jeder Abschnitt eine H2.
- **Schüler:innen:** Den früheren Kinderbereich gibt es nicht mehr als eigene Seite. Seine Inhalte erscheinen auf Start- und Materialseite direkt nach der Auswahl „Schüler:innen“ (`schueler_zuerst()` in `bauen.py`). `kinder.html` leitet auf `index.html?rolle=schueler` weiter.
- **Ansicht per Link:** `?rolle=schueler`, `eltern`, `lehrkraefte` oder `fachkraefte` stellt die Ansicht direkt ein.

## Offene Stellen finden
Im Code suchen nach:
- `TEXT PRÜFEN` – Demo-Texte und Angaben, die fachlich oder rechtlich geprüft werden müssen
- `DATEI:` – fehlende Material-Downloads (PDF)
- `BILD:` – fehlende Bilder (Open-Graph-Bild, Teamfoto)
- `DOMAIN PRÜFEN` – echte Domain in `bauen.py` eintragen
- `[eckige Klammern]` – Angaben in Impressum, Datenschutz, Barrierefreiheit, Über uns

Hilfenummern und Erreichbarkeiten: Stand 06.11.2026 (aus `Website 1/inhalte/recherche/`). Vor Veröffentlichung und danach regelmäßig erneut prüfen.

## Veröffentlichen

### GitHub Pages (für Nutzertests)
Die Seite ist fertig gebaut und läuft ohne Server-Technik, auf jedem Rechner und in jedem Unterordner. Alle Links sind relativ, es gibt keine externen Skripte oder Schriften. `.nojekyll` und `404.html` sind vorhanden.

1. Auf github.com ein **neues, öffentliches** Repository anlegen, z. B. `netzfest`, ohne README.
2. Den **Inhalt dieses Ordners** hochladen, also `index.html` direkt in der obersten Ebene. Die Weboberfläche von GitHub nimmt nur 100 Dateien auf einmal, darum entweder **GitHub Desktop** („Add existing repository“ → diesen Ordner wählen → Publish) oder im Terminal:
   ```
   cd "…/Website 2/netzfest-html"
   git init -b main
   git add .
   git commit -m "netzfest für Nutzertests"
   git remote add origin https://github.com/NAME/netzfest.git
   git push -u origin main
   ```
3. Im Repository: **Settings → Pages → Build and deployment → Source: „Deploy from a branch“, Branch `main`, Ordner `/ (root)`** → Save.
4. Nach ein bis zwei Minuten läuft die Seite unter `https://NAME.github.io/netzfest/`.
5. Optional, für Vorschaubilder beim Teilen des Links: in `_werkstatt/bauen.py` `BASE_URL = "https://NAME.github.io/netzfest"` eintragen, `python3 _werkstatt/bauen.py` ausführen und erneut hochladen.

**Testbetrieb:** `TESTBETRIEB = True` in `_werkstatt/bauen.py` hält die Seite aus Suchmaschinen heraus (noindex). Das passt, solange Impressum und Datenschutz noch Platzhalter sind. Für den echten Start auf `False` setzen und neu bauen.

Was im Repository mit hochgeladen wird, aber nicht verlinkt ist: `_werkstatt/` (Generator und Daten), `BAUPLAN.md`, `LIESMICH.md`. Das ist unschädlich, alles ist im öffentlichen Repository aber lesbar.

Die Merkliste speichert pro Browser. Auf `name.github.io` teilen sich beide Websites zwar die Adresse, sie nutzen aber verschiedene Speicher-Schlüssel und kommen sich nicht in die Quere.

### Andere Anbieter
Netlify, Uberspace oder ein eigener Webspace: den Ordner hochladen und `404.html` als Fehlerseite einstellen.
