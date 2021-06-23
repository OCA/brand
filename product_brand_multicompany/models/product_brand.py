# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    company_ids = fields.Many2many(
        comodel_name="res.company",
        string="Companies",
        ondelete="restrict",
    )
