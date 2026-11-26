#!/usr/bin/env python3
"""A página do grupo (/grupo/ e /en/group/): os outros sites do grupo d'O Carro
Elétrico, cada um com a sua mascote ao lado de um balão. Todos os sites do grupo
têm esta página no seu estilo, com a mesma ordem e os mesmos textos: a
referência é o GRUPO do O Carro Elétrico (scripts/oce.py e site/strings.json
de lá), por isso uma mudança começa lá.

Stdlib só. O pages.yml corre-o ao montar o site:

    python3 scripts/build_grupo.py public

Escreve public/grupo/index.html, public/en/group/index.html e copia as
imagens de assets/grupo/ (a marca de cada site; pano.svg é o logótipo do
Panoramax) para public/grupo/.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "grupo"
SITE = "https://nap.ocarroeletrico.com"
GH = "https://github.com/CarregaErvilhas/"
PATHS = {"pt": "/grupo/", "en": "/en/group/"}

# A ordem é a mesma em todos os sites do grupo; este diz "Estás aqui".
# O AmpereArchive não tem página para visitar e o código é privado, por agora.
GROUP = [
    {"id": "carro", "site": "https://ocarroeletrico.com/", "repo": GH + "OCarroEletrico"},
    {"id": "ohmigo", "site": "https://ohmigo.ocarroeletrico.com/", "repo": GH + "ohmigo-mcp"},
    {"id": "voltaria", "site": "https://voltaria.ocarroeletrico.com/", "repo": GH + "voltaria"},
    {"id": "ceme", "site": "https://ceme.ocarroeletrico.com/", "repo": GH + "CEME"},
    {"id": "nap", "here": True, "repo": GH + "nap-dashboard"},
    {"id": "oop", "site": "https://olhaoposto.ocarroeletrico.com/", "repo": GH + "OlhaOPosto"},
    {"id": "pano", "site": "https://panoramax.ocarroeletrico.com/", "repo": GH + "OlhaOPosto/tree/main/panoramax"},
    {"id": "ampere", "repo": GH + "AmpereArchive", "private": True},
]

T = {
    "pt": {
        "html_lang": "pt-PT", "og_locale": "pt_PT",
        "title": "Os sites do grupo | Postos PT",
        "desc": "O Carro Elétrico, o ohmigo, o Voltaria, o Comparador CEME, o Postos PT, o olh'o'posto, o Panoramax e o AmpereArchive: o que faz cada um e onde está o código.",
        "eyebrow": "O grupo",
        "h1": "Eu conto os postos. Para o resto, há vizinhos.",
        "lead": "Onde estão os postos, se estão livres e o que o NAP diz deles, isso é comigo. Quanto custa carregar, o que diz a lei ou como é o posto já são perguntas de outros sites, feitos pela mesma comunidade. O código de todos está no GitHub.",
        "bubble": "Pus os vizinhos no mapa.",
        "self_alt": "O pino de mapa azul do Postos PT, com cara e um raio",
        "open": "Abrir o site", "here": "Estás aqui", "code": "Código no GitHub", "private": "GitHub (privado, por agora)",
        "back": "Voltar ao dashboard", "other": "EN", "other_title": "English",
        "sites": {
            'carro': {"name": "O Carro Elétrico", "host": "ocarroeletrico.com", "desc": "A mobilidade elétrica em Portugal explicada a quem conduz: carregar em casa e na rua, condomínio, instalação, apoios e impostos. Cada facto com a lei e a fonte.", "mascot": "O carrinho repórter d'O Carro Elétrico, cor de laranja, com chapéu de imprensa e microfone"},
            'ohmigo': {"name": "ohmigo", "host": "ohmigo.ocarroeletrico.com", "desc": "Pergunta ao ChatGPT ou ao Claude quanto custa carregar e onde fica mais barato. O ohmigo conhece os preços de todos os postos públicos do país, dentro e fora da rede MOBI.E.", "mascot": "O ohmi, a ficha verde com cara do ohmigo"},
            'voltaria': {"name": "Voltaria", "host": "voltaria.ocarroeletrico.com", "desc": "O conhecimento por trás dos outros: a lei, as normas e as regras da mobilidade elétrica em Portugal, escritas para assistentes de IA. Cada facto com a sua fonte.", "mascot": "O livro azul do Voltaria, com um raio na capa"},
            'ceme': {"name": "Comparador CEME", "host": "ceme.ocarroeletrico.com", "desc": "Compara os tarifários de quem te vende a energia na rede MOBI.E. Faz as contas com as tarifas de acesso às redes, o preço do mercado ibérico e os impostos, à hora a que carregas.", "mascot": "A mascote do Comparador CEME, uma calculadora cor-de-rosa com um raio no ecrã"},
            'nap': {"name": "Postos PT", "host": "nap.ocarroeletrico.com", "desc": "Todos os postos públicos que o Ponto de Acesso Nacional publica. Procura perto de ti, vê o estado ao vivo, as estatísticas da rede e os erros nos dados.", "mascot": "O pino de mapa azul do Postos PT, com cara e um raio"},
            'oop': {"name": "olh'o'posto", "host": "olhaoposto.ocarroeletrico.com", "desc": "Fotos dos postos e das tomadas, tiradas pela comunidade. Cada posto tem um link que nunca muda, pelo ID oficial, para qualquer app ou mapa mostrar como é o posto antes de lá chegares.", "mascot": "O Pic, a ficha Type 2 cor de âmbar do olh'o'posto, com uma objetiva e um flash"},
            'pano': {"name": "Panoramax", "host": "panoramax.ocarroeletrico.com", "desc": "Onde ficam guardadas as fotos do olh'o'posto, com o mapa e o visualizador. É um servidor Panoramax, o software livre de fotos de rua que o OpenStreetMap usa, montado só para postos de carregamento.", "mascot": "O logótipo do Panoramax"},
            'ampere': {"name": "AmpereArchive", "host": "ohm-age.ocarroeletrico.com", "desc": "Guarda a história dos postos. Lê o NAP a cada minuto e arquiva o que mudou, porque o NAP só mostra o presente. É daqui que o ohmigo tira o estado ao vivo e o Postos PT o histórico.", "mascot": "A caixa de arquivo roxa do AmpereArchive, de óculos e com um cronómetro", "note": "Não tem página para visitar: é um arquivo de dados que os outros leem."},
        },
    },
    "en": {
        "html_lang": "en", "og_locale": "en_GB",
        "title": "The group's sites | Postos PT",
        "desc": "O Carro Elétrico, ohmigo, Voltaria, the CEME comparator, Postos PT, olh'o'posto, Panoramax and AmpereArchive: what each one does and where the code is.",
        "eyebrow": "The group",
        "h1": "I count the chargers. For the rest, there are neighbours.",
        "lead": "Where the chargers are, whether they're free and what the NAP says about them, that's my job. What a charge costs, what the law says or what a charger looks like are questions for other sites, made by the same community. All their code is on GitHub.",
        "bubble": "I put the neighbours on the map.",
        "self_alt": "Postos PT's blue map pin, with a face and a lightning bolt",
        "open": "Open the site", "here": "You are here", "code": "Code on GitHub", "private": "GitHub (private, for now)",
        "back": "Back to the dashboard", "other": "PT", "other_title": "Português",
        "sites": {
            'carro': {"name": "O Carro Elétrico", "host": "ocarroeletrico.com", "desc": "Electric mobility in Portugal explained for drivers: charging at home and on the road, condos, installation, grants and tax. Every fact with the law and its source.", "mascot": "O Carro Elétrico's little reporter car, orange, with a press hat and a microphone"},
            'ohmigo': {"name": "ohmigo", "host": "ohmigo.ocarroeletrico.com", "desc": "Ask ChatGPT or Claude what a charge costs and where it's cheapest. ohmigo knows the prices of every public charger in the country, on the MOBI.E network and off it.", "mascot": "Ohmi, ohmigo's green plug with a face"},
            'voltaria': {"name": "Voltaria", "host": "voltaria.ocarroeletrico.com", "desc": "The knowledge behind the others: the law, the standards and the rules of electric mobility in Portugal, written for AI assistants. Every fact with its source.", "mascot": "Voltaria's blue book, with a lightning bolt on the cover"},
            'ceme': {"name": "CEME comparator", "host": "ceme.ocarroeletrico.com", "desc": "Compares the tariffs of whoever sells you the energy on the MOBI.E network. It does the maths with the grid access tariffs, the Iberian market price and the taxes, at the hour you charge.", "mascot": "The CEME comparator's mascot, a pink calculator with a lightning bolt on its screen"},
            'nap': {"name": "Postos PT", "host": "nap.ocarroeletrico.com", "desc": "Every public charger the National Access Point publishes. Search near you, see the live status, the network's statistics and the errors in the data.", "mascot": "Postos PT's blue map pin, with a face and a lightning bolt"},
            'oop': {"name": "olh'o'posto", "host": "olhaoposto.ocarroeletrico.com", "desc": "Photos of chargers and their sockets, taken by the community. Every charger has a link that never changes, by its official ID, so any app or map can show what it looks like before you get there.", "mascot": "Pic, olh'o'posto's amber Type 2 plug, with a lens and a flash"},
            'pano': {"name": "Panoramax", "host": "panoramax.ocarroeletrico.com", "desc": "Where olh'o'posto's photos are stored, with the map and the viewer. It's a Panoramax server, the free street-photo software OpenStreetMap uses, set up for charging stations only.", "mascot": "The Panoramax logo"},
            'ampere': {"name": "AmpereArchive", "host": "ohm-age.ocarroeletrico.com", "desc": "Keeps the chargers' history. It reads the NAP every minute and archives what changed, because the NAP only shows the present. ohmigo gets its live status from here, and Postos PT its history.", "mascot": "AmpereArchive's purple archive box, with glasses and a stopwatch", "note": "There's no page to visit: it's a data archive the others read."},
        },
    },
}

ICON_CODE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 7 3 12l5 5M16 7l5 5-5 5M14 4l-4 16"/></svg>'
ICON_LOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/></svg>'

# Cores de cada site, só para o círculo atrás da mascote e o ponto antes do endereço.
COLORS = {"carro": "#ff6b4a", "ohmigo": "#22c55e", "voltaria": "#2f5bd0", "ceme": "#db2777",
          "nap": "#0284c7", "oop": "#f2b33d", "pano": "#8f2a85", "ampere": "#8b5cf6"}

CSS = """
:root { --bg:#0f172a; --card:#1e293b; --ink:#e2e8f0; --mut:#94a3b8; --acc:#38bdf8; --line:#334155; }
* { box-sizing:border-box; margin:0; padding:0; }
body { background:var(--bg); color:var(--ink); font:16px/1.55 -apple-system,Segoe UI,Roboto,sans-serif; padding:24px; }
a, a:visited { color:var(--acc); }
.wrap { max-width:1000px; margin:0 auto; }
.top { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:28px; font-size:14px; }
.top .lang { border:1px solid var(--line); border-radius:6px; padding:4px 12px; font-weight:700; font-size:12px; text-decoration:none; color:var(--mut); }
.hero { display:grid; grid-template-columns:minmax(0,1fr) 240px; gap:24px 40px; align-items:center; margin-bottom:44px; }
.eyebrow { display:inline-block; color:var(--acc); font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:.06em; margin-bottom:10px; }
h1 { font-size:clamp(26px,4vw,38px); line-height:1.15; margin-bottom:12px; }
.lead { color:var(--mut); font-size:17px; max-width:40em; }
.stage { position:relative; display:grid; place-items:center; aspect-ratio:1; }
.stage::before, .pic::before { content:""; position:absolute; inset:5%; border-radius:50%; background:color-mix(in srgb, var(--c) 30%, var(--bg)); }
.stage img { position:relative; width:62%; height:auto; }
.bubble { position:absolute; top:0; right:0; max-width:11em; background:var(--card); border:1px solid var(--line); border-radius:12px 12px 12px 3px; padding:8px 12px; font-weight:600; font-size:14px; }
.mates { list-style:none; display:flex; flex-direction:column; gap:28px; }
.mate { display:grid; grid-template-columns:150px minmax(0,1fr); gap:22px; align-items:center; max-width:820px; }
.mate:nth-child(even) { grid-template-columns:minmax(0,1fr) 150px; margin-left:auto; }
.mate:nth-child(even) .pic { order:2; }
.pic { position:relative; display:grid; place-items:center; aspect-ratio:1; }
.pic img { position:relative; width:72%; height:auto; max-height:82%; object-fit:contain; }
.say { position:relative; background:var(--card); border-radius:10px; padding:18px 20px; }
.say::before { content:""; position:absolute; top:50%; left:-8px; width:16px; height:16px; margin-top:-8px; background:var(--card); transform:rotate(45deg); }
.mate:nth-child(even) .say::before { left:auto; right:-8px; }
.say h2 { font-size:22px; margin:2px 0 6px; }
.say p { margin-bottom:10px; }
.host { display:flex; align-items:center; gap:8px; color:var(--mut); font-size:13px; font-weight:600; overflow-wrap:anywhere; }
.host::before { content:""; flex:none; width:9px; height:9px; border-radius:50%; background:var(--c); }
.note { color:var(--mut); font-size:14px; }
.links { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:4px 0 0 !important; }
.btn { display:inline-flex; align-items:center; gap:8px; min-height:44px; padding:8px 16px; border-radius:6px; font-weight:700; font-size:14px; text-decoration:none; }
a.btn.main, a.btn.main:visited { background:var(--acc); color:#0b1220; }
a.btn.line, a.btn.line:visited { border:1px solid var(--line); color:var(--ink); }
.btn svg { width:17px; height:17px; fill:none; stroke:currentColor; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }
.here { background:#164e63; color:#a5f3fc; }
footer { color:var(--mut); font-size:12px; margin-top:40px; padding-top:12px; border-top:1px solid #27334a; }
@media (max-width:720px) {
  body { padding:16px; }
  .hero { grid-template-columns:minmax(0,1fr); }
  .stage { width:190px; margin:0 auto; }
  .mate, .mate:nth-child(even) { grid-template-columns:minmax(0,1fr); gap:6px; margin-left:0; }
  .mate .pic, .mate:nth-child(even) .pic { order:0; width:120px; margin:0 auto; }
  .say::before, .mate:nth-child(even) .say::before { top:-8px; left:50%; right:auto; margin:0 0 0 -8px; }
}
@media (forced-colors:active) { .stage::before, .pic::before, .say::before { display:none; } .say { border:1px solid CanvasText; } }
"""

# O favicon do dashboard: o raio azul sobre o fundo escuro.
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230f172a'/%3E"
           "%3Cpath d='M37 6 15 37h14l-4 21 22-31H33z' fill='%2338bdf8'/%3E%3C/svg%3E")


def esc(s):
    return html.escape(s, quote=True)


def size(id_):
    """O tamanho do viewBox de cada SVG, para a página não saltar enquanto as imagens carregam."""
    svg = (ASSETS / f"{id_}.svg").read_text(encoding="utf-8")
    w, h = re.search(r'viewBox="[\d.-]+ [\d.-]+ ([\d.]+) ([\d.]+)"', svg).groups()
    return round(float(w)), round(float(h))


def mate(lang, g):
    t = T[lang]
    s = t["sites"][g["id"]]
    w, h = size(g["id"])
    if g.get("here"):
        go = f'<span class="btn here">{t["here"]}</span>'
    elif g.get("site"):
        go = f'<a class="btn main" href="{esc(g["site"])}">{t["open"]} <span aria-hidden="true">→</span></a>'
    else:
        go = ""
    code = f'<a class="btn line" href="{esc(g["repo"])}">{ICON_LOCK if g.get("private") else ICON_CODE}{t["private"] if g.get("private") else t["code"]}</a>'
    note = f'\n      <p class="note">{esc(s["note"])}</p>' if s.get("note") else ""
    return f"""  <li class="mate" style="--c:{COLORS[g['id']]}">
    <div class="pic"><img src="/grupo/{g['id']}.svg" alt="{esc(s['mascot'])}" width="{w}" height="{h}" loading="lazy"></div>
    <div class="say">
      <p class="host">{esc(s['host'])}</p>
      <h2>{esc(s['name'])}</h2>
      <p>{esc(s['desc'])}</p>{note}
      <p class="links">{go}{code}</p>
    </div>
  </li>"""


def page(lang):
    t = T[lang]
    other = "en" if lang == "pt" else "pt"
    url = SITE + PATHS[lang]
    w, h = size("nap")
    jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": t["title"], "url": url,
              "inLanguage": t["html_lang"],
              "hasPart": [{"@type": "WebSite", "name": t["sites"][g["id"]]["name"], "url": g.get("site") or SITE + "/"}
                          for g in GROUP if g.get("site") or g.get("here")]}
    # < escapado: nenhuma string fecha o <script>.
    ld = json.dumps(jsonld, ensure_ascii=False).replace("<", "\\u003c")
    items = "\n".join(mate(lang, g) for g in GROUP)
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t['title'])}</title>
<meta name="description" content="{esc(t['desc'])}">
<link rel="icon" href="{FAVICON}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="pt-PT" href="{SITE + PATHS['pt']}">
<link rel="alternate" hreflang="en" href="{SITE + PATHS['en']}">
<link rel="alternate" hreflang="x-default" href="{SITE + PATHS['pt']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="EV NAP Portugal">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(t['title'])}">
<meta property="og:description" content="{esc(t['desc'])}">
<meta property="og:locale" content="{t['og_locale']}">
<meta property="og:image" content="{SITE}/dashboard.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f172a">
<script type="application/ld+json">{ld}</script>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<nav class="top"><a href="/{'' if lang == 'pt' else '?lang=en'}">← {t['back']}</a><a class="lang" href="{PATHS[other]}" hreflang="{T[other]['html_lang']}" lang="{T[other]['html_lang']}" title="{t['other_title']}">{t['other']}</a></nav>
<main>
<section class="hero">
  <div>
    <span class="eyebrow">{t['eyebrow']}</span>
    <h1>{t['h1']}</h1>
    <p class="lead">{t['lead']}</p>
  </div>
  <div class="stage" style="--c:{COLORS['nap']}">
    <img src="/grupo/nap.svg" alt="{esc(t['self_alt'])}" width="{w}" height="{h}">
    <p class="bubble">{t['bubble']}</p>
  </div>
</section>
<ol class="mates">
{items}
</ol>
</main>
<footer>© O Carro Elétrico / Fernando Miguel · <a href="https://github.com/CarregaErvilhas/nap-dashboard">GitHub</a></footer>
</div>
</body>
</html>
"""


def main(out):
    out = Path(out)
    for lang, path in PATHS.items():
        dest = out / path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(lang), encoding="utf-8")
    for g in GROUP:
        shutil.copyfile(ASSETS / f"{g['id']}.svg", out / "grupo" / f"{g['id']}.svg")
    print(f"grupo: {', '.join(PATHS.values())} em {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "public")
