# Copyright 2023 Francesco Apruzzese <cescoap@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):

    _inherit = "stock.move"

    product_brand_id = fields.Many2one(
        comodel_name="product.brand",
        related="product_id.product_brand_id",
        string="Brand",
        store=True,
    )
