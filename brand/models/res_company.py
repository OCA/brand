# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

BRAND_USE_LEVEL_SELECTION = [
    ('no', 'No Use'),
    ('optional', 'Optional'),
    ('required', 'Required'),
]
BRAND_USE_LEVEL_DEFAULT_VALUE = 'no'
BRAND_USE_LEVEL_REQUIRED_LEVEL = 'required'


class ResCompany(models.Model):

    _inherit = 'res.company'

    brand_use_level = fields.Selection(
        string="Brand Use Level",
        selection=BRAND_USE_LEVEL_SELECTION,
        default=BRAND_USE_LEVEL_DEFAULT_VALUE,
    )
