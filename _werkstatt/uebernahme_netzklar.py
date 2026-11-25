"""Aufruf im Ordner netzfest-html:  python3 _werkstatt/uebernahme_netzklar.py  – danach python3 _werkstatt/bauen.py

Übernimmt die 27 Einheiten von Website 1 (NETZKLAR) als Materialien in Website 2 (netzfest).
Website 1 wird nur gelesen. Mehrfach ausführbar: frühere Übernahmen werden ersetzt."""
import json
import re
import sys
from pathlib import Path

PROJ = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]  # Ordner „Webentwicklung mit Claude“
W1 = PROJ / "Website 1" / "inhalte"
ZIEL = PROJ / "Website 2" / "netzfest-html" / "_werkstatt" / "materialien.json"

einheiten = json.loads((W1 / "daten.json").read_text("utf-8"))["einheiten"]
inhalte = json.loads((W1 / "inhalte-einheiten.json").read_text("utf-8"))

TYP = {"lehrkraefte": "unterrichtseinheit", "eltern": "leitfaden", "fachkraefte": "baustein", "schueler": "selbstlernen"}
THEMA = {
    "lk-1": "hass", "lk-2": "hass", "lk-3": "hass", "lk-4": "hass", "lk-5": "hass", "lk-6": "hass",
    "lk-7": "cybermobbing", "lk-8": "cybermobbing", "lk-vorfall": "cybermobbing",
    "lk-9": "fakenews", "lk-10": "fakenews", "lk-11": "fakenews", "lk-12": "fakenews",
    "el-1": "cybermobbing", "el-2": "hass", "el-3": "cybermobbing", "el-4": "cybermobbing", "el-5": "fakenews",
    "fk-1": "cybermobbing", "fk-2": "cybermobbing", "fk-3": "cybermobbing", "fk-4": "hass", "fk-5": "fakenews",
    "sc-1": "hass", "sc-2": "cybermobbing", "sc-3": "cybermobbing", "sc-4": "fakenews",
}
NIVEAU = {
    "einstieg": ["lk-1", "lk-2", "lk-7", "lk-9", "sc-1", "sc-2", "sc-3", "sc-4", "el-1", "el-2", "el-5", "fk-1"],
    "basis": ["lk-3", "lk-4", "lk-5", "lk-6", "lk-10", "lk-vorfall", "el-3", "el-4", "fk-2"],
    "vertiefung": ["lk-8", "lk-11", "lk-12", "fk-3", "fk-4", "fk-5"],
}
NIVEAU_VON = {eid: n for n, ids in NIVEAU.items() for eid in ids}


def slug(t):
    t = t.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def alter_und_schule(e):
    zg = e["zielgruppe"]
    if zg == "lehrkraefte":
        k = [int(x) for x in re.findall(r"\d+", e["fuer"])]
        a_min, a_max = k[0] + 5, min(18, k[-1] + 5)
        return a_min, a_max, ["sek1", "sek2"] if k[-1] >= 11 else ["sek1"]
    if zg == "schueler":
        return 10, 18, ["sek1", "sek2"]
    if zg == "eltern":
        return 6, 17, []
    return None, None, []


daten = json.loads(ZIEL.read_text("utf-8"))
eigene = [m for m in daten["materialien"] if m.get("herkunft") != "netzklar"]
vorhandene_ids = {m["id"] for m in eigene}

neu = []
for e in einheiten:
    if e.get("herkunft"):  # recherchiertes Zusatzmaterial steht bereits direkt in netzfest
        continue
    mid = slug(e["titel"])
    if mid in vorhandene_ids:
        mid = slug(e["titel"]) + "-" + e["zielgruppe"]
    a_min, a_max, schulen = alter_und_schule(e)
    x = inhalte.get(e["id"], {})
    labels = {a["key"]: a["label"] for a in e["anpassung"]}
    m = {
        "id": mid,
        "titel": e["titel"],
        "kurz": e["kurz"],
        "typ": TYP[e["zielgruppe"]],
        "thema": THEMA[e["id"]],
        "fuer": [e["zielgruppe"]],
        "niveau": NIVEAU_VON[e["id"]],
        "schularten": schulen,
        "dauer": e["dauer"],
        "startseite": [],
        "lernziele": e["lernziele"],
        "ablauf": [{"min": b["min"], "titel": b["titel"], "text": " ".join(b["ablauf"])} for b in e["bloecke"]],
        "enthalten": e["material"],
        "hinweis": e["hinweis"],
        "vorwissen": e["vorwissen"],
        "anpassung": [{"label": a["label"], "text": a["text"]} for a in e["anpassung"] if a["text"] != "Wie beschrieben."],
        "hintergrund": [{"text": h["text"], "quelle": h["anbieter"], "url": h["url"]} for h in x.get("hintergrund", [])],
        "tipps": [{"text": t["text"], "quelle": t["anbieter"], "url": t["url"],
                   "fuer": " · ".join(labels.get(k, k) for k in t.get("stufe", []))} for t in x.get("tipps", [])],
        "arbeitsmaterial": [
            {"titel": mat["titel"], "hinweis": mat.get("hinweis", ""),
             "punkte": mat.get("punkte", []),
             "fassungen": [{"fuer": labels.get(k, k), "punkte": v} for k, v in mat.get("stufen", {}).items()]}
            for mat in x.get("material", [])],
        "weiterlesen": [{"titel": w["titel"], "url": w["url"], "quelle": w["anbieter"], "kurz": w.get("kurz", "")} for w in x.get("weiterlesen", [])],
        "herkunft": "netzklar",
    }
    if a_min:
        m["alter_min"], m["alter_max"] = a_min, a_max
    neu.append(m)

ids = [m["id"] for m in eigene + neu]
assert len(ids) == len(set(ids)), "doppelte IDs"
daten["materialien"] = eigene + neu
ZIEL.write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", "utf-8")
print(f"{len(eigene)} eigene + {len(neu)} übernommene Materialien = {len(ids)}")
