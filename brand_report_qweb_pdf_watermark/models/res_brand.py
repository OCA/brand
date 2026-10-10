# © 2025 OBS Solutions BV <http://obs-solutions.com>

from odoo import fields, models


class ResBrand(models.Model):
    _inherit = "res.brand"

    pdf_watermark = fields.Binary("Watermark")
