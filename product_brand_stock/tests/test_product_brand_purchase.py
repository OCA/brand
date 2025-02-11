# Copyright 2023 Francesco Apruzzese <cescoap@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestStockMove(BaseCommon):
    @classmethod
    def setUpClass(self):
        super().setUpClass()

        # Create product brand
        self.product_brand = self.env["product.brand"].create({"name": "Test Brand"})

        # Create a product with a brand
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "is_storable": True,
                "product_brand_id": self.product_brand.id,
            }
        )

        # Create a stock.move record
        self.stock_move = self.env["stock.move"].create(
            {
                "name": "Test Move",
                "product_id": self.product.id,
                "product_uom_qty": 10,
                "product_uom": self.product.uom_id.id,
                "location_id": self.env.ref("stock.stock_location_stock").id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            }
        )

    def test_product_brand_on_stock_move(self):
        # Check if the 'product_brand_id' field is correctly set
        # on the stock.move record
        self.assertEqual(
            self.stock_move.product_brand_id,
            self.product_brand,
            "The product brand on the stock move should match the product's brand.",
        )

    def test_product_brand_on_stock_move_line(self):
        # Create a stock move line linked to the stock move
        stock_move_line = self.env["stock.move.line"].create(
            {
                "move_id": self.stock_move.id,
                "product_id": self.product.id,
                "product_uom_id": self.product.uom_id.id,
                "location_id": self.env.ref("stock.stock_location_stock").id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            }
        )

        # Check if the 'product_brand_id' is correctly set on the stock move line
        self.assertEqual(
            stock_move_line.product_brand_id,
            self.product_brand,
            "The product brand on the stock move line "
            "should match the product's brand.",
        )

    def test_product_brand_on_stock_quant(self):
        # Create a stock quant for the product
        stock_quant = self.env["stock.quant"].create(
            {
                "product_id": self.product.id,
                "location_id": self.env.ref("stock.stock_location_stock").id,
                "quantity": 10,
            }
        )

        # Check if the 'product_brand_id' is correctly set on the stock quant
        self.assertEqual(
            stock_quant.product_brand_id,
            self.product_brand,
            "The product brand on the stock quant should match the product's brand.",
        )
