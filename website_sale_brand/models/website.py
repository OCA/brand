# Copyright 2026 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    brand_id = fields.Many2one(
        comodel_name="res.brand",
        string="Brand",
        help="Brand to use for this website",
    )

    def _prepare_sale_order_values(self, partner_sudo):
        vals = super()._prepare_sale_order_values(partner_sudo)
        brand = self.salesteam_id.brand_id or self.brand_id
        if brand:
            vals["brand_id"] = brand.id
        return vals
