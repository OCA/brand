# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def _prepare_contract_value(self, contract_template):
        self.ensure_one()
        values = super()._prepare_contract_value(contract_template)
        values["brand_id"] = self.brand_id.id
        return values
