import tempfile
import unittest
from pathlib import Path
from bot import load_products, validate_link, build, product_card

class StoreTests(unittest.TestCase):
    def test_affiliate_url(self):
        self.assertTrue(validate_link("https://link.amazon/B09jCjhaW"))
        self.assertFalse(validate_link("javascript:alert(1)"))
        self.assertFalse(validate_link("https://fake.example/product"))
    def test_product_catalog(self):
        data = load_products()
        self.assertGreaterEqual(len(data), 1)
        self.assertTrue(all(p["status"] == "approved" for p in data))
    def test_generated_design(self):
        template = Path("preview/vitrine.html").read_text(encoding="utf-8")
        html = build(load_products(), template)
        self.assertIn("SeuPetFeliz", html)
        self.assertNotIn("BeraldoSales", html)
        self.assertIn("Ver na Amazon", html)
        self.assertIn("mobile-nav", html)
        self.assertEqual(html.count("Imagem ilustrativa"), len(load_products()))
        self.assertIn("training-pad.svg", html)
        self.assertNotIn("images.unsplash.com/photo-1552053831-71594a27632d?w=680", html)
        self.assertNotIn("Catálogo real importado do GitHub", html)
        self.assertNotIn("Seleção Pet | Recomendações", html)
        self.assertNotIn("amazon.com.br/s?k=", html)
        self.assertNotIn("const testProducts=", html)
        self.assertIn("id=\"catalogGrid\"", html)
        self.assertEqual(html.count('<article class="product"'), len(load_products()))
    def test_licensed_image_and_fallback(self):
        p = dict(id="x", title="Brinquedo Macaco", category="Brinquedos",
                 description="Teste", url="https://link.amazon/test", status="approved",
                 image_url="https://example.com/authorized-photo.jpg",
                 image_source="owner-licensed")
        card = product_card(p)
        self.assertIn("https://example.com/authorized-photo.jpg", card)
        self.assertIn("plush-toy.svg", card)
        self.assertIn("Imagem do produto", card)

    def test_default_image_fallback(self):
        p = load_products()[0]
        self.assertIn("Imagem ilustrativa", product_card(p))
        self.assertIn("preview/assets/", product_card(p))

    def test_reject_injection(self):
        sample = dict(id="x",title="<script>alert(1)</script>",category="Brinquedos",description="OK",url="https://link.amazon/abc",status="approved")
        html = build([sample], Path("preview/vitrine.html").read_text(encoding="utf-8"))
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)

if __name__ == "__main__":
    unittest.main()
