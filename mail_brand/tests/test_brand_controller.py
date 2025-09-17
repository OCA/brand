import base64

from odoo.tests import HttpCase

from odoo.addons.mail_brand.tests.common import MailBrandCommon


class TestBrandController(HttpCase, MailBrandCommon):
    def test_company_logo_brand(self):
        brand_partner = self.env["res.partner"].create(
            {"name": "Test Brand Partner", "image_1920": self.icon_base64}
        )
        brand = self.env["res.brand"].create({"partner_id": brand_partner.id})
        response = self.url_open(f"/logo.png?company={brand.id}&bstyle=1")
        self.assertEqual(response.status_code, 200, "Controller should return success")
        self.assertEqual(
            response.headers["Content-Type"],
            "image/png",
            "Content type should be image/png",
        )

        fetched_brand = self.env["res.brand"].browse(brand.id)
        self.assertTrue(
            response.content == base64.b64decode(fetched_brand.logo_web),
            "Logo content should match computed logo_web",
        )

    def test_company_logo_default(self):
        response = self.url_open("/logo.png?company=1&bstyle=0")
        self.assertEqual(response.status_code, 200, "Controller should return success")
        self.assertEqual(
            response.headers["Content-Type"],
            "image/png",
            "Content type should be image/png",
        )
