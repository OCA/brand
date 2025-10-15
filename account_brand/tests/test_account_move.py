# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestAccountMove(TransactionCase):
    def setUp(self):
        super().setUp()
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "lst_price": 100.0,
            }
        )
        self.account_receivable = self.env["account.account"].create(
            {
                "name": "Partner Receivable",
                "code": "RCV00",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )
        self.account_receivable_brand_default = self.env["account.account"].create(
            {
                "name": "Receivable Brand Default",
                "code": "RCV01",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )
        self.account_receivable_partner_brand_default = self.env[
            "account.account"
        ].create(
            {
                "name": "Receivable Partner Brand Default",
                "code": "RCV02",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )
        self.partner_id = self.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

        self.journal = self.env["account.journal"].create(
            {"type": "sale", "code": "SALE", "name": "Sale journal"}
        )

        self.partner_id.property_account_receivable_id = self.account_receivable
        self.account_revenue = self.env["account.account"].create(
            {"name": "Test sale", "code": "XX.700", "account_type": "income"}
        )
        self.move = self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "journal_id": self.journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "name": "something",
                            "discount": 10.00,
                            "price_unit": 42,
                            "account_id": self.account_revenue.id,
                            "journal_id": self.journal.id,
                        }
                    )
                ],
            }
        )

        self.brand_id = self.env["res.brand"].create({"name": "Brand"})

    def _get_receivable_account(self, move):
        return self.move.line_ids.filtered(
            lambda line: line.account_id.account_type == "asset_receivable"
        ).account_id

    def test_on_change_partner_id(self):
        account = self._get_receivable_account(self.move)
        self.assertEqual(account, self.account_receivable)
        partner_account_brand = self.env["res.partner.account.brand"].create(
            {
                "partner_id": False,
                "account_id": self.account_receivable_brand_default.id,
                "brand_id": self.brand_id.id,
                "account_type": "asset_receivable",
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
            account,
            self.account_receivable_partner_brand_default,
        )
        move = self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "brand_id": self.brand_id.id,
                "move_type": "out_invoice",
            }
        )
        account = self._get_receivable_account(move)
        self.assertEqual(
            account,
            self.account_receivable_partner_brand_default,
        )
