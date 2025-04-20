from io import BytesIO

from PIL import Image

from odoo.tests import HttpCase

from odoo.addons.mail_brand.tests.common import MailBrandCommon


class TestBrandController(HttpCase, MailBrandCommon):
    def test_company_logo_brand(self):
        brand_partner = self.env["res.partner"].create(
            {"name": "Test Brand Partner", "image_1920": self.icon_bytes}
        )
        self.test_brand.partner_id = brand_partner.id
        self.test_brand._compute_logo_web()

        fetched_brand = self.env["res.brand"].browse(self.test_brand.id)

        response = self.url_open(f"/logo.png?company={fetched_brand.id}&bstyle=1")
        self.assertEqual(response.status_code, 200, "Controller should return success")
        self.assertEqual(
            response.headers["Content-Type"],
            "image/png",
            "Content type should be image/png",
        )

        image_stream = BytesIO(response.content)
        with Image.open(image_stream) as img:
            self.assertEqual(img.width, 180, "Processed image width should be 180")
            self.assertTrue(
                img.height > 0, "Processed image height should be greater than 0"
            )

    def test_company_logo_default(self):
        response = self.url_open("/logo.png?company=1&bstyle=0")
        self.assertEqual(response.status_code, 200, "Controller should return success")
        self.assertEqual(
            response.headers["Content-Type"],
            "image/png",
            "Content type should be image/png",
        )
