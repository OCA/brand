# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super().setUp()
        self.account_receivable = self.env["account.account"].create(
            {
                "name": "Receivable",
                "code": "TEST.400000",
                "account_type": "asset_receivable",
                "reconcile": True,
                "company_ids": [self.env.company.id],
            }
        )
        self.account_payable = self.env["account.account"].create(
            {
                "name": "Payable",
                "code": "TEST.440000",
                "account_type": "liability_payable",
                "reconcile": True,
                "company_ids": [self.env.company.id],
            }
        )
        self.account_income = self.env["account.account"].create(
            {
                "name": "Income",
                "code": "TEST.700000",
                "account_type": "income",
                "company_ids": [self.env.company.id],
            }
        )
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "property_account_receivable_id": self.account_receivable.id,
                "property_account_payable_id": self.account_payable.id,
            }
        )
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "invoice_policy": "order",
                "property_account_income_id": self.account_income.id,
            }
        )
        self.brand = self.env["res.brand"].create({"name": "brand"})
        self.sale = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "brand_id": self.brand.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        }
                    )
                ],
            }
        )
        self.journal = self.env["account.journal"].create(
            {
                "name": "Sale Journal",
                "code": "SALE",
                "type": "sale",
                "company_id": self.env.company.id,
            }
        )
        self.sale.company_id.brand_use_level = "required"
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
        team = self.env["crm.team"].create({"name": "Test Team"})
        team.brand_id = brand2.id

        sale.team_id = team.id
        sale._onchange_team_id()
        self.assertEqual(sale.brand_id, brand2)

        team.brand_id = False
        sale.brand_id = brand.id
        sale._onchange_team_id()
        self.assertEqual(sale.brand_id, brand)
