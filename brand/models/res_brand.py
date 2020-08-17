# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResBrand(models.Model):

    _name = 'res.brand'
    _description = 'Brand'

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
        index=True,
        auto_join=True,
        delegate=True,
        ondelete="restrict",
    )

    brandname = fields.Char(
        string="Nom du template"
    )

    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('gecko_brandname', False):
                # Only goes off when the custom_search is in the context values.
                result.append((record.id, record.brandname))
            else:
                result.append((record.id, record.name))
        return result
