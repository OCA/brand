# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class ResBrandMixin(models.AbstractModel):

    _inherit = "res.brand.mixin"

    allowed_payment_mode_ids = fields.Many2many(
        related="brand_id.allowed_payment_mode_ids"
    )

    @api.onchange("brand_id")
    def onchange_brand_allowed_payment_mode(self):
        self.ensure_one()
        domain = []
        if self.brand_id and self.allowed_payment_mode_ids:
            domain = [("id", "in", self.allowed_payment_mode_ids.ids)]
        return {"domain": {"payment_mode_id": domain}}
