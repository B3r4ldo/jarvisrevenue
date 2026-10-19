#!/usr/bin/env python3
"""JARVIS Revenue Bot: generates a static, compliant-by-default affiliate catalog."""
import csv
import html
import json
import os
import pathlib
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'products.csv'
OUT = ROOT / 'site'
FIELDS = {'id','title','category','description','url','status'}


def valid_url(value):
    p = urlparse(value.strip())
    return p.scheme == 'https' and bool(p.hostname) and not p.username and not p.password


def load():
    if not DATA.exists():
        raise SystemExit('Missing data/products.csv')
    with DATA.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if not FIELDS.issubset(reader.fieldnames or []):
            raise SystemExit('Missing required CSV columns: ' + ', '.join(sorted(FIELDS)))
        results, ids = [], set()
        for number, item in enumerate(reader, 2):
            if (item.get('status') or '').strip().lower() != 'approved':
                continue
            value = {k: (item.get(k) or '').strip() for k in FIELDS}
            if not value['id'] or value['id'] in ids:
                raise SystemExit(f'Row {number}: duplicate or empty id')
            if not valid_url(value['url']):
                raise SystemExit(f'Row {number}: invalid HTTPS URL')
            if not value['title'] or not value['category'] or not value['description']:
                raise SystemExit(f'Row {number}: missing content')
            ids.add(value['id'])
            results.append(value)
    return results


def main():
    items = load()
    OUT.mkdir(exist_ok=True)
    esc = lambda v: html.escape(v, quote=True)
    cards = []
    for p in items:
        cards.append(f'''<article class="card" data-search="{esc((p['title']+' '+p['category']+' '+p['description']).lower())}">
          <span class="tag">{esc(p['category'])}</span><h2>{esc(p['title'])}</h2>
          <p>{esc(p['description'])}</p>
          <a href="{esc(p['url'])}" target="_blank" rel="nofollow sponsored noopener noreferrer">Ver produto no parceiro ↗</a>
        </article>''')
    count = len(items)
    date = datetime.now(timezone.utc).strftime('%d/%m/%Y')
    page = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Seleção Pet | Recomendações</title><meta name="description" content="Seleção editorial de acessórios pet com links de parceiros.">
<style>body{font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:#f6f8fb;color:#1c2430;margin:0;line-height:1.6}header{background:#142436;color:white;padding:48px 20px}main,header>div,footer>div{max-width:980px;margin:auto}.subtitle{color:#c5d8e9}main{padding:32px 20px}h1{font-size:2.4rem;margin:0}input{width:100%;box-sizing:border-box;padding:15px;border:1px solid #cbd5e1;border-radius:9px;font-size:1rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px;margin-top:22px}.card{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:22px;display:flex;flex-direction:column;gap:10px}.card h2{font-size:1.2rem;line-height:1.3;margin:0}.card p{margin:0;color:#475569;flex:1}.tag{font-size:.8rem;color:#175b50;font-weight:700}.card a{background:#146b5b;padding:11px;border-radius:8px;color:white;text-decoration:none;text-align:center;font-weight:600}[hidden]{display:none!important}footer{background:#e8edf2;padding:20px;font-size:.85rem;color:#39485b}small{color:#6a7585}a:focus,input:focus{outline:2px solid #0e9c84}</style></head>
<body><header><div><h1>Seleção Pet</h1><p class="subtitle">Curadoria independente de acessórios e soluções para animais de estimação.</p></div></header>
<main><p><strong>Aviso de publicidade:</strong> Alguns links são de afiliados e podemos receber comissão por compras qualificadas, sem custo adicional para você. As recomendações são editoriais; confira disponibilidade e preço no parceiro antes de comprar.</p>
<label for="search"><strong>Encontre um produto</strong></label><input id="search" type="search" placeholder="Pesquise categoria, nome ou benefício" autocomplete="off">
<p id="count">''' + str(count) + ''' recomendações disponíveis</p><section class="grid" id="products">''' + ''.join(cards) + '''</section>
<p id="empty" hidden>Nenhum produto encontrado. Tente outro termo.</p><p><small>Última geração do catálogo: ''' + date + '''. Preços e estoques não são monitorados por este site.</small></p></main>
<footer><div>Conteúdo informativo e publicitário. Não fornecemos atendimento, garantia ou venda direta. Antes de publicar, substitua este aviso pelos dados de contato, política de privacidade e termos adequados ao seu negócio.</div></footer>
<script>const q=document.querySelector('#search'),cards=[...document.querySelectorAll('.card')],count=document.querySelector('#count'),empty=document.querySelector('#empty');q.addEventListener('input',()=>{let n=0;const s=q.value.toLocaleLowerCase('pt-BR').trim();for(const c of cards){const ok=c.dataset.search.includes(s);c.hidden=!ok;if(ok)n++}count.textContent=n+' recomendações encontradas';empty.hidden=n!==0});</script></body></html>'''
    (OUT / 'index.html').write_text(page, encoding='utf-8')
    (OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\n', encoding='utf-8')
    (OUT / 'catalog.json').write_text(json.dumps({'generated_utc':datetime.now(timezone.utc).isoformat(),'count':count,'categories':sorted({p['category'] for p in items})},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Generated {count} approved products in {OUT}')

if __name__ == '__main__':
    main()
