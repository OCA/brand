# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    brand_use_level = fields.Selection(
        string="Brand Use Level",
        related="company_id.brand_use_level",
        readonly=False,
    )
