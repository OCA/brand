# Copyright 2022 Snakebyte
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import image_process


class ResBrand(models.Model):

    _inherit = "res.brand"

    logo_web = fields.Binary(compute="_compute_logo_web", store=True, attachment=False)

    @api.depends("partner_id.image_1920")
    def _compute_logo_web(self):
        for brand in self:
            brand.logo_web = image_process(brand.partner_id.image_1920, size=(180, 0))
