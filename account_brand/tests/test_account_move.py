# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestAccountMove(SavepointCase):
    def setUp(self):
        super(TestAccountMove, self).setUp()
        self.product = self.env.ref("product.product_product_4")
        account_receivable_type = self.env.ref("account.data_account_type_receivable")
        self.account_receivable = self.env["account.account"].create(
            {
                "name": "Partner Receivable",
                "code": "RCV00",
                "user_type_id": account_receivable_type.id,
                "reconcile": True,
            }
        )
        self.account_receivable_brand_default = self.env["account.account"].create(
            {
                "name": "Receivable Brand Default",
                "code": "RCV01",
                "user_type_id": account_receivable_type.id,
                "reconcile": True,
            }
        )
        self.account_receivable_partner_brand_default = self.env[
            "account.account"
        ].create(
            {
                "name": "Receivable Partner Brand Default",
                "code": "RCV02",
                "user_type_id": account_receivable_type.id,
                "reconcile": True,
            }
        )
        self.partner_id = self.env.ref("base.res_partner_12")
        self.partner_id.property_account_receivable_id = self.account_receivable
        type_revenue = self.env.ref("account.data_account_type_revenue")
        self.account_revenue = self.env["account.account"].create(
            {"name": "Test sale", "code": "XX_700", "user_type_id": type_revenue.id}
        )
        self.move = self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "type": "out_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 42,
                            "name": "something",
                            "account_id": self.account_revenue.id,
                        },
                    )
                ],
            }
        )

        self.brand_id = self.env["res.brand"].create({"name": "Brand"})

    def _get_receivable_account(self, move):
        user_type_receivable = self.env.ref("account.data_account_type_receivable")
        return self.move.line_ids.filtered(
            lambda l, u_type=user_type_receivable: l.account_id.user_type_id == u_type
        ).account_id

    def test_on_change_partner_id(self):

        account = self._get_receivable_account(self.move)
        self.assertEqual(account, self.account_receivable)
        partner_account_brand = self.env["res.partner.account.brand"].create(
            {
                "partner_id": False,
                "account_id": self.account_receivable_brand_default.id,
                "brand_id": self.brand_id.id,
                "account_type": "receivable",
            }
        )
        self.move._onchange_partner_id()
        account = self._get_receivable_account(self.move)
        self.assertEqual(account, self.account_receivable)
        self.move.brand_id = self.brand_id
        self.move._onchange_partner_id()
        account = self._get_receivable_account(self.move)
        self.assertEqual(account, self.account_receivable_brand_default)
        partner_account_brand.update(
            {
                "partner_id": self.partner_id.id,
                "account_id": self.account_receivable_partner_brand_default.id,
            }
        )
        self.move._onchange_partner_id()
        account = self._get_receivable_account(self.move)
        self.assertEqual(
            account, self.account_receivable_partner_brand_default,
        )
        move = self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "brand_id": self.brand_id.id,
                "type": "out_invoice",
            }
        )
        account = self._get_receivable_account(move)
        self.assertEqual(
            account, self.account_receivable_partner_brand_default,
        )
