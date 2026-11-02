# Copyright 2026 Juliano Henriquez <juliano@consultoriahenca.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo.addons.base.tests.common import BaseCommon


class TestProductBrandValuation(BaseCommon):
    _test_user_groups = (
        "stock.group_stock_manager",
        "product.group_product_manager",
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand = cls.env["product.brand"].create({"name": "Valuation Brand"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Branded Stock",
                "is_storable": True,
                "standard_price": 12,
                "product_brand_id": cls.brand.id,
            }
        )

    def test_branded_inventory_valuation(self):
        move = self.env["stock.move"].create(
            {
                "product_id": self.product.id,
                "product_uom_qty": 3,
                "location_id": self.env.ref("stock.stock_location_suppliers").id,
                "location_dest_id": self.env.ref("stock.stock_location_stock").id,
            }
        )
        move._action_confirm()
        move.write({"quantity": 3, "picked": True})
        move._action_done()
        self.assertEqual(self.product.qty_available, 3)
        self.assertEqual(self.product.total_value, 36)

        view = self.env["product.product"].get_view(
            view_id=self.env.ref("stock.product_product_stock_tree").id,
            view_type="list",
        )
        arch = etree.fromstring(view["arch"])
        self.assertTrue(arch.xpath("//field[@name='product_brand_id']"))
        self.assertTrue(arch.xpath("//field[@name='total_value']"))
        groups = self.env["product.product"]._read_group(
            [("product_brand_id", "=", self.brand.id)],
            ["product_brand_id"],
            ["id:recordset"],
        )
        self.assertEqual(len(groups), 1)
        brand, products = groups[0]
        self.assertEqual(brand, self.brand)
        self.assertEqual(products, self.product)
        self.assertEqual(sum(products.mapped("total_value")), 36)
