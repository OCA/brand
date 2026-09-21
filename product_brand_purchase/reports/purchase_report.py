# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import SQL


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Brand")

    def _select(self):
        select_str = super()._select()
        return SQL("%s, t.product_brand_id as product_brand_id", select_str)

    def _group_by(self):
        group_by_str = super()._group_by()
        return SQL("%s, t.product_brand_id", group_by_str)
