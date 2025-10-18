# © 2023 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import os

from odoo.tests.common import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestResPartner(BaseCommon):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.brand = self.env["res.brand"].create(
            {
                "name": "Brand A",
            }
        )

        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "brand_id": self.brand.id,
            }
        )

    def test_brand_id(self):
        """Test if the brand_id is correctly assigned to the partner."""
        self.assertEqual(
            self.partner.brand_id,
            self.brand,
            "Brand ID is not assigned correctly to the partner.",
        )

    def test_brand_logo(self):
        """Test if the brand_logo field correctly references the brand's logo."""
        # Build the relative path to the image dynamically (from the module root)
        module_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(
            module_path, "..", "static", "description", "carrouf.png"
        )
        image_path = os.path.abspath(image_path)

        # Load the image file from the relative path
        with open(image_path, "rb") as image_file:
            brand_image = base64.b64encode(image_file.read())

        # Set the image on the brand
        self.brand.write(
            {
                "image_128": brand_image,
            }
        )

        # Check if the partner's brand_logo field is correctly updated
        self.assertEqual(
            self.partner.brand_logo,
            brand_image,
            "Brand logo is not correctly related to the partner.",
        )
