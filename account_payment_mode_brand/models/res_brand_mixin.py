# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class ResBrandMixin(models.AbstractModel):

    _inherit = "res.brand.mixin"

    allowed_payment_mode_ids = fields.Many2many(
        comodel_name="account.payment.mode",
        compute="_compute_allowed_payment_mode_ids",
    )

    @api.depends('brand_id')
    def _compute_allowed_payment_mode_ids(self):
        all_payment_mode = self.env['account.payment.mode'].search([])
        for rec in self:
            if rec.brand_id and rec.brand_id.allowed_payment_mode_ids:
                rec.allowed_payment_mode_ids = (
                    rec.brand_id.allowed_payment_mode_ids
                )
            else:
                rec.allowed_payment_mode_ids = all_payment_mode
