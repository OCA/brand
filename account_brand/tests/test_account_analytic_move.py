# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestAccountAnalyticMove(TransactionCase):
    def setUp(self):
        super().setUp()
        self.account = self.env["account.account"].create(
            {
                "name": "Test sale",
                "code": "XX_700",
                "user_type_id": self.env.ref("account.data_account_type_revenue").id,
            }
        )
        self.move = self.env["account.move"].create(
            {
                "partner_id": self.env.ref("base.res_partner_12").id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.env.ref("product.product_product_4").id,
                            "quantity": 1,
                            "price_unit": 42,
                            "name": "something",
                            "account_id": self.account.id,
                        },
                    )
                ],
            }
        )
        self.brand_id = self.env["res.brand"].create({"name": "Brand"})

    def test_move_analytic_account_onchange_brand(self):
        self.brand_id.analytic_account_id = self.env["account.analytic.account"].create(
            {"name": "analytic account"}
        )
        self.move.brand_id = self.brand_id
        self.assertFalse(self.move.invoice_line_ids.mapped("analytic_account_id"))
        self.move._onchange_brand_id()
        self.assertEqual(
            self.move.invoice_line_ids.mapped("analytic_account_id"),
            self.brand_id.analytic_account_id,
        )
