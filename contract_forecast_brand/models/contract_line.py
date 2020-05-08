# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractLine(models.Model):

    _inherit = "contract.line"

    @api.multi
    def _prepare_contract_line_forecast_period(
        self, period_date_start, period_date_end, recurring_next_date
    ):
        res = super()._prepare_contract_line_forecast_period(
            period_date_start, period_date_end, recurring_next_date
        )
        res["brand_id"] = self.contract_id.brand_id.id
        return res
