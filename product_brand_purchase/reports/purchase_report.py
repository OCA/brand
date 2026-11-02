# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Brand")

    def _select_list(self, table):
        return super()._select_list(table) + [
            table.product_id.product_tmpl_id.product_brand_id
        ]
