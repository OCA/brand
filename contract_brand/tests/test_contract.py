# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.contract.tests.test_contract import TestContractBase


class TestContract(TestContractBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand_id = cls.env["res.brand"].create({"name": "brand"})
        cls.analytic_plan = cls.env["account.analytic.plan"].create(
            {"name": "analytic plan"}
        )
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "analytic account",
                "plan_id": cls.analytic_plan.id,
            }
        )

    def test_contract_create_branded_move(self):
        """It should create a branded move based on the contract brand"""
        self.contract.brand_id = self.brand_id
        move = self.contract.recurring_create_invoice()
        self.assertEqual(move.brand_id, self.brand_id)

    def test_contract_analytic_account_onchange_brand(self):
        self.brand_id.analytic_distribution = {self.analytic_account.id: 100.0}
        self.assertFalse(
            any(self.contract.contract_line_ids.mapped("analytic_distribution"))
        )
        self.contract.brand_id = self.brand_id
        for line in self.contract.contract_line_ids:
            self.assertEqual(
                line.analytic_distribution, self.brand_id.analytic_distribution
            )
