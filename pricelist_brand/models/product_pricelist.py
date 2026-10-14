# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _get_applicable_rules_domain(self, products, **kwargs):
        domain = super()._get_applicable_rules_domain(products, **kwargs)
        return domain & (
            Domain("product_brand_id", "=", False)
            | Domain("product_brand_id", "in", products.product_brand_id.ids)
        )


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    product_brand_id = fields.Many2one(
        comodel_name="product.brand",
        string="Brand",
        ondelete="cascade",
        help="Specify a brand if this rule only applies to products"
        " belonging to this brand. Keep empty otherwise.",
    )
    applied_on = fields.Selection(
        selection_add=[("25_brand", "Brand"), ("2_product_category",)],
        ondelete={"25_brand": "cascade"},
    )

    @api.depends("product_brand_id")
    def _compute_applied_on(self):
        res = super()._compute_applied_on()
        for item in self:
            if item.product_brand_id:
                item.applied_on = "25_brand"
        return res

    def _is_applicable_for(self, product, quantity, *, uom=None, **kwargs):
        if not super()._is_applicable_for(product, quantity, uom=uom, **kwargs):
            return False
        return (
            self.applied_on != "25_brand"
            or product.product_brand_id == self.product_brand_id
        )

    @api.constrains(
        "applied_on", "product_id", "product_tmpl_id", "categ_id", "product_brand_id"
    )
    def _check_product_consistency(self):
        for item in self:
            if item.applied_on == "25_brand" and not item.product_brand_id:
                raise ValidationError(
                    self.env._(
                        "Please specify the brand for which this rule should be applied"
                    )
                )
        return super()._check_product_consistency()

    @api.depends(
        "applied_on", "categ_id", "product_tmpl_id", "product_id", "product_brand_id"
    )
    def _compute_name(self):
        res = super()._compute_name()
        for item in self:
            if item.product_brand_id and item.applied_on == "25_brand":
                item.name = self.env._("Brand: %s", item.product_brand_id.display_name)
        return res

    @api.model
    def _sanitize_brand_target_values(self, values):
        applied_on = values.get("applied_on")
        if applied_on == "25_brand" or (
            not applied_on and values.get("product_brand_id")
        ):
            values.update(product_id=False, product_tmpl_id=False, categ_id=False)
        elif applied_on or any(
            values.get(name) for name in ("product_id", "product_tmpl_id", "categ_id")
        ):
            values["product_brand_id"] = False
        return values

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(
            [self._sanitize_brand_target_values(dict(values)) for values in vals_list]
        )

    def write(self, values):
        return super().write(self._sanitize_brand_target_values(dict(values)))
