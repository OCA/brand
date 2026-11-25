# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountAnalyticDistributionModel(models.Model):
    _inherit = "account.analytic.distribution.model"

    brand_id = fields.Many2one(
        "res.brand",
        ondelete="restrict",
        help="Select a brand for which the analytic distribution will be used"
        " (e.g. create new customer invoice or Sales order linked to this brand, "
        "it will automatically take this as an analytic account)",
    )

    @api.model
    def _get_default_search_domain_vals(self):
        return super()._get_default_search_domain_vals() | {"brand_id": False}
