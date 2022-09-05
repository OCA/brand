# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.sale = self.env.ref("sale.sale_order_1")
        self.sale.company_id.brand_use_level = "required"
        self.sale.brand_id = self.env["res.brand"].create({"name": "brand"})
        self.sale.order_line.mapped("product_id").write({"invoice_policy": "order"})
        self.sale.action_confirm()

    def test_create_invoice(self):
        """It should create branded invoice"""
        self.assertEqual(self.sale.invoice_status, "to invoice")
        invoice = self.sale._create_invoices()
        self.assertEqual(invoice.brand_id, self.sale.brand_id)

    def test_create_down_payment_invoice(self):
        """It should create branded down-payment invoice"""
        advance_payment_wizard = self.env["sale.advance.payment.inv"].create(
            {
                "advance_payment_method": "fixed",
                "fixed_amount": 10.0,
                "sale_order_ids": [(6, 0, self.sale.ids)],
            }
        )
        advance_payment_wizard.create_invoices()
        invoice = self.sale.order_line.mapped("invoice_lines").mapped("move_id")
        self.assertEqual(invoice.brand_id, self.sale.brand_id)

    def test_brand_onchange_team(self):
        sale = self.sale.copy()

        brand = sale.brand_id
        brand2 = self.env["res.brand"].create({"name": "brand"})
        team = self.env.ref("sales_team.team_sales_department")
        team.brand_id = brand2.id

        sale.team_id = team.id
        sale._onchange_team_id()
        self.assertEqual(sale.brand_id, brand2)

        team.brand_id = False
        sale.brand_id = brand.id
        sale._onchange_team_id()
        self.assertEqual(sale.brand_id, brand)
