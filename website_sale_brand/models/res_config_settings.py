# Copyright 2022 Gecko escalade Sàrl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    brand_id = fields.Many2one(
        comodel_name='res.brand',
        related='website_id.brand_id',
        readonly=False
    )
