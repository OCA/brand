# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import SQL


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Brand")

    def _select(self):
        return SQL("%s, t.product_brand_id as product_brand_id", super()._select())

    def _group_by(self):
        return SQL("%s, t.product_brand_id", super()._group_by())
