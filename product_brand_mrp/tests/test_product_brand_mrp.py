# Copyright 2023 Francesco Apruzzese <cescoap@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.base.tests.common import BaseCommon


class TestMrpProduction(BaseCommon):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.product_brand = self.env["product.brand"].create({"name": "Test Brand"})
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "product_brand_id": self.product_brand.id,
            }
        )

    def test_product_brand_on_mrp_production(self):
        production = self.env["mrp.production"].create(
            {
                "product_id": self.product.id,
                "product_qty": 10.0,
            }
        )
        self.assertEqual(
            production.product_brand_id,
            self.product_brand,
            "The product_brand_id on MrpProduction "
            "should match the brand of the product.",
        )
