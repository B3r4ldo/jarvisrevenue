#!/usr/bin/env python3
"""SeuPetFeliz: validate curated affiliate CSV and render responsive static storefront."""
import csv
import html
import json
import pathlib
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "products.csv"
PREVIEW = ROOT / "preview" / "vitrine.html"
OUT = ROOT / "site"
REQUIRED = {"id", "title", "category", "description", "url", "status"}
ALLOWED_HOSTS = {"link.amazon", "amazon.com.br", "www.amazon.com.br", "amzn.to"}

def validate_link(url):
    try:
        p = urlparse(url)
        return p.scheme == "https" and p.hostname in ALLOWED_HOSTS and not p.username and not p.password
    except ValueError:
        return False

def load_products(source=SOURCE):
    with open(source, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise ValueError("Faltam colunas: " + ", ".join(sorted(REQUIRED - set(reader.fieldnames or []))))
        seen, approved = set(), []
        for line, row in enumerate(reader, 2):
            if None in row:
                raise ValueError(f"Linha {line}: colunas extras ou vírgula sem aspas")
            if (row.get("status") or "").strip().lower() != "approved":
                continue
            p = {key: (row.get(key) or "").strip() for key in REQUIRED}
            if any(not p[key] for key in ("id", "title", "category", "description")):
                raise ValueError(f"Linha {line}: campo obrigatório vazio")
            if p["id"] in seen:
                raise ValueError(f"Linha {line}: id duplicado")
            if not validate_link(p["url"]):
                raise ValueError(f"Linha {line}: use link HTTPS autorizado da Amazon")
            seen.add(p["id"])
            approved.append(p)
    return approved

def image_for(title, category):
    t = title.casefold()
    if any(x in t for x in ("tapete", "pad", "seco", "secão")):
        return "training-pad"
    if any(x in t for x in ("areia", "granulado", "pipicat", "viva verde", "mitzi", "great pets")):
        return "cat-litter"
    if any(x in t for x in ("bifinho", "biscrok", "dreamies", "temptations", "petisco")):
        return "treats"
    if any(x in t for x in ("sachê", "sache")):
        return "wet-food"
    if any(x in t for x in ("ração", "racao", "whiskas adultos")):
        return "dry-food"
    if any(x in t for x in ("macaco", "pelúcia", "pelucia", "brinquedo")):
        return "plush-toy"
    if any(x in t for x in ("saquinho", "cata-caca")):
        return "poop-bags"
    return "treats" if category == "Cães" else "training-pad"

def product_card(p):
    e = lambda value: html.escape(value, quote=True)
    img = "../preview/assets/" + image_for(p["title"], p["category"]) + ".svg"
    search = (p["title"]+" "+p["description"]+" "+p["category"]).casefold()
    return (
        '<article class="product" data-search="'+e(search)+'" data-category="'+e(p["category"])+'">'
        '<div class="product-visual"><img src="'+e(img)+'" alt="Ilustração representativa do tipo de produto" loading="lazy">'
        '<small>Imagem ilustrativa</small></div>'
        '<div class="product-content"><span class="tag">'+e(p["category"])+'</span>'
        '<h4>'+e(p["title"])+'</h4>'
        '<p>Confira a embalagem, variante e disponibilidade diretamente na Amazon.</p>'
        '<a class="btn" href="'+e(p["url"])+'" rel="sponsored nofollow noopener noreferrer" target="_blank">Ver na Amazon →</a>'
        '</div></article>'
    )


def build(products, template):
    """Generate the commercial storefront from the approved product catalog."""
    start_marker = '<div class="products" id="catalogGrid">'
    end_marker = '</div></section><section class="features">'
    first = template.find(start_marker)
    if first < 0:
        raise ValueError("Product grid marker missing from storefront template")
    after_grid = template.find(end_marker, first)
    if after_grid < 0:
        raise ValueError("Grid closing marker missing")
    return template[:first + len(start_marker)] + ''.join(product_card(p) for p in products) + template[after_grid:]


def main():
    products = load_products()
    template = PREVIEW.read_text(encoding="utf-8")
    page = build(products, template)
    page = page.replace("../preview/assets/", "assets/")
    OUT.mkdir(parents=True, exist_ok=True)
    import shutil
    assets = OUT / "assets"
    assets.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "preview" / "favicon.svg", OUT / "favicon.svg")
    for source in (ROOT / "preview" / "assets").glob("*.svg"):
        shutil.copy2(source, assets / source.name)
    (OUT/"index.html").write_text(page, encoding="utf-8")
    (OUT/"robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    (OUT/"catalog.json").write_text(json.dumps({
        "generated_utc":datetime.now(timezone.utc).isoformat(),
        "count":len(products),
        "categories":sorted({p["category"] for p in products})
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SeuPetFeliz: {len(products)} products generated")

if __name__ == "__main__":
    main()
