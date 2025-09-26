# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    @api.depends("contract_id.brand_id")
    def _compute_analytic_distribution(self):
        self.analytic_distribution = False
        for rec in self.filtered(lambda line: line.contract_id.brand_id):
            rec.analytic_distribution = rec.contract_id.brand_id.analytic_distribution
