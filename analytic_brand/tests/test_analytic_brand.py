# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.base.tests.common import BaseCommon


class TestResBrand(BaseCommon):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        # Create a plan (assuming a Plan model exists and is required)
        self.plan = self.env["account.analytic.plan"].create(
            {
                "name": "Test Plan",
            }
        )

        # Create an analytic account with the plan_id set
        self.analytic_account = self.env["account.analytic.account"].create(
            {
                "name": "Test Analytic Account",
                "plan_id": self.plan.id,
            }
        )

        # Create a brand with the analytic account
        self.res_brand = self.env["res.brand"].create(
            {
                "name": "Test Brand",
                "analytic_account_id": self.analytic_account.id,
            }
        )

    def test_analytic_account_assignment(self):
        """Test if the analytic_account_id is assigned correctly"""
        self.assertEqual(
            self.res_brand.analytic_account_id,
            self.analytic_account,
            "The analytic_account_id field should be assigned correctly.",
        )
