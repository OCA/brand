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
        cls.analytic_plan2 = cls.env["account.analytic.plan"].create(
            {"name": "analytic plan 2"}
        )
        cls.analytic_account2 = cls.env["account.analytic.account"].create(
            {
                "name": "analytic account 2",
                "plan_id": cls.analytic_plan2.id,
            }
        )

    def test_contract_create_branded_move(self):
        """It should create a branded move based on the contract brand"""
        self.contract.brand_id = self.brand_id
        move = self.contract.recurring_create_invoice()
        self.assertEqual(move.brand_id, self.brand_id)

    def test_contract_analytic_account_onchange_brand(self):
        analytic_distribution = {str(self.analytic_account.id): 100.0}
        self.env["account.analytic.distribution.model"].create(
            {
                "brand_id": self.brand_id.id,
                "analytic_distribution": analytic_distribution,
            }
        )
        self.assertFalse(
            any(self.contract.contract_line_ids.mapped("analytic_distribution"))
        )
        self.contract.brand_id = self.brand_id
        for line in self.contract.contract_line_ids:
            self.assertEqual(line.analytic_distribution, analytic_distribution)

    def test_contract_analytic_distribution_combined(self):
        """
        Analytic distribution model for the product + analytic on the brand
        -> Combine both
        """
        contract_line = self.contract.contract_line_ids[0]
        product = contract_line.product_id
        self.env["account.analytic.distribution.model"].create(
            {
                "product_id": product.id,
                "analytic_distribution": {str(self.analytic_account.id): 100},
            }
        )
        contract_line._compute_analytic_distribution()
        self.assertEqual(
            contract_line.analytic_distribution, {str(self.analytic_account.id): 100}
        )
        self.env["account.analytic.distribution.model"].create(
            {
                "brand_id": self.brand_id.id,
                "analytic_distribution": {str(self.analytic_account2.id): 100},
            }
        )
        self.contract.brand_id = self.brand_id
        self.assertEqual(
            contract_line.analytic_distribution,
            {str(self.analytic_account.id): 100, str(self.analytic_account2.id): 100},
        )
