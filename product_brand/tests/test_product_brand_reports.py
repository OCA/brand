# Copyright 2026 Juliano Henriquez <juliano@consultoriahenca.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import Command, fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestProductBrandReports(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.sudo().group_ids += cls.env.ref("sales_team.group_sale_manager")
        cls.brand = cls.env["product.brand"].create({"name": "Report Brand"})
        cls.product_a.product_brand_id = cls.brand
        cls.product_b.product_brand_id = False

    def test_sale_report_brand(self):
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner_a.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": product.id,
                            "product_uom_qty": quantity,
                            "price_unit": 100,
                            "tax_ids": [Command.clear()],
                        }
                    )
                    for product, quantity in [(self.product_a, 2), (self.product_b, 3)]
                ],
            }
        )
        order.action_confirm()
        domain = [("order_reference", "=", f"sale.order,{order.id}")]
        report = self.env["sale.report"]
        lines = report.search(domain)
        self.assertEqual(
            lines.filtered(
                lambda line: line.product_id == self.product_a
            ).product_brand_id,
            self.brand,
        )
        self.assertFalse(
            lines.filtered(
                lambda line: line.product_id == self.product_b
            ).product_brand_id
        )
        groups = report._read_group(
            domain, ["product_brand_id"], ["product_uom_qty:sum", "price_subtotal:sum"]
        )
        self.assertEqual(
            {brand.id: (qty, total) for brand, qty, total in groups},
            {self.brand.id: (2, 200), False: (3, 300)},
        )

    def test_invoice_report_brand(self):
        invoice = self.env["account.move"].create(
            {
                "partner_id": self.partner_a.id,
                "move_type": "out_invoice",
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": product.id,
                            "quantity": quantity,
                            "price_unit": 100,
                            "tax_ids": [Command.clear()],
                        }
                    )
                    for product, quantity in [(self.product_a, 2), (self.product_b, 3)]
                ],
            }
        )
        invoice.action_post()
        domain = [("move_id", "=", invoice.id)]
        report = self.env["account.invoice.report"]
        lines = report.search(domain)
        self.assertEqual(
            lines.filtered(
                lambda line: line.product_id == self.product_a
            ).product_brand_id,
            self.brand,
        )
        self.assertFalse(
            lines.filtered(
                lambda line: line.product_id == self.product_b
            ).product_brand_id
        )
        groups = report._read_group(
            domain, ["product_brand_id"], ["quantity:sum", "price_subtotal:sum"]
        )
        self.assertEqual(
            {brand.id: (qty, total) for brand, qty, total in groups},
            {self.brand.id: (2, 200), False: (3, 300)},
        )
