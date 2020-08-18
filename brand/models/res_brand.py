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

class ResBrandName(models.Model):

    _name = 'res.brand.name'
    _description = 'Brand Name'

    name = fields.Char(
        string="Template",
    )
    brand = fields.Many2one(
        comodel_name="res.brand",
        string="brand",
        required=True,
    )
