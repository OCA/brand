# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from odoo.addons.brand.models.res_company import BRAND_USE_LEVEL_NO_USE_LEVEL


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.sale = self.env.ref("sale.sale_order_1")
        self.sale.company_id.brand_use_level = "required"
        self.sale.brand_id = self.env["res.brand"].create({"name": "brand"})
        self.sale.order_line.mapped("product_id").write({"invoice_policy": "order"})
        self.sale.action_confirm()

    def test_terms_url(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "account.use_invoice_terms", True
        )

        self.sale.brand_id.write(
            {
                "website": "https://odoo-community.org",
                "terms_type": "html",
                "invoice_terms": "We are not responsible for or product to work",
                "terms_page": "/terms",
            }
        )
        self.assertEqual(
            self.sale.brand_id.terms_url, "https://odoo-community.org/terms"
        )
        self.sale._onchange_brand_id()
        self.assertEqual(
            self.sale.note,
            "<p>Terms &amp; Conditions: https://odoo-community.org/terms</p>",
        )

        self.sale.brand_id.write({"terms_type": "plain"})
        self.sale._onchange_brand_id()
        self.assertEqual(
            self.sale.note,
            "<p>We are not responsible for or product to work</p>",
        )

        self.env["ir.config_parameter"].sudo().set_param(
            "account.use_invoice_terms", False
        )
        self.sale.brand_id.write({"terms_type": "plain"})
        self.sale._onchange_brand_id()
        self.assertEqual(
            self.sale.note,
            "",
        )

        self.env["ir.config_parameter"].sudo().set_param(
            "account.use_invoice_terms", True
        )
        self.env.company.write(
            {
                "terms_type": "plain",
                "invoice_terms": "Company terms",
                "brand_use_level": BRAND_USE_LEVEL_NO_USE_LEVEL,
            }
        )
        self.sale.brand_id = False
        self.sale._onchange_brand_id()
        self.assertEqual(self.sale.note, "<p>Company terms</p>")

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
