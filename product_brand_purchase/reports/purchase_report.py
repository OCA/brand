# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseReport(models.Model):

    _inherit = "purchase.report"

    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Brand")

    def _select(self):
        select_str = super(PurchaseReport, self)._select()
        return select_str + ", t.product_brand_id as product_brand_id"

    def _group_by(self):
        group_by_str = super(PurchaseReport, self)._group_by()
        return group_by_str + ", t.product_brand_id"
