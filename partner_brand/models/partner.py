# © 2023 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    brand_id = fields.Many2one(comodel_name="res.brand")
    brand_logo = fields.Image(
        string="Brand logo",
        related="brand_id.partner_id.image_128",
    )
