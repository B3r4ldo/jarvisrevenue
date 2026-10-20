#!/usr/bin/env python3
"""BeraldoSales: validate curated affiliate CSV and render responsive static storefront."""
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

IMAGES = {
    "Cães": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=680&q=80",
    "Gatos": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=680&q=80",
    "Brinquedos": "https://images.unsplash.com/photo-1535294435445-d7249524ef2e?w=680&q=80",
    "Acessórios": "https://images.unsplash.com/photo-1601758125946-6ec2ef64daf8?w=680&q=80",
    "Higiene": "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=680&q=80",
    "Ofertas": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=680&q=80",
}

def product_card(p):
    e = lambda s: html.escape(s, quote=True)
    photo = IMAGES.get(p["category"], IMAGES["Cães"])
    search = (p["title"]+" "+p["category"]).casefold()
    return (
        '<article class="product" data-search="'+e(search)+'" data-category="'+e(p["category"])+'">'
        '<div class="product-visual"><img src="'+e(photo)+'" alt="Fotografia editorial ilustrativa de '+e(p["category"])+'" loading="lazy" decoding="async">'
        '<small>Imagem ilustrativa</small></div>'
        '<div class="product-content"><span class="tag">'+e(p["category"])+'</span>'
        '<h4 style="font-size:17px">'+e(p["title"])+'</h4>'
        '<p style="font-size:13px">Confira variante, preço e estoque na Amazon.</p>'
        '<a class="btn" href="'+e(p["url"])+'" rel="sponsored nofollow noopener noreferrer" target="_blank">Ver na Amazon →</a>'
        '</div></article>'
    )


def build(products, template):
    """Generate the commercial storefront from the approved product catalog."""
    first = template.find('<article class="product"')
    if first < 0:
        raise ValueError("Product grid marker missing from storefront template")
    end_marker = '</div></section></main>'
    after_grid = template.find(end_marker, first)
    if after_grid < 0:
        raise ValueError("Grid closing marker missing")
    # Keep styling, filtering, links, and surrounding layout; replace the demo cards.
    return template[:first] + ''.join(product_card(p) for p in products) + template[after_grid:]


def main():
    products = load_products()
    template = PREVIEW.read_text(encoding="utf-8")
    page = build(products, template)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"index.html").write_text(page, encoding="utf-8")
    (OUT/"robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    (OUT/"catalog.json").write_text(json.dumps({
        "generated_utc":datetime.now(timezone.utc).isoformat(),
        "count":len(products),
        "categories":sorted({p["category"] for p in products})
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"BeraldoSales: {len(products)} products generated")

if __name__ == "__main__":
    main()
