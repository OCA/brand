# Copyright 2026 Juliano Henriquez <juliano@consultoriahenca.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from io import BytesIO

from PIL import Image

from odoo.tools import BinaryBytes

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerBrand(BaseCommon):
    _test_user_groups = (
        "base.group_system",
        "base.group_partner_manager",
    )

    def test_partner_brand_logo(self):
        image = BytesIO()
        Image.new("RGB", (32, 32), "blue").save(image, format="PNG")
        brand = self.env["res.brand"].create(
            {"name": "Brand", "image_1920": BinaryBytes(image.getvalue())}
        )
        self.partner.brand_id = brand
        self.assertEqual(self.partner.brand_logo.content, brand.image_128.content)
        self.assertTrue(self.partner.brand_logo)
        self.partner.brand_id = False
        self.assertFalse(self.partner.brand_logo)
