# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.fields import Date
from odoo.tools import mute_logger
from odoo.addons.contract.tests.test_contract import TestContractBase


class TestContract(TestContractBase):
    @mute_logger("odoo.addons.queue_job.models.base")
    def setUp(self):
        super(TestContract, self).setUp()
        self.brand_id = self.env["res.brand"].create({"name": "brand"})
        self.line_vals["date_start"] = Date.today()
        self.line_vals["recurring_next_date"] = Date.today()
        self.acct_line = (
            self.env["contract.line"]
            .with_context(test_queue_job_no_delay=True)
            .create(self.line_vals)
        )

    @mute_logger("odoo.addons.queue_job.models.base")
    def test_contract_forecast_brand(self):
        """ It should create a branded forecast line"""
        self.assertTrue(self.acct_line.forecast_period_ids)
        self.assertFalse(self.acct_line.forecast_period_ids[0].brand_id)
        self.contract.with_context(test_queue_job_no_delay=True).write(
            {"brand_id": self.brand_id.id}
        )
        self.assertTrue(self.acct_line.forecast_period_ids)
        self.assertEqual(
            self.acct_line.forecast_period_ids[0].brand_id, self.brand_id
        )
