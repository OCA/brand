# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move", "res.brand.mixin"]

    brand_id = fields.Many2one(
        states={
            "open": [("readonly", True)],
            "in_payment": [("readonly", True)],
            "paid": [("readonly", True)],
            "cancel": [("readonly", True)],
        }
    )
