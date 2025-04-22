# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.fields import Date

from odoo.addons.contract.tests.test_contract import TestContractBase


class TestContract(TestContractBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, queue_job__no_delay=True))
        cls.brand_id = cls.env["res.brand"].create({"name": "brand"})
        cls.line_vals["date_start"] = Date.today()
        cls.line_vals["recurring_next_date"] = Date.today()
        cls.acct_line = cls.env["contract.line"].create(cls.line_vals)

    def test_contract_forecast_brand(self):
        """It should create a branded forecast line"""
        self.assertTrue(self.acct_line.forecast_period_ids)
        self.assertFalse(self.acct_line.forecast_period_ids[0].brand_id)
        self.contract.with_context(queue_job__no_delay=True).write(
            {"brand_id": self.brand_id.id}
        )
        self.assertTrue(self.acct_line.forecast_period_ids)
        self.assertEqual(self.acct_line.forecast_period_ids[0].brand_id, self.brand_id)
