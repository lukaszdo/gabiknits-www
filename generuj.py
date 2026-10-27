#!/usr/bin/env python3
"""Generator stron głównych Gabi Knits w siedmiu językach.

Teksty są w `teksty.py` (słownik T), układ w funkcji page(), wygląd w assets/site.css.
Zrzuty aplikacji: assets/shots/<język>/*.png; brakujące zastępuje szkic z assets/shots/_szkic/.
Uruchomienie: `python3 generuj.py` nadpisuje index.html (angielski, w korzeniu) i pl/, cs/, de/, nb/, da/, sv/index.html.
Polityka prywatności (privacy/, xx/privacy/) i regulamin (terms/, xx/terms/) są pisane ręcznie -
generator podmienia w nich tylko przełącznik języków i odnośniki hreflang.
Na końcu zapisuje sitemap.xml (wszystkie strony bez „noindex”) i robots.txt - dla Google Search Console.
"""
import re
import struct
import sys
from html import escape
from pathlib import Path

sys.dont_write_bytecode = True          # bez __pycache__ w repozytorium strony
from teksty import T                    # teksty strony w siedmiu językach

ROOT = Path(__file__).parent
# Czeski od 2026-10-25, zaraz po polskim.
LANGS = ["en", "pl", "cs", "de", "nb", "da", "sv"]
NAMES = {"en": "EN", "pl": "PL", "cs": "CS", "de": "DE", "nb": "NO", "da": "DA", "sv": "SV"}
COMPANY = "ŁUKASZ DOMAŃSKI IT ONE STUDIO"
EMAIL = "contact@gabiknits.app"

# Cennik ukryty do startu w sklepie (decyzja 2026-10-08: strategia cenowa nie wychodzi przed premierą).
# Teksty sekcji zostają w słowniku T; True przywraca sekcję „Cena” i odnośnik w nagłówku.
SHOW_PRICE = False

# Aplikacja w sklepie (decyzja 2026-10-09). Przed startem: „Wkrótce w Google Play” na górze i blok
# kontaktu na dole. Po starcie (True): na górze i na dole przycisk do sklepu, a blok na dole zachęca
# do pobrania. UWAGA: wtedy Google wymaga oficjalnej odznaki „Get it on Google Play” (wytyczne marki)
# zamiast naszej - podmienić play_badge() na oficjalny plik odznaki w każdym języku.
LAUNCHED = False
PLAY_URL = "https://play.google.com/store/apps/details?id=app.gabiknits"

# Skąd przyszła instalacja (2026-10-27): parametr referrer z UTM - Play Console pokazuje go w raportach
# pozyskiwania (źródło i kampania), na stronie bez skryptów i ciasteczek. Kampania = wersja językowa
# strony, żeby było widać, który język przyprowadza instalacje. Wartość referrer musi być zakodowana (%3D, %26).
def play_url(lang):
    return f"{PLAY_URL}&referrer=utm_source%3Dgabiknits.app%26utm_medium%3Dwebsite%26utm_campaign%3D{lang}"

# Podpis przycisku menu na wąskim ekranie (jedyny tekst spoza T - jedno słowo na język).
MENU = {"en": "Menu", "pl": "Menu", "cs": "Menu", "de": "Menü", "nb": "Meny", "da": "Menu", "sv": "Meny"}

# Flagi do wyboru języka - rysowane w SVG w treści strony (bez zewnętrznych plików).
# Angielski: flaga Wielkiej Brytanii. Identyfikator przycięcia zależy od miejsca użycia
# (przełącznik stoi na stronie kilka razy, a id w dokumencie musi być jedyny).
FLAGS = {
    "en": '<svg viewBox="0 0 60 30"><clipPath id="uk{k}"><path d="M0 0v30h60V0z"/></clipPath><g clip-path="url(#uk{k})">'
          '<path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/>'
          '<path d="M0 0l60 30m0-30L0 30" stroke="#C8102E" stroke-width="2.4"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/>'
          '<path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></g></svg>',
    "pl": '<svg viewBox="0 0 16 10"><path d="M0 0h16v5H0z" fill="#fff"/><path d="M0 5h16v5H0z" fill="#DC143C"/></svg>',
    # Czechy: biały pas u góry, czerwony u dołu, niebieski trójkąt od drzewca do środka.
    "cs": '<svg viewBox="0 0 6 4"><path d="M0 0h6v2H0z" fill="#fff"/><path d="M0 2h6v2H0z" fill="#D7141A"/><path d="M0 0l3 2-3 2z" fill="#11457E"/></svg>',
    "de": '<svg viewBox="0 0 5 3"><path d="M0 0h5v1H0z" fill="#000"/><path d="M0 1h5v1H0z" fill="#DD0000"/><path d="M0 2h5v1H0z" fill="#FFCE00"/></svg>',
    "nb": '<svg viewBox="0 0 22 16"><path d="M0 0h22v16H0z" fill="#BA0C2F"/><path d="M6 0h4v16H6zM0 6h22v4H0z" fill="#fff"/>'
          '<path d="M7 0h2v16H7zM0 7h22v2H0z" fill="#00205B"/></svg>',
    "da": '<svg viewBox="0 0 37 28"><path d="M0 0h37v28H0z" fill="#C8102E"/><path d="M12 0h4v28h-4zM0 12h37v4H0z" fill="#fff"/></svg>',
    "sv": '<svg viewBox="0 0 16 10"><path d="M0 0h16v10H0z" fill="#006AA7"/><path d="M5 0h2v10H5zM0 4h16v2H0z" fill="#FECC00"/></svg>',
}


def lang_nav(lang, href, label="Language", key=""):
    """Przełącznik języków z flagami; [href] - adres strony w danym języku względem bieżącej."""
    items = []
    for l in LANGS:
        flag = FLAGS[l].replace("{k}", key)
        inner = f'<span class="flag" aria-hidden="true">{flag}</span><span>{NAMES[l]}</span>'
        if l == lang:
            items.append(f'<span class="cur" lang="{l}" aria-current="page">{inner}</span>')
        else:
            items.append(f'<a href="{href(l)}" hreflang="{l}" lang="{l}">{inner}</a>')
    return f'<nav class="lang" aria-label="{label}">' + "".join(items) + "</nav>"


# Ikony - rysowane ręcznie na siatce 24×24, kreska 1,75 px, zaokrąglone końce (styl jak w aplikacji:
# hierarchię niesie kreska, nie kolor). Kolor bierze z currentColor.
ICONS = {
    "check": '<path d="M5 12.5l4.2 4.2L19 7"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2.2"/><path d="M3.8 7.2l8.2 6 8.2-6"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5M12 14.5v2"/>',
    # filary: znajduje schemat / rząd zawsze na widoku / na każdym ekranie (do 2026-10-24 „stworzona dla e-inku”)
    "find": '<path d="M3.5 3.5h9v9h-9zM3.5 8h9M8 3.5v9"/><circle cx="16" cy="16" r="3.8"/><path d="M18.8 18.8l2.2 2.2"/>',
    "row": '<rect x="3.5" y="4" width="17" height="16" rx="2"/><path d="M3.5 9.5h17M3.5 14.5h17"/>'
           '<path d="M2 9.5h20v5H2z" fill="currentColor" fill-opacity=".2" stroke-width="2"/>',
    "tablet": '<rect x="5" y="2.5" width="14" height="19" rx="2.2"/><path d="M5 17h14M10.5 19.3h3"/>',
    "bookmark": '<path d="M7.2 3.5h9.6c.7 0 1.2.5 1.2 1.2V20.5l-6-4-6 4V4.7c0-.7.5-1.2 1.2-1.2z"/><path d="M9.5 8.5h5"/>',
    # e-ink: gruba ramka zamiast koloru / bez animacji / duże przyciski i numery / sprawdzona na BOOX
    "frame": '<path d="M4 4.5h16M4 19.5h16"/><rect x="2.5" y="9" width="19" height="6" rx="1" stroke-width="2.75"/>',
    "still": '<circle cx="12" cy="12" r="8.5"/><path d="M10 9v6M14 9v6"/>',
    "tabletcheck": '<rect x="5" y="2.5" width="14" height="19" rx="2.2"/><path d="M5 17h14M9.2 10.2l2 2 3.8-3.8"/>',
    "buttons": '<rect x="3" y="13" width="7.5" height="7" rx="2"/><rect x="13.5" y="13" width="7.5" height="7" rx="2"/>'
               '<path d="M8 16.5H5.5M7 15l-1.5 1.5L7 18M16 16.5h2.5M17 15l1.5 1.5L17 18M12 3.5v6M9.5 7l2.5 2.5L14.5 7"/>',
    # funkcje (kolejność jak feats w T)
    "sequence": '<rect x="2.5" y="8.5" width="6" height="7" rx="1.5"/><rect x="15.5" y="8.5" width="6" height="7" rx="1.5"/>'
                '<path d="M9.5 12h5M12.6 10l2 2-2 2"/>',
    "cat": '<path d="M5 10.5V4.5l4 3.2h6l4-3.2v6a7 7 0 0 1-14 0z"/><path d="M9.5 12.2v.6M14.5 12.2v.6M10.8 15.3l1.2.8 1.2-.8"/>',
    "layers": '<path d="M12 3.5l8.5 4.5-8.5 4.5L3.5 8z"/><path d="M3.5 12l8.5 4.5 8.5-4.5M3.5 16l8.5 4.5 8.5-4.5"/>',
    "key": '<rect x="3.5" y="4.5" width="4" height="4" rx=".8"/><rect x="3.5" y="10" width="4" height="4" rx=".8"/>'
           '<rect x="3.5" y="15.5" width="4" height="4" rx=".8"/><path d="M10.5 6.5h10M10.5 12h8M10.5 17.5h9"/>',
    "follow": '<path d="M3 12h18M12 2.8v5M9.6 5.2L12 2.8l2.4 2.4M12 21.2v-5M9.6 18.8l2.4 2.4 2.4-2.4"/>',
    "clock": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4.2l2.8 1.8M9.5 2.8h5"/>',
    # filiżanka z parą - „Postaw kawę” (pas pod kontaktem i stopka)
    "coffee": '<path d="M4 9.5h12v4.5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M16 11h1.5a2.5 2.5 0 0 1 0 5H16M8 3.5c-.7.9-.7 1.9 0 2.8M12 3.5c-.7.9-.7 1.9 0 2.8"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.5 3.5 5.3 3.5 8.5s-1.1 6-3.5 8.5c-2.4-2.5-3.5-5.3-3.5-8.5s1.1-6 3.5-8.5z"/>',
}
PILLAR_ICONS = ["find", "row", "tablet"]
EINK_ICONS = ["frame", "still", "buttons", "tabletcheck"]
# Funkcje: jedna ikona na kartę, w kolejności feats z T (sekwencja, legenda, kilka schematów, rząd na środku,
# licznik czasu, prowadzony pierwszy projekt z kotem Gabi, postęp zapisuje się sam, języki).
# Zmiana kolejności tekstów → tu też.
FEAT_ICONS = ["sequence", "key", "layers", "follow", "clock", "cat", "bookmark", "globe"]


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def play_badge(text, cls="", href=None):
    """Odznaka „Wkrótce w Google Play” w stylu odznaki sklepu - własny znak (zaokrąglony trójkąt
    w kolorach marki), nie oficjalny znak Google Play. Część przed „Google Play” idzie małym pismem."""
    pre, sep, _ = text.partition("Google Play")
    words = (f'<span class="small">{escape(pre.strip())}</span><span class="big">Google Play</span>'
             if sep else f'<span class="big">{escape(text)}</span>')
    mark = ('<svg class="mark" viewBox="0 0 32 32" aria-hidden="true">'
            '<path d="M9 5.6c0-1.6 1.7-2.5 3-1.7l15.2 10.4c1.2.8 1.2 2.6 0 3.4L12 28.1c-1.3.9-3-.1-3-1.7z" fill="#E9846A"/>'
            '<path d="M13.2 12.5l3.6 3.5-3.6 3.5M17.6 12.5l3.6 3.5-3.6 3.5" fill="none" stroke="#FBF7F2" stroke-width="1.75" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')
    c = f"store {cls}".strip()
    if href:
        return f'<a class="{c} link" href="{href}" aria-label="{escape(text)}">{mark}<span class="words">{words}</span></a>'
    return f'<div class="{c}" role="img" aria-label="{escape(text)}">{mark}<span class="words">{words}</span></div>'


# --- Zrzuty: prawdziwe PNG z assets/shots/<lang>/, a do czasu ich powstania szkice SVG z _szkic/
SKETCH = {"eink": (900, 1200), "phone": (540, 1170), "tablet": (1280, 800),
          "step1": (540, 1170), "step2": (540, 1170), "step3": (540, 1170)}


def shot(lang, name):
    """Ścieżka zrzutu względem korzenia strony: PNG danego języka, jeśli jest, inaczej szkic."""
    png = f"assets/shots/{lang}/{name}.png"
    return png if (ROOT / png).exists() else f"assets/shots/_szkic/{name}.svg"


def shot_size(path, name):
    """Szerokość i wysokość do atrybutów <img> (proporcje rezerwują miejsce przed wczytaniem)."""
    if path.endswith(".png"):
        with open(ROOT / path, "rb") as f:
            head = f.read(24)
        return struct.unpack(">II", head[16:24])
    return SKETCH[name]


def img(t, lang, up, name, lazy=True):
    path = shot(lang, name)
    w, h = shot_size(path, name)
    extra = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="{up}{path}" width="{w}" height="{h}" alt="{escape(t["alt"][name])}"{extra}>'


def text(s):
    """Tekst do treści strony: escape + „e-ink” w jednym kawałku (bez łamania na „E-” / „Ink”
    w nagłówkach; dotyczy też odmian: e-inku, E-Ink-Tablets)."""
    return re.sub(r"(?i)\be-ink[\w-]*", lambda m: f'<span class="nw">{m.group(0)}</span>', escape(s))


def device(kind, inner):
    """Ramka urządzenia z CSS: e-ink (grafit, szerszy dolny margines jak BOOX), telefon, tablet."""
    return f'<div class="device {kind}"><div class="screen">{inner}</div></div>'


def home(lang):
    return "" if lang == "en" else f"{lang}/"


def page(lang):
    t = T[lang]
    up = "" if lang == "en" else "../"          # do korzenia strony
    e = text                                    # tekst w treści; w atrybutach samo escape()
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="https://gabiknits.app/{home(l)}">' for l in LANGS
    ) + '\n<link rel="alternate" hreflang="x-default" href="https://gabiknits.app/">'
    href = lambda l: f"{up}{home(l)}"
    # Kolejność w menu jak sekcje na stronie: od 2026-10-24 e-ink po funkcjach (wcześniej pierwszy) -
    # stronę otwierają telefon i tablet, e-ink to atut dla tych, którzy go mają.
    ids = ["how", "features", "eink", "faq", "contact"]
    nav = list(t["nav"])
    labels = nav[1:3] + nav[0:1] + nav[3:]
    if SHOW_PRICE:
        ids.insert(3, "price")
        labels.insert(3, t["price_title"])
    links = "".join(f'<a href="#{i}">{e(n)}</a>' for i, n in zip(ids, labels))
    privacy = f'{up}{home(lang)}privacy/'
    terms = f'{up}{home(lang)}terms/'
    # „Postaw kawę” (2026-10-22): mały odnośnik tylko w stopce strony głównej, w językach, które mają
    # klucz "tip" i stronę xx/tip/. Nigdy w polityce prywatności ani regulaminie - te strony otwiera
    # aplikacja, a Google Play zdejmuje aplikacje prowadzące do płatności poza sklepem (AnkiDroid 2026).
    # Po uwadze użytkownika (sam odnośnik w stopce był niewidoczny): także pas z filiżanką pod blokiem
    # kontaktu, na samym końcu strony - z dala od góry strony i od pobierania aplikacji.
    tip_url = f"{up}{home(lang)}tip/"
    tip = (f' · <a class="foot-tip" href="{tip_url}">{icon("coffee")}<span>{e(t["tip"])}</span></a>'
           if "tip" in t else "")
    tipband = (f'<section class="sec tipband"><div class="wrap"><div class="tip-card">'
               f'<span class="badge-ico">{icon("coffee")}</span>'
               f'<div class="tip-text"><h2>{e(t["tip_title"])}</h2><p>{e(t["tip_text"])}</p></div>'
               f'<a class="tip-go" href="{tip_url}">{icon("coffee")}<span>{e(t["tip"])}</span></a>'
               f'</div></div></section>\n' if "tip" in t else "")

    trust = "".join(f"<li>{icon('check')}<span>{e(x)}</span></li>" for x in t["hero_trust"])
    pillars = "".join(
        f'<div class="pillar"><span class="badge-ico">{icon(PILLAR_ICONS[k])}</span>'
        f"<div><h3>{e(a)}</h3><p>{e(b)}</p></div></div>"
        for k, (a, b) in enumerate(t["pillars"])
    )
    epoints = "".join(
        f'<li><span class="sq">{icon(EINK_ICONS[k])}</span><div><h3>{e(a)}</h3><p>{e(b)}</p></div></li>'
        for k, (a, b) in enumerate(t["eink_points"])
    )
    steps = "".join(
        f'<li class="step"><div class="tile">{device("phone", img(t, lang, up, f"step{k}"))}</div>'
        f'<div class="step-text"><span class="n" aria-hidden="true">{k}</span><h3>{e(a)}</h3><p>{e(b)}</p></div></li>'
        for k, (a, b) in enumerate(t["steps"], 1)
    )
    feats = "".join(
        f'<li class="card"><span class="badge-ico">{icon(FEAT_ICONS[k])}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>'
        for k, (a, b) in enumerate(t["feats"])
    )
    plans = ""
    for k, (name, price, per, trial) in enumerate(t["plans"]):
        best = k == 1
        plans += (
            f'<div class="plan{" best" if best else ""}">'
            + (f'<span class="tag">{e(t["best"])}</span>' if best else "")
            + f'<h3 class="name">{e(name)}</h3><div class="price">{e(price)}</div>'
            + f'<div class="per">{e(per)}</div>'
            + f'<div class="trial">{icon("check")}<span>{t["trial_yes"] if trial else e(t["trial_no"])}</span></div></div>'
        )
    # Film z Gabi (Veo, 8 s) - zapętlony, bez dźwięku. Przy „ograniczaniu ruchu” w systemie zostaje
    # sam kadr (CSS ukrywa film). Bez skryptów, więc film wczytuje się razem ze stroną (2,4 MB).
    film = (f'<div class="cta-film">'
            f'<video class="motion" src="{up}assets/media/gabi.mp4" poster="{up}assets/media/gabi.jpg" '
            f'autoplay muted loop playsinline preload="auto" width="960" height="540" aria-hidden="true"></video>'
            f'<img class="still" src="{up}assets/media/gabi.jpg" width="960" height="540" alt="{escape(t["video_alt"])}" loading="lazy" decoding="async">'
            f'</div>')
    if LAUNCHED:
        side = (f'<h2>{e(t["get_title"])}</h2><p>{e(t["get_text"])}</p>'
                f'{play_badge(t["get_badge"], "light on-dark", href=play_url(lang))}'
                f'<p class="cta-small">{e(t["get_contact"])} <a class="mail-link" href="mailto:{EMAIL}">{EMAIL}</a></p>')
    else:
        side = (f'<h2>{e(t["cta_title"])}</h2><p>{e(t["cta_text"])}</p>'
                f'<a class="mail" href="mailto:{EMAIL}">{icon("mail")}<span>{EMAIL}</span></a>')
    cta = (f'<section id="contact" class="sec cta"><div class="wrap"><div class="cta-card">'
           f'{film}<div class="cta-main">{side}</div></div></div></section>')
    price = (
        f"""<section id="price" class="sec pricing"><div class="wrap">
  <header class="sec-head center"><h2>{e(t["price_title"])}</h2><p class="lead">{e(t["price_lead"])}</p></header>
  <div class="plans">{plans}</div>
  <p class="note">{e(t["price_note"])}</p>
</div></section>

"""
        if SHOW_PRICE else ""
    )
    ppoints = "".join(f"<li>{icon('check')}<span>{e(p)}</span></li>" for p in t["priv_points"])
    faq = "".join(
        f'<details><summary><span>{e(q)}</span><i aria-hidden="true"></i></summary><p>{e(a)}</p></details>'
        for q, a in t["faq"]
    )
    sh = t["shots"]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(t["title"])}</title>
<meta name="description" content="{escape(t["desc"])}">
<meta name="theme-color" content="#FBF7F2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121820" media="(prefers-color-scheme: dark)">
<link rel="icon" type="image/png" href="{up}favicon.png">
<link rel="preload" href="{up}assets/prata.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="{up}assets/site.css">
{alts}
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="{href(lang)}"><img src="{up}assets/logo.png" alt="" width="44" height="44">Gabi Knits</a>
  <nav class="nav" aria-label="{escape(MENU[lang])}">{links}</nav>
  <div class="langs-top">{lang_nav(lang, href, key="t")}</div>
  <details class="menu">
    <summary>{icon("menu")}<span>{e(MENU[lang])}</span></summary>
    <div class="menu-panel">
      <nav class="menu-links" aria-label="{escape(MENU[lang])}">{links}</nav>
      {lang_nav(lang, href, key="m")}
    </div>
  </details>
</div></header>
<main>
<section class="hero"><div class="wrap">
  <div class="hero-text">
    <p class="eyebrow">{e(t["hero_eyebrow"])}</p>
    <h1>{e(t["hero_title"])}</h1>
    <p class="hero-lead">{e(t["hero_text"])}</p>
    {play_badge(t["get_badge"], href=play_url(lang)) if LAUNCHED else play_badge(t["soon"])}
    <ul class="trust">{trust}</ul>
  </div>
  <div class="stage">
    {device("tablet", img(t, lang, up, "tablet", lazy=False))}
    {device("phone", img(t, lang, up, "phone", lazy=False))}
  </div>
</div></section>

<section class="pillars-sec"><div class="wrap"><div class="pillars">{pillars}</div></div></section>

<section id="how" class="sec how"><div class="wrap">
  <header class="sec-head center"><h2>{e(t["how_title"])}</h2><p class="lead">{e(t["how_lead"])}</p></header>
  <ol class="steps">{steps}</ol>
</div></section>

<section id="features" class="sec features"><div class="wrap">
  <header class="sec-head center"><h2>{e(t["feat_title"])}</h2><p class="lead">{e(t["feat_lead"])}</p></header>
  <ul class="cards">{feats}</ul>
</div></section>

<section id="eink" class="sec eink"><div class="wrap">
  <div class="eink-shot">{device("eink", img(t, lang, up, "eink"))}</div>
  <div class="eink-text">
    <p class="eyebrow">{e(t["eink_eyebrow"])}</p>
    <h2>{e(t["eink_title"])}</h2>
    <p class="lead">{e(t["eink_text"])}</p>
    <ul class="epoints">{epoints}</ul>
  </div>
</div></section>

<section class="sec devices"><div class="wrap">
  <header class="sec-head center"><h2>{e(t["devices_title"])}</h2><p class="lead">{e(t["devices_lead"])}</p></header>
  <div class="trio">
    <figure class="d-phone">{device("phone", img(t, lang, up, "step3"))}<figcaption>{e(sh[1])}</figcaption></figure>
    <figure class="d-tablet">{device("tablet", img(t, lang, up, "tablet"))}<figcaption>{e(sh[2])}</figcaption></figure>
    <figure class="d-eink">{device("eink", img(t, lang, up, "eink"))}<figcaption>{e(sh[0])}</figcaption></figure>
  </div>
</div></section>

{price}<section class="sec privacy"><div class="wrap">
  <div class="priv-card">
    <div class="priv-main">
      <span class="badge-ico big">{icon("lock")}</span>
      <h2>{e(t["priv_title"])}</h2>
      <p>{e(t["priv_text"])}</p>
      <a class="more" href="{privacy}">{e(t["priv_link"])}{icon("arrow")}</a>
    </div>
    <ul class="priv-points">{ppoints}</ul>
  </div>
</div></section>

<section id="faq" class="sec faq"><div class="wrap">
  <header class="sec-head"><h2>{e(t["faq_title"])}</h2></header>
  <div class="faq-list">{faq}</div>
</div></section>

{cta}
{tipband}</main>
<footer class="foot"><div class="wrap">
  <div class="foot-row">
    <a class="brand" href="{href(lang)}"><img src="{up}assets/logo.png" alt="" width="36" height="36" loading="lazy">Gabi Knits</a>
    {lang_nav(lang, href, key="f")}
  </div>
  <div class="foot-row small">
    <span>{e(COMPANY)} · <span class="nw">{e(t["vat"])}</span></span>
    <span><a href="{privacy}">{e(t["privacy"])}</a> · <a href="{terms}">{e(t["terms"])}</a>{tip} · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  </div>
</div></footer>
</body>
</html>
"""


for lang in LANGS:
    out = ROOT / home(lang) / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(lang), encoding="utf-8")
    print("zapisano", out.relative_to(ROOT))

# Polityka prywatności i regulamin (2026-10-17) są pisane ręcznie - generator podmienia w nich tylko przełącznik języków
# i (od 2026-10-25, przy dodaniu czeskiego) listę <link rel="alternate" hreflang> w nagłówku, żeby nowy język
# w LANGS nie wymagał ręcznej poprawki czternastu plików.
for doc in ("privacy", "terms"):
    for lang in LANGS:
        path = ROOT / home(lang) / doc / "index.html"
        up = "../" if lang == "en" else "../../"
        text = path.read_text(encoding="utf-8")
        nav = lang_nav(lang, lambda l: f"{up}{home(l)}{doc}/")
        text, n = re.subn(r'<nav class="lang"[^>]*>.*?</nav>', lambda _: nav, text, count=1, flags=re.S)
        assert n == 1, path
        alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{up}{home(l)}{doc}/">\n' for l in LANGS)
        text, n = re.subn(r'(?:<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n)+', lambda _: alts, text, count=1)
        assert n == 1, path
        path.write_text(text, encoding="utf-8")
        print("przełącznik języków:", path.relative_to(ROOT))

# Mapa witryny i robots.txt dla Google Search Console (2026-10-27): wszystkie strony index.html z repozytorium
# poza oznaczonymi „noindex” (strona testerek), więc nowa strona albo język trafiają do mapy same.
SITE = "https://gabiknits.app/"
pages = []
for path in sorted(ROOT.rglob("index.html")):
    rel = path.relative_to(ROOT)
    if rel.parts[0].startswith(".") or "noindex" in path.read_text(encoding="utf-8"):
        continue
    pages.append(SITE + ("" if rel.parent == Path(".") else rel.parent.as_posix() + "/"))
pages.sort(key=lambda u: (u.count("/"), u))
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc></url>\n" for u in pages) + "</urlset>\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8")
print(f"mapa witryny: {len(pages)} stron, robots.txt")
