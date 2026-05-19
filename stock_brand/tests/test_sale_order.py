from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleOrderStockPickingBrandID(BaseCommon):
    def test_stock_picking_brand_id(self):
        """
        Test stock.picking brand_id is same as sale.order's brand_id
        """
        product = self.env["product.product"].create(
            {"name": "Test Product", "type": "consu"}
        )
        brand_id = self.env["res.brand"].create({"name": "Brand1"})
        vals = {
            "partner_id": self.partner.id,
            "partner_invoice_id": self.partner.id,
            "partner_shipping_id": self.partner.id,
            "brand_id": brand_id.id,
            "order_line": [
                Command.create(
                    {
                        "name": product.name,
                        "product_id": product.id,
                        "product_uom_qty": 2,
                        "product_uom_id": product.uom_id.id,
                        "price_unit": product.list_price,
                    },
                )
            ],
            "picking_policy": "direct",
        }
        self.so = self.env["sale.order"].create(vals)

        # confirm our standard so, check the picking brand id
        self.so.action_confirm()
        self.assertTrue(self.so.picking_ids, "Sale Stock: no picking created")
        self.assertEqual(self.so.picking_ids[0].brand_id.id, self.so.brand_id.id)
