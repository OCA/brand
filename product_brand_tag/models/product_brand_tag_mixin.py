# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import sql

from odoo import api, fields, models

from odoo.addons.http_routing.models.ir_http import slugify


class ProductBrandTag(models.AbstractModel):
    _name = "product.brand.tag.mixin"
    _description = "Product Brand Tag Mixin"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(
        compute="_compute_code", inverse="_inverse_code", readonly=False, store=True
    )
    color = fields.Integer(string="Color Index")
    product_brand_ids = fields.Many2many(
        comodel_name="product.brand",
        string="Brands",
        column1="tag_id",
        column2="brand_id",
    )
    brands_count = fields.Integer(string="# of brands", compute="_compute_brands_count")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company.id,
    )

    _sql_constraints = [
        (
            "tag_code_uniq",
            "unique(code, company_id)",
            "Tag code must be unique inside a company",
        ),
    ]

    @api.depends("name")
    def _compute_code(self):
        for rec in self:
            rec.code = slugify(rec.name)

    def _inverse_code(self):
        for rec in self:
            # Make sure is always normalized
            rec.code = slugify(rec.code)

    @api.depends("product_brand_ids")
    def _compute_brands_count(self):
        count = self._get_brands_count("product_brand_ids")
        for rec in self:
            rec.brands_count = count.get(rec.id, 0)

    def _get_brands_count(self, rel_field_name):
        res = {}
        if self.ids:
            field = self._fields[rel_field_name]
            query = sql.SQL(
                """
                SELECT {column1}, COUNT(*)
                FROM {relation}
                WHERE {column1} IN %s
                GROUP BY {column1}
                """
            ).format(
                relation=sql.Identifier(field.relation),
                column1=sql.Identifier(field.column1),
            )
            self.env.cr.execute(query, (tuple(self.ids),))
            res = dict(self.env.cr.fetchall())
        return res
