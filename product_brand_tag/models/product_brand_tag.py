# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductBrandTag(models.Model):
    _name = "product.brand.tag"
    _inherit = "product.brand.tag.mixin"
    _description = "Product Brand Tag"

    product_brand_ids = fields.Many2many(relation="product_brand_tag_rel")
