# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    def _get_applicable_rules_domain(self, products, date, **kwargs):
        res = super()._get_applicable_rules_domain(products, date)
        if products._name == "product.template":
            brand_domain = ("product_brand_id", "in", products.product_brand_id.ids)
        else:
            brand_domain = (
                "product_brand_id",
                "in",
                products.product_tmpl_id.product_brand_id.ids,
            )
        res = expression.AND(
            [
                res,
                [
                    ("|"),
                    ("product_brand_id", "=", False),
                    (brand_domain),
                ],
            ]
        )
        return res

class ProductPricelistItem(models.Model):

    _inherit = "product.pricelist.item"

    product_brand_id = fields.Many2one(
        comodel_name="product.brand",
        string="Brand",
        ondelete="cascade",
        help="Specify a brand if this rule only applies to products"
        "belonging to this brand. Keep empty otherwise.",
    )
    applied_on = fields.Selection(
        selection_add=[("25_brand", "Brand")], ondelete={"25_brand": "set default"}
    )

    @api.constrains("product_id", "product_tmpl_id", "categ_id", "product_brand_id")
    def _check_product_consistency(self):
        super(ProductPricelistItem, self)._check_product_consistency()
        for item in self:
            if item.applied_on == "25_brand" and not item.product_brand_id:
                raise ValidationError(
                    _("Please specify the brand for which this rule should be applied")
                )

    @api.depends(
        "applied_on",
        "categ_id",
        "product_tmpl_id",
        "product_id",
        "compute_price",
        "fixed_price",
        "pricelist_id",
        "percent_price",
        "price_discount",
        "price_surcharge",
        "product_brand_id",
    )
    def _get_pricelist_item_name_price(self):
        super(ProductPricelistItem, self)._get_pricelist_item_name_price()
        for item in self:
            if item.product_brand_id and item.applied_on == "25_brand":
                item.name = _("Brand: %s") % (item.product_brand_id.display_name)

    @api.onchange("product_id", "product_tmpl_id", "categ_id", "product_brand_id")
    def _onchange_rule_content(self):
        super(ProductPricelistItem, self)._onchange_rule_content()

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("applied_on", False):
                # Ensure item consistency for later searches.
                applied_on = values["applied_on"]
                if applied_on == "25_brand":
                    values.update(
                        dict(product_id=None, product_tmpl_id=None, categ_id=None)
                    )
                elif applied_on == "3_global":
                    values.update(dict(product_brand_id=None))
                elif applied_on == "2_product_category":
                    values.update(dict(product_brand_id=None))
                elif applied_on == "1_product":
                    values.update(dict(product_brand_id=None))
                elif applied_on == "0_product_variant":
                    values.update(dict(product_brand_id=None))
        return super(ProductPricelistItem, self).create(vals_list)

    def write(self, values):
        if values.get("applied_on", False):
            # Ensure item consistency for later searches.
            applied_on = values["applied_on"]
            if applied_on == "25_brand":
                values.update(
                    dict(product_id=None, product_tmpl_id=None, categ_id=None)
                )
            elif applied_on == "3_global":
                values.update(dict(product_brand_id=None))
            elif applied_on == "2_product_category":
                values.update(dict(product_brand_id=None))
            elif applied_on == "1_product":
                values.update(dict(product_brand_id=None))
            elif applied_on == "0_product_variant":
                values.update(dict(product_brand_id=None))
        return super(ProductPricelistItem, self).write(values)
