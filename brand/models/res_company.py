# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

BRAND_USE_LEVEL_NO_USE_LEVEL = "no"
BRAND_USE_LEVEL_REQUIRED_LEVEL = "required"

BRAND_USE_LEVEL_SELECTION = [
    (BRAND_USE_LEVEL_NO_USE_LEVEL, "Do not use brands on business document"),
    ("optional", "Optional"),
    (BRAND_USE_LEVEL_REQUIRED_LEVEL, "Required"),
]


class ResCompany(models.Model):
    _inherit = "res.company"

    brand_use_level = fields.Selection(
        string="Brand Use Level",
        selection=BRAND_USE_LEVEL_SELECTION,
        default=BRAND_USE_LEVEL_NO_USE_LEVEL,
    )
