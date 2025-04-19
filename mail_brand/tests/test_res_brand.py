from odoo.addons.mail_brand.tests.common import MailBrandCommon


class TestResBrand(MailBrandCommon):
    def test_compute_logo_web(self):
        partner = self.env["res.partner"].create(
            {"name": "Test Partner", "image_1920": self.icon_base64}
        )
        brand = self.env["res.brand"].create({"partner_id": partner.id})
        self.assertTrue(brand.logo_web, "logo_web should be computed and not empty")
