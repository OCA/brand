# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class ResBrand(models.Model):
    _name = "res.brand"
    _description = "Brand"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
        index=True,
        auto_join=True,
        delegate=True,
        ondelete="restrict",
    )
