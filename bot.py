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

def product_card(p):
    e = lambda s: html.escape(s, quote=True)
    search = (p["title"]+" "+p["description"]+" "+p["category"]).casefold()
    # The illustration is decorative; no fake product photo or price is published.
    return (
        '<article class="product" data-search="'+e(search)+'" data-category="'+e(p["category"])+'">'
        '<div class="product-visual" aria-label="Ilustração decorativa de produto pet">🧸</div>'
        '<div class="product-content"><span class="tag">'+e(p["category"])+'</span>'
        '<h3>'+e(p["title"])+'</h3><p>'+e(p["description"])+'</p>'
        '<a class="btn" href="'+e(p["url"])+'" rel="sponsored nofollow noopener noreferrer" '
        'target="_blank">Ver na Amazon →</a></div></article>'
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
