# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models

from .res_company import (
    BRAND_USE_LEVEL_SELECTION,
    BRAND_USE_LEVEL_NO_USE_LEVEL,
)


class ResConfigSetting(models.TransientModel):

    _inherit = 'res.config.settings'

    brand_use_level = fields.Selection(
        string="Brand Use Level",
        selection=BRAND_USE_LEVEL_SELECTION,
        default=BRAND_USE_LEVEL_NO_USE_LEVEL,
        related='company_id.brand_use_level',
        readonly=False,
    )
