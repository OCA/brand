# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractContract(models.Model):

    _name = 'contract.contract'
    _inherit = ['contract.contract', 'res.brand.mixin']

    @api.multi
    def _prepare_invoice(self, date_invoice, journal=None):
        self.ensure_one()
        values = super()._prepare_invoice(date_invoice, journal)
        values["brand_id"] = self.brand_id.id
        return values
