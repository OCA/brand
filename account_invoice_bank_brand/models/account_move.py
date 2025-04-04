# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_onchange_create(self):
        res = super()._get_onchange_create()
        return OrderedDict(
            [("_onchange_brand", ["partner_bank_id"])] + list(res.items())
        )

    @api.onchange("brand_id")
    def _onchange_brand(self):
        move_type = self.move_type or self.env.context.get("move_type", "out_invoice")
        if (
            move_type in ("out_invoice", "in_refund")
            and self.brand_id
            and self.brand_id.partner_bank_id
        ):
            self.partner_bank_id = self.brand_id.partner_bank_id
