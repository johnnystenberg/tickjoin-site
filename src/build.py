#!/usr/bin/env python3
"""Bygger startsidan per språk från src/template.html och src/<språk>.json.

    python3 src/build.py

Engelska hamnar i roten (/index.html), övriga språk i /<språk>/index.html. Lägg till ett språk
genom att kopiera src/en.json till src/<språk>.json, översätta och ta skärmbilder till
assets/screens/<språk>/ (se README).
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
ICONS = {
    "alarm": '<path d="M12 7v5l3 2"/><circle cx="12" cy="13" r="8"/><path d="M5 3 2 6M19 3l3 3"/>',
    "join": '<rect x="2.5" y="6" width="13" height="12" rx="3"/><path d="m15.5 10.5 6-3.5v10l-6-3.5"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="3"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>',
}
# Plattformskorten: bild, ram och bildens storlek. Mac- och Android-bilderna görs med src/platform-shots.sh.
PLATFORM_SHOTS = {
    "iphone": ("next", "phone", (590, 1280)),
    "mac": ("mac", "screen", (590, 801)),
    "android": ("android", "phone android", (590, 1049)),
}


def esc(value):
    return html.escape(value, quote=True)


def icon(name):
    return (f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def render(t, languages, template):
    lang = t["lang"]
    base = "" if t["path"] == "/" else "../"

    def shot(name, alt, cls="phone", size=(590, 1280)):
        # Bilder som saknas på språket (alarmet tas på telefon) visas på engelska.
        shot_lang = lang if (ROOT / "assets" / "screens" / lang / f"{name}.webp").exists() else "en"
        width, height = size
        return (f'<div class="{cls}"><img src="{base}assets/screens/{shot_lang}/{name}.webp" '
                f'alt="{esc(t["shot_alt"])} {esc(alt)}" width="{width}" height="{height}" loading="lazy" decoding="async"></div>')

    pillars = "\n".join(
        f'<article class="pillar">{icon(i)}<h3>{esc(h)}</h3><p>{esc(p)}</p></article>' for i, h, p in t["pillars"])

    def platform(key, name, text, requires):
        image, cls, size = PLATFORM_SHOTS[key]
        return (f'<article class="card platform"><div class="media">{shot(image, name, cls, size)}</div>'
                f'<h3>{esc(name)}</h3><p>{esc(text)}</p><p class="requires">{esc(requires)}</p></article>')

    platforms = "\n".join(platform(*p) for p in t["platforms"])
    gallery = "\n".join(
        f'<figure>{shot(n, h)}<figcaption><strong>{esc(h)}</strong>{esc(p)}</figcaption></figure>'
        for n, h, p in t["screens"])
    features = "\n".join(f'<article class="feature"><h3>{esc(h)}</h3><p>{esc(p)}</p></article>' for h, p in t["features"])
    privacy = "\n".join(f'<li><strong>{esc(h)}</strong>{esc(p)}</li>' for h, p in t["privacy_points"])
    free = "\n".join(f"<li>{esc(p)}</li>" for p in t["free_points"])
    pro = "\n".join(f"<li>{esc(p)}</li>" for p in t["pro_points"])
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{l["lang"]}" href="https://tickjoin.com{l["path"]}">' for l in languages)
    current = ' aria-current="page"'
    switcher = " · ".join(
        f'<a href="{l["path"]}" lang="{l["lang"]}" data-lang="{l["lang"]}"{current if l["lang"] == lang else ""}>'
        f'{esc(l["name"])}</a>' for l in languages)
    menu = "".join(
        f'<a href="{l["path"]}" lang="{l["lang"]}" data-lang="{l["lang"]}"{current if l["lang"] == lang else ""}>'
        f'{esc(l["name"])}</a>' for l in languages)
    targets = {l["lang"].lower(): l["path"] for l in languages if l["path"] != "/"}
    if "pt-br" in targets:
        targets.setdefault("pt", targets["pt-br"])  # Portugisiska från Portugal får hellre Brasilien än engelska.
    paths = json.dumps(targets, separators=(",", ":"))
    hero_shot = shot("next", t["screens"][0][1], "phone hero-phone").replace(' loading="lazy"', ' fetchpriority="high"')
    notify = f'mailto:support@tickjoin.com?subject={esc(t["notify_subject"]).replace(" ", "%20")}'

    values = {
        "lang": lang, "title": esc(t["title"]), "description": esc(t["description"]), "alternates": alternates,
        "base": base, "redirect": "true" if t["path"] == "/" else "false",
        "badge": esc(t["badge"]), "hero_title": esc(t["hero_title"]), "hero_text": esc(t["hero_text"]),
        "hero_note": esc(t["hero_note"]), "cta_notify": esc(t["cta_notify"]), "notify": notify,
        "cta_more": esc(t["cta_more"]), "hero_shot": hero_shot, "pillars": pillars,
        "platforms_title": esc(t["platforms_title"]), "platforms_text": esc(t["platforms_text"]), "platforms": platforms,
        "gallery_title": esc(t["gallery_title"]), "gallery_text": esc(t["gallery_text"]), "gallery": gallery,
        "features_title": esc(t["features_title"]), "features": features,
        "privacy_title": esc(t["privacy_title"]), "privacy": privacy, "privacy_link": esc(t["privacy_link"]),
        "pricing_title": esc(t["pricing_title"]), "free_name": esc(t["free_name"]), "free_price": esc(t["free_price"]),
        "free": free, "pro_name": esc(t["pro_name"]), "pro_price": esc(t["pro_price"]), "pro_alt": esc(t["pro_alt"]),
        "pro_trial": esc(t["pro_trial"]), "pro": pro,
        "it_title": esc(t["it_title"]), "it_text": esc(t["it_text"]), "it_link": esc(t["it_link"]),
        "it_href": "/it/" if lang == "sv" else "/it/#english",
        "privacy_href": "/privacy/" if lang == "sv" else "/privacy/#english",
        "support_href": "/support/" if lang == "sv" else "/support/#english",
        "footer_privacy": esc(t["footer_privacy"]), "footer_it": esc(t["footer_it"]),
        "footer_support": esc(t["footer_support"]),
        "language": esc(t["language"]), "switcher": switcher, "menu": menu, "paths": paths,
        "current_name": esc(t["name"]),
    }
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    assert "{{" not in out, out[out.index("{{"):out.index("{{") + 40]
    return out


def main():
    template = (SRC / "template.html").read_text()
    texts = [json.loads(p.read_text()) for p in sorted(SRC.glob("*.json"))]
    # /it/ är IT-sidan, så italienska ligger på /it-it/.
    assert all(t["path"] not in ("/it/", "/privacy/", "/support/") for t in texts), "språksidan krockar med en annan sida"
    texts.sort(key=lambda t: (t["path"] != "/", t["lang"]))
    for t in texts:
        target = ROOT / t["path"].strip("/") / "index.html" if t["path"] != "/" else ROOT / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(t, texts, template))
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
