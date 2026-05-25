# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("brand_id")
    def _compute_partner_bank_id(self):
        res = super()._compute_partner_bank_id()
        for move in self:
            if (
                move.move_type in ("out_invoice", "in_refund")
                and move.brand_id
                and move.brand_id.partner_bank_id
            ):
                move.partner_bank_id = move.brand_id.partner_bank_id
        return res
