from odoo import fields
from odoo.tests.common import TransactionCase


class TestProductPricelistBrandPrint(TransactionCase):
    def setUp(self):
        super().setUp()
        # Create a test pricelist
        self.pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test Pricelist",
            }
        )
        # Create a pricelist print wizard
        self.pricelist_print = self.env["product.pricelist.print"].create(
            {
                "pricelist_id": self.pricelist.id,
                "date": fields.Date.today(),
            }
        )

    def test_brand_id_field_exists(self):
        self.assertTrue(
            "brand_id" in self.pricelist_print, "Wizard should have brand_id field"
        )

    def test_brand_id_field_type(self):
        field = self.env["product.pricelist.print"]._fields["brand_id"]
        self.assertEqual(field.type, "many2one", "brand_id should be a Many2one field")
        self.assertEqual(
            field.comodel_name, "res.brand", "brand_id should relate to res.brand model"
        )
