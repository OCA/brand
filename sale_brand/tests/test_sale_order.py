# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.sale = self.env.ref("sale.sale_order_1")
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
            {"advance_payment_method": "fixed", "fixed_amount": 10.0}
        )
        advance_payment_wizard.with_context(active_ids=self.sale.ids).create_invoices()
        invoice = self.sale.order_line.mapped("invoice_lines").mapped("move_id")
        self.assertEqual(invoice.brand_id, self.sale.brand_id)

    def test_sale_analytic_account_onchange_brand(self):
        draft_sale = self.sale.copy()
        draft_sale.brand_id.analytic_account_id = self.env[
            "account.analytic.account"
        ].create({"name": "analytic account"})
        self.assertFalse(draft_sale.analytic_account_id)
        draft_sale._onchange_brand_id()
        self.assertEqual(
            draft_sale.analytic_account_id,
            draft_sale.brand_id.analytic_account_id,
        )
