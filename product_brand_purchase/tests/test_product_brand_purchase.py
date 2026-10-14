# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestPurchaseReport(BaseCommon):
    _test_user_groups = ("purchase.group_purchase_manager",)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.brand = cls.env["product.brand"].create({"name": "Test Brand"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "product_brand_id": cls.brand.id,
                "type": "consu",
            }
        )
        cls.purchase_order = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner.id,
            }
        )
        cls.purchase_order_line = cls.env["purchase.order.line"].create(
            {
                "order_id": cls.purchase_order.id,
                "product_id": cls.product.id,
                "name": "Test Purchase Order Line",
                "price_unit": 100.0,
                "product_qty": 1.0,
            }
        )
        cls.unbranded_product = cls.product.copy({"product_brand_id": False})
        cls.purchase_order_line.copy(
            {"product_id": cls.unbranded_product.id, "product_qty": 2}
        )
        cls.purchase_order.button_confirm()

    def test_purchase_report_brand(self):
        report = self.env["purchase.report"].search(
            [("product_brand_id", "=", self.brand.id)]
        )
        self.assertTrue(
            report, "The purchase report should contain an entry for the product brand."
        )
        self.assertEqual(
            report[0].product_brand_id,
            self.brand,
            "The product brand in the report should match the created brand.",
        )

    def test_purchase_report_group_by_brand(self):
        groups = self.env["purchase.report"]._read_group(
            [("order_id", "=", self.purchase_order.id)],
            ["product_brand_id"],
            ["qty_ordered:sum", "untaxed_total:sum"],
        )
        self.assertEqual(
            {brand.id: (qty, total) for brand, qty, total in groups},
            {self.brand.id: (1, 100), False: (2, 200)},
        )
