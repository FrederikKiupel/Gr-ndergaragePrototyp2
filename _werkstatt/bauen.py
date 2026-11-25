#!/usr/bin/env python3
"""
netzfest – Seitengenerator
==========================
Baut aus  _werkstatt/seiten/*.html  (Seiteninhalte)
und       _werkstatt/materialien.json  (Materialbibliothek)
alle fertigen HTML-Dateien im Hauptordner neu, dazu assets/js/daten.js und sitemap.xml.

Aufruf im Ordner netzfest-html:   python3 _werkstatt/bauen.py

Die erzeugten *.html im Hauptordner NICHT direkt bearbeiten – Änderungen gehen beim nächsten Lauf verloren.
Kopf, Navigation, Fuß, Hilfenummern und Materialkarten stehen in dieser Datei.
"""
import html
import json
import math
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WERK = ROOT / "_werkstatt"

# ------------------------------------------------------------------ Einstellungen
# Adresse der veröffentlichten Website OHNE / am Ende, z. B. "https://NAME.github.io/netzfest".
# Leer lassen, solange sie nicht feststeht: Dann entfallen Canonical, og:url, og:image und Sitemap –
# alle Links bleiben relativ und die Seite läuft auf jedem Server und in jedem Unterordner.
BASE_URL = ""
# Testbetrieb (Nutzertests): Suchmaschinen sollen die Seite nicht aufnehmen. Für den echten Start auf False setzen.
TESTBETRIEB = True
SITE = "netzfest"
STAND_HILFE = "06.11.2026"  # Datum der letzten Prüfung der Hilfenummern

NAV = [
    ("materialien.html", "Materialien", "materialien"),
    ("spiele.html", "Spiele", "spiele"),
    ("wissen.html", "Wissen", "wissen"),
    ("hilfe.html", "Hilfe", "hilfe"),
    ("ueber-uns.html", "Über uns", "ueber-uns"),
]

ROLLEN = [
    ("schueler", "Schüler:innen", "Schüler:innen", "cap", "Spiele, Infos und Hilfe, wenn es online gerade wehtut."),
    ("eltern", "Eltern", "Eltern", "heart", "Dein Kind ist betroffen? So kannst du ruhig reagieren."),
    ("lehrkraefte", "Lehrkräfte", "Lehrkräfte", "book", "Fertige Unterrichtsideen von 15 bis 90 Minuten."),
    ("fachkraefte", "Soziale Arbeit & Psychologie", "Fachkräfte", "compass", "Hintergrundwissen und Material für Beratung und Prävention."),
]

THEMEN = {
    "cybermobbing": ("Cybermobbing", "wissen-cybermobbing.html", "chat"),
    "hass": ("Hass & Beleidigung im Netz", "wissen-hass.html", "megaphone"),
    "fakenews": ("Fake News & Desinformation", "wissen-fakenews.html", "magnifier"),
}
TYPEN = {
    "unterrichtseinheit": "Unterrichtseinheit", "arbeitsblatt": "Arbeitsblatt", "video": "Video",
    "podcast": "Podcast", "artikel": "Artikel", "workshop": "Workshop", "spiel": "Spiel",
    "leitfaden": "Gesprächsleitfaden", "baustein": "Beratungsbaustein", "selbstlernen": "Selbstlern-Einheit",
}
NIVEAUS = {"einstieg": "Einstieg", "basis": "Basiswissen", "vertiefung": "Vertiefung"}
ZIELGRUPPEN = {"schueler": "Schüler:innen", "eltern": "Eltern", "lehrkraefte": "Lehrkräfte", "fachkraefte": "Fachkräfte"}
SCHULARTEN = {"grundschule": "Grundschule", "sek1": "Sek I", "sek2": "Sek II", "berufsschule": "Berufsschule", "foerderschule": "Förderschule"}
ALTER = [("10-12", "10–12 J."), ("12-14", "12–14 J."), ("14-16", "14–16 J."), ("16-18", "16–18 J.")]
ZEIT = [("15", "bis 15 Min."), ("45", "bis 45 Min."), ("90", "bis 90 Min.")]

# Hilfenummern – Quelle: inhalte/recherche/recherche-a.json (Abruf 06.11.2026). Vor Veröffentlichung erneut prüfen.
HILFE = [
    {"id": "kjt", "name": "Nummer gegen Kummer – Kinder- und Jugendtelefon", "kurz": "Nummer gegen Kummer",
     "tel": "116 111", "fuer": "Kinder und Jugendliche",
     "wann": "Mo–Sa 14–20 Uhr · kostenlos, anonym, erscheint nicht auf der Telefonrechnung. Samstags beraten Jugendliche Jugendliche.",
     "url": "https://www.nummergegenkummer.de/kinder-und-jugendberatung/"},
    {"id": "eltern", "name": "Nummer gegen Kummer – Elterntelefon", "kurz": "Elterntelefon",
     "tel": "0800 111 0 550", "fuer": "Eltern und Bezugspersonen",
     "wann": "Mo, Mi, Fr 9–17 Uhr · Di, Do 9–19 Uhr · kostenlos und anonym",
     "url": "https://www.nummergegenkummer.de/elternberatung/"},
    {"id": "online", "name": "Nummer gegen Kummer – Online-Beratung", "kurz": "Chat & Mail",
     "tel": "", "fuer": "Kinder, Jugendliche, junge Erwachsene",
     "wann": "Mail jederzeit (Antwort meist innerhalb von 2 Tagen) · Chat Mo–Do 14–20 Uhr · anonym mit Benutzername",
     "url": "https://www.nummergegenkummer.de/kinder-und-jugendberatung/faq-online-beratung/"},
    {"id": "juuuport", "name": "JUUUPORT – Beratung durch junge Scouts", "kurz": "JUUUPORT",
     "tel": "", "fuer": "Jugendliche und junge Erwachsene",
     "wann": "Frage jederzeit online stellen · Antwort innerhalb von 48 Stunden · kostenlos, vertraulich, ohne echten Namen",
     "url": "https://beratung.juuuport.de/"},
    {"id": "cmh", "name": "Cybermobbing-Hilfe e. V. – Peer-Beratung", "kurz": "Cybermobbing-Hilfe",
     "tel": "", "fuer": "Kinder und Jugendliche",
     "wann": "Schreiben rund um die Uhr · Antwort in der Regel innerhalb von 24 Stunden",
     "url": "https://www.cybermobbing-hilfe.de/"},
    {"id": "hateaid", "name": "HateAid – Betroffenenberatung", "kurz": "HateAid",
     "tel": "030 252 088 38", "fuer": "Betroffene digitaler Gewalt",
     "wann": "Telefonsprechstunde Mo 10–13 Uhr, Do 15–18 Uhr · kostenlos, vertraulich, Erstkontakt anonym möglich",
     "url": "https://hateaid.org/betroffenenberatung/"},
    {"id": "seelsorge", "name": "TelefonSeelsorge", "kurz": "TelefonSeelsorge",
     "tel": "0800 111 0 111", "fuer": "Menschen in seelischen Krisen",
     "wann": "Auch 0800 111 0 222 oder 116 123 · kostenlos",
     "url": "https://hateaid.org/ratgeber/"},
    {"id": "notruf", "name": "Polizei-Notruf", "kurz": "Notruf",
     "tel": "110", "fuer": "Akute Bedrohung oder Gefahr",
     "wann": "Rund um die Uhr · bei Lebensgefahr 112",
     "url": ""},
]

# ------------------------------------------------------------------ Icons (eigene, einfache Linien-Icons)
_P = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "shield": '<path d="M12 3l7 2.8v5.4c0 4.4-3 8.1-7 9.8-4-1.7-7-5.4-7-9.8V5.8z"/><path d="M8.8 12.2l2.3 2.3 4.2-4.4"/>',
    "cap": '<path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.5v4c1.5 1.6 3.4 2.4 5.5 2.4s4-.8 5.5-2.4v-4"/><path d="M21.5 9.5v5"/>',
    "heart": '<path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.4a4.3 4.3 0 0 1 7.5 2.4C19.5 15.4 12 20 12 20z"/><path d="M9 12.5l2 2 4-4"/>',
    "book": '<path d="M3.5 5.5c2.8-.9 5.6-.6 8.5 1.1 2.9-1.7 5.7-2 8.5-1.1v13c-2.8-.9-5.6-.6-8.5 1.1-2.9-1.7-5.7-2-8.5-1.1z"/><path d="M12 6.6v13"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "bookmark": '<path d="M6.5 3.5h11v17L12 16.6l-5.5 3.9z"/>',
    "bookmark-on": '<path d="M6.5 3.5h11v17L12 16.6l-5.5 3.9z" fill="currentColor"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "phone": '<path d="M5 3.5h3.2l1.6 4.2-2.2 1.5a11.5 11.5 0 0 0 7.2 7.2l1.5-2.2 4.2 1.6V19a1.6 1.6 0 0 1-1.7 1.6C10.4 20.1 3.9 13.6 3.4 5.2A1.6 1.6 0 0 1 5 3.5z"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
    "sliders": '<path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/>',
    "chat": '<path d="M4 5.5h16v10H9.5L5 19.5v-4H4z"/><path d="M12 8.5v3M12 13.5v.01"/>',
    "megaphone": '<path d="M3.5 10v4h3l8 4.5v-13l-8 4.5z"/><path d="M18 9a4 4 0 0 1 0 6"/><path d="M7 14.5l1.2 5h2.3"/>',
    "magnifier": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/><path d="M8 10.5l1.8 1.8 3.2-3.3"/>',
    "sparkles": '<path d="M12 3.5l1.8 4.7 4.7 1.8-4.7 1.8L12 16.5l-1.8-4.7L5.5 10l4.7-1.8z"/><path d="M18.5 15.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
    "game": '<rect x="2.5" y="7" width="19" height="11" rx="4"/><path d="M7 10.5v4M5 12.5h4"/><path d="M15.5 11.5h.01M18 13.5h.01"/>',
    "download": '<path d="M12 4v11M7 10.5l5 5 5-5"/><path d="M4.5 19.5h15"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "list": '<path d="M9 6.5h11M9 12h11M9 17.5h11"/><path d="M4 6.5l1 1 2-2M4 12l1 1 2-2M4 17.5l1 1 2-2"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "users": '<circle cx="9" cy="8.5" r="3.5"/><path d="M2.5 19.5c.6-3.5 3.2-5.5 6.5-5.5s5.9 2 6.5 5.5"/><path d="M16 5.2a3.5 3.5 0 0 1 0 6.6M18 14.4c1.9.8 3.1 2.6 3.5 5.1"/>',
    "life": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.5"/><path d="M6 6l3.5 3.5M14.5 14.5L18 18M18 6l-3.5 3.5M9.5 14.5L6 18"/>',
    "camera": '<path d="M4 7.5h3.5l1.5-2.5h6l1.5 2.5H20v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "ban": '<circle cx="12" cy="12" r="8.5"/><path d="M6 6l12 12"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "hand": '<path d="M8 12V6a1.5 1.5 0 0 1 3 0v5M11 11V4.5a1.5 1.5 0 0 1 3 0V11M14 11V6a1.5 1.5 0 0 1 3 0v7c0 4-2.5 7-6.5 7-2.6 0-4.3-1.3-5.6-3.4L3 13.4a1.5 1.5 0 0 1 2.4-1.8L8 14"/>',
    "scale": '<path d="M12 4v16M7.5 20h9M5 7h14"/><path d="M5 7l-2.5 6a3 3 0 0 0 5 0zM19 7l-2.5 6a3 3 0 0 0 5 0z"/>',
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.5v.01"/>',
    "external": '<path d="M14 4.5h5.5V10M19.5 4.5L11 13"/><path d="M18 14v5.5H4.5V6H10"/>',
    "smile": '<circle cx="12" cy="12" r="8.5"/><path d="M8.5 14c.9 1.3 2 2 3.5 2s2.6-.7 3.5-2M9 9.5h.01M15 9.5h.01"/>',
    "image": '<rect x="3.5" y="5" width="17" height="14" rx="2"/><circle cx="9" cy="10" r="1.7"/><path d="M20.5 16l-5-5-8 8"/>',
    "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="M4 7l8 6 8-6"/>',
    "flag": '<path d="M5 21V4M5 4.5h11l-2 4 2 4H5"/>',
}


def icon(name, cls="", label=None):
    a11y = f'role="img" aria-label="{esc(label)}"' if label else 'aria-hidden="true"'
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" {a11y} focusable="false">{_P[name]}</svg>')


def esc(s):
    return html.escape(str(s), quote=True)


CTA_ARROW = ('<svg viewBox="0 0 17.4 17.4" fill="none" aria-hidden="true" focusable="false">'
             '<path d="M11.35 1.52l2.76 3.16c1.87 2.15 1.87 5.63 0 7.78l-2.76 3.16" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>'
             '<path d="M15.5 8.63H1.07" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>')


def cta(href, label):
    return (f'<a class="cta" href="{href}"><span class="cta__label">{label}</span>'
            f'<span class="cta__arrow" aria-hidden="true">{CTA_ARROW}</span></a>')


def tel_href(t):
    return "tel:" + re.sub(r"[^\d+]", "", t)


# ------------------------------------------------------------------ Materialien
def dauer_parts(m):
    d = m["dauer"]
    if d >= 120 and d % 60 == 0:
        return str(d // 60), "Std."
    return str(d), "Min."


def dauer_text(d):
    if d < 60:
        return f"{d} Min."
    h, r = divmod(d, 60)
    return f"{h} Std. {r} Min." if r else f"{h} Std."


def alter_text(m):
    return f'{m["alter_min"]}–{m["alter_max"]} J.' if m.get("alter_min") else "alle Altersstufen"


def save_btn(mid, with_label=False):
    label = '<span class="lbl">Merken</span>' if with_label else '<span class="sr-only">Merken</span>'
    return (f'<button type="button" class="save-btn" data-save="{esc(mid)}" aria-pressed="false" title="Zur Merkliste hinzufügen">'
            f'{icon("bookmark", "off")}{icon("bookmark-on", "on")}{label}</button>')


def material_card(m, heading="h3"):
    zahl, einheit = dauer_parts(m)
    thema_label, _, glyph = THEMEN[m["thema"]]
    search_text = (m["titel"] + " " + m["kurz"]).lower()
    alter = f'{m["alter_min"]}-{m["alter_max"]}' if m.get("alter_min") else ""
    return f'''<article class="mcard" data-id="{esc(m["id"])}" data-typ="{m["typ"]}" data-thema="{m["thema"]}" data-zielgruppe="{" ".join(m["fuer"])}" data-niveau="{m["niveau"]}" data-schule="{" ".join(m["schularten"])}" data-alter="{alter}" data-dauer="{m["dauer"]}" data-text="{esc(search_text)}">
  <div class="mcard__top">
    <div><p class="mcard__typ">{TYPEN[m["typ"]]}</p><p class="mcard__dauer">{zahl}<small>{einheit}</small></p></div>
    {icon(glyph, "mcard__glyph")}
  </div>
  <div class="mcard__save">{save_btn(m["id"])}</div>
  <div class="mcard__body">
    <{heading} class="mcard__title"><a href="material-{m["id"]}.html">{esc(m["titel"])}</a></{heading}>
    <p class="mcard__summary">{esc(m["kurz"])}</p>
    <p class="mcard__meta"><span class="tag">{thema_label}</span><span class="tag">{alter_text(m)}</span><span class="tag">{NIVEAUS[m["niveau"]]}</span></p>
  </div>
</article>'''


def chips(group, options):
    return "".join(f'<button type="button" class="chip" data-filter="{group}" data-value="{k}" aria-pressed="false">{esc(v)}</button>' for k, v in options)


def library_html(materials):
    haupt = [
        ("fuer", "Für wen?", list(ZIELGRUPPEN.items())),
        ("thema", "Welches Thema?", [(k, v[0]) for k, v in THEMEN.items()]),
        ("zeit", "Wie viel Zeit hast du?", ZEIT),
    ]
    weitere = [
        ("alter", "Alter", ALTER),
        ("schule", "Schulart", list(SCHULARTEN.items())),
        ("niveau", "Wissensstand", list(NIVEAUS.items())),
    ]
    fs = lambda gs: "\n".join(
        f'<fieldset><legend>{label}</legend><div class="chips">{chips(key, opts)}</div></fieldset>' for key, label, opts in gs)
    fieldsets = (fs(haupt) + '\n<details class="filters__more" data-more-filters><summary>Weitere Filter: Alter, Schulart, Wissensstand</summary>'
                 + fs(weitere) + "</details>")
    cards = "\n".join(material_card(m) for m in materials)
    return f'''<div class="wrap wrap--wide library" data-library>
  <aside class="filters" id="filter-panel" aria-labelledby="filter-title">
    <div class="filters__head">
      <div><h2 id="filter-title">Filter</h2><p class="filters__count" data-count aria-live="polite">{len(materials)} Materialien</p></div>
      <button type="button" class="text-btn" data-reset>Zurücksetzen</button>
    </div>
    {fieldsets}
    <button type="button" class="btn btn--ink btn--lg filter-done" data-filter-done>Ergebnisse anzeigen</button>
  </aside>
  <div>
    <div class="library__tools">
      <label class="search"><span class="sr-only">Materialien durchsuchen</span>{icon("search")}<input type="search" data-search placeholder="Titel oder Stichwort suchen …" autocomplete="off"></label>
      <button type="button" class="btn btn--ghost filter-toggle" data-filter-toggle aria-expanded="false" aria-controls="filter-panel">{icon("sliders")} Filter <span data-active-count></span></button>
    </div>
    <div class="cards" data-cards>
{cards}
    </div>
    <div class="empty" data-empty hidden>
      <h2>Nichts gefunden</h2>
      <p>Mit dieser Kombination passt kein Material. Nimm einen Filter heraus oder setze alles zurück.</p>
      <p style="margin-top:1.25rem"><button type="button" class="btn btn--ink" data-reset>Filter zurücksetzen</button></p>
    </div>
  </div>
</div>'''


def startseite_picks(materials):
    """Je Rolle (und 'alle') die ersten drei Materialien mit passendem 'startseite'-Eintrag."""
    picks = {}
    for key in ["alle"] + [r[0] for r in ROLLEN]:
        picks[key] = [m["id"] for m in materials if key in m.get("startseite", [])][:3]
    out = []
    for m in materials:
        roles = [k for k, ids in picks.items() if m["id"] in ids]
        if roles:
            hidden = "" if "alle" in roles else " hidden"
            out.append(f'<div class="card-slot" data-fuer="{" ".join(roles)}"{hidden}>{material_card(m)}</div>')
    return "\n".join(out)


def _quelle(x):
    return f' <span class="source">· <a href="{esc(x["url"])}" rel="noopener">{esc(x["quelle"])}</a></span>' if x.get("url") else ""


def _punkte(punkte):
    if not punkte:
        return ""
    if isinstance(punkte[0], dict):
        dp = lambda t: t if t.rstrip()[-1:] in "?!:" else t + ":"
        return "<ul>" + "".join(f"<li><strong>{esc(dp(x['titel']))}</strong> {esc(x['text'])}</li>" for x in punkte) + "</ul>"
    return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in punkte) + "</ul>"


def zusatz_panels(m):
    """Zusätzliche Inhalte (aus der NETZKLAR-Übernahme): Hintergrund, Tipps, Arbeitsmaterial, Anpassung, Weiterlesen.
    Jeder Block ist ein Panel mit genau einer Überschrift – keine Unterüberschriften-Kaskade."""
    vorne, hinten = [], []
    if m.get("hintergrund"):
        li = "".join(f"<li>{esc(h['text'])}{_quelle(h)}</li>" for h in m["hintergrund"])
        vorne.append(f'<section class="panel"><h2>{icon("info")} Hintergrund</h2><ul>{li}</ul></section>')
    if m.get("tipps"):
        li = "".join(f"<li>{('<strong>' + esc(t['fuer']) + ':</strong> ') if t.get('fuer') else ''}{esc(t['text'])}{_quelle(t)}</li>" for t in m["tipps"])
        vorne.append(f'<section class="panel"><h2>{icon("sparkles")} Tipps</h2><ul>{li}</ul></section>')
    if m.get("arbeitsmaterial"):
        teile = []
        for a in m["arbeitsmaterial"]:
            body = (f'<p class="muted">{esc(a["hinweis"])}</p>' if a.get("hinweis") else "") + _punkte(a.get("punkte"))
            for f in a.get("fassungen", []):
                body += f"<p><strong>Fassung {esc(f['fuer'])}</strong></p>" + _punkte(f["punkte"])
            teile.append(f"<details><summary>{esc(a['titel'])}</summary><div class=\"acc-body\">{body}</div></details>")
        vorne.append(f'<section class="panel"><h2>{icon("book")} Arbeitsmaterial</h2><div class="accordion" style="margin-top:1rem">{"".join(teile)}</div></section>')
    if m.get("anpassung"):
        li = "".join(f"<li><strong>{esc(a['label'])}:</strong> {esc(a['text'])}</li>" for a in m["anpassung"])
        vorne.append(f'<section class="panel"><h2>{icon("users")} An die Gruppe anpassen</h2><ul>{li}</ul></section>')
    if m.get("weiterlesen"):
        li = "".join(f'<li><a href="{esc(w["url"])}" rel="noopener">{esc(w["titel"])}</a> <span class="source">· {esc(w["quelle"])}</span>'
                     + (f'<br><span class="muted small">{esc(w["kurz"])}</span>' if w.get("kurz") else "") + "</li>" for w in m["weiterlesen"])
        hinten.append(f'<section class="panel"><h2>{icon("external")} Weiterlesen</h2><ul>{li}</ul><p class="source">Externe Seiten anderer Anbieter. <!-- TEXT PRÜFEN: Links vor Veröffentlichung erneut prüfen --></p></section>')
    return "\n    ".join(vorne), "\n    ".join(hinten)


def detail_page(m, materials):
    thema_label, thema_url, _ = THEMEN[m["thema"]]
    schul = ", ".join(SCHULARTEN[s] for s in m["schularten"]) or "schulunabhängig"
    facts = [
        ("Format", TYPEN[m["typ"]]), ("Dauer", dauer_text(m["dauer"])), ("Alter", alter_text(m)),
        ("Wissensstand", NIVEAUS[m["niveau"]]), ("Schulart", schul),
        ("Für", ", ".join(ZIELGRUPPEN[z] for z in m["fuer"])),
    ] + ([("Vorwissen", m["vorwissen"])] if m.get("vorwissen") else [])
    facts_html = "".join(f"<div><dt>{a}</dt><dd>{esc(b)}</dd></div>" for a, b in facts)
    ziele = "".join(f"<li>{esc(z)}</li>" for z in m.get("lernziele", []))
    enthalten = "".join(f"<li>{esc(z)}</li>" for z in m.get("enthalten", []))
    if m.get("ablauf"):
        steps = "".join(
            f'<li><span class="min">{s["min"]} Min.</span><strong>{esc(s["titel"])}</strong>'
            + (f'<span class="muted small">{esc(s["text"])}</span>' if s["text"] else "") + "</li>" for s in m["ablauf"])
        ablauf = f'<section class="panel"><h2>{icon("clock")} Ablauf</h2><ol class="timeline">{steps}</ol></section>'
    elif m.get("einsatz"):
        ablauf = (f'<section class="panel"><h2>{icon("list")} So setzt du es ein</h2><ul>'
                  + "".join(f"<li>{esc(e)}</li>" for e in m["einsatz"]) + "</ul></section>")
    else:
        ablauf = ""
    hinweis = (f'<div class="note note--amber"><strong>Bitte beachten</strong>{esc(m["hinweis"])}</div>' if m.get("hinweis") else "")
    extra_vorne, extra_hinten = zusatz_panels(m)
    if m.get("basis"):
        b = m["basis"]
        aktion_haupt = (f'<a class="btn btn--ink btn--lg" href="{esc(b["url"])}" rel="noopener">{icon("external")} Zum Material bei {esc(b["anbieter"])}</a>')
        aktion_hinweis = (f'<p class="small muted" style="margin-top:1rem">Grundlage: „{esc(b["titel"])}“'
                          + (f' · {esc(b["format"])}' if b.get("format") else "") + ' · externe Seite. Ablauf und Arbeitsmaterial unten sind von netzfest. <!-- TEXT PRÜFEN: Link vor Veröffentlichung prüfen --></p>')
    else:
        aktion_haupt = (f'<!-- DATEI: Download-PDF für „{esc(m["titel"])}“ fehlt noch -->\n    '
                        f'<a class="btn btn--ink btn--lg" href="#download-hinweis" data-download>{icon("download")} Material herunterladen</a>')
        aktion_hinweis = '<p class="small muted" id="download-hinweis" style="margin-top:1rem">Demo: Die Datei wird ergänzt, sobald das Material fertig ist.</p>'
    related = [x for x in materials if x["thema"] == m["thema"] and x["id"] != m["id"]][:3]
    related_html = "\n".join(material_card(x) for x in related)
    jsonld = {
        "@context": "https://schema.org", "@type": "LearningResource", "name": m["titel"], "description": m["kurz"],
        "learningResourceType": TYPEN[m["typ"]], "timeRequired": f'PT{m["dauer"]}M', "inLanguage": "de",
        "isAccessibleForFree": True, "educationalLevel": NIVEAUS[m["niveau"]],
        "audience": [{"@type": "Audience", "audienceType": ZIELGRUPPEN[z]} for z in m["fuer"]],
        "teaches": m.get("lernziele", []),
    }
    if BASE_URL:
        jsonld["url"] = f'{BASE_URL}/material-{m["id"]}.html'
    body = f'''<!-- TEXT PRÜFEN: Demo-Material -->
<div class="page-head"><div class="wrap wrap--wide">
  <nav class="breadcrumb" aria-label="Brotkrumen"><ol><li><a href="index.html">Start</a></li><li><a href="materialien.html">Materialien</a></li><li aria-current="page">{esc(m["titel"])}</li></ol></nav>
  <h1>{esc(m["titel"])}</h1>
  <p class="lead">{esc(m["kurz"])}</p>
  <div class="detail__actions">
    {aktion_haupt}
    {save_btn(m["id"], True)}
  </div>
  {aktion_hinweis}
</div></div>
<div class="wrap wrap--wide detail">
  <div class="stack">
    {hinweis}
    <section class="panel"><h2>{icon("target")} Lernziele</h2><ul>{ziele}</ul></section>
    {ablauf}
    {extra_vorne}
    <section class="panel"><h2>{icon("list")} Enthalten</h2><ul>{enthalten}</ul></section>
    {extra_hinten}
  </div>
  <aside class="detail__aside" aria-label="Eckdaten">
    <dl class="facts">{facts_html}</dl>
    <div class="note"><strong>Mehr zum Thema</strong><a class="link-arrow" href="{thema_url}">{thema_label} verstehen {icon("arrow")}</a></div>
  </aside>
</div>
<section class="section section--white"><div class="wrap wrap--wide">
  <div class="section-head"><h2>Weitere Materialien zu {thema_label}</h2><a class="link-arrow" href="materialien.html?thema={m["thema"]}">Alle zu diesem Thema {icon("arrow")}</a></div>
  <div class="cards">{related_html}</div>
</div></section>'''
    return dict(titel=f'{m["titel"]} – Material', beschreibung=m["kurz"], nav="materialien", body=body, jsonld=jsonld)


# ------------------------------------------------------------------ Bausteine für Seiten
def role_cards():
    out = []
    for key, label, _, ic, tag in ROLLEN:
        out.append(f'''<button type="button" class="role-card role-card--foto" data-role-pick="{key}" aria-pressed="false">
  {foto("rolle-" + key, "rolle")}
  <span class="icon-tile">{icon(ic)}</span>
  <span class="role-card__title">{label}</span>
  <span class="role-card__text">{tag}</span>
  <span class="role-card__check" aria-hidden="true">✓</span>
</button>''')
    return '<div class="roles">' + "\n".join(out) + "</div>"


def numbers_list(ids):
    items = []
    for h in HILFE:
        if h["id"] not in ids:
            continue
        right = (f'<a class="numbers__tel" href="{tel_href(h["tel"])}">{h["tel"]}</a>' if h["tel"]
                 else f'<a class="numbers__tel" href="{h["url"]}" rel="noopener">online</a>')
        items.append(f'<li><span class="numbers__name">{esc(h["kurz"])} <span class="muted" style="font-weight:500">· {esc(h["fuer"])}</span></span>'
                     f'<span class="numbers__when">{esc(h["wann"])}</span>{right}</li>')
    return '<ul class="numbers">' + "".join(items) + "</ul>"


def help_cards(ids=None):
    out = []
    for h in HILFE:
        if ids and h["id"] not in ids:
            continue
        urgent = " help-card--urgent" if h["id"] == "notruf" else ""
        tel = f'<a class="help-card__tel" href="{tel_href(h["tel"])}">{h["tel"]}</a>' if h["tel"] else ""
        link = (f'<a class="link-arrow" href="{h["url"]}" rel="noopener">Zur Website {icon("external")}</a>' if h["url"] else "")
        out.append(f'''<article class="help-card{urgent}"><p class="help-card__for">{esc(h["fuer"])}</p><h3>{esc(h["name"])}</h3>{tel}<p>{esc(h["wann"])}</p>{link}</article>''')
    return '<div class="help-grid">' + "\n".join(out) + "</div>"


def navigator_static():
    """Fallback ohne JavaScript – steht auf hilfe.html."""
    return '''<div class="nav-static" data-nav-static>
  <p>Ohne JavaScript zeigen wir dir hier die wichtigsten Schritte für alle Situationen:</p>
  <h3>Sofort</h3>
  <ol>
    <li><strong>Nicht antworten.</strong> Antworten stacheln Täter:innen oft weiter an.</li>
    <li><strong>Beweise sichern:</strong> Screenshots mit Datum, Uhrzeit, Absender und Link.</li>
    <li><strong>Melden und blockieren</strong> – über die Meldefunktion der Plattform.</li>
    <li><strong>Mit jemandem reden:</strong> Eltern, Lehrkraft, Freund:in oder eine Beratung unten.</li>
  </ol>
  <h3>Bei Drohung oder Gefahr</h3>
  <ul><li>Polizei-Notruf <a href="tel:110">110</a> · bei Lebensgefahr <a href="tel:112">112</a></li></ul>
</div>'''


def navigator_shell(prefix):
    return f'''<div class="navigator" data-navigator data-prefix="{prefix}" hidden>
  <div class="nav-step">
    <h3 id="{prefix}-q1">1. Wer ist betroffen?</h3>
    <div class="chips" role="group" aria-labelledby="{prefix}-q1">
      <button type="button" class="chip" data-q="wer" data-a="ich" aria-pressed="false">Ich selbst</button>
      <button type="button" class="chip" data-q="wer" data-a="andere" aria-pressed="false">Jemand, den ich kenne</button>
      <button type="button" class="chip" data-q="wer" data-a="kind" aria-pressed="false">Mein Kind</button>
      <button type="button" class="chip" data-q="wer" data-a="gruppe" aria-pressed="false">Jemand aus meiner Klasse / Gruppe (als Fachkraft)</button>
    </div>
  </div>
  <div class="nav-step">
    <h3 id="{prefix}-q2">2. Was passiert gerade?</h3>
    <div class="chips" role="group" aria-labelledby="{prefix}-q2">
      <button type="button" class="chip" data-q="was" data-a="mobbing" aria-pressed="false">Beleidigt, ausgelacht oder ausgeschlossen</button>
      <button type="button" class="chip" data-q="was" data-a="bild" aria-pressed="false">Ein Foto oder Video wird verbreitet</button>
      <button type="button" class="chip" data-q="was" data-a="drohung" aria-pressed="false">Drohung oder Erpressung</button>
      <button type="button" class="chip" data-q="was" data-a="hass" aria-pressed="false">Hass wegen Herkunft, Religion, Geschlecht …</button>
      <button type="button" class="chip" data-q="was" data-a="fake" aria-pressed="false">Gerücht, Fake-Profil oder Lüge</button>
    </div>
  </div>
  <div class="nav-result" data-result aria-live="polite" hidden></div>
</div>'''


def akut_dialog():
    return f'''<dialog class="akut-dialog" id="akut-dialog" aria-labelledby="akut-title">
  <div class="akut-dialog__head">
    <h2 id="akut-title">Erste-Hilfe-Navigator</h2>
    <button type="button" class="icon-btn icon-btn--outline" data-dialog-close>{icon("close")}<span class="sr-only">Schließen</span></button>
  </div>
  <div class="akut-dialog__body">
    <p class="muted" style="margin-bottom:1.25rem">Zwei Fragen, dann bekommst du die nächsten Schritte und die passende Anlaufstelle. Nichts davon wird gespeichert.</p>
    {navigator_shell("dlg")}
  </div>
  <p class="akut-dialog__foot">Bei akuter Gefahr: Polizei <a href="tel:110">110</a> · Lebensgefahr <a href="tel:112">112</a> · <a href="hilfe.html">Alle Hilfsangebote</a></p>
</dialog>'''


def wave(text):
    out, i = [], 0
    for wi, word in enumerate(text.split(" ")):
        letters = ""
        for ch in word:
            letters += f'<span class="l" style="--i:{i}">{esc(ch)}</span>'
            i += 1
        sep = " " if wi < len(text.split(" ")) - 1 else ""
        out.append(f'<span class="w">{letters}{sep}</span>')
    return f'<span class="sr-only">{esc(text)}</span><span class="wave" aria-hidden="true">{"".join(out)}</span>'


def static_net():
    """Statisches Netz als SVG – Fallback für reduzierte Bewegung."""
    rnd = random.Random(7)
    w, h = 1440, 760
    pts = [(rnd.uniform(0, w), rnd.uniform(0, h)) for _ in range(70)]
    lines = []
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            d = math.dist(pts[a], pts[b])
            if d < 150:
                op = round(0.35 * (1 - d / 150), 3)
                lines.append(f'<line x1="{pts[a][0]:.0f}" y1="{pts[a][1]:.0f}" x2="{pts[b][0]:.0f}" y2="{pts[b][1]:.0f}" stroke-opacity="{op}"/>')
    dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.2"/>' for x, y in pts)
    return (f'<svg class="hero__net-static" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            f'<g stroke="#7C9885" stroke-width="1">{"".join(lines)}</g><g fill="#28666E" fill-opacity=".45">{dots}</g></svg>')


def schueler_zuerst(ort):
    """Früherer Kinderbereich. Erscheint, sobald „Schüler:innen“ gewählt ist – vor der Materialauswahl."""
    weiter = ('<a class="link-arrow" href="#fuer-dich">Weiter zu Material für dich ' + icon("arrow") + '</a>' if ort == "start"
              else '<a class="link-arrow" href="#filter-panel">Weiter zur Materialauswahl ' + icon("arrow") + '</a>')
    return f'''<!-- TEXT PRÜFEN: Sprache mit Schüler:innen (10–14 J.) testen -->
<section class="fuer-schueler" id="fuer-schueler-{ort}" data-fuer="schueler" hidden aria-labelledby="fs-{ort}">
  <div class="wrap">
    <h2 id="fs-{ort}">Online läuft gerade etwas schief?</h2>
    <p class="lead">Drei Dinge, die dir sofort helfen. Und Menschen, die dir zuhören.</p>
    <ul class="kid-tips">
      <li class="kid-tip"><span class="icon-tile">{icon("heart")}</span><h3>Du bist nicht schuld</h3><p>Wenn jemand gemein zu dir ist, liegt das nicht an dir. Niemand darf dich fertigmachen.</p></li>
      <li class="kid-tip"><span class="icon-tile">{icon("camera")}</span><h3>Mach ein Bildschirmfoto</h3><p>So kannst du später zeigen, was passiert ist. Dann blockier die Person.</p></li>
      <li class="kid-tip"><span class="icon-tile">{icon("chat")}</span><h3>Erzähl es jemandem</h3><p>Deinen Eltern, einer Lehrerin, einem Lehrer oder deinen Freund:innen. Die helfen dir.</p></li>
    </ul>
    <div class="kid-actions">
      <a class="kid-big kid-big--ink" href="tel:116111"><span class="icon-tile">{icon("phone")}</span><span><small>Nummer gegen Kummer · kostenlos · Mo–Sa 14–20 Uhr</small><strong>116 111</strong></span></a>
      <a class="kid-big kid-big--sky" href="spiele.html"><span class="icon-tile">{icon("game")}</span><span><small>Spiel · 6 Runden</small><strong>Fake Detektiv</strong></span></a>
    </div>
    <div class="kid-faq">
      <h3>Fragen, die oft kommen</h3>
      <div class="accordion">
        <details><summary>Muss ich einen Kettenbrief weiterschicken?</summary><div class="acc-body"><p>Nein! Es passiert nichts Schlimmes, wenn du ihn nicht weiterschickst. Das ist nur ausgedacht, damit du Angst bekommst. Lösch ihn einfach oder zeig ihn einem Erwachsenen.</p></div></details>
        <details><summary>Was, wenn ich selbst etwas Gemeines geschrieben habe?</summary><div class="acc-body"><p>Das kann passieren. Wichtig ist, was du jetzt machst: Lösch es, entschuldige dich und hör auf mitzumachen. Das ist mutig.</p></div></details>
        <details><summary>Jemand will Fotos von mir haben. Was soll ich tun?</summary><div class="acc-body"><p>Schick keine Fotos – auch wenn die Person nett ist oder dir etwas verspricht. Sag sofort einem Erwachsenen Bescheid, dem du vertraust. Du bekommst keinen Ärger.</p></div></details>
        <details><summary>Bekomme ich Handyverbot, wenn ich es erzähle?</summary><div class="acc-body"><p>Die meisten Erwachsenen wollen dir helfen und nicht bestrafen. Du kannst auch sagen: „Ich erzähle dir was, aber bitte nimm mir nicht das Handy weg.“ Und wenn du lieber mit jemand Fremdem redest: 116 111.</p></div></details>
      </div>
    </div>
    <p style="margin-top:1.5rem">{weiter}</p>
  </div>
</section>'''


WEITERLEITUNG_KINDER = '''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Weitergeleitet | netzfest</title>
<meta http-equiv="refresh" content="0; url=index.html?rolle=schueler#fuer-schueler-start">
<link rel="canonical" href="index.html"></head>
<body><p>Der Kinderbereich ist jetzt Teil der Startseite: <a href="index.html?rolle=schueler#fuer-schueler-start">Weiter zu den Tipps für Schüler:innen</a>.</p></body></html>
'''


# ------------------------------------------------------------------ Seitenrahmen
def header(active):
    current = ' aria-current="page"'
    nav = "".join(
        f'<li><a href="{href}"{current if key == active else ""}>{label}</a></li>' for href, label, key in NAV)
    role_items = "".join(
        f'<button type="button" role="menuitemradio" aria-checked="false" data-role-set="{k}">{icon(ic)}<span>{label}</span></button>'
        for k, label, _, ic, _ in ROLLEN)

    def role_menu(suffix):
        return f'''<div class="role-menu" data-role-menu>
      <button type="button" class="role-menu__btn" aria-haspopup="true" aria-expanded="false" aria-controls="role-list-{suffix}" data-role-toggle>
        {icon("users")}<span class="role-menu__pre">Ansicht:</span> <span data-role-label>Alle</span>{icon("chev", "chev")}
      </button>
      <div class="role-menu__list" id="role-list-{suffix}" role="menu" hidden>
        <p>Ich bin …</p>{role_items}
        <button type="button" role="menuitem" class="reset" data-role-set="">Alle Inhalte zeigen</button>
      </div>
    </div>'''

    return f'''<a class="skip-link" href="#inhalt">Zum Inhalt springen</a>
<header class="header">
  <div class="wrap wrap--wide header__bar">
    <a class="logo" href="index.html" aria-label="netzfest – Startseite"><span class="logo__mark">{icon("shield").replace('stroke="currentColor"', 'stroke="#FEDC97"')}</span>netzfest</a>
    <nav class="nav" aria-label="Hauptnavigation"><ul>{nav}</ul></nav>
    <div class="header__tools">
      <a class="icon-btn icon-btn--label" href="sammlung.html">{icon("bookmark")}<span class="icon-btn__text">Merkliste</span><span class="sr-only"> (Meine Merkliste)</span><span class="badge" data-save-count hidden>0</span></a>
      {role_menu("desk")}
      <a class="akut-btn" href="hilfe.html#navigator" data-akut><span class="akut-dot" aria-hidden="true"></span><span><span class="akut-long">Sofort-</span>Hilfe</span></a>
      <button type="button" class="icon-btn icon-btn--outline menu-btn" aria-expanded="false" aria-controls="mobile-nav" data-menu-toggle>{icon("menu")}<span class="sr-only">Menü</span></button>
    </div>
  </div>
  <div class="mobile-nav" id="mobile-nav" hidden>
    <div class="wrap">
      <nav aria-label="Hauptnavigation mobil"><ul>{nav}<li><a href="sammlung.html">Meine Merkliste</a></li></ul></nav>
      {role_menu("mob")}
    </div>
  </div>
</header>'''


def footer():
    return f'''<footer class="footer">
  <div class="wrap wrap--wide footer__grid">
    <div>
      <a class="logo" href="index.html"><span class="logo__mark">{icon("shield").replace('stroke="currentColor"', 'stroke="#FEDC97"')}</span>netzfest</a>
      <p>Kostenlose Materialien, Spiele und Wissen gegen Cybermobbing, Hass im Netz und Desinformation – für Schule, Familie und Beratung.</p>
    </div>
    <nav aria-labelledby="f1"><h2 id="f1">Entdecken</h2><ul>
      <li><a href="materialien.html">Materialien</a></li><li><a href="spiele.html">Spiele</a></li><li><a href="wissen.html">Wissen & Glossar</a></li></ul></nav>
    <nav aria-labelledby="f2"><h2 id="f2">Hilfe</h2><ul>
      <li><a href="hilfe.html">Hilfe & Beratung</a></li><li><a href="hilfe.html#beweise">Beweise sichern</a></li><li><a href="hilfe.html#melden">Melden</a></li><li><a href="sammlung.html">Meine Merkliste</a></li></ul></nav>
    <nav aria-labelledby="f3"><h2 id="f3">Über netzfest</h2><ul>
      <li><a href="ueber-uns.html">Über uns</a></li><li><a href="impressum.html">Impressum</a></li><li><a href="datenschutz.html">Datenschutz</a></li><li><a href="barrierefreiheit.html">Barrierefreiheit</a></li></ul></nav>
  </div>
  <div class="footer__bottom"><div class="wrap wrap--wide">© 2026 netzfest · Prototyp · Hilfenummern Stand {STAND_HILFE} · Kein Tracking, keine Cookies.</div></div>
</footer>'''


# ------------------------------------------------------------------ Fotos
# Stockfotos von Unsplash (Unsplash-Lizenz: kostenlos, auch kommerziell, Nennung nicht Pflicht – wir nennen trotzdem).
# Dateien: assets/img/fotos/<name>-800|1600.webp|jpg, Format 3:2. Einsetzen in Seiten mit {{FOTO:name}}.
FOTOS = {
    "cybermobbing": {"alt": "Ein Jugendlicher sitzt auf Stufen, schaut auf sein Handy und hält sich die Hand vors Gesicht.",
                     "von": "Vullnet Ademaj", "url": "https://unsplash.com/photos/q70r_0BWzVY"},
    "hass": {"alt": "Eine junge Frau stützt den Kopf in die Hand und liest nachdenklich auf ihrem Handy.",
             "von": "Kev Costello", "url": "https://unsplash.com/photos/w3jVXGkYZCw"},
    "fakenews": {"alt": "Eine Frau schaut durch eine Lupe.",
                 "von": "Houcine Ncib", "url": "https://unsplash.com/photos/P5L8gICF0CI"},
    "hilfe": {"alt": "Zwei junge Menschen sitzen nebeneinander und halten sich im Arm.",
              "von": "Priscilla Du Preez", "url": "https://unsplash.com/photos/eIWIn7BvVXk"},
    "spiele": {"alt": "Eine jugendliche Person sitzt entspannt auf dem Sofa und tippt auf ihrem Handy.",
               "von": "Hiki App", "url": "https://unsplash.com/photos/vvW2WF-999g"},
    "wissen": {"alt": "Blick über die Schultern von Schüler:innen nach vorn zur Lehrkraft im Klassenraum.",
               "von": "Taylor Flowe", "url": "https://unsplash.com/photos/4nKOEAQaTgA"},
    "rolle-schueler": {"alt": "Eine Gruppe Jugendlicher sitzt draußen zusammen und lacht in die Kamera.",
                       "von": "Tim Mossholder", "url": "https://unsplash.com/photos/hOF1bWoet_Q"},
    "rolle-eltern": {"alt": "Mutter und Tochter liegen auf dem Bett und schauen gemeinsam auf ein Tablet.",
                     "von": "Vitaly Gariev", "url": "https://unsplash.com/photos/qmPZkwFj48s"},
    "rolle-lehrkraefte": {"alt": "Ein Lehrer spricht vor einer Klasse, die Schüler:innen hören an ihren Tischen zu.",
                          "von": "Vitaly Gariev", "url": "https://unsplash.com/photos/LscaHTQsmIY"},
    "rolle-fachkraefte": {"alt": "Eine Beraterin spricht mit einer Jugendlichen, die auf einem Sofa sitzt.",
                          "von": "Vitaly Gariev", "url": "https://unsplash.com/photos/QxkvMblcaJ0"},
    "gespraech": {"alt": "Drei Jugendliche sitzen zusammen und reden miteinander.",
                  "von": "Timur Shakerzianov", "url": "https://unsplash.com/photos/HeazjhCA_5s"},
    "gegenrede": {"alt": "Im Unterricht meldet sich eine Schülerin mit erhobener Hand zu Wort.",
                  "von": "Taylor Flowe", "url": "https://unsplash.com/photos/NTur2_QKpg0"},
    "recherche": {"alt": "Eine Jugendliche recherchiert konzentriert am Laptop.",
                  "von": "Annie Spratt", "url": "https://unsplash.com/photos/xKJUnFwfz3s"},
    "beweise": {"alt": "Zwei Hände halten ein Smartphone.",
                "von": "Paul Hanaoka", "url": "https://unsplash.com/photos/HbyYFFokvm0"},
    "gruppenarbeit": {"alt": "Fünf Schüler arbeiten im Klassenraum gemeinsam an einem Tisch und schreiben.",
                      "von": "Yegor Makarenko", "url": "https://unsplash.com/photos/vOpkxzkJx9I"},
}

FOTO_SIZES = {
    "karte": "(min-width: 64em) 22rem, (min-width: 40em) 50vw, 100vw",
    "kopf": "(min-width: 64em) 28rem, 18rem",
    "rolle": "(min-width: 64em) 16rem, 50vw",
    "text": "(min-width: 40em) 40rem, 100vw",
}


def foto(name, art="karte"):
    """Responsives Foto. art="karte": in Karten. art="kopf": im Seitenkopf (erst ab 640 px sichtbar).
    art="rolle": in den Rollenkarten (erst ab 576 px sichtbar). art="text": im Fließtext.
    Die Bilder ergänzen Überschriften, die dasselbe sagen – darum alt="" (dekorativ)."""
    assert name in FOTOS, f"unbekanntes Foto {name}"
    sizes = FOTO_SIZES[art]
    laden = 'loading="lazy" decoding="async"'  # auch im Kopf: auf dem Handy ausgeblendet, wird dann gar nicht geladen
    b = f"assets/img/fotos/{name}"
    return (f'<picture class="foto foto--{art}">'
            f'<source type="image/webp" srcset="{b}-800.webp 800w, {b}-1600.webp 1600w" sizes="{sizes}">'
            f'<img src="{b}-800.jpg" srcset="{b}-800.jpg 800w, {b}-1600.jpg 1600w" sizes="{sizes}" '
            f'width="800" height="533" alt="" {laden}></picture>')


def bildnachweis():
    li = "".join(f'<li>{esc(f["alt"])} Foto: {esc(f["von"])}, <a href="{f["url"]}" rel="noopener">Unsplash</a></li>'
                 for f in FOTOS.values())
    return f"<ul>{li}</ul>"


def page(fname, titel, beschreibung, nav, body, jsonld=None):
    full_title = f"{titel} | {SITE}" if fname != "index.html" else f"{SITE} – Gemeinsam stark im Netz"
    url = f"{BASE_URL}/{'' if fname == 'index.html' else fname}"
    ld = ""
    if jsonld:
        items = jsonld if isinstance(jsonld, list) else [jsonld]
        ld = "\n".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in items)
    robots = '<meta name="robots" content="noindex">' if TESTBETRIEB or fname in ("404.html", "sammlung.html") else ""
    absolut = (f'''<link rel="canonical" href="{url}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">''' if BASE_URL else "")
    return f'''<!doctype html>
<html lang="de" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(beschreibung)}">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(beschreibung)}">
<meta property="og:locale" content="de_DE">
{absolut}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#033F63">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/styles.css">
<script>document.documentElement.className='js';try{{var r=localStorage.getItem('netzfest:rolle');if(r)document.documentElement.dataset.role=JSON.parse(r)||''}}catch(e){{}}</script>
{ld}
</head>
<body>
{header(nav)}
<main id="inhalt" tabindex="-1">
{body}
</main>
{footer()}
{akut_dialog()}
<script src="assets/js/daten.js"></script>
<script src="assets/js/app.js"></script>
</body>
</html>
'''


# ------------------------------------------------------------------ Seiten aus _werkstatt/seiten
META_RE = re.compile(r"^<!--\s*\n(.*?)\n-->\s*\n", re.S)


def read_page(path):
    raw = path.read_text(encoding="utf-8")
    m = META_RE.match(raw)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        raw = raw[m.end():]
    return meta, raw


def main():
    data = json.loads((WERK / "materialien.json").read_text(encoding="utf-8"))
    materials = data["materialien"]
    ids = [m["id"] for m in materials]
    assert len(ids) == len(set(ids)), "Material-IDs müssen eindeutig sein"

    by_topic = {k: "\n".join([material_card(m) for m in materials if m["thema"] == k][:3]) for k in THEMEN}

    snippets = {
        "ROLLENKARTEN": role_cards(),
        "CTA_MATERIALIEN": cta("materialien.html", "Alle Materialien entdecken"),
        "STARTSEITE_KARTEN": startseite_picks(materials),
        "BIBLIOTHEK": library_html(materials),
        "ALLE_KARTEN": "\n".join(material_card(m) for m in materials),
        "SPIEL_KARTEN": "\n".join(material_card(m) for m in materials if m["typ"] == "spiel"),
        "NUMMERN_KURZ": numbers_list(["kjt", "eltern", "hateaid"]),
        "NUMMERN_KINDER": numbers_list(["kjt", "online"]),
        "HILFEKARTEN": help_cards(),
        "NAVIGATOR": navigator_shell("page") + navigator_static(),
        "NETZ": static_net(),
        "STAND_HILFE": STAND_HILFE,
        "ANZAHL_MATERIAL": str(len(materials)),
        "KARTEN_CYBERMOBBING": by_topic["cybermobbing"],
        "KARTEN_HASS": by_topic["hass"],
        "KARTEN_FAKENEWS": by_topic["fakenews"],
        "BILDNACHWEIS": bildnachweis(),
    }

    written = []
    for path in sorted((WERK / "seiten").glob("*.html")):
        meta, body = read_page(path)
        body = re.sub(r"\{\{ICON:([a-z-]+)\}\}", lambda mm: icon(mm.group(1)), body)
        body = re.sub(r"\{\{FOTO:([a-z]+)(?::([a-z]+))?\}\}", lambda mm: foto(mm.group(1), mm.group(2) or "karte"), body)
        body = re.sub(r"\{\{SCHUELER_ZUERST:([a-z]+)\}\}", lambda mm: schueler_zuerst(mm.group(1)), body)
        for key, val in snippets.items():
            body = body.replace("{{" + key + "}}", val)
        leftover = re.findall(r"\{\{[A-Z_:a-z-]+\}\}", body)
        assert not leftover, f"{path.name}: unbekannte Platzhalter {leftover}"
        jsonld = json.loads(meta["jsonld"]) if meta.get("jsonld") else None
        (ROOT / path.name).write_text(page(path.name, meta.get("titel", SITE), meta.get("beschreibung", ""), meta.get("nav", ""), body, jsonld), encoding="utf-8")
        written.append(path.name)

    for m in materials:
        d = detail_page(m, materials)
        fname = f'material-{m["id"]}.html'
        (ROOT / fname).write_text(page(fname, d["titel"], d["beschreibung"], d["nav"], d["body"], d["jsonld"]), encoding="utf-8")
        written.append(fname)

    (ROOT / "kinder.html").write_text(WEITERLEITUNG_KINDER, encoding="utf-8")

    # alte Detailseiten entfernen, deren Material nicht mehr existiert
    for old in ROOT.glob("material-*.html"):
        if old.name not in written:
            old.unlink()

    # Daten für JavaScript (Navigator, Merkliste)
    js_data = {
        "hilfe": {h["id"]: {k: h[k] for k in ("name", "kurz", "tel", "fuer", "wann", "url")} for h in HILFE},
        "rollen": {k: short for k, _, short, _, _ in ROLLEN},
        "materialien": {m["id"]: m["titel"] for m in materials},  # Merkliste: nur gültige IDs, Titel für Ansagen
    }
    (ROOT / "assets" / "js").mkdir(parents=True, exist_ok=True)
    (ROOT / "assets" / "js" / "daten.js").write_text(
        "/* Automatisch erzeugt von _werkstatt/bauen.py – nicht direkt bearbeiten. */\n"
        f"window.NETZFEST = {json.dumps(js_data, ensure_ascii=False, indent=1)};\n", encoding="utf-8")

    # Sitemap braucht absolute Adressen – nur mit BASE_URL. Ohne sie wird eine alte Sitemap entfernt.
    urls = [n for n in written if n not in ("404.html", "sammlung.html")]
    if BASE_URL and not TESTBETRIEB:
        sitemap = "".join(f"<url><loc>{BASE_URL}/{'' if n == 'index.html' else n}</loc></url>" for n in urls)
        (ROOT / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>\n', encoding="utf-8")
        (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    else:
        if (ROOT / "sitemap.xml").exists():
            (ROOT / "sitemap.xml").unlink()
        (ROOT / "robots.txt").write_text("User-agent: *\n" + ("Disallow: /\n" if TESTBETRIEB else "Allow: /\n"), encoding="utf-8")
    # GitHub Pages: kein Jekyll – Dateien werden genau so ausgeliefert, wie sie hier liegen
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    modus = "Testbetrieb (noindex)" if TESTBETRIEB else "Live"
    print(f"✓ {len(written)} Seiten erzeugt, dazu assets/js/daten.js und robots.txt · {modus} · Adresse: {BASE_URL or 'relativ (noch keine eingetragen)'}")


if __name__ == "__main__":
    main()
