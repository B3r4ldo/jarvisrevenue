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
PREVIEW = ROOT / "preview" / "index.html"
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
    # The interactive 12-item preview is a navigation test, not the live catalog.
    # Remove its demo-data script so that test search links cannot reach production.
    template = re.sub(r'<script>\\s*const testProducts=.*?</script>', '', template, flags=re.S)
    template = re.sub(r'<script>\\s*/\\* Catálogo real importado do GitHub:.*?</script>', '', template, flags=re.S)
    start = template.find('<article class="product"')
    if start < 0:
        raise ValueError("Marcador de produto ausente no template")
    end = template.find("</article>", start)
    if end < 0:
        raise ValueError("Cartão de produto incompleto")
    template = template[:start] + "".join(product_card(p) for p in products) + template[end + len("</article>"):]
    template = template.replace("BeraldoSales 2.3 — Prévia", "BeraldoSales | Boutique Pet Premium")
    template = template.replace("Prévia de testes 2.3", "Curadoria pet")
    template = template.replace("A versão pública permanece inalterada.", "Confira condições e disponibilidade no parceiro.")
    # Rewire category tiles and the search form to the approved products only.
    behavior = """
<script>
(() => {
  const cards = [...document.querySelectorAll('#catalogGrid article.product')];
  const search = document.getElementById('search');
  const section = document.getElementById('produtos');
  const fold = s => (s || '').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLocaleLowerCase('pt-BR');
  let category = '';
  const notice = document.createElement('p');
  notice.id='catalog-status';
  notice.setAttribute('role','status');
  notice.style.cssText='font-size:14px;color:#465f52;margin:12px 0';
  document.getElementById('catalogGrid').before(notice);
  function refresh() {
    let n=0;
    const term=fold(search.value.trim());
    cards.forEach(card => {
      const ok = (!category || fold(card.dataset.category)===fold(category)) && fold(card.dataset.search).includes(term);
      card.hidden = !ok;
      if(ok)n++;
    });
    notice.textContent = n ? n + ' recomendação' + (n===1?'':'ões') + ' disponível' + (n===1?'':'is') : 'Ainda não temos recomendações aprovadas para esta busca ou categoria.';
  }
  const categories=['Cães','Gatos','Brinquedos','Acessórios','Higiene','Ofertas'];
  document.querySelectorAll('.cat').forEach((item,index) => item.addEventListener('click', e => {
    e.preventDefault();category=categories[index] || '';search.value='';refresh();section.scrollIntoView({behavior:'smooth'});
  }));
  document.querySelectorAll('.desktop-nav a,.mobile-nav a').forEach(item => {
    if(categories.includes(item.textContent.trim())) item.addEventListener('click', e => {
      e.preventDefault();category=item.textContent.trim();search.value='';refresh();section.scrollIntoView({behavior:'smooth'});
    });
  });
  search.addEventListener('input',refresh);
  document.getElementById('searchForm').addEventListener('submit',e=>{e.preventDefault();refresh();section.scrollIntoView({behavior:'smooth'});});
  refresh();
})();
</script>
"""
    return template.replace("</body></html>", behavior + "</body></html>")

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
