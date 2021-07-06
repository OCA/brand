# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    tag_ids = fields.Many2many(
        string="Primary Tags",  # change label
        domain="[('id', 'not in', secondary_tag_ids)]",
    )
    secondary_tag_ids = fields.Many2many(
        string="Secondary Tags",
        comodel_name="product.brand.tag",
        relation="product_brand_secondary_tag_rel",
        column1="brand_id",
        column2="tag_id",
        domain="[('id', 'not in', tag_ids)]",
    )
