import tempfile
import unittest
from pathlib import Path
from bot import load_products, validate_link, build

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
        template = Path("preview/index.html").read_text(encoding="utf-8")
        html = build(load_products(), template)
        self.assertIn("BeraldoSales", html)
        self.assertIn("Ver na Amazon", html)
        self.assertIn("mobile-nav", html)
        self.assertNotIn("Catálogo real importado do GitHub", html)
        self.assertNotIn("Seleção Pet | Recomendações", html)
    def test_reject_injection(self):
        sample = dict(id="x",title="<script>alert(1)</script>",category="Brinquedos",description="OK",url="https://link.amazon/abc",status="approved")
        html = build([sample], Path("preview/index.html").read_text(encoding="utf-8"))
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)

if __name__ == "__main__":
    unittest.main()
