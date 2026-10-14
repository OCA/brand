from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleOrderStockPickingBrandID(BaseCommon):
    _test_user_groups = (
        "base.group_system",
        "base.group_partner_manager",
        "sales_team.group_sale_manager",
        "stock.group_stock_manager",
    )

    def _create_sale(self):
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
        return self.env["sale.order"].create(vals)

    def test_stock_picking_brand_id(self):
        sale = self._create_sale()
        sale.action_confirm()
        self.assertTrue(sale.picking_ids, "Sale Stock: no picking created")
        self.assertEqual(sale.picking_ids.brand_id, sale.brand_id)

    def test_stock_picking_with_required_brand(self):
        sale = self._create_sale()
        sale.company_id.brand_use_level = "required"
        sale.action_confirm()
        self.assertTrue(sale.picking_ids)
        self.assertEqual(sale.picking_ids.brand_id, sale.brand_id)

    def test_internal_picking_does_not_require_brand(self):
        self.env.company.brand_use_level = "required"
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        )
        picking_type = warehouse.int_type_id
        picking_type.active = True
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": picking_type.id,
                "location_id": picking_type.default_location_src_id.id,
                "location_dest_id": picking_type.default_location_dest_id.id,
            }
        )
        self.assertFalse(picking.is_brand_required)
