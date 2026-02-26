# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _get_analytic_distribution_arguments(self):
        """
        Add the brand inside the arguments
        """
        arguments = super()._get_analytic_distribution_arguments()
        if self.contract_id.brand_id:
            arguments["brand_id"] = self.contract_id.brand_id.id
        return arguments

    @api.depends("contract_id.brand_id")
    def _compute_analytic_distribution(self):
        return super()._compute_analytic_distribution()
