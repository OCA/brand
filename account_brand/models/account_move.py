# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from typing import ClassVar

from odoo import api, fields, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit: ClassVar = ["account.move", "res.brand.mixin"]

    brand_id = fields.Many2one(inverse="_inverse_brand_id")

    def _is_brand_required(self):
        self.ensure_one()
        if self.move_type not in ("out_invoice", "out_refund"):
            return False
        return super()._is_brand_required()

    @api.depends("move_type")
    def _compute_is_brand_required(self):
        return super()._compute_is_brand_required()

    @api.onchange("brand_id")
    def _inverse_brand_id(self):
        self.line_ids._conditional_add_to_compute(
            "account_id", lambda line: line.display_type == "payment_term"
        )
