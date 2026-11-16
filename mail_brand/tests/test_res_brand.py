import base64

from odoo.api import call_kw
from odoo.tools.image import image_process

from odoo.addons.mail_brand.tests.common import MailBrandCommon


class TestResBrand(MailBrandCommon):
    def test_compute_logo_web(self):
        partner = self.env["res.partner"].create(
            {"name": "Test Partner", "image_1920": self.icon_base64}
        )
        brand = self.env["res.brand"].create({"partner_id": partner.id})
        self.assertTrue(brand.logo_web, "logo_web should be computed and not empty")

    def test_write_through_rpc(self):
        """RPC clients (XML-RPC, JSON-RPC) write through call_kw, with the ids"""
        call_kw(
            self.env["res.brand"],
            "write",
            [self.test_brand.ids, {"name": "Renamed Brand"}],
            {},
        )
        self.assertEqual(self.test_brand.name, "Renamed Brand")

    def test_logo_web_follows_image(self):
        brand = self.env["res.brand"].create({"name": "Logo Brand"})
        brand.write({"image_1920": self.icon_base64})
        expected = base64.b64encode(
            image_process(base64.b64decode(self.icon_base64), size=(180, 0))
        )
        self.assertEqual(brand.logo_web, expected)
