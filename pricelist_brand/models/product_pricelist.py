# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    def _compute_price_rule_get_items(
        self, products_qty_partner, date, uom_id, prod_tmpl_ids, prod_ids, categ_ids
    ):
        self.ensure_one()
        product_tmpls = self.env["product.template"].browse(prod_tmpl_ids)
        brand_ids = product_tmpls.mapped("product_brand_id").ids
        # Load all rules
        self.env["product.pricelist.item"].flush(["price", "currency_id", "company_id"])
        self.env.cr.execute(
            """
            SELECT
                item.id
            FROM
                product_pricelist_item AS item
            LEFT JOIN product_category AS categ ON item.categ_id = categ.id
            LEFT JOIN product_brand AS brand ON item.product_brand_id = brand.id
            WHERE
                (item.product_tmpl_id IS NULL OR item.product_tmpl_id = any(%s))
                AND (item.product_id IS NULL OR item.product_id = any(%s))
                AND (item.categ_id IS NULL OR item.categ_id = any(%s))
                AND (item.product_brand_id IS NULL OR item.product_brand_id = any(%s))
                AND (item.pricelist_id = %s)
                AND (item.date_start IS NULL OR item.date_start<=%s)
                AND (item.date_end IS NULL OR item.date_end>=%s)
            ORDER BY
                item.applied_on, item.min_quantity desc,
                categ.complete_name desc, item.id desc
            """,
            (prod_tmpl_ids, prod_ids, categ_ids, brand_ids, self.id, date, date),
        )
        # NOTE: if you change `order by` on that query, make sure it matches
        # _order from model to avoid inconstencies and undeterministic issues.

        item_ids = [x[0] for x in self.env.cr.fetchall()]
        return self.env["product.pricelist.item"].browse(item_ids)


class ProductPricelistItem(models.Model):

    _inherit = "product.pricelist.item"

    product_brand_id = fields.Many2one(
        comodel_name="product.brand",
        string="Brand",
        ondelete="cascade",
        help="Specify a brand if this rule only applies to products"
        "belonging to this brand. Keep empty otherwise.",
    )
    applied_on = fields.Selection(selection_add=[("25_brand", "Brand")])

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
    def _onchane_rule_content(self):
        super(ProductPricelistItem, self)._onchane_rule_content()

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
