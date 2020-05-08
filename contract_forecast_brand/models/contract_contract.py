# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    @api.model
    def _get_forecast_update_trigger_fields(self):
        return super()._get_forecast_update_trigger_fields() + ["brand_id"]
