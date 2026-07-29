# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import tagged

from odoo.addons.base.tests.common import BaseCommon


# Run tests in post-install because creating a res.brand creates a res.partner
# And there is an issue creating a new partner with required field autopost_bills
# in addon account (default value not set up because this addon doesn't depend
# on account)
@tagged("post_install", "-at_install")
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

        # Create a brand with the analytic distribution: 100% on the analytic account
        self.res_brand = self.env["res.brand"].create(
            {
                "name": "Test Brand",
                "analytic_distribution": {self.analytic_account.id: 100.0},
            }
        )

    def test_analytic_account_assignment(self):
        """Test if the analytic_account_id is assigned correctly"""
        self.assertEqual(
            self.res_brand.analytic_distribution,
            {str(self.analytic_account.id): 100.0},
            "The analytic_distribution field should be assigned correctly.",
        )
