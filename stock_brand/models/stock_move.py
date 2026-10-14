# Copyright 2026 Juliano Henriquez <juliano@consultoriahenca.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        values = super()._get_new_picking_values()
        brands = self.sale_line_id.order_id.brand_id
        if len(brands) == 1:
            values["brand_id"] = brands.id
        return values
