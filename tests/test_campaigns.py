import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from bot import build, load_products
from campaigns import generate

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.images=[]; self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='img': self.images.append(a['src'])
        if tag=='a': self.links.append(a['href'])

class CampaignTests(unittest.TestCase):
    def test_campaign_pages_keep_affiliate_links_assets_and_consent(self):
        products=load_products()
        template=Path('preview/vitrine.html').read_text()
        home=build(products,template).replace('</head>','<script>window.GA4_MEASUREMENT_ID="G-856CES1QJK";</script></head>')
        configs=json.loads(Path('commercial/campaigns.json').read_text())
        by_id={p['id']:p for p in products}
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            generate(products,home,out)
            for c in configs:
                page=(out/'guias'/(c['slug']+'.html')).read_text()
                parser=Links();parser.feed(page)
                self.assertTrue(all(by_id[i]['url'] in parser.links for i in c['products']))
                self.assertEqual(len(parser.images),len(c['products']))
                for src in parser.images:
                    self.assertTrue((Path('preview')/src.replace('../','')).is_file(),src)
                self.assertIn('sp_analytics_consent',page)
                self.assertIn('G-856CES1QJK',page)
                self.assertIn('click_affiliate_link',page)
                self.assertIn('campaign_page',page)
                self.assertNotIn('<script async src="https://www.googletagmanager',page)
                self.assertIn('Imagens ilustrativas',page)

if __name__=='__main__': unittest.main()
