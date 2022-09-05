# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super()._prepare_invoice_values(order, name, amount, so_line)
        res["brand_id"] = order.brand_id.id
        return res
