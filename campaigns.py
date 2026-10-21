"""Build campaign pages and a deterministic 14-day content queue from reviewed data."""
import csv
import html
import json
import re
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent
BASE = 'https://b3r4ldo.github.io/jarvisrevenue/'

def generate(products, home, out):
    from bot import product_card
    campaigns = json.loads((ROOT / 'commercial/campaigns.json').read_text())
    by_id = {p['id']: p for p in products}
    style = re.search(r'<style>(.*?)</style>', home, re.S).group(1)
    # Reuse the current consent controller: no GA4 script loads before acceptance.
    consent = home[home.index('<style>#sp-consent'):home.rindex('</body>')]
    ga = re.search(r'<script>window.GA4_MEASUREMENT_ID=.*?</script>', home)
    ga = ga.group(0) if ga else ''
    target = out / 'guias'
    target.mkdir(exist_ok=True)
    for c in campaigns:
        cards = ''.join(product_card(by_id[i]) for i in c['products']).replace('../preview/assets/', '../assets/')
        title = html.escape(c['title'])
        tips = ''.join('<li>'+html.escape(t)+'</li>' for t in c['tips'])
        page = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title} | SeuPetFeliz</title><meta name="description" content="{html.escape(c["intro"],quote=True)}">'
            f'<link rel="canonical" href="{BASE}guias/{c["slug"]}.html">'
            '<link rel="icon" href="../favicon.svg">'+ga+'<style>'+style+
            '.guide{max-width:1200px;margin:auto;padding:28px 5%}.guide h1{font-size:clamp(28px,4vw,44px);line-height:1.15}'
            '.guide li{margin:12px 0}.guide .products{margin-top:24px}.disclosure{font-size:13px;color:#53655a}'
            '</style></head><body><header class="header"><a class="brand" href="../index.html"><strong>SeuPet<span>Feliz</span></strong></a>'
            '<a href="../index.html#produtos">Ver toda a seleção →</a></header><main class="guide">'
            f'<h1>{title}</h1><p>{html.escape(c["intro"])}</p><ul>{tips}</ul>'
            '<p class="disclosure">Publicidade · Como associado da Amazon, eu ganho com compras qualificadas.</p>'
            f'<div class="products" id="catalogGrid">{cards}</div>'
            '<p class="disclosure">Imagens ilustrativas geradas por IA. Confira a embalagem, a variante, o preço, o frete e a disponibilidade na Amazon. A seleção não representa teste prático dos produtos.</p>'
            '</main><script>window.dataLayer=window.dataLayer||[];'
            'document.getElementById("catalogGrid").addEventListener("click",function(e){'
            'const a=e.target.closest("a[href]");if(!a)return;const p=a.closest(".product");if(!p)return;'
            'window.dispatchEvent(new CustomEvent("sp_analytics_event",{detail:{event:"click_affiliate_link",params:{'
            'product_id:p.dataset.productId,product_category:p.dataset.category,product_name:p.querySelector("h4").textContent,'
            'campaign_page:location.pathname}}}));});</script>'+consent+'</body></html>')
        (target / (c['slug']+'.html')).write_text(page, encoding='utf-8')
    hooks = [
        (0,'Antes de comprar tapete higiênico, confira estas 3 coisas.'),
        (1,'Areia para gatos: preço por pacote ou por quilo?'),
        (0,'30 ou 50 unidades? Faça a conta antes de repor.'),
        (2,'Petisco de 150 g: confira a indicação e a porção na embalagem.'),
        (1,'O que conferir antes de trocar a areia do seu gato?'),
        (0,'80x60 ou 60x60? Meça o espaço antes de escolher.'),
        (1,'Reposição da semana: compare material, peso e consumo.'),
        (0,'O pacote mais barato pode ter menos unidades. Compare.'),
        (2,'Um agrado na rotina: compare o preço por 100 g.'),
        (1,'Biodegradável? Confira o material e as instruções de descarte.'),
        (0,'O tamanho do tapete faz parte da escolha.'),
        (1,'Confira o peso e a variante antes de finalizar a compra.'),
        (2,'Petisco não substitui alimento completo. Confira o rótulo.'),
        (0,'Hora de repor? Compare medidas, quantidade e custo unitário.')]
    queue=[]
    for day,(idx,hook) in enumerate(hooks,1):
        c=campaigns[idx]
        params=urlencode(dict(utm_source='instagram',utm_medium='organic_social',utm_campaign='rotina_pet_14d',utm_content=f'dia_{day:02}'))
        url=BASE+'guias/'+c['slug']+'.html?'+params
        caption=hook+' '+c['intro']+' Veja as opções no link do perfil. Publicidade: podemos receber comissão por compras qualificadas. Imagens ilustrativas.'
        queue.append(dict(day=day,status='draft',channel='instagram',format='Imagem 1080x1080',headline=hook,caption=caption,destination_url=url,product_ids=','.join(c['products']),visual_brief='Peça pronta em commercial/creatives/dia-NN.webp. Imagem ilustrativa com aviso visível.'))
    with open(ROOT/'commercial/content-14-days.csv','w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=queue[0].keys());writer.writeheader();writer.writerows(queue)
    (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in [BASE]+[BASE+'guias/'+c['slug']+'.html' for c in campaigns])+'</urlset>')
