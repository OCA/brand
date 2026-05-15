# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestAccountMove(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create({"name": "Test Product"})
        cls.account_receivable = cls.env["account.account"].create(
            {
                "name": "Partner Receivable",
                "code": "RCV00",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )
        cls.account_receivable_brand_default = cls.env["account.account"].create(
            {
                "name": "Receivable Brand Default",
                "code": "RCV01",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )
        cls.account_receivable_partner_brand_default = cls.env[
            "account.account"
        ].create(
            {
                "name": "Receivable Partner Brand Default",
                "code": "RCV02",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )
        cls.partner.property_account_receivable_id = cls.account_receivable
        cls.account_revenue = cls.env["account.account"].create(
            {"name": "Test sale", "code": "XX.700", "account_type": "income"}
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Sale Journal",
                "code": "SAL",
                "type": "sale",
                "company_id": cls.env.company.id,
            }
        )
        cls.move = cls.env["account.move"].create(
            {
                "journal_id": cls.journal.id,
                "partner_id": cls.partner.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "quantity": 1,
                            "price_unit": 42,
                            "name": "something",
                            "account_id": cls.account_revenue.id,
                        },
                    )
                ],
            }
        )

        cls.brand_id = cls.env["res.brand"].create({"name": "Brand"})

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
                "partner_id": self.partner.id,
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
                "partner_id": self.partner.id,
                "brand_id": self.brand_id.id,
                "move_type": "out_invoice",
            }
        )
        account = self._get_receivable_account(move)
        self.assertEqual(
            account,
            self.account_receivable_partner_brand_default,
        )
