from odoo.addons.base.tests.common import BaseCommon


class TestStockValuationLayer(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_brand = cls.env["product.brand"].create({"name": "Brand A"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product A",
                "product_brand_id": cls.product_brand.id,
            }
        )
        cls.stock_valuation_layer = cls.env["stock.valuation.layer"].create(
            {
                "product_id": cls.product.id,
                "company_id": cls.env.ref("base.main_company").id,
                "quantity": 10,
                "unit_cost": 100.0,
            }
        )

    def test_product_brand_id_on_stock_valuation_layer(self):
        self.assertEqual(
            self.stock_valuation_layer.product_brand_id,
            self.product_brand,
            "The product_brand_id should match the product's brand.",
        )
