# Copyright 2022 Snakebyte
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging

from odoo import api, fields, models
from odoo.tools.image import image_process

_logger = logging.getLogger(__name__)


class ResBrand(models.Model):
    _inherit = "res.brand"

    logo_web = fields.Binary(compute="_compute_logo_web", store=True, attachment=False)

    @api.model
    def write(self, vals):
        if "image_1920" in vals:
            for rec in self:
                brands = self.env["res.brand"].search([("partner_id", "=", rec.id)])
                brands._compute_logo_web()
        return super().write(vals)

    @api.depends("partner_id.image_1920")
    def _compute_logo_web(self):
        for brand in self:
            img = brand.partner_id.image_1920
            brand.logo_web = False
            if img:
                try:
                    decoded_image = base64.b64decode(img)
                    processed_image = image_process(decoded_image, size=(180, 0))
                    if processed_image:
                        brand.logo_web = base64.b64encode(processed_image)
                except Exception as e:
                    _logger.error(f"Error computing brand logo_web: {e}")
