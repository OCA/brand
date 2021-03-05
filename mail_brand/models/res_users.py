# Copyright 2021 Yves Goldberg
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResUsers(models.Model):

    _inherit = "res.users"

    brand_ids = fields.Many2one(
        "res.brand",
        "Brands",
    )
    brand_for_mails_id = fields.Many2one(
        "res.brand",
        "Brand For Mails",
        domain="[('id', 'in', brand_ids)]",
    )
