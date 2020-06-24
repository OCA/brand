# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from .res_company import BRAND_USE_LEVEL_NO_USE_LEVEL, BRAND_USE_LEVEL_SELECTION


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    brand_use_level = fields.Selection(
        string="Brand Use Level",
        selection=BRAND_USE_LEVEL_SELECTION,
        default=BRAND_USE_LEVEL_NO_USE_LEVEL,
        related="company_id.brand_use_level",
        readonly=False,
    )
