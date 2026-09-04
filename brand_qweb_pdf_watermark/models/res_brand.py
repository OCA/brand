# Copyright 2024 OCA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResBrand(models.Model):
    _inherit = "res.brand"

    pdf_watermark = fields.Binary(
        string="Watermark",
        help="Upload a PDF or image file to use as a watermark for this brand.",
    )
