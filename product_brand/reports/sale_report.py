# Copyright 2018 Tecnativa - David Vidal
# Copyright 2020 Tecnativa - João Marques
# Copyright 2022 NuoBiT - Eric Antones
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Brand")

    def _select_dict(self, table):
        return super()._select_dict(table) | {
            "product_brand_id": table.product_id.product_tmpl_id.product_brand_id
        }
