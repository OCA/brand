# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestAccountMove(BaseCommon):
    _test_user_groups = (
        "account.group_account_manager",
        "base.group_partner_manager",
    )

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
        return move.line_ids.filtered(
            lambda line: line.account_id.account_type == "asset_receivable"
        ).account_id

    def _create_brand_rule(self, **values):
        return self.env["res.partner.account.brand"].create(
            {
                "account_id": self.account_receivable_brand_default.id,
                "brand_id": self.brand_id.id,
                "account_type": "asset_receivable",
                **values,
            }
        )

    def test_default_brand_account_on_brand_change(self):
        self._create_brand_rule()
        self.assertEqual(
            self._get_receivable_account(self.move), self.account_receivable
        )
        self.move.brand_id = self.brand_id
        self.assertEqual(
            self._get_receivable_account(self.move),
            self.account_receivable_brand_default,
        )
        self.move.brand_id = False
        self.assertEqual(
            self._get_receivable_account(self.move), self.account_receivable
        )

    def test_partner_brand_account_on_create(self):
        self._create_brand_rule()
        self._create_brand_rule(
            partner_id=self.partner.id,
            account_id=self.account_receivable_partner_brand_default.id,
        )
        move = self.move.copy({"brand_id": self.brand_id.id})
        self.assertEqual(
            self._get_receivable_account(move),
            self.account_receivable_partner_brand_default,
        )

    def test_default_brand_account_on_partner_change(self):
        self._create_brand_rule()
        self._create_brand_rule(
            partner_id=self.partner.id,
            account_id=self.account_receivable_partner_brand_default.id,
        )
        self.move.brand_id = self.brand_id
        self.assertEqual(
            self._get_receivable_account(self.move),
            self.account_receivable_partner_brand_default,
        )
        self.move.partner_id = self.env["res.partner"].create(
            {
                "name": "Another customer",
                "property_account_receivable_id": self.account_receivable.id,
            }
        )
        self.assertEqual(
            self._get_receivable_account(self.move),
            self.account_receivable_brand_default,
        )

    def test_brand_without_account_rule(self):
        self.move.brand_id = self.brand_id
        self.assertEqual(
            self._get_receivable_account(self.move), self.account_receivable
        )

    def test_vendor_brand_account(self):
        payable = self.env["account.account"].create(
            {
                "name": "Brand payable",
                "code": "PAY01",
                "account_type": "liability_payable",
                "reconcile": True,
            }
        )
        self._create_brand_rule(account_id=payable.id, account_type="liability_payable")
        purchase_journal = self.env["account.journal"].create(
            {"name": "Purchases", "code": "PUR", "type": "purchase"}
        )
        expense = self.env["account.account"].create(
            {"name": "Purchases", "code": "EXP01", "account_type": "expense"}
        )
        move = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "journal_id": purchase_journal.id,
                "partner_id": self.partner.id,
                "brand_id": self.brand_id.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Purchase",
                            "quantity": 1,
                            "price_unit": 42,
                            "account_id": expense.id,
                        }
                    )
                ],
            }
        )
        self.assertEqual(
            move.line_ids.filtered(
                lambda line: line.display_type == "payment_term"
            ).account_id,
            payable,
        )
