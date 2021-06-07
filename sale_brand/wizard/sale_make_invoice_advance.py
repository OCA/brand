# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        values = super()._prepare_invoice_values(order, name, amount, so_line)
        if order.brand_id:
            values.update({"brand_id": order.brand_id.id})
        return values

    def _create_invoice(self, order, so_line, amount):
        invoice = super()._create_invoice(order, so_line, amount)
        invoice.brand_id = order.brand_id
        invoice._onchange_partner_id()
        return invoice
