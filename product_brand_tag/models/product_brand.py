# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name="product.brand.tag",
        relation="product_brand_tag_rel",
        column1="brand_id",
        column2="tag_id",
    )
