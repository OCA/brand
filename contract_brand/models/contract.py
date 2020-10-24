# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractContract(models.Model):

    _name = "contract.contract"
    _inherit = ["contract.contract", "res.brand.mixin"]

    def _prepare_invoice(self, date_invoice, journal=None):
        self.ensure_one()
        values, move_form = super()._prepare_invoice(date_invoice, journal)
        values["brand_id"] = self.brand_id.id
        return values, move_form

    @api.onchange("brand_id", "contract_line_ids")
    def _onchange_brand_id(self):
        res = super()._onchange_brand_id()
        for contract in self:
            if contract.brand_id:
                analytic_account = contract.brand_id.analytic_account_id
                contract.contract_line_ids.update(
                    {"analytic_account_id": analytic_account.id}
                )
        return res
