# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResBrand(models.Model):

    _inherit = "res.brand"

    allowed_payment_mode_ids = fields.Many2many(
        comodel_name="account.payment.mode", string="Allowed payment modes"
    )
