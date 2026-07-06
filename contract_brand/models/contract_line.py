# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    @api.depends("contract_id.brand_id")
    def _compute_analytic_distribution(self):
        res = super()._compute_analytic_distribution()
        for rec in self.filtered(lambda line: line.contract_id.brand_id):
            brand_analytic_distribution = (
                rec.contract_id.brand_id.analytic_distribution or {}
            )
            if brand_analytic_distribution:
                line_analytic_distribution = rec.analytic_distribution or {}
                rec.analytic_distribution = (
                    line_analytic_distribution | brand_analytic_distribution
                )
        return res
