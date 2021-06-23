# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, exceptions, fields, models


class ProductBrandTag(models.Model):
    _inherit = "product.brand.tag"

    product_brand_ids = fields.Many2many(
        string="Primary for brands",
        domain="[('id', 'not in', secondary_product_brand_ids)]",
    )
    secondary_product_brand_ids = fields.Many2many(
        comodel_name="product.brand",
        string="Secondary for brands",
        relation="product_brand_secondary_tag_rel",
        column1="tag_id",
        column2="brand_id",
        help="Assign as secondary tag to these brands.",
        domain="[('id', 'not in', product_brand_ids)]",
    )
    secondary_brands_count = fields.Integer(
        string="# of secondary brands", compute="_compute_secondary_brands_count"
    )

    @api.depends("secondary_product_brand_ids")
    def _compute_secondary_brands_count(self):
        count = self._get_brands_count("secondary_product_brand_ids")
        for rec in self:
            rec.secondary_brands_count = count.get(rec.id, 0)

    @api.constrains("product_brand_ids", "secondary_product_brand_ids")
    def _check_brands_relation(self):
        errored = []
        for rec in self:
            if set(rec.product_brand_ids.ids).intersection(
                rec.secondary_product_brand_ids.ids
            ):
                errored.append(rec)
        if errored:
            raise exceptions.UserError(self._check_brands_relation_error_msg(errored))

    def _check_brands_relation_error_msg(self, errored):
        return _(
            "You can assign a tag either as primary or secondary. "
            "The following tags have been assigned to the same brand as primary and secondary: "
            "\n    %s"
        ) % ", ".join([x.name for x in errored])
