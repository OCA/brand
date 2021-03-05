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

    @api.onchange("brand_ids")
    def _on_change_brand_ids(self):
        if (
            self.brand_for_mails_id
            and self.brand_for_mails_id.id
            not in self.brand_ids.ids
        ):
            self.brand_for_mails_id = False
